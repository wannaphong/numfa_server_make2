# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from chatterbot.logic import LogicAdapter
from pythainlp.tokenize import word_tokenize
from nltk import NaiveBayesClassifier
from chatterbot.conversation import Statement


class TimeLogicAdapter(LogicAdapter):
    """
    The TimeLogicAdapter returns the current time.

    :kwargs:
        * *positive* (``list``) --
          The time-related questions used to identify time questions.
          Defaults to a list of thai sentences.
        * *negative* (``list``) --
          The non-time-related questions used to identify time questions.
          Defaults to a list of thai sentences.
    """
    def can_process(self, statement):
        if 'เวลา' in word_tokenize(statement.text) or 'โมง' in word_tokenize(statement.text) or 'เพลา' in word_tokenize(statement.text):
            return True
        else:
            return False
    def __init__(self, **kwargs):
        super(TimeLogicAdapter, self).__init__(**kwargs)
        self.positive = kwargs.get('positive', [" ".join(word_tokenize(i)) for i in ['ตอนนี้เป็นเวลาเท่าไร','ขณะนี้เป็นเวลาเท่าไร','เวลาเท่าไร','กี่โมงแล้ว','เพลาเท่าไร','ดูเวลาให้หน่อย']])

        self.negative = kwargs.get('negative', [" ".join(word_tokenize(i)) for i in ['ถึงเวลานอนแล้ว','กาลเวลาไม่เคยรอใคร','ตรงต่อเวลา','อีกกี่นาที','เวลาค่อยๆเดินผ่านไป','เวลาที่ไม่มีใคร','ตอนนี้น่าเบื่อ']])

        labeled_data = (
            [(name, 0) for name in self.negative] +
            [(name, 1) for name in self.positive]
        )

        train_set = [
            (self.time_question_features(text), n) for (text, n) in labeled_data
        ]

        self.classifier = NaiveBayesClassifier.train(train_set)

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
        now = datetime.now()

        time_features = self.time_question_features(statement.text.lower())
        confidence = self.classifier.classify(time_features)
        response = Statement('ขณะนี้เป็นเวลา ' + now.strftime('%H:%M')+" นาฬิกาค่ะ")
        response.confidence = float(confidence)
        return response