import json
import time
from threading import Thread

import requests

from app_source.logger import log, log_error
from yandex_speech_kit.speech_kit import YandexApiException
from yandex_speech_kit.speech_kit_settings import yandex_settings


def renew_token():
    body = {"yandexPassportOauthToken": yandex_settings.yandex_passport_token}
    log(f"Try to renew Yandex token")
    response = requests.post(r'https://iam.api.cloud.yandex.net/iam/v1/tokens', json=body)
    if response.status_code != 200:
        raise YandexApiException(f"Yandex API exception {response.status_code} {response.content}")
    response_body = json.loads(response.content)
    yandex_settings.am_token = response_body['iamToken']


def token_renewal_task():
    prev_run = 0
    while True:
        now = time.time()
        try:
            passport_token = yandex_settings.yandex_passport_token
            log("Renew Yandex token task iteration")
            if not passport_token or now - prev_run < yandex_settings.token_renewal_interval:
                time.sleep(yandex_settings.token_renewal_interval)
            else:
                renew_token()
        except Exception as exp:
            log_error(f"Exception happened on Yandex token renewal {exp}")
        prev_run = now


__RENEWAL_THREAD = Thread(
    name="YandexTokenRenewal-thread",
    target=token_renewal_task,
    daemon=True
)
__RENEWAL_THREAD.start()

if __name__ == '__main__':
    passport_token = yandex_settings.passport_token
    body = {
        "yandexPassportOauthToken": passport_token
    }
    response = requests.post(r'https://iam.api.cloud.yandex.net/iam/v1/tokens', json=body)
    print(response.status_code)
    print(response.content)
    if response.status_code == 200:
        response_body = json.loads(response.content)
        print(response_body)
        print(response_body['iamToken'])
