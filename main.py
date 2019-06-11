"""
This script runs a QA system accepting questions on `stdin`.
"""
from __future__ import absolute_import

import logging
import sys
from music_qa import MusicQa

# Un-comment to see debug logging
logging.basicConfig(
    format="%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.INFO,
)


def handle_input_text(line):
    splits = line.split("\t")
    id = None

    if len(splits) == 1:
        question = splits[0]
    else:
        id = splits[0]
        question = splits[1]

    return (id, question.rstrip())


def main():
    """ Main program. """

    # Setup the QA system
    qa_system = MusicQa()

    # Iterate through all the lines provided by the user
    for line in sys.stdin:
        # Extract the question text (and id) from the line
        (id, question) = handle_input_text(line)
        # Answer the question
        answer = qa_system.answer(question)
        # Print the answer
        if id:
            print("{}\t{}".format(id, answer))
        else:
            print(answer)


if __name__ == "__main__":
    main()
