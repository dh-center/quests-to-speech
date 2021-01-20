import json
import time
from threading import Thread

import requests

from app_source.logger import main_logger
from yandex_speech_kit.speech_kit import SpeechKit
from yandex_speech_kit.speech_kit_settings import yandex_settings


# Script to renew token from Yandex

def token_renew(forced: bool = False):
    """
    renew token method, to refresh a token
    :param forced: if true runs once and returns
    """
    prev_run = 0
    while True:
        now = time.time()
        try:
            passport_token = yandex_settings.YANDEX_PASSPORT_TOKEN
            main_logger.log("Renew Yandex token task iteration")
            if not forced and (not passport_token or now - prev_run < yandex_settings.TOKEN_RENEWAL_INTERVAL):
                time.sleep(yandex_settings.TOKEN_RENEWAL_INTERVAL)
            else:
                body = {"yandexPassportOauthToken": yandex_settings.YANDEX_PASSPORT_TOKEN}
                main_logger.log(f"Try to renew Yandex token")
                response = requests.post(r'https://iam.api.cloud.yandex.net/iam/v1/tokens', json=body)
                if response.status_code != 200:
                    raise SpeechKit.YandexApiException(
                        f"Yandex API exception {response.status_code} {response.content}")
                response_body = json.loads(response.content)
                yandex_settings.AM_TOKEN = response_body['iamToken']

                if forced:
                    return
        except Exception as exp:
            main_logger.log_error(f"Exception happened on Yandex token renewal {exp}")
        prev_run = now


# job to renew token periodically
__RENEWAL_THREAD = Thread(
    name="YandexTokenRenewal-thread",
    target=token_renew,
    daemon=True
)
__RENEWAL_THREAD.start()
