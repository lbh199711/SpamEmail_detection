# SpamEmail_detection
Spam filter using naive bayes classification

nb_train.py
   * to run: python3 nb_train.py [train_set dir] <br />
   * prior.npy, prob.npy, word_count.npy is the data learned from the given training set<br />
   * to use your own data delete the default npy data first<br />
   
nb_classify.py
   * to run: python3 nb_classify.py test_file<br />
   * need the data from nb_train.py to work<br />

> train.tar.gz contains training data set, you can use your own if you wish to.<br />
> all given .npy data is trained using the given data set, delete before training on new data set.<br />
> data set should contains raw-email with name "inmail.*id*"<br />
> data set should contain index file that contains the information about each raw-email with format "class inmail.*id*" on each line<br />

