from enum import Enum, auto

class AppState(Enum):
    CONFIGS = auto()
    WAITING_ANSWER = auto()
    WAITING_QUESTION = auto()