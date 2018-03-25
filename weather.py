# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from chatterbot.logic import LogicAdapter
from pythainlp.tokenize import word_tokenize
from nltk import NaiveBayesClassifier
from chatterbot.conversation import Statement

class WeatherLogicAdapter(LogicAdapter):
    """
    A logic adapter that returns information regarding the weather and
    the forecast for a specific location. Currently, only basic information
    is returned, but additional features are planned in the future.
    """

    def __init__(self, **kwargs):
        super(WeatherLogicAdapter, self).__init__(**kwargs)
        self.positive = kwargs.get('positive', [" ".join(word_tokenize(i)) for i in ['พยากรณ์อากาศ','สภาพอากาศ','ตอนนี้อากาศเป็นอย่างไร','สภาพอากาศ']])

        self.negative = kwargs.get('negative', [" ".join(word_tokenize(i)) for i in ['อากาศวันนี้ร้อน','อากาศหนาวมาก','อากาศร้อน','ไม่เห็นหนาวเลย']])

        labeled_data = (
            [(name, 0) for name in self.negative] +
            [(name, 1) for name in self.positive]
        )

        train_set = [
            (self.time_question_features(text), n) for (text, n) in labeled_data
        ]

        self.classifier = NaiveBayesClassifier.train(train_set)
    def can_process(self, statement):
        if 'พยากรณ์' in word_tokenize(statement.text) or  'พยากรณ์อากาศ' in word_tokenize(statement.text)  or 'อากาศ' in word_tokenize(statement.text):
            return True
        else:
            return False
    def time_question_features(self, text):
        """
        Provide an analysis of significant features in the string.
        """
        features = {}

        # A list of all words from the known sentences
        all_words = " ".join(self.positive + self.negative).split()

        # A list of the first word in each of the known sentence
        all_first_words = []
        for sentence in self.positive + self.negative:
            all_first_words.append(
                sentence.split(' ', 1)[0]
            )

        for word in word_tokenize(text):
            features['first_word({})'.format(word)] = (word in all_first_words)

        for word in word_tokenize(text):
            features['contains({})'.format(word)] = (word in all_words)

        for letter in 'abcdefghijklmnopqrstuvwxyzกขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮุูึๆไำะัํี๊ฯโเ้็่๋า.แิื์ใๅ':
            features['count({})'.format(letter)] = text.lower().count(letter)
            features['has({})'.format(letter)] = (letter in text.lower())

        return features
    def process(self, statement):
        time_features = self.time_question_features(statement.text.lower())
        confidence = self.classifier.classify(time_features)
        response = Statement('weather')
        response.confidence = float(confidence)
        return response