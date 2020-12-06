import requests
from pydub import AudioSegment

from configs.yandex_speech_kit_config import YANDEX_CONFIG


class YandexApiException(RuntimeError):
    pass


def synthesize(ssml_text):
    folder_id = YANDEX_CONFIG.folder_id
    iam_token = YANDEX_CONFIG.am_token
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
        "voice": YANDEX_CONFIG.voice,
        "emotion": YANDEX_CONFIG.emotion
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise YandexApiException("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk


if __name__ == "__main__":
    text = """Привет Саша! Вот несколько примеров использования SSML.
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
