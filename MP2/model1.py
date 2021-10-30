# Simple model used as baseline.

import sys
# Used to import several high-complexity mathematical functions
import numpy as np
# Used to import Porter-stemmer algorith
from nltk.stem import PorterStemmer

""" Function that uses porter-stemmer algorith for stemmatization """
def stemming(phrase):
    porter = PorterStemmer()
    for word in phrase.split(" "):
        phrase = phrase.replace(word, porter.stem(word))
    return phrase


""" Applies Jaccard algorithm on 2 diferent questions """
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
        threshold = 0.0
        similarQuestions = np.matrix()
        trainQuestions = set(trainLine.split("\t")[1] for trainLine in self.trainFile)
        for index,testLine in enumarate(self.testFile):      
            for trainQuestion in trainQuestions:
                tmp = jaccard(stemming(trainQuestion), stemming(testLine.split("\t")[1]))
                if tmp > threshold:
                    similarQuestions[index] = tmp
        #for question in similarQuestions:
            #TODO: jaccard for Responses
        
        # TO DO: answer CATEGORY
        # code or smth

        # Closes all files
        self.close()

        
    """ Closes all open files """
    def close(self):
        # closes files
        self.testFile.close()
        self.trainFile.close()
