import requests
from base64 import b64encode


def captcha_solver(f, conf):
    # conf = ProfileLoader(current_dir=PWD).conf
    with open(f, "rb") as image_file:
        encoded_string = b64encode(image_file.read()).decode('ascii')
        url = 'https://api.apitruecaptcha.org/one/gettext'
        data = {
            'userid': conf['captcha_api']['id'],
            'apikey': conf['captcha_api']['apikey'],
            'data': encoded_string
        }
        response = requests.post(url=url, json=data)
        data = response.json()
    return data


def handle_captcha_solved_result(solved_result):
    try:
        return solved_result['result']
    except KeyError:
        return None
