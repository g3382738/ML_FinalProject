import operator
import string
import os
import numpy as np

stop = ['2']


stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'subject']


def DicCreator(filepath):
    dict = {}
    f = open(filepath)
    # create a dictionary that contains all the words after eliminating the stopwords in file
    # and count the # of each word
    for line in f:
        # eliminate the punctuation
        line = line.translate(None, string.punctuation)
        # eliminate the number
        line = line.translate(None, string.digits)
        for word in line.strip().lower().split():
            if word not in stopwords:
                if dict.has_key(word):
                    dict[word] += 1
                else:
                    dict[word] = 1
    # sort the dictionary, return the result in 2-D array form with[(word, # of word),()...]
    # dictSorted = sorted(dict.items(), key = operator.itemgetter(1), reverse = True)
    return dict


def dictMerge(dict1, dict2):
    for key in dict2:
        if dict1.has_key(key):
            dict1[key] += dict2[key]
        else:
            dict1[key] = dict2[key]
    return dict1


def calculateTotalDict(folderpath):
    wholeDict = {}
    for file in os.listdir(folderpath):
        Path = folderpath + file
        dict = DicCreator(Path)
        wholeDict = dictMerge(wholeDict, dict)
    return wholeDict


def extractTopWords(dict):
    dictSorted = sorted(dict.items(), key = operator.itemgetter(1), reverse = True)
    top = []
    for i in range(len(dict)):
        top.append(dictSorted[i][0])

    return top


def extractTopWordsWithNumber(dict, number):
    dictSorted = sorted(dict.items(), key = operator.itemgetter(1), reverse = True)
    top = []
    for i in range(0, number):
        top.append(dictSorted[i][0])
        # print dictSorted[i][:]
    return top


def combineTopWordVector(topDict1, topDict2):
    for element in topDict2:
        if element not in topDict1:
            topDict1.append(element)
    return topDict1


def resultVector(ffp1,ffp2):
    dict1 = calculateTotalDict(ffp1)
    topDict1 = extractTopWordsWithNumber(dict1,100)
    # print topDict1
    dict2 = calculateTotalDict(ffp2)
    topDict2 = extractTopWordsWithNumber(dict2,100)
    result = combineTopWordVector(topDict1, topDict2)
    return result

def transfer(fileDj, vocabulary):
    file = open(fileDj)
    text = file.read().lower()
    BOWDj = np.zeros(len(vocabulary)+1)
    for word in text:
        if word in vocabulary:
            index = vocabulary.index(word)
            BOWDj[index] += 1
        else:
            BOWDj[173] += 1
    file.close()
    return BOWDj

def loadData(Path):

    trainDir = Path + "/enron1"
    trainPosDir = trainDir + "/spam"
    trainNegDir = trainDir + "/ham"
    testDir = Path + "/enron2"
    testPosDir = testDir + "/spam"
    testNegDir = testDir + "/ham"
    Xtrain = []
    ytrain = []
    Xtest = []
    ytest = []

    for file in os.listdir(trainPosDir):
        path = trainPosDir + "/" + file
        Xtrain.append(transfer(path, vocabulary))
        ytrain.append(1)

    for file in os.listdir(trainNegDir):
        path = trainNegDir + "/" + file
        Xtrain.append(transfer(path, vocabulary))
        ytrain.append(0)


    for file in os.listdir(testPosDir):
        path = testPosDir + "/" + file
        Xtest.append(transfer(path, vocabulary))
        ytest.append(1)

    for file in os.listdir(testNegDir):
        path = testNegDir + "/" + file
        Xtest.append(transfer(path, vocabulary))
        ytest.append(0)

    Xtrain = np.asarray(Xtrain)
    ytrain = np.asarray(ytrain)
    Xtest = np.asarray(Xtest)
    ytest = np.asarray(ytest)

    return Xtrain, Xtest, ytrain, ytest

def naiveBayesMulFeature_train(Xtrain, ytrain):

    alpha = 1
    posCount = np.sum(Xtrain[ytrain == 1], axis = 0)
    thetaPos = (posCount + alpha) / (Xtrain[ytrain == 1].sum() + alpha * len(vocabulary))
    negCount = np.sum(Xtrain[ytrain == 0], axis = 0)
    thetaNeg = (negCount + alpha) / (Xtrain[ytrain == 0].sum() + alpha * len(vocabulary))
    print Xtrain[0:30]
    print "posCount is :", posCount
    print "totalCount is :", Xtrain[ytrain == 1].sum()
    return thetaPos, thetaNeg

if __name__ == "__main__":

    ffp1 = "../dataset/processed/enron1/spam/"
    ffp2 = "../dataset/processed/enron1/ham/"
    path = "../dataset/processed/"
    vocabulary = resultVector(ffp1,ffp2)
    print len(vocabulary)
    Xtrain, Xtest, ytrain, ytest = loadData(path)
    # print len(Xtrain)
    # print len(Xtest)
    # print len(ytrain)
    # print len(ytest)
    thetaPos, thetaNeg = naiveBayesMulFeature_train(Xtrain, ytrain)
    print "thetaPos is: ", thetaPos
    print "thetaNeg is: ", thetaNeg

    # result = extractTopWords(dict)
    # print result
    # path1 = "../dataset/processed/enron1/enron1/spam/0008.2003-12-18.GP.spam.txt"
    # path2 = "../dataset/processed/enron1/enron1/spam/0017.2003-12-18.GP.spam.txt"
    # d1 = DicCreator(path1)
    # d2 = DicCreator(path2)
    # print d1
    # print d2
    # dict = dictMerge(d1, d2)
    # print dict
    # result = extractTopWords(dict, 3)
    # print result
