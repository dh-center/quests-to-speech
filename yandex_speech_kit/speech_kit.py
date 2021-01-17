import os
import time

import requests
from pydub import AudioSegment

from app_source.app_settings import settings
from yandex_speech_kit.speech_kit_settings import yandex_settings


def create_speech_file(ssml_text: str, file_name: str) -> str:
    """
    Self explanatory by its signature, creates mp3 file from text and saves it in a file with specific name
    :param ssml_text: to create mp3 file from
    :param file_name: to save mp3 file with
    :return: mp3_file_path to given file
    """
    tmp_file_name = f"tmp-{time.time()}{file_name}.raw"
    tmp_file_path = os.path.join(settings.data_folder, tmp_file_name)
    try:
        with open(tmp_file_path, "wb") as tmp_file:
            for audio_content in synthesize(ssml_text):
                tmp_file.write(audio_content)
        mp3_file_path = os.path.join(settings.mp3_location, file_name)
        AudioSegment.from_file(
            tmp_file_path, channels=1, sample_width=2, frame_rate=48000
        ).export(mp3_file_path, format="mp3")
        return mp3_file_path
    finally:
        if os.path.isfile(tmp_file_path):
            os.remove(tmp_file_path)


class YandexApiException(RuntimeError):
    pass


def synthesize(ssml_text):
    """
    This method makes api call to string -> mp3 file service provider, in the given case to yandex.
    It will return generator of audio content bytes chunks, you can use to get resultant file.
    :param ssml_text: text to synthesize
    """
    folder_id = yandex_settings.folder_id
    iam_token = yandex_settings.am_token
    ssml_text = f"<speak>{ssml_text}</speak>"
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {
        'Authorization': 'Bearer ' + iam_token,
    }

    data = {
        'ssml': ssml_text,
        'lang': 'ru-RU',
        'folderId': folder_id,
        'format': 'lpcm',
        'sampleRateHertz': 48000,
        "speed": 1,
        "voice": yandex_settings.kit_voice,
        "emotion": yandex_settings.kit_emotion
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise YandexApiException("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk


if __name__ == "__main__":
    text = """Привет! Вот несколько примеров использования SSML.
  Вы можете добавить в текст паузу любой длины:<break time="2s"/> та-дааам!
  Или разметить текст на параграфы и предложения. Паузы между параграфами длиннее.
  <p><s>Первое предложение</s><s>Второе предложение</s></p>
  А еще вы можете подменять фразы.
  Например, чтобы произносить аббревиатуры и <sub alias="тому подобное">т.п.</sub>
"""
    with open("try.raw", "wb") as f:
        for audio_content in synthesize(text):
            f.write(audio_content)
    AudioSegment.from_file("try.raw", channels=1, sample_width=2, frame_rate=48000).export("try_new1.mp3", format="mp3")
