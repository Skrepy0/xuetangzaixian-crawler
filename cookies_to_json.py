import json


def cookie_to_json(cookie_str):
    cookies = {}
    for item in cookie_str.split(';'):
        if '=' in item:
            key, value = item.strip().split('=', 1)
            cookies[key] = value
    return json.dumps(cookies, indent=2)


cookie_string = input("Enter Cookie:")
json_output = cookie_to_json(cookie_string)
print(json_output)
