import json
from dataclasses import dataclass
from io import BytesIO

import aiohttp
import docx2txt
import magic
import PyPDF2
from odf import teletype
from odf import text as odf_text
from odf.opendocument import load
from striprtf.striprtf import rtf_to_text

from config import YAGPT_KEY, YAGPT_MODEL_URI

mime = magic.Magic(mime=True)


async def get_text(filename: str):
    async with aiohttp.ClientSession() as session:
        url = filename
        async with session.get(url) as resp:
            if resp.status == 200:
                body = await resp.read()

                mimetype = mime.from_buffer(body)

                print(mimetype)

                match mimetype:
                    case "text/plain":
                        return body.decode()
                    case "text/rtf":
                        return rtf_to_text(body.decode())
                    case "application/vnd.oasis.opendocument.text":
                        textdoc = load(BytesIO(body))
                        allparas = textdoc.getElementsByType(odf_text.P)
                        return " ".join([teletype.extractText(i) for i in allparas])

                    case "application/pdf":
                        pdf_reader = PyPDF2.PdfReader(BytesIO(body))

                        text = ""

                        for page_num in range(len(pdf_reader.pages)):
                            page = pdf_reader.pages[page_num]
                            text += page.extract_text()
                        return text

                    case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        return docx2txt.process(BytesIO(body))


@dataclass
class Info:
    fio: str


async def parse(filename: str):
    data = await get_text(filename)
    if not data:
        return filename, {}

    prompt = {
        "modelUri": YAGPT_MODEL_URI,
        "completionOptions": {
            "stream": False,
            "temperature": 0.5,
            "maxTokens": "2000",
        },
        "messages": [
            {
                "role": "system",
                "text": "Тебе необходимо по произвольно написанному резюме определить основную информацию о работнике. Верни в формате json (не используя вставку кода) такую информацию, как: ФИО (ключ fio), адрес электронной почты (ключ email), возраст (ключ age, тип int), опыт (ключ experience (вернуть в формате количество месяцев)), стек технологий (массив строк, ключ stack), предыдущие места работы (ключ jobs) (массив словарей, содержащих название компаний (ключ name), должность (ключ post), начало работы (start, unixtime, тип int), конец работы (end, unixtime; если не известно то 0, тип int)). Если какой-то информации нет в тексте соответствующему ключу пустое значение",
            },
            {
                "role": "user",
                "text": data,
            },
        ],
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YAGPT_KEY}",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=prompt) as resp:
            result = await resp.json()
            print(result)
            result = result["result"]["alternatives"][0]["message"]["text"]
            result = result.replace("#", "")
            result = result.replace("*", "")

    print("pars", result)
    return filename, json.loads(result)
