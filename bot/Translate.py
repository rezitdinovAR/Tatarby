import requests
import base64

def translate_text(tr_mode:int, text:str):

    translate = requests.get("https://translate.tatar/translate?lang="+str(tr_mode)+"&text=" + text)
    text = translate.text[
        translate.text.find("<mt>") + 4: translate.text.rfind("</mt>")
    ]

    return text

def synth_tatar_speach(text:str, path: str):

    response = requests.get('https://tat-tts.api.tatarby.tugantel.tatar/listening/?text='+text)

    with open(f'{path}' ,mode='wb') as f: #проблема в FileExistsError поэтому удаляйте предыдущий temp.wav
            f.write(base64.b64decode(response.text[15:response.text.find(',')])) #т.к. при вызове создаётся новый

    return path
