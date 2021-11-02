# Model that Pre-processes words and uses SVM algorithm.

# To exit the system
from functools import total_ordering
import sys
# To stem with Porter-stemmer algorithm
from nltk.stem import PorterStemmer
# To remove stop words
from nltk.corpus import stopwords


""" Counts the frequency of a given word in a list of phrases """
def count(word, listOfWords):
    num = 0
    for w in listOfWords:
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
            self.wordsInCategory = {'MUSIC': [], 'GEOGRAPHY': [], 'LITERATURE': [], 'HISTORY': [], 'SCIENCE': []}
            # Number of words in each category
            self.nWordsInCategory = dict.fromkeys(self.wordsInCategory.keys(), 0)
            # Set of unique words
            self.uniqueWords = set()
            # |V| = number of unique words
            self.nUniqueWords = 0
            # Var to get the number of line in the train file
            self.num_lines = 0
            # Stores the probability of class = Nc/N
            self.pCategory = dict.fromkeys(self.wordsInCategory.keys(), 0)
            # Set of stop words
            self.stop_words = set(stopwords.words('english'))        
            # Set of stop chars
            self.stop_chars = {'_', ':', '?', '!', ';', '\"', '&', '\'', '(', ')', '\\', '[', '] ', '-'}
            # Object that can apply porter stemmer algorithm
            self.porter = PorterStemmer()

        # if exception is found reading file
        except OSError:
            print("Could not open/read file")
            sys.exit()


    """ Method that uses porter-stemmer algorith for stemmatization 
        and removes all the words in nltk english stop words english list
        + some that we added, such as , _ : ? ! ...
        Ex: \"\"Tom! -> tom
    """
    def preProcessing(self, word):
        # Removes unecessary chars like the ones in the example above
        for char in word:
            if char in self.stop_chars:
                word = word.replace(char, "")
                
        # If word is stop word, discards it
        if word in self.stop_words:
            return ""
             
        return self.porter.stem(word)   


    """ Calculate the probability of the line having a certain category """
    def pcl(self, category, listQA):
        
        # Gets the probability of the category
        pb = self.pCategory[category]
        
        # Loops through the list with question and answer 
        for qa in listQA:
            # Loops through all words in question and asnwer
            for word in qa.split():
                # Calculates probability of word belonging to the category
                # P = ( nº word in category + 1) / (total nº words in category + dimension of vocabulary)
                pb *= ( count(word, self.wordsInCategory[category]) + 1 ) / ( self.nWordsInCategory[category] + self.nUniqueWords )
        
        return pb


    """ Starts to run module """
    def compute(self):
        # Loops through all lines in trainfile 
        for line in self.trainFile:
            
            # splits line in Category, Question, Answer. Removes \n
            splittedLine = line.strip().split("\t")

            for qaPos in (1, 2):
                # Loops through every word in line's question + answer
                for word in splittedLine[qaPos].split():
                    newWord = self.preProcessing(word)
                    if newWord != '':
                        # Pre processes the word and adds it to the wordsInCategory
                        self.wordsInCategory[splittedLine[0]].append(newWord)
                        # Adds word to set of unique words
                        self.uniqueWords.add(newWord)
            
            
            # counts total number of lines in file
            self.num_lines += 1

        for category in self.wordsInCategory.keys():
            # counts number of words for each category
            self.nWordsInCategory[category] = len(self.wordsInCategory[category])
    
        # Calculates derivative probability = Number of Category lines / Total number of lines
        for category in self.pCategory.keys():
            self.pCategory[category] = self.nWordsInCategory[category]/self.num_lines

        # Gets the number of unique words
        self.nUniqueWords = len(self.uniqueWords)

        # Runs the Naive Bayes algorithm 
        # Loops through all the lines in the test file
        for line in self.testFile:
            # splits line in Category, Question, Answer. Removes \n
            splittedLine = line.strip().split("\t")
            
            for qaPos in (1, 2):
                # Loops through every word in line's question + answer
                for word in splittedLine[qaPos].split():
                    splittedLine[qaPos] = splittedLine[qaPos].replace(word, self.preProcessing(word))

            maxP = 0.0
            result = ""
            # Loops through all possible categories
            for category in self.wordsInCategory.keys():
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
