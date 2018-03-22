import logging
import operator
from collections import Counter

from image_detection.train_images.classify_image import get_image_classification


class Recognition(object):
    DEFAULT_BEST_SCORE = 0.73

    def __init__(self, filename):
        self.filename = filename

    def classify_image(self):
        classifications = get_image_classification(self.filename)
        logging.debug(classifications)
        max_key = max(classifications.keys(), key=float)
        keys = {}
        if max_key > self.DEFAULT_BEST_SCORE:
            logging.debug('max_key={}'.format(max_key))
            image_classification = classifications[max_key]['value']
        else:
            keys_values = [sentences['value']
                           for key, sentences in classifications.items()]
            logging.debug('keys_values={}'.format(keys_values))
            keys = self.find_keyword(keys_values)
            logging.debug('keys={}'.format(keys))
            max_count_key = max(keys.items(), key=operator.itemgetter(1))
            logging.debug('max_count_key={}'.format(max_count_key[0]))
            image_classification = max_count_key[0]

        return {
            'value': image_classification,
            'helpers': keys,
            'accuracy': max_key}

    def find_keyword(self, keywords):
        words = []
        for keyword in keywords:
            sentence = str(keyword).split()
            sentence = self.get_common_keys_in_sentence(sentence)
            words += sentence
        return dict(Counter(words))

    def get_common_keys_in_sentence(self, sentence):
        new_words = []
        words = sentence
        for word in words:
            for second_word in words:
                if word in second_word:
                    if word is second_word:
                        pass
                    else:
                        found_word = second_word.replace(word, '')
                        if ',' in found_word:
                            found_word = found_word.replace(',', '')
                        new_words.append(found_word)
        new_words = [char for char in new_words if char != '']
        words = [old_word.replace(',', ' ') for old_word in words]
        all_words = words + new_words
        return all_words
