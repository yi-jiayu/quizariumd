import os


class TelegramConfig:
    def __init__(self, session_file, username, api_id, api_hash, phone, password):
        self.session_file = session_file
        self.username = username
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.password = password

    @classmethod
    def from_environment(cls):
        prefix = 'TELEGRAM'
        suffixes = ('SESSION_FILE', 'USERNAME', 'API_ID', 'API_HASH', 'PHONE', 'PASSWORD')
        variable_names = [f'{prefix}_{variable_name}' for variable_name in suffixes]
        variables = [os.getenv(variable_name) for variable_name in variable_names]
        return TelegramConfig(*variables)
