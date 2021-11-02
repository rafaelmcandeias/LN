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
    # TRAIN: Foste ao urban? Sim
    #        Vai chover amanha? nao
    # DEV:   Mamei nove gajas? bue pouco mpt
    #         

    """ Jaccard(QD, QT1) -> se>0 -> Jaccard(RD, RT1) -> se>max -> max = JAccard
    """
     
    def compute(self):
        # [C1, C2, ..., Cn]
        trainCategories = list()
        # [Q1, Q2, ..., Qn]
        trainQuestions = list()
        # [A1, A2, ..., An]
        trainAnswers = list()

        for trainLine in self.trainFile:
            splittedTrainLine = trainLine.split("\t")

            trainCategories.append(splittedTrainLine[0])
            trainQuestions.append(stemming(splittedTrainLine[1]))
            trainAnswers.append(stemming(splittedTrainLine[2].strip()))
        
        result = ""
        threshold = 0.0
        maxJac = 0.0
        # Loops through all lines in test file
        for testLine in self.testFile:
            # Parts test line 
            splittedTestLine = testLine.split("\t")
            stemmedTestQuestion = stemming(splittedTestLine[1])
            stemmedTestAnswer = stemming(splittedTestLine[2].strip())
            
            for i in range(len(trainQuestions)):
                tmp = jaccard(trainQuestions[i], stemmedTestQuestion)
                    
                if tmp > threshold:
                    tmp += jaccard(trainAnswers[i], stemmedTestAnswer)
                    if tmp > maxJac:
                        maxJac = tmp
                        result = trainCategories[i]
            maxJac = 0.0
            print(result)
        # Closes all files
        self.close()

        
    """ Closes all open files """
    def close(self):
        # closes files
        self.testFile.close()
        self.trainFile.close()
