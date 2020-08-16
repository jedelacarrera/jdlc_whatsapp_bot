from unittest.mock import Mock


class TwilioClientMock:
    def __init__(self):
        self.send_message = Mock()
