from base64 import b64encode


class BaseAuthFlow:
    def make_auth_header(self) -> dict:
        return {
            "Authorization": "Basic %s"
                             % b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        }

    @staticmethod
    def wrapper(**kwargs):
        return {k: v for k, v in kwargs.items() if v is not None}
