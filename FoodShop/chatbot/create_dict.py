from Preprocess1 import Preprocess1
from tensorflow.keras import preprocessing
import pickle

# 말뭉치 데이터 읽어오기
def read_corpus_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
    return data

# 말뭉치 데이터 가져오기
corpus_data = read_corpus_data('c:/workspace/FoodShop/chatbot/data/corpus.txt')

# 말뭉치 데이터에서 키워드만 추출해서 사전 리스트 생성
p = Preprocess1(userdic='c:/workspace/FoodShop/chatbot/data/user_dic.tsv')
dict = []
for c in corpus_data:
    pos = p.pos(c[1])
    for k in pos:
        dict.append(k[0])

# 사전에 사용될 word2index 생성
tokenizer = preprocessing.text.Tokenizer(oov_token='OOV') # 사전의 첫번째 인덱스: OOV
tokenizer.fit_on_texts(dict)
word_idnex = tokenizer.word_index

# 단어 인덱스 사전 파일 생성
f = open('c:/workspace/FoodShop/chatbot/data/chatbot_dict.bin', 'wb')
try:
    pickle.dump(word_idnex, f)
except Exception as e:
    print(e)
finally:
    f.close()
print('완료되었습니다.')