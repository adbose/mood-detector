# based on the tutorial from http://fjavieralba.com/basic-sentiment-analysis-with-python.html

import nltk
import yaml
from nltk.stem import WordNetLemmatizer


class Splitter(object):
    def __init__(self):
        self.nltk_sentences_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, text):
        """
        Input format: A paragraph of text.
        Output format: A list of lists of words in the text.
            e.g.: 'This is a sentence. This is another one.'
            Gets converted into a list of list of sentences where each sentence is a list of tokens.
            [['this', 'is', 'a', 'sentence', '.'], ['This', 'is', 'another', 'one', '.']]
        """

        print('\nConverting the text into list of sentences...')
        sentences_list = self.nltk_sentences_splitter.tokenize(text)
        print(sentences_list)

        print('\nTransforming the list of sentences so that each sentence is a list of tokens...')
        tokenized_text = [self.nltk_tokenizer.tokenize(sentence.lower()) for sentence in sentences_list]
        print(tokenized_text)

        return tokenized_text


class PosTagger(object):
    def __init__(self):
        pass

    def pos_tag(self, tokenized_text):
        """
            Input format: list of lists of words.
                e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
            Output format: list of lists of tagged tokens. Each tagged tokens has a form, a lemma, and a list of tags
                e.g: [[('this', 'this', ['DT']), ('is', 'be', ['VB']), ('a', 'a', ['DT']),
                ('sentence', 'sentence', ['NN'])], [('this', 'this', ['DT']), ('is', 'be', ['VB']),
                ('another', 'another', ['DT']), ('one', 'one', ['CARD'])]]
        """

        lemmatizer = WordNetLemmatizer()
        print('\nConverting the tokenised text into POS tagged object...')
        pos_tagged_text_list = [nltk.pos_tag(each_sentence_list) for each_sentence_list in tokenized_text]
        # convert it into [(word, lemma, [tags]), (.,.,[.]), ...]
        pos_tagged_word_lemma_text_list = [[(word, lemmatizer.lemmatize(word), [postag]) for (word, postag) in sentence]
                                           for sentence in pos_tagged_text_list]
        print(pos_tagged_word_lemma_text_list)

        return pos_tagged_word_lemma_text_list


class DictionaryTagger(object):

    def __init__(self, dictionary_paths):
        files = [open(path, 'r') for path in dictionary_paths]
        dictionaries = [yaml.load(dict_file, Loader=yaml.FullLoader) for dict_file in files]
        map(lambda x: x.close(), files)
        self.dictionary = {}
        self.max_key_size = 0

        for current_dict in dictionaries:  # dictionary format {keyword : [positive], ...}
            print('Current Dictionary...\n', current_dict)
            for key in current_dict:
                if key in self.dictionary:  # i.e. if key in dictionary object keys...
                    self.dictionary[key].extend(current_dict[key])
                else:
                    self.dictionary[key] = current_dict[key]
                    self.max_key_size = max(self.max_key_size, len(key))

    def tag(self, pos_tagged_text):  # after entire preprocessing pipeline

        return [self.tag_sentence(sentence) for sentence in pos_tagged_text]  # sentence in the form of list of tokens

    def tag_sentence(self, sentence, tag_with_lemmas=False):
        """
            The result is only one tagging of all the possible ones.
            The resulting tagging is determined by these two priority rules:
                - longest matches have higher priority
                - search is made from left to right
        """
        tagged_sentence = []
        length = len(sentence)  # number of tokens in the sentence
        if self.max_key_size == 0:
            self.max_key_size = length

        i = 0
        while i < length:
            j = min(i + self.max_key_size, length)
            tagged = False
            while j > i:
                expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
                expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
                if tag_with_lemmas:
                    literal = expression_lemma
                else:
                    literal = expression_form

                if literal in self.dictionary:
                    # self.logger.debug("found: %s" % literal)
                    is_single_token = j - i == 1
                    original_position = i
                    i = j
                    taggings = [tag for tag in self.dictionary[literal]]
                    tagged_expression = (expression_form, expression_lemma, taggings)

                    if is_single_token:  # if the tagged literal is a single token, conserve its previous taggings
                        original_token_tagging = sentence[original_position][2]
                        tagged_expression[2].extend(original_token_tagging)
                    tagged_sentence.append(tagged_expression)
                    tagged = True
                else:
                    j = j - 1
            if not tagged:
                tagged_sentence.append(sentence[i])
                i += 1
        return tagged_sentence


# separate helper function to preprocess input text into pos tagged object of the input text
def postag(text):

    splitter = Splitter()
    postagger = PosTagger()

    tokenized_text = splitter.split(text)
    pos_tagged_sentences = postagger.pos_tag(tokenized_text)

    return pos_tagged_sentences


# function to add sentiment tag to pos tagged object of the input text
def dicttag(pos_tagged_text):
    dicttagger = DictionaryTagger(['dicts/positive.yml', 'dicts/negative.yml', 'dicts/inc.yml', 'dicts/dec.yml'])

    return dicttagger.tag(pos_tagged_text)


# separate helper function to return a positive, negative or 0 based on the sentiment being positive or negative
# used by the sentiment_score method used to find the final value of the calculated sentiment
def value_of(sentiment):
    if sentiment == 'positive':
        return 1
    if sentiment == 'negative':
        return -1

    return 0


# called by the driver function to calculate the sentiment based on positive and negative keywords
def get_sentiment_score(dict_tagged_sentences):
    return sum([value_of(tag) for sentence in dict_tagged_sentences for token in sentence for tag in token[2]])


# calculating score taking into account degree of positive and negative keywords
def sentence_score(sentence_tokens, previous_token, acum_score):
    if not sentence_tokens:
        return acum_score
    else:
        current_token = sentence_tokens[0]
        tags = current_token[2]
        token_score = sum([value_of(tag) for tag in tags])
        if previous_token is not None:
            previous_tags = previous_token[2]
            if 'inc' in previous_tags:
                token_score *= 2.0
            elif 'dec' in previous_tags:
                token_score /= 2.0
            elif 'inv' in previous_tags:
                token_score *= -1.0
        return sentence_score(sentence_tokens[1:], current_token, acum_score + token_score)


# called by the driver function to calculate the sentiment based on weight of dictionary keywords
def get_sentiment_score2(review):
    return sum([sentence_score(sentence, None, 0.0) for sentence in review])


# main driver code
def main():
    """
        Driver code for the mood detector app.
    """
    text = """
            What can I say about this place? The staff of the restaurant is nice and the eggplant is not bad. Apart
            from that, very uninspired food, lack of atmosphere and too expensive. I am a staunch vegetarian and was 
            sorely disappointed with the veggie options on the menu. Will be the last time I visit, I recommend others
            to avoid.
           """
    print('The original text is...\n', text)

    pos_tagged_text = postag(text)

    dict_tagged_text = dicttag(pos_tagged_text)
    print('\nThe preprocessed, tokenized and dictionary tagged text is...')
    print(dict_tagged_text)

    print('\nBasic keyword based sentiment score: ', get_sentiment_score(dict_tagged_text))
    # We accept this score because it's the net sum of positive and negative scores. A net positive score can be
    # considered positive
    print('\nSentiment score of dictionary tagged with weights and inverse on keywords: ',
          get_sentiment_score2(dict_tagged_text))


if __name__ == '__main__':
    main()















