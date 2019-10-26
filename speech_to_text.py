import requests
import pyaudio
import sys
import time
import wave
import numpy as np
import matplotlib.pyplot as plt
import copy
import threading

subscription_key="9c9c8c950a5042328ab194953df08cd0"

def get_token(key):
    token_url="https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers={"Ocp-Apim-Subscription-Key":key}
    response=requests.post(token_url,headers)
    accsess_token=str(response.text)
    print(accsess_token)


def speech_to_text(file_path,key,rate):
    data=[]
    with open(file_path,"rb") as f:
        data=f.read()

    # with open("test.wav","wb") as f:
    #     f.write(data)

    speech_text_url="https://westus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=ja-JP&format=detailed"
    headers={
        "Ocp-Apim-Subscription-Key":key,
        "Content-type":'audio/wav; codec="audio/pcm";  samplerate={0}'.format(rate),
        "Accept":"application/json"
        }
    response=requests.post(speech_text_url,data=data,headers=headers)
    print(response.text)


def speech_to_text_chunk(data,key,rate,is_first=False):
    speech_text_url="https://westus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=ja-JP&format=detailed"
    headers={
        "Ocp-Apim-Subscription-Key":key,
        "Content-type":'audio/wav; codec="audio/pcm";  samplerate={0}'.format(rate),
        "Accept":"application/json",
        "Transfer-Encoding":"chunked"
        }
    # if is_first:
    #     headers["Expect"]="100-continue"

    response=requests.post(speech_text_url,data=data,headers=headers)
    print(response)


def chunk_test(file_path,key,rate):
    fdata=[]
    with open(file_path,"rb") as f:
        fdata=f.read()

    hdata=fdata[0:44]
    data=fdata[44:]

    # speech_to_text(file_path,key,rate)
    speech_to_text_chunk(fdata,key,rate,True)
    # speech_to_text_chunk(data,key,rate,True)
    # speech_to_text_chunk(data,key,rate,True)
    # speech_to_text_chunk(data,key,rate)


def record(all,recording):
    chunk = 1024 * 16
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
    counter=0
    for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
        data = stream.read(chunk)

        x = np.frombuffer(data, dtype="int16")
        if max(x)>1000:
            print("record!")
            counter=int(RATE / chunk * 3)
            # speech_to_text("rec.wav",subscription_key,RATE)

        if counter>0:
            all.append(data)
            # thread=threading.Thread(target=speech_to_text_chunk,args=([data,subscription_key,RATE,True]))
            # thread.start()
            #speech_to_text_chunk(data,subscription_key,RATE,True)
            counter-=1

# speech_to_text_chunk(b"",subscription_key,RATE)

    stream.close()
    p.terminate()

    wf = wave.open("rec.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(all))
    wf.close()

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
        x = np.frombuffer(graph_data, dtype="int16")
        x=x[-min(8000*3,len(x)):]

        plt.clf()
        plt.plot(x)
        plt.pause(0.1)

    # speech_to_text("rec.wav",subscription_key,8000)
    # speech_to_text_chunk(all,subscription_key,8000)


if __name__=="__main__":
    # get_token(subscription_key)
    # speech_to_text("sample001.wav",subscription_key,8000)
    # audio_test()
    chunk_test("rec.wav",subscription_key,8000)
