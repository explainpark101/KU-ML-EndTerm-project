

id_name = "12월 05일"



import numpy as np

import pandas as pd

from tensorflow.keras.models import Sequential

from keras.layers import Dense, LSTM



def load_data(filename, label=True):  # 필요에 따라 레이블을 사용할수도 안할수도 있음

    df = pd.read_csv(filename)

    X = df.loc[:, ["GR", "ILD_log10", "DeltaPHI", "PHIND", "NM_M", "RELPOS"]].values

    if label:

        y = df.loc[:, "Facies"].values - 1  # 레이블 값을 지난번과 다르게 0~8까지로 사용하도록 변경

        return X, y

    else:

        return X


X, y = load_data("training_data.csv")  # 지난번과 같은 데이터


y.min(), y.max()



import tensorflow as tf  # 텐서플로우를 이용해서 마음대로 네트워크 구성
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dropout, Dense
from tensorflow import keras


model = Sequential()
#print(X.shape,y.shape)


X = X.reshape(X.shape[0], X.shape[1], 1) #LSTM 모델 이용을위한 3차원배열 reshape

model = Sequential()
model.add(LSTM(512,input_shape=(6, 1),return_sequences=True)) #input_shape은 x의 라벨값 6개 시퀀스 출력은 True 512차원 출력
model.add(Dropout(0.3)) #과적합 방지를 위한 드랍아웃 비율은 0.3
model.add(LSTM(256, return_sequences=True)) #LSTM 층  256차원출력
model.add(Dropout(0.3)) #드랍아웃 층
model.add(LSTM(128)) #LSTM층 128차원 출력
model.add(Dense(128)) #은닉층
model.add(Dropout(0.3)) #드랍아웃 층
model.add(Dense(9)) #은닉층
model.add(Dense(9, activation='softmax')) #활성화 함수 소프트맥스 사용 출력은 0~8 사이인 9개의 차원출력
model.compile(loss='categorical_crossentropy', optimizer='rmsprop' ,metrics=['accuracy'])
model.summary()

model.fit(X, y, epochs=200,
          batch_size=8, verbose=1)




X_test = load_data("test_data_no_label.csv", label=False)  # 레이블이 없는 테스트파일을 이용해서 예측했던 클래스를 csv로 저장

X_test= X_test.reshape(X_test.shape[0], X_test.shape[1], 1) # LSTM층 에 맞게 형변환

y_score = model.predict(X_test)


y_pred = np.argmax(y_score, axis=1)
print(y_pred)
pd.Series(y_pred, name='Facies').to_csv(id_name + ".csv")