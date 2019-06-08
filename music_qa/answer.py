"""
A module containing the Answer intermediary class.
"""


class Answer:
    """
    A class handling an answer and its display.
    """

    def __init__(self, answer):
        self.answer = answer

    def __str__(self):
        if self.answer is None:
            str_ = "No answer found."
        else:
            str_ = "Answer: " + self.answer
        return str_
