import os
from manager.tokenManager import TokenManager
class BaseApp:
    def __init__(self):
        self.token_manager = TokenManager()
        self.user_token = self.token_manager.load_token()

    def load_token(self):
        return self.token_manager.load_token()

    def save_token(self, token):
        self.token_manager.save_token(token)

    def clear_token(self):
        self.token_manager.clear_token()