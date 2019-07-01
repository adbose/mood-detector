from advanced_mood import *

def main():
    text = input('Enter your text below...\n')
    pos_tagged_text = postag(text)
    dict_tagged_text = dicttag(pos_tagged_text)
    sentiment_score = get_sentiment_score2(dict_tagged_text)
    print('The sentiment score is: ', sentiment_score)


    if sentiment_score > 0:
        print('The sentiment is positive')
    elif sentiment_score < 0:
        print('The sentiment is negative')
    else:
        print('The sentiment is mixed')


if __name__ =='__main__':
    main()
