import requests

subscription_key="7cb9a1e89af7482cbe0089c3528a05a8"

def get_token(key):
    token_url="https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers={"Ocp-Apim-Subscription-Key":key}
    response=requests.post(token_url,headers)
    accsess_token=str(response.text)
    print(accsess_token)

def test():
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


if __name__=="__main__":
    # get_token(subscription_key)
    test()
