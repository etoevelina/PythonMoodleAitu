import os

class TokenManager:
    def save_token(self, token):
        with open("token.txt", "w") as file:
            file.write(token if token is not None else "")

    def load_token(self):
        if os.path.exists("token.txt"):
            with open("token.txt", "r") as file:
                return file.read().strip()
        return None

    def clear_token(self):
        with open("token.txt", "w") as file:
            file.write("")