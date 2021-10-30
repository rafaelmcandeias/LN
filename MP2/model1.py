# Simple model used as baseline.

import sys
from nltk.stem import PorterStemmer


def stemming(phrase):
    porter = PorterStemmer()
    for word in phrase.split(" "):
        phrase.replace(word, porter.stem(word))
    return phrase


"""Applies Jaccard algorithm on 2 diferent questions"""
def jaccard(question1, question2):
    # Split the documents and create tokens
    doc1_tokens = set(question1.split())
    doc2_tokens = set(question2.split())

    # Calculate the Jaccard Similarity
    return len(doc1_tokens.intersection(doc2_tokens)) / len(doc1_tokens.union(doc2_tokens))


""" This model uses a Jaccard algorithm to calculate the similarity
    between the read line and all the lines in the training file.
    Selects the category of the trainning line wich is more similar.
"""
class M1:
    
    def __init__(self, testFile, trainFile) -> None:    
        # opens files for reading
        try:
            self.testFile = open(testFile, "r")
            self.trainFile = open(trainFile, "r")
        
        # if exception is found reading file
        except OSError:
            print("Could not open/read file")
            sys.exit()


    """ Apllies Jaccard to every input line on the test
        # for each line in test file, apllies jaccard with each line in train
        # returns the category of the line in trainFile with te biggest jaccard
        # complexity: O(n^2) BAD
     """
    def compute(self):
        # Creates set with questions from the test file
        trainQuestions = set(trainLine.split("\t")[1] for trainLine in self.trainFile)
        
        for testLine in self.testFile:
            maximum = -1.0
            category = ""
            for trainQuestion in trainQuestions:
                tmp = jaccard(stemming(trainQuestion), stemming(testLine.split("\t")[1]))
                if maximum < tmp:
                    maximum = tmp
                    category = testLine.split("\t")[0]
            print(category)
        
        # Closes all files
        self.close()

        
    """ Closes all open files """
    def close(self):
        # closes files
        self.testFile.close()
        self.trainFile.close()
