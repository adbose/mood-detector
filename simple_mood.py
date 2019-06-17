
positive_keywords = ["great", "happy", "amazing", "fantastic", "like", "love", "good", "awesome", "cool", "best",
                     "exciting"]
negative_keywords = ["disgusting", "boring", "sad", "depressing", "hate", "shit", "bad", "terrible", "horrible",
                     "annoying", "worst"]


# sample_sentence = "I am happy about being sad"
def analyse_mood(expression):
    words = expression.strip().lower().split()
    positive_mood_counter = 0
    negative_mood_counter = 0
    for word in words:
        if word in positive_keywords:
            positive_mood_counter += 1
        elif word in negative_keywords:
            negative_mood_counter += 1
        else:
            continue

    if positive_mood_counter >= negative_mood_counter:
        return 'positive'
    else:
        return 'negative'


# testing the file standalone
def main():
    stop = False
    while not stop:
        expression = input('Express your feelings...\n')
        mood = analyse_mood(expression)
        print(mood)  # should print the label 'positive' or 'negative'
        c = input('Do you want to continue? (y/n): ')
        if c == 'n':
            stop = True
            print('Quitting judging your feelings...')
        else:
            continue


if __name__ == '__main__':
    main()
