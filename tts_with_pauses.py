# https://gist.github.com/moha-abdi/8ddbcb206c38f592c65ada1e5479f2bf

import asyncio
from typing import Union, Optional
from pydub import AudioSegment
import io
from edge_tts import Communicate


class NoPausesFound(Exception):
    def __init__(self, description=None) -> None:
        self.description = (
            "No pauses were found in the text. Please consider using `edge_tts.Communicate` instead."
        )
        super().__init__(self.description)


class CommWithPauses:
    def __init__(
        self,
        text: str,
        voice: str = "en-US-JennyNeural",
        max_pause: int = 6,  # in seconds
    ) -> None:
        self.text = text
        self.voice = voice
        self.max_pause = max_pause * 1000
        self.parsed = self.parse_text()
        self.file = io.BytesIO()

    def parse_text(self):
        if "[pause:" not in self.text:
            yield 0, self.text.strip()
            return

        parts = self.text.split("[pause:")
        for i, part in enumerate(parts):
            if "]" in part:
                pause_time, content = part.split("]", 1)
                pause_time = self.parse_time(pause_time)
                yield pause_time, content.strip()
            else:
                content = part
                yield 0, content.strip()

    def parse_time(self, time_str: str) -> int:
        if time_str.endswith("ms"):
            time_value = int(float(time_str[:-2]))
        elif time_str.endswith("s"):
            time_value = int(float(time_str[:-1]) * 1000)
        else:
            raise ValueError("Invalid pause time format. Use 's' or 'ms'.")
        return min(time_value, self.max_pause)

    def generate_pause(self, time: int) -> bytes:
        silent = AudioSegment.silent(time, frame_rate=24000)
        return silent.raw_data

    async def generate_audio(self, text: str) -> bytes:
        temp_chunk = io.BytesIO()
        communicate = Communicate(text, self.voice)
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                temp_chunk.write(chunk["data"])

        temp_chunk.seek(0)
        decoded_chunk = AudioSegment.from_mp3(temp_chunk)
        return decoded_chunk.raw_data

    async def chunkify(self):
        for pause_time, content in self.parsed:
            if pause_time and not content:
                self.file.write(self.generate_pause(pause_time))
            elif content:
                if pause_time:
                    self.file.write(self.generate_pause(pause_time))
                self.file.write(await self.generate_audio(content))

    async def save(
        self,
        audio_fname: Union[str, bytes],
        metadata_fname: Optional[Union[str, bytes]] = None,
    ) -> None:
        await self.chunkify()
        self.file.seek(0)
        audio = AudioSegment.from_raw(
            self.file,
            sample_width=2,
            frame_rate=24000,
            channels=1,
        )
        audio.export(audio_fname, format="mp3")
