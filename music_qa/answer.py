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
            return "No answer found."
        elif isinstance(self.answer, list) and len(self.answer) == 1:
            str_ = str(self.answer[0])
        elif isinstance(self.answer, bool):
            if self.answer:
                str_ = "Yes"
            else:
                str_ = "No"
        elif isinstance(self.answer, list) and len(self.answer) > 1:
            for val in self.answer:
                str_ = str_ + val + "\t"
                str_.strip()
        else:
            str_ = str(self.answer)

        return "Answer: " + str_
