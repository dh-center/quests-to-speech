import json
import time
from threading import Thread

import requests

from configs.yandex_speech_kit_config import YANDEX_CONFIG
from server.utils.logger import log_error, log
from server.utils.yandex_speech.yandex_speech_processor import YandexApiException


def renew_token():
    body = {
        "yandexPassportOauthToken": YANDEX_CONFIG.passport_token
    }
    log(f"Try to renew Yandex token")
    response = requests.post(r'https://iam.api.cloud.yandex.net/iam/v1/tokens', json=body)
    if response.status_code != 200:
        raise YandexApiException(f"VK API exception {response.status_code}")
    response_body = json.loads(response.content)
    YANDEX_CONFIG.set_am_token(response_body['iamToken'])


def token_renewal_task():
    prev_run = 0
    while True:
        now = time.time()
        try:
            passport_token = YANDEX_CONFIG.passport_token
            log("Renew Yandex token task iteration")
            if not passport_token or now - prev_run < YANDEX_CONFIG.TOKEN_RENEWAL_INTERVAL:
                time.sleep(YANDEX_CONFIG.TOKEN_RENEWAL_INTERVAL)
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
    passport_token = YANDEX_CONFIG.passport_token
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
