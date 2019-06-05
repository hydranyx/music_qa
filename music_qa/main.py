"""
The main entry point which executes the QA system.
"""
import sys
from question_clf import get_question_type
from queries import x_of_y, description, boolean

QUESTION = ""  # make question intp a struct?


def print_examples():
    """ Prints (50) example questions. """
    print(
        """ Example questions:
        What is a birthdate
	    From which album is Dancing Queen?
	    What is the birth name of Dave Grohl?
	    When was Lovely Day by Bill Withers released?
	    What are Michael Jackson's causes of death?
	    What country is Kraftwerk from?
	    Did Mozart play on violin?
	    How many children does Chris Martin have?
	    In what genres does Taylor Swift perform?
	    Stewart Copeland was the drummer with which band?

        What is the birth name of Eminem?
        What is Eminem's birth name?
        When was B.B. King born?
        Where is the birth place/birthplace/place of birth of B.B King?
        Where is B.B. King's birth place/birthplace/place of birth?
        What is the official website of De Staat?
        Who is the partner of Jay Z?
        Who is Jay Z's wife?
        Who was the composer of The Four Seasons?
        What is the record label of The Clash
        """
    )


def main():
    """ The main application. """

    # Print the examples
    print_examples()

    # Iterate through all lines provided by the user
    for line in sys.stdin:
        # Strip the trailing newline
        question = line.rstrip()  # make the question into a struct, (structs in python)

        question_type = get_question_type(question)

        if question_type == 0:
            print("x_of_y_map")
            answer = x_of_y(question)
        elif question_type == 1:
            print("boolean")
            answer = boolean(question)
        elif question_type == 2:
            print("description")
            answer = description(question)


if __name__ == "__MAIN__":
    main()
