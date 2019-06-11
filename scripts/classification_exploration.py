import sys
import spacy

NLP = spacy.load("en_core_web_lg")
CLASSIFICATION_MAPPER = {
    "boolean": ["Is only a"],
    "list": ["What are the"],
    "highest": ["What is the highest"],
    "description": ["What is a"],
}


def classify_question(question):
    highest_score = 0
    final_classiciation = None
    print(CLASSIFICATION_MAPPER)
    for classification, mapper in CLASSIFICATION_MAPPER.items():
        for sentence in mapper:
            score = NLP(sentence).similarity(NLP(question))
            print(classification, score)
            if score > highest_score:
                highest_score = score
                final_classification = classification

    return final_classification


def main():
    for line in sys.stdin:
        question = line.rstrip()
        print(classify_question(question))


if __name__ == "__main__":
    main()
