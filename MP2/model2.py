# Model that Pre-processes words and uses algorithm.

# To exit the system
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
    stop_chars = {'_', ':', '?', '!', ';', '\"'}

    porter = PorterStemmer()
    
    for word in phrase.split():
        # Removes unecessary chars like the ones in the example above
        for char in stop_chars:
            if word.find(char) != -1:
                phrase = phrase.replace(word, word.replace(char, ''))
                word = word.replace(char, '')
            
        # Applies porter stemmer to word in phrase
        if word not in stop_words:
            phrase = phrase.replace(word, porter.stem(word))
        # Removes a stop word from the phrase
        else:
            phrase = phrase.replace(word, '')
    
    return phrase


""" This model uses a algorithm to calculate the similarity
    between the read line and all the lines in the training file.
    Selects the category of the trainning line wich is more similar.
"""
class M2:

    def __init__(self, testFile, trainFile) -> None:
        # opens files for reading
        try:
            self.testFile = open(testFile, "r")
            self.trainFile = open(trainFile, "r")

        # if exception is found reading file
        except OSError:
            print("Could not open/read file")
            sys.exit()

    """ Starts to run module """
    def compute(self):
        for line in self.trainFile:
            question = line.split("\t")[1]
            print("A:", question)
            print("D:", preProcessing(question))
        
        self.close()


    """ Closes all open files """
    def close(self):
        self.testFile.close()
        self.trainFile.close()
