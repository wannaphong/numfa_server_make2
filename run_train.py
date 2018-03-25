# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from thai import thai
import db_chat_train,db_chat_log
chatbot = ChatBot(
    'Fah', # ชื่อแชตบ็อต
    storage_adapter='chatterbot.storage.SQLStorageAdapter', # กำหนดการจัดเก็บ ในที่นี้เลือก chatterbot.storage.SQLStorageAdapter เก็บเป็น Sqllite
    database='fah2.sqlite3', # ที่ตั้งฐานข้อมูล
    statement_comparison_function=thai,
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'timenow.TimeLogicAdapter',
        'weather.WeatherLogicAdapter',
        {
            'import_path':'chatterbot.logic.LowConfidenceAdapter',
            'threshold':0.65,
            'default_response': 'ขออภัยค่ะ ฉันไม่เข้าใจสิ่งที่คุณต้องการบอกฉันค่ะ'
        }
    ]
)
chatbot.set_trainer(ListTrainer)
def train_data(text):
	chatbot.train(text.split(','))
	return True
def get_chatbot(text):
	text_sent=chatbot.get_response(text)
	db_chat_log.add_data(text,text_sent)
	return text_sent
if __name__ == '__main__':
	while True:
		text=input("Text : ")
		if text=="exit":
			break
		train_data(text)