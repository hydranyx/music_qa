"""
A module containing the Answer intermediary class.
"""
import re


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

            regex = r"([0-9\-]*)"
            date = re.search(regex, str_)

            if date.group():
                str_ = date.group()

        elif isinstance(self.answer, bool):
            if self.answer:
                str_ = "Yes"
            else:
                str_ = "No"
        elif isinstance(self.answer, list) and len(self.answer) > 1:
            str_ = ""
            for val in self.answer:
                str_ = str_ + val + "\t"
                str_.strip()
        else:
            str_ = str(self.answer)

        return "Answer: " + str_
