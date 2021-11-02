# Model that Pre-processes words and uses SVM algorithm.

# To exit the system
from functools import total_ordering
import sys
# To stem with Porter-stemmer algorithm
from nltk.stem import PorterStemmer
# To remove stop words
from nltk.corpus import stopwords


""" Function that uses porter-stemmer algorith for stemmatization 
    and removes all the words in nltk english stop words english list
    + some that we added, such as , _ : ? ! ...
    Ex: \"This character writes, \"\"Tom and me found the money that the robbers hid....we got six thousand dollars apiece\"\"\"
"""
def preProcessing(phrase):
    # Set of stop words
    stop_words = set(stopwords.words('english'))
    stop_words.add('...')
    # Set of stop chars
    stop_chars = {'_', ':', '?', '!', ';', '\"', '&', '\'', '(', ')', '\\', '[', '] ', '-'}

    porter = PorterStemmer()
    for word in phrase.split():
        # Removes unecessary chars like the ones in the example above
        for char in word:
            if char in stop_chars:
                phrase = phrase.replace(word, word.replace(char, ''))
                word = word.replace(char, '')
            
        # Applies porter stemmer to word in phrase
        if word not in stop_words:
            phrase = phrase.replace(word, porter.stem(word))
        # Removes a stop word from the phrase
        else:
            phrase = phrase.replace(word, '')
    return phrase


""" Counts the frequency of a given word in a list of phrases """
def count(word, list):
    num = 0
    for phrase in list:
        for w in phrase:
            if word == w:
                num += 1
    return num


""" This model uses a Naive bayes algorithm + Pre-processing """
class M2:

    def __init__(self, testFile, trainFile) -> None:
        try:
            # Opens testFile
            self.testFile = open(testFile, "r")
            # Opens trainFile
            self.trainFile = open(trainFile, "r")
            # Creates dataset of categories with their questions and answers
            self.database = {'MUSIC': [], 'GEOGRAPHY': [], 'LITERATURE': [], 'HISTORY': [], 'SCIENCE': []}
            # Number of words in each category
            self.wordsInCategory = dict.fromkeys(self.database.keys(), 0)
            # Set of unique words
            self.uniqueWords = set()
            # |V| = number of unique words
            self.vocabularyExtension = 0
            # Var to get the number of line in the train file
            self.num_lines = 0
            # Stores the probability of class = Nc/N
            self.derivatives = dict.fromkeys(self.database.keys(), 0)

        # if exception is found reading file
        except OSError:
            print("Could not open/read file")
            sys.exit()


    """ Calculate the probability of the line having a certain category """
    def pcl(self, category, listQA):
        
        # Gets the probability of the category
        pb = self.derivatives[category]
        
        # Loops through the list with question and answer 
        for qa in listQA:
            # Loops through all words in question and asnwer
            for word in qa.split():
                # Calculates probability of word belonging to the category
                # P = ( nº word in all lines with category + 1) / (nº words in all lines in category + dimension of vocabulary)
                pb *= ( count(word, self.database[category]) + 1 ) / (self.wordsInCategory[category] + self.vocabularyExtension)
        
        return pb


    """ Starts to run module """
    def compute(self):
        # Loops through all lines in trainfile 
        for line in self.trainFile:
            # splits line in Category, Question, Answer
            splittedLine = line.split("\t")
            # Applies preProcessing to Question
            splittedLine[1] = preProcessing(splittedLine[1])
            # Stores the question on its database category
            self.database[splittedLine[0]].append(splittedLine[1])
            # Applies preProcessing to Answer
            preProcessing(splittedLine[2].strip())
            # Stores the answer on its database category
            self.database[splittedLine[0]].append(splittedLine[2])
            # counts total number of lines in file
            self.num_lines += 1
            # counts number of lines for each category
            self.wordsInCategory[splittedLine[0]] += 1
            
            # Loops through all the words in the question and answer
            for qa in splittedLine[1:]:
                for word in qa.split():
                    # Adds the word to the created set. Repeated words won't be added
                    self.uniqueWords.add(word)

        # Calculates derivative probability = Number of Category lines / Total number of lines
        for category in self.derivatives.keys():
            self.derivatives[category] = self.wordsInCategory[category]/self.num_lines

        # Gets the number of unique words
        self.vocabularyExtension = len(self.uniqueWords)

        # Runs the Naive Bayes algorithm 
        # Loops through all the lines in the test file
        for line in self.testFile:
            # splits line in Category, Question, Answer
            splittedLine = line.split("\t")
            # Applies preProcessing to Question
            splittedLine[1] = preProcessing(splittedLine[1])
            # Applies preProcessing to Answer
            splittedLine[2] = preProcessing(splittedLine[2].strip())
            
            maxP = 0.0
            result = ""
            # Loops through all possible categories
            for category in self.database.keys():
                # Calculates the Probability(Category|Line)
                tmp = self.pcl(category, splittedLine[1:])
                # if max is lower than the recent calculated probabilty, updates possible solution
                if maxP < tmp:
                    maxP = tmp
                    result = category
            print(result)
        
        self.close()


    """ Closes all open files """
    def close(self):
        self.testFile.close()
        self.trainFile.close()
