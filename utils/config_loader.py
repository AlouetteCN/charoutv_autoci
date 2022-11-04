import configparser
import os
import sys

from constants import base


class ProfileLoader:

    '''
    design as formatter below:
    [telegram_api]
    api_id=
    api_hash=

    [captcha_api]
    id=
    apikey=

    [base]
    retry_times=10
    use_system_env=False
    '''

    def __init__(self, current_dir) -> None:
        self.current_dir = current_dir
        self.path = os.path.join(self.current_dir, "config.ini")
        print(os.path.abspath(__file__))

        self._config = configparser.ConfigParser()
        self.check_config()

    def _load(self):
        # load all config and return as a dict
        _configs = self._config.read(self.path)
        return _configs

    def _dump(self):
        # Write basic config to config file
        self._config.add_section('telegram_api')
        self._config.set('telegram_api', 'api_id', '')
        self._config.set('telegram_api', 'api_hash', '')

        self._config.add_section('captcha_api')
        self._config.set('captcha_api', 'id', '')
        self._config.set('captcha_api', 'apikey', '')

        self._config.add_section('base')
        self._config.set('base', 'retry_times', '10')
        self._config.set('base', 'use_system_env', 'False')
        self._config.set('base', 'client_name', '')

        with open(self.path, 'w') as configfile:
            self._config.write(configfile)

    def load(self):
        self._load()
        return self._config

    def dump(self):
        self._dump()

    def check_config(self):
        if not os.path.isfile(self.path):
            fp = open(self.path, 'w+')
            fp.close()
            self.dump()
            print('Default config file has been generated, please edit it.')
            sys.exit(0)

        def T(c):
            return False if c == '' or c is None else True

        self.load()

        if not T(self._config['telegram_api']['api_hash']):
            sys.exit("Missing api_hash in telegram_api session. https://my.telegram.org/auth?to=apps")

        if not T(self._config['telegram_api']['api_id']):
            sys.exit("Missing api_id in telegram_api session. https://my.telegram.org/auth?to=apps")

        if not T(self._config['captcha_api']['id']):
            sys.exit("Missing id in captcha_api session. https://truecaptcha.org/")

        if not T(self._config['captcha_api']['apikey']):
            sys.exit("Missing apikey in captcha_api session. https://truecaptcha.org/")

        if not T(self._config['base']['retry_times']):
            print("Missing retry_times in base session, use 10 by default")
            self._config['base']['retry_times'] = base.RETRY_TERMS

        if not T(self._config['base']['use_system_env']):
            print("Missing use_system_env in base session, use False by default")
            self._config['base']['use_system_env'] = base.USE_ENV

        if not T(self._config['base']['client_name']):
            print("Missing client_name in base session, use hostname by default")
            self._config['base']['client_name'] = base.CLIENT_NAME
