# Model that Pre-processes words and uses SVM algorithm.

# To exit the system
import sys
# To stem with Porter's stemmer algorithm
from nltk.stem import PorterStemmer
# To remove stop words
from nltk.corpus import stopwords


""" Counts the frequency of a given word in a list of words """
def count(word, listOfWords):
    num = 0
    for w in listOfWords:
        if word == w:
            num += 1
    return num


""" This model uses a Complement Naive bayes algorithm + Pre-processing 
    pwnc = nº vezes que a w esta nas outras categorias / nº de w's nas outras categorias
    ppnc = pwnc0 * pwnc1 * ... * pwncn
    P = p(categoria) / ppnc
"""
class M2:

    def __init__(self, testFile, trainFile) -> None:
        try:
            # Opens testFile
            self.testFile = open(testFile, "r")
            # Opens trainFile
            self.trainFile = open(trainFile, "r")
            # Shows all words in each category. Repetitions allowed
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
            self.stop_chars = {'!', '\"', '&', '\-'}
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


    """ pwnc = nº vezes que a w esta nas outras categorias / nº de w's nas outras categorias """
    def pwnc(self, word, category):
        timesWordNotInC = 0
        wordsNotInC = 0

        for c in self.wordsInCategory.keys():
            if c != category:
                timesWordNotInC += self.wordsInCategory[c].count(word)
                wordsNotInC += self.nWordsInCategory[c]
        
        # For smoothing, add 1 to top and |V| to bottom
        return (timesWordNotInC + 1 ) / (wordsNotInC + self.nUniqueWords)


    """ ppnc = pwnc0 * pwnc1 * ... * pwncn 
        P = p(categoria) / ppnc
    """
    def p(self, category, listQA):

        # Gets the probability of the category
        pc = self.pCategory[category]
        # Probability of a phrase not being from all other categories
        ppnc = 1.0
        # Loops through the list with question and answer
        for qa in listQA:
            # Loops through all words in question and asnwer
            for word in qa.split():
                ppnc *= self.pwnc(word, category)

        return pc / ppnc


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
            self.nWordsInCategory[category] = len(
                self.wordsInCategory[category])

        # Calculates derivative probability = Number of Category lines / Total number of lines
        for category in self.pCategory.keys():
            self.pCategory[category] = self.nWordsInCategory[category] / self.num_lines

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
                    # Pre Processes each word and updates the question or answer
                    splittedLine[qaPos] = splittedLine[qaPos].replace(
                        word, self.preProcessing(word))

            maxP = 0.0
            result = ""
            # Loops through all possible categories
            for category in self.wordsInCategory.keys():
                # Calculates the Probability(Category|Line^)
                tmp = self.p(category, splittedLine[1:])
                # if max is lower than the recent calculated probabilty, updates possible solution
                if maxP < tmp:
                    maxP = tmp
                    result = category

            # Prints most probable category
            print(result)

        # Closes all files
        self.close()


    """ Closes all open files """
    def close(self):
        # Closes test file
        self.testFile.close()
        # Closes train file
        self.trainFile.close()
