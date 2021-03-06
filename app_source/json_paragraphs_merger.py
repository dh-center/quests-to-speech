import json
from typing import Dict

from app_source.app_settings import app_settings


class JsonMerger:
    @staticmethod
    def merge_json(json_data: Dict, res: list = None):
        """
        :param json_data: json to join in one text (each block to be merged, should have key "text")
        :return: merged json
        """
        if res is None:
            res = []
        if isinstance(json_data, list):
            for block in json_data:
                JsonMerger.merge_json(block, res)
        elif isinstance(json_data, dict):
            for key, block in json_data.items():
                if isinstance(block, str):
                    if key in app_settings.SET_KEY_WORDS:
                        res.append(block)
                    continue
                JsonMerger.merge_json(block, res)
        return res

    @staticmethod
    def merge_json_to_text_for_yandex(json_data: Dict) -> str:
        """

        :param json_data: json to surround with <p> tags by paragraphs
        :return: string formatted
        """
        return '\n'.join(f"<p>{line}</p>" for line in JsonMerger.merge_json(json_data))


json_merger = JsonMerger()

# Example
if __name__ == '__main__':
    json_data = json.loads("""
{
    "time": "2020-12-08T11:25:14.216Z",
    "blocks": [
      {
        "type": "locationInstance",
        "data": {
          "locationInstanceId": "TG9jYXRpb25JbnN0YW5jZTo1ZmNmNTQ0MTE2NTk3YTUwYzEwZjMyYmI="
        }
      },
      {
        "type": "test",
        "data": {
          "text": "Как называл Маяковский упадочное настроение среди молодежи?",
          "answers": [
            "Солжиница;",
            "Есенищина;",
            "Гумильвица;",
            "Сологубщина."
          ],
          "correctAnswerIndex": 1,
          "rightAnswerMessage": "Да! Правильный ответ - Есенищина .  Причина образования слова - противостояние Есенина и Маяковского. ",
          "wrongAnswerMessage": "Упс, неверно.. Правильный ответ - Есенищина .  Причина образования слова - противостояние Есенина и Маяковского. "
        }
      },
      {
        "type": "test",
        "data": {
          "text": "Как называл Маяковский упадочное настроение среди людей?",
          "answers": [
            "Солжиница;",
            "Есенищина;",
            "Гумильвица;",
            "Сологубщина."
          ],
          "correctAnswerIndex": 1,
          "rightAnswerMessage": "Да! Правильный ответ - Есенищина .  Причина образования слова - противостояние Есенина и Маяковского. ",
          "wrongAnswerMessage": "Упс, неверно.. Правильный ответ - Есенищина .  Причина образования слова - противостояние Есенина и Маяковского. "
        }
      }
    ]
}
""")
    print(json_data)
    print(JsonMerger.merge_json_to_text_for_yandex(json_data))
