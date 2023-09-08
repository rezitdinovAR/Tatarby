import requests
def Translation(tr_mode:int, text:str):

    try:
        translate = requests.get("https://translate.tatar/translate?lang="+str(tr_mode)+"&text=" + text)
    except ...:
        print('Translation error. Check tr_mode')
        return 0

    return translate.text