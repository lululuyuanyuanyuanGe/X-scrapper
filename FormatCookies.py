import json

def load_and_transform_cookies(file_path):
    with open(file_path, 'r') as f:
        cookies_list = json.load(f)

    cookies_dict = {cookie["name"]: cookie["value"] for cookie in cookies_list if "name" in cookie and "value" in cookie}
    return cookies_dict