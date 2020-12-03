import hashlib


def hash_text(text: str) -> str:
    sha = hashlib.sha256()
    sha.update(str.encode(text))
    return f"{sha.hexdigest()}-{len(text)}"


if __name__ == '__main__':
    res1 = hash_text("hello_world")
    print(hash_text("hello_world2"))
    assert res1 == hash_text("hello_world")
