import Translate
import os


class Book:


    def __init__(self, bool_id: int, title_ru: str, title_tat: str, desc_ru: str, desc_tat: str, path: str,
                 content: str):
        self.book_id = bool_id
        self.title = dict()
        self.desc = dict()
        self.path = ""
        self.content = ""
        self.pages = {
            "ru": [],
            "tat": [],
            "audio": []
        }
        self.title["ru"] = title_ru
        self.title["tat"] = title_tat
        self.desc["ru"] = desc_ru
        self.desc["tat"] = desc_tat
        self.path = path
        content = content.replace(':', '')
        content = content.replace('"', '')
        content = content.replace('-', '')
        content = content.replace('—', '')
        content = content.replace(';', '')
        t = 0
        l = 0
        for i in range(len(content)):
            t += 1
            if t > 700:
                if content[t] == ' ':
                    self.pages["ru"].append(content[l:i])
                    page = len(self.pages["ru"]) - 1
                    if not os.path.isfile(f"tat_text/{bool_id}.{page}.txt"):
                        # translate = Translate.translate_text(0, self.pages["ru"][-1])
                        # with open(f"tat_text/{bool_id}.{page}.txt", "w", encoding="utf-8") as file:
                        #     file.write(translate)
                        translate = ""
                    else:
                        with open(f"tat_text/{bool_id}.{page}.txt", "r", encoding="utf-8") as file:
                            translate = "".join(file.readlines())
                    self.pages["tat"].append(translate)
                    if not os.path.isfile(f"audio/{bool_id}.{page}.wav"):
                        self.pages["audio"].append(
                            # Translate.synth_tatar_speach(self.pages["tat"][-1], f"audio/{bool_id}.{page}.wav")
                            f"audio.ogg"
                        )
                    else:
                        self.pages["audio"].append(f"audio/{bool_id}.{page}.wav")
                    l = i
                    t = 0

    def to_string(self, language):
        return f"""{self.title[language]}

{self.desc[language]}

/book{self.book_id}"""
