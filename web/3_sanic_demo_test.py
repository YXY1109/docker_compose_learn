import requests


def demo1():
    api_url = "http://127.0.0.1:8011/api"
    response = requests.get(api_url, timeout=60)
    response.raise_for_status()
    result = response.json()
    print(result)


def demo2():
    api_url = "http://127.0.0.1:8011/api/add"
    payload = {"a": 2, "b": 18}
    response = requests.post(api_url, json=payload, timeout=60)
    response.raise_for_status()
    result = response.json()
    print(result)


if __name__ == '__main__':
    demo1()
    demo2()
