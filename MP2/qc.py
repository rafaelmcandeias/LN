# Main py file. Manages the two models

import argparse
from model1 import m1
from model2 import m2

""" Main function that parses the command line and calls
    the other models.
"""
if __name__ == "__main__":
    # To read the command line
    parser = argparse.ArgumentParser()

    # -test testFile –train trainFile
    parser.add_argument("-test", "--testFile", help="TestFile")
    parser.add_argument("-train", "--trainFile", help="TrainFile")

    # gets the input command
    args = parser.parse_args()
    m1(args.testFile)
    m2(args.trainFile)

    print("TestFile {} TrainFile {} ".format(args.testFile, args.trainFile))