"""
O ficheiro calcula accuracy do nosso resultado com o dev
"""
if __name__ == "__main__":
    resultsFile = open("results.txt", "r")
    testFile = open("dev.txt", "r")

    testlines = testFile.readlines()
    resultslines = resultsFile.readlines()

    rights = 0

    for linePos in range(len(testlines)):
        if testlines[linePos].split("\t")[0] == resultslines[linePos][:-1]:
            rights += 1
    
    print("Accuracy:", rights/len(testlines))
