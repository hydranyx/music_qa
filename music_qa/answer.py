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
        elif isinstance(self.answer, list) and len(self.answer) == 1:
            str_ = "Answer:" + str(self.answer[0])
        elif isinstance(self.answer, bool):
            if self.answer:
                str_ = "Answer: Yes"
            else:
                str_ = "Answer: No"
        else:
            str_ = "Answer: " + str(self.answer)
        return str_
