import threading
import json
from chatbot.db.DatabaseConfig import *
from chatbot.db.Database import Database
from chatbot.server.BotServer import BotServer
from chatbot.Preprocess2 import Preprocess2
from chatbot.IntentModel import IntentModel
from chatbot.NerModel import NerModel
from chatbot.FindAnswer import FindAnswer

# 전처리 객체 생성
p = Preprocess2(word2index_dic='c:/workspace/FoodShop/chatbot/data/chatbot_dict.bin',
                userdic='c:/workspace/FoodShop/chatbot/data/user_dic.tsv')

# 의도 파악 모델
intent = IntentModel(model_name='c:/workspace/FoodShop/chatbot/model/intent_model.h5',
                     preprocess=p)

# 개체명 인식 모델
ner = NerModel(model_name='c:/workspace/FoodShop/chatbot/model/ner_model.h5',
               preprocess=p)

def to_client(conn, addr, params):
    db = params['db']
    try:
        db.connect() # DB 연결
        # 데이터 수신
        read = conn.recv(2048)
        print('='* 50)
        print('Connection from: %s' % str(addr))
        # 클라이언트 연결이 끊어지거나, 오류가 있는 경우
        if read is None or not read:
            print('클라이언트 연결이 끊어졌습니다.')
            exit(0)
        # json 데이터로 변환
        recv_json_data = json.loads(read.decode())
        print('데이터 수신:', recv_json_data)
        query = recv_json_data['Query']
        # 의도 파악
        intent_predict = intent.predict_class(query)
        intent_name = intent.labels[intent_predict]
        # 개체명 파악
        ner_predicts = ner.predict(query)
        ner_tags = ner.predict_tags(query)
        # 답변 검색
        try:
            f = FindAnswer(db)
            answer_text, answer_image = f.search(intent_name, ner_tags)
            answer = f.tag_to_word(ner_predicts, answer_text)
        except:
            answer = '죄송해요. 무슨 말인지 모르겠어요. 조금 더 공부 할게요.'
            answer_image = None
        send_json_data_str = {
            'Query': query,
            'Answer': answer,
            'AnswerImageUrl': answer_image,
            'Intent': intent_name,
            'NER': str(ner_predicts)
        }
        message = json.dumps(send_json_data_str)
        conn.send(message.encode())
    except Exception as ex:
        print(ex)
    finally:
        if db is not None:
            db.close() # db 연결 끊기
        conn.close()

if __name__ == '__main__':
    # 질문/답변 학습 DB 연결 객체 생성
    db = Database(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
    )
    print('DB 접속')
    port = 5050
    listen = 100
    # 봇 서버 동작
    bot = BotServer(port, listen)
    bot.create_sock()
    print('bot start')
    while True:
        conn, addr = bot.ready_for_client()
        params = {
            'db': db
        }
        client = threading.Thread(target=to_client,
                                  args=(conn, addr, params))
        client.start()