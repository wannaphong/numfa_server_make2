# -*- coding: utf-8 -*-
'''
pip install googletrans
'''
from googletrans import Translator
translator = Translator()
def translator_to_thai(text):
	return translator.translate(text,dest='th').text