# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from thai import thai
import db_chat_log
chatbot = ChatBot(
    'Fah', # ชื่อแชตบ็อต
    storage_adapter='chatterbot.storage.SQLStorageAdapter', # กำหนดการจัดเก็บ ในที่นี้เลือก chatterbot.storage.SQLStorageAdapter เก็บเป็น Sqllite
    database='fah2.sqlite3', # ที่ตั้งฐานข้อมูล
    statement_comparison_function=thai,
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.unescape_html'
    ],
    filters=['chatterbot.filters.RepetitiveResponseFilter'],
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        #'timenow.TimeLogicAdapter',
        #'weather.WeatherLogicAdapter',
        {
            'import_path':'chatterbot.logic.LowConfidenceAdapter',
            'threshold':0.65,
            'default_response': 'ขออภัยค่ะ ฉันไม่เข้าใจสิ่งที่คุณต้องการบอกฉันค่ะ'
        }
    ]
)
def get_chatbot(text):
	text_sent=chatbot.get_response(text)
	db_chat_log.add_data(text,text_sent)
	return str(text_sent)
if __name__ == '__main__':
	while True:
		text=input("Text : ")
		if text=="exit":
			break
		response = get_chatbot(text)
		print(response)
