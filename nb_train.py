from utils import *
import sys
import math
import numpy as np

def main():
    if len(sys.argv) < 2:
        print("nb_train [train_set dir]")
        return
    spam_list = []
    ham_list = []
    # word_count item => "word":[spam,ham]
    word_count = {}
    prior = [0, 0]

    # read index
    try:
        index_file = open(sys.argv[1]+'/index', 'r')
    except:
        print("training index does not exist")
        return

    for line in index_file:
        line = line.split()
        if len(line)<2:
            continue
        if len(line[1])<7:
            continue
        if line[1][:7] != "inmail.":
            continue
        if line[0].lower() == "spam":
            spam_list.append(line[1])
        elif line[0].lower() == "ham":
            ham_list.append(line[1]) 
    index_file.close()

    # go through both classes 
    i = 0 
    for id_class in [spam_list, ham_list]:
        
        # prior
        prior[i] = len(id_class)/float(len(spam_list)+len(ham_list))

        # counts
        for id_file in id_class:
            word_list = striptext(sys.argv[1]+'/'+id_file)
            for word in word_list:
                try:
                    count = word_count[word]
                except KeyError:
                    count = [0, 0]
                count[i] = count[i] + 1
                word_count[word] = count
        i += 1

    # calculate total count for each class
    total_count = [0, 0]
    for word in word_count:
        total_count[1] += word_count[word][1]
        total_count[0] += word_count[word][0]

    # calculate condprob, we change word_count to condprob
    for word in word_count:
        count = word_count[word]
        spam_prob = (count[0]+1)/float(total_count[0]+1)
        ham_prob = (count[1]+1)/float(total_count[1]+1)
        word_count[word] = [spam_prob, ham_prob]

    # set a condprob for spam/ham if count = 0
    spam_prob = 1/float(total_count[0]+1)
    ham_prob = 1/float(total_count[1]+1)

    # test section
    # read index reusing spam_list and ham_list
    # on training set first since we also need to know the accuracy of that
    index_file = open(sys.argv[1]+'/index', 'r')

    spam_list = []
    ham_list = []
    for line in index_file:
        line = line.split()
        if len(line)<2:
            continue
        if len(line[1])<7:
            continue
        if line[1][:7] != "inmail.":
            continue
        if line[0].lower() == "spam":
            spam_list.append(line[1])
        elif line[0].lower() == "ham":
            ham_list.append(line[1])
    index_file.close()

    # go through both classes and test on document if result
    # is same as the document class accurate_count++
    i = 0
    accurate_count = 0

    for id_class in [spam_list, ham_list]:

        # go through each file
        for id_file in id_class:
            word_list = striptext(sys.argv[1] + '/' + id_file)
            score = [0, 0]

            # calculate score for spam/ham
            for j in [0, 1]:
                score[j] = math.log2(prior[j])

                for word in word_list:
                    if word in word_count:
                        count = word_count[word][j]
                    elif j == 0:
                        count = spam_prob
                    elif j == 1:
                        count = ham_prob
                    score[j] += math.log2(count)

            # see which one is larger and see if it fit with the set
            if max(score) == score[i]:
                accurate_count += 1
        i += 1

    # calculate accuracy
    accuracy = accurate_count/float(len(spam_list)+len(ham_list))

    print("Training accuracy: " + "{:.2%}".format(accuracy))


    # save data output
    np.save('word_count',word_count)
    np.save('prior',prior)
    np.save('prob',[spam_prob,ham_prob])

    

    

main()
