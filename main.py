"""
This script runs a QA system accepting questions on `stdin`.
"""
from __future__ import absolute_import

import logging
import sys
from music_qa import MusicQa

# Un-comment to see debug logging
# logging.basicConfig(level=logging.DEBUG)


def main():
    """ Main program. """

    # Setup the QA system
    qa_system = MusicQa()

    # Iterate through all the lines provided by the user
    for line in sys.stdin:
        # Strip the trailing newline
        question = line.rstrip()
        # Answer the question
        answer = qa_system.answer(question)
        # Print the answer
        print(answer)


if __name__ == "__main__":
    main()
