import math
import sys
import numpy as np
from utils import *

def main():
    
    if len(sys.argv) < 2:
        print("nb_classify email")
        return 
    # load
    try:
        prior = np.load('prior.npy')
        prob = np.load('prob.npy')
        word_count = np.load('word_count.npy').item()
             
    except NameError:
        print('data set does not exist, run nb_train first')
        return
    spam_prob = prob[0]
    ham_prob = prob[1]
    word_list = striptext(sys.argv[1])
    score = [0, 0]

    # calculate score for spam/ham
    for i in [0, 1]:
        score[i] = math.log2(prior[i])

        for word in word_list:
            if word in word_count:
                count = word_count[word][i]
            elif i == 0:
                count = spam_prob
            elif i == 1:
                count = ham_prob
            score[i] += math.log2(count)
    if score[0] > score[1]:
        print('It is most likely to be a spam email')
    elif score[0] < score[1]:
        print('It is most likely to be an useful mail')
    else:
        print('Inconclusive')


main()
