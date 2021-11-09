# Simple model used as baseline.

import sys
# Used to import Porter-stemmer algorith
from nltk.stem import PorterStemmer


""" This model uses a Jaccard algorithm to calculate the similarity
    between the read line and all the lines in the training file.
    Selects the category of the trainning line wich is more similar.
"""
class M1:
    
    def __init__(self, testFile, trainFile) -> None:    
        # opens files for reading
        try:
            # Stores the test file
            self.testFile = open(testFile, "r")
            # Stores the train file
            self.trainFile = open(trainFile, "r")
            # Ci has the category of the line i of the train file [C1, C2, ..., Cn]
            self.trainCategories = list()
            # Qi has the pre-processed question of the line i of the train file [Q1, Q2, ..., Qn]
            self.trainQuestions = list()
            # Ai has the pre-processed answer of the line i of the train file [A1, A2, ..., An]
            self.trainAnswers = list()
            # Algorithm for stemming
            self.porter = PorterStemmer()
            # Stores the threshold value
            self.threshold = 0.0
        
        # if exception is found reading any of the given files
        except OSError:
            print("Could not open/read file")
            sys.exit()


    """ Function that uses porter-stemmer algorith for stemmatization """
    def stem(self, phrase):
        for word in phrase.split(" "):
            phrase = phrase.replace(word, self.porter.stem(word))
        return phrase


    """ Applies Jaccard algorithm on 2 diferent questions """
    def jaccard(self, phrase1, phrase2):
        # Split the documents and create tokens
        doc1_tokens = set(phrase1.split())
        doc2_tokens = set(phrase2.split())

        # Calculate the Jaccard Similarity
        return len(doc1_tokens.intersection(doc2_tokens)) / len(doc1_tokens.union(doc2_tokens))


    """ Apllies Jaccard to every input line on the test
        # for each line in test file, apllies jaccard with each line in train
        # returns the category of the line in trainFile with te biggest jaccard
        # complexity: O(n^2) BAD
     """
    def compute(self):

        for trainLine in self.trainFile:
            splittedTrainLine = trainLine.split("\t")

            self.trainCategories.append(splittedTrainLine[0])
            self.trainQuestions.append(self.stem(splittedTrainLine[1]))
            self.trainAnswers.append(self.stem(splittedTrainLine[2].strip()))
        
        result = ""
        maxJac = 0.0
        # Loops through all lines in test file
        for testLine in self.testFile:
            # Parts test line 
            splittedTestLine = testLine.split("\t")
            stemmedTestQuestion = self.stem(splittedTestLine[1])
            stemmedTestAnswer = self.stem(splittedTestLine[2].strip())
            
            for i in range(len(self.trainQuestions)):
                tmp = self.jaccard(self.trainQuestions[i], stemmedTestQuestion)
                    
                if tmp > self.threshold:
                    tmp += self.jaccard(self.trainAnswers[i], stemmedTestAnswer)
                    if tmp > maxJac:
                        maxJac = tmp
                        result = self.trainCategories[i]
            maxJac = 0.0
            print(result)
        # Closes all files
        self.close()

        
    """ Closes all open files """
    def close(self):
        # closes files
        self.testFile.close()
        self.trainFile.close()
