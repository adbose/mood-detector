from advanced_mood import *


def main():
    stop = False
    while not stop:
        text = input('Enter your text below...\n')
        pos_tagged_text = postag(text)
        dict_tagged_text = dicttag(pos_tagged_text)
        print(dict_tagged_text)
        sentiment_score = get_sentiment_score2(dict_tagged_text)
        print('The sentiment score is: ', sentiment_score)

        if sentiment_score > 0:
            print('The sentiment is positive')
        elif sentiment_score < 0:
            print('The sentiment is negative')
        else:
            print('The sentiment is mixed')

        c = input('Do you want to continue? (y/n): ')
        if c == 'n':
            stop = True
            print('Quitting judging your feelings...')
        else:
            continue


if __name__ == '__main__':
    main()
