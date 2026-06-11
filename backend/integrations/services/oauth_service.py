import secrets


class OAuthService:

    @staticmethod
    def generate_access_token():
        return secrets.token_hex(32)

    @staticmethod
    def generate_refresh_token():
        return secrets.token_hex(64)