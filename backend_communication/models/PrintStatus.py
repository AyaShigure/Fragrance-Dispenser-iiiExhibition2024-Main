from enum import Enum
from .Perfume import Perfume, Food


class PrintStatus(str, Enum):
    PRINTING = "PRINTING"
    COMPLETED = "COMPLETED"
    NOT_FOUND = "NOT_FOUND"