import requests
import pyaudio
import sys
import time
import wave
import numpy as np
import matplotlib.pyplot as plt
import copy
import threading

subscription_key="7cb9a1e89af7482cbe0089c3528a05a8"

def get_token(key):
    token_url="https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers={"Ocp-Apim-Subscription-Key":key}
    response=requests.post(token_url,headers)
    accsess_token=str(response.text)
    print(accsess_token)


def speech_to_text():
    data=[]
    with open("sample001.wav","rb") as f:
        data=f.read()

    # with open("test.wav","wb") as f:
    #     f.write(data)

    speech_text_url="https://westus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=ja-JP&format=detailed"
    headers={
        "Ocp-Apim-Subscription-Key":"9c9c8c950a5042328ab194953df08cd0",
        "Content-type":'audio/wav; codec="audio/pcm";  samplerate=22000',
        "Accept":"application/json"
        }
    response=requests.post(speech_text_url,data=data,headers=headers)
    print(response.text)


def record(all,recording):
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    #RATE = 44100
    RATE = 8000
    RECORD_SECONDS = 10

    p = pyaudio.PyAudio()

    stream = p.open(
        format = FORMAT,
        channels = CHANNELS,
        rate = RATE,
        input = True,
        frames_per_buffer = chunk
    )

    #all = []
    for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
        data = stream.read(chunk)
        all.append(data)

    stream.close()
    p.terminate()
    recording[0]=False

    # data = b''.join(all)
    #
    # #%matplotlib inline
    # x = np.frombuffer(data, dtype="int16") / 32768.0
    #
    # plt.figure(figsize=(15,3))
    # plt.plot(x)
    # #plt.show()
    # plt.pause(0.1)

    # x = np.fft.fft(np.frombuffer(data, dtype="int16"))
    #
    # plt.figure(figsize=(15,3))
    # plt.plot(x.real[:int(len(x)/2)])
    # plt.show()


def audio_test():

    all=[]
    recording=[True]

    thread=threading.Thread(target=record,args=([all,recording]))
    thread.start()

    plt.figure(figsize=(15,3))
    while(recording[0]):
        graph_data = b''.join(all)
        x = np.frombuffer(graph_data, dtype="int16") / 32768.0
        x=x[-min(8000*3,len(x)):]

        plt.clf()
        plt.plot(x)
        plt.pause(0.1)


if __name__=="__main__":
    # get_token(subscription_key)
    # speech_to_text()
    audio_test()
