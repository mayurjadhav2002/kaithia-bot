operation = {
    "group": 1,
    "translation": 1,
    "Generate-text": 3,
    "Summary": 5,
    "grammer": 1,
    "other": 5
}
class User:
    def __init__(self, name, email, id, username):
        self._id: int = None
        self._username: str = None
        self.is_active: bool = None
        self.tokens_remaining = None

    def get_user_tokens(self):
        pass
    
    def update_user_tokens(self, operation_type):
        self.tokens_remaining = self.tokens_remaining - operation[operation_type]
    
    def calculate_user_score(self):
        pass
    
    def send_notification(self):
        pass
    
    def check_user_status(self):
        pass