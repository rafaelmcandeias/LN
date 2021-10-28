# Simple model used as baseline.
# 
import sys
import linecache

class M1:
    def __init__(self, testFile, trainFile) -> None:
        # opens files for reading
        # trains and tests
        try:
            self.testFile = open(testFile, "r")
            self.trainFile = open(trainFile, "r")
            #self.train()
            #self.test()
            # closes files
            self.testFile.close()
            self.trainFile.close()
        
        # if exception is found reading file
        except OSError:
            print("Could not open/read file")
            sys.exit()


    #def train(self, ):
        # for debugging
        #print("training...")


    """ Method that it's used to test the model """
    #def test(self):
        # for debugging
        #print("testing...")
