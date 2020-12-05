import json


def merge_json(json_data, res: list = None):
    if res is None:
        res = []
    if isinstance(json_data, list):
        for block in json_data:
            merge_json(block, res)
    elif isinstance(json_data, dict):
        for key, block in json_data.items():
            if isinstance(block, str):
                if key == 'text':
                    res.append(block)
                continue
            merge_json(block, res)
    return res


def merge_json_to_text(json_data) -> str:
    return "\n".join(merge_json(json_data))


if __name__ == '__main__':
    json_data = json.loads("""
{
  "time": 1607078179960,
  "blocks": [
    {
      "type": "header",
      "data": {
        "text": "Editor.js",
        "level": 2
      }
    },
    {
      "type": "paragraph",
      "data": {
        "text": "Hey. Meet the new Editor. On this page you can see it in action — try to edit this text."
      }
    },
    {
      "type": "header",
      "data": {
        "text": "Key features",
        "level": 3
      }
    }
  ]
}
    """)
    print(json_data)
    print(merge_json_to_text(json_data))
