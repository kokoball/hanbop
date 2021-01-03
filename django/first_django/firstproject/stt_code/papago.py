import os
import sys
import urllib.request
import json

def translate(text):
    client_id = "1JCDEWadHrknViXMvXTa" # 개발자센터에서 발급받은 Client ID 값
    client_secret = "sr6M6ubuQL" # 개발자센터에서 발급받은 Client Secret 값

    encText = urllib.parse.quote(text)
    data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)

    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        res = (response_body.decode('utf-8'))
        return json.loads(res)['message']['result']['translatedText']
    else:
        print("Error Code:" + rescode)
