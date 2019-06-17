import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle


# NLTK library expects any input string in the format of a dictionary with keys as the words and values as True or False
# This is how the Naive Bayes classifier expects the input
def create_word_features(words):
    # words here is a list of words
    useful_words = [word.lower() for word in words if word.lower() not in stopwords.words("english")]
    words_dict = dict([(word, True) for word in useful_words])
    # print(words_dict)
    return words_dict


def model_trainer():
    neg_reviews = []
    # getting the fileids of all 'neg' reviews in a list and iterating through those ids
    for fileid in movie_reviews.fileids('neg'):
        words = movie_reviews.words(fileid)
        neg_reviews.append((create_word_features(words), "negative"))

    print(neg_reviews[0])
    print(len(neg_reviews))

    pos_reviews = []
    for fileid in movie_reviews.fileids('pos'):
        words = movie_reviews.words(fileid)
        pos_reviews.append((create_word_features(words), "positive"))

    print(pos_reviews[0])
    print(len(pos_reviews))

    train_set = neg_reviews[:750] + pos_reviews[:750]
    test_set = neg_reviews[750:] + pos_reviews[750:]
    print(len(train_set), len(test_set))

    # creating our classifier
    global classifier
    classifier = NaiveBayesClassifier.train(train_set)

    # saving the classifier
    with open('my_dumped_classifier.pkl', 'wb') as fid:
        pickle.dump(classifier, fid)
    fid.close()
    # checking the accuracy of the classifier from the test data
    accuracy = nltk.classify.util.accuracy(classifier, test_set)
    print(accuracy * 100)


# function to return the mood
def mood_classifier(words_dict):
    global classifier
    mood = classifier.classify(words_dict)
    return mood  # returns 'positive' or 'negative'


# checking how the model works
def main():
    # model_trainer()
    # uncomment the line above to train the model, else load the trained model saved in the same directory
    # load the saved classifier
    global classifier
    with open('my_dumped_classifier.pkl', 'rb') as fid:
        classifier = pickle.load(fid)
    fid.close()

    stop = False
    while not stop:
        expression = input('Express your feelings...\n')
        words = word_tokenize(expression)
        words_dict = create_word_features(words)
        mood = mood_classifier(words_dict)  # should print the label 'positive' or 'negative'
        print(mood)
        c = input('Do you want to continue? (y/n): ')
        if c == 'n':
            stop = True
            print('Quitting judging your feelings...')
        else:
            continue


if __name__ == '__main__':
    main()
