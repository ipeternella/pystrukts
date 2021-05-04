"""
Exceptions raised by Symbol tables.
"""


class KeyErrorWithRank(KeyError):
    """
    Raised when a key was not found on a symbol table (dictionary). It also contains
    and extra attribute: the rank of the searched key. The rank means the amount of less
    keys present in the dictionary that are less than the searched key.
    """

    rank: int

    def __init__(self, rank: int, *args: object) -> None:
        super().__init__(*args)
        self.rank = rank
