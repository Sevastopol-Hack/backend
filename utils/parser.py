import asyncio
from dataclasses import dataclass
from io import BytesIO

import aiohttp
import PyPDF2
import docx2txt
import magic
from odf import teletype
from odf import text as odf_text
from odf.opendocument import load
from striprtf.striprtf import rtf_to_text

mime = magic.Magic(mime=True)

YAGPT_KEY = "AQVN2Vd-gMlDAjVPAKNMAYxb7t6JpNOag60-Mcgz"
YAGPT_MODEL_URI = "gpt://b1g2ahktcv1255vqabvd/yandexgpt"


async def get_text(filename: str):
    # mimetype = mime.from_file(filename)

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
                        print(allparas)
                        return " ".join([teletype.extractText(i) for i in allparas])
                        # teletype.extractText(allparas[0])
                        # print()
                        # return teletype.extractText(allparas[0])
                    case "application/pdf":
                        pdf_reader = PyPDF2.PdfReader(BytesIO(body))

                        text = ''

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
    print(data)
    if not data:
        return

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
                "text": "Тебе необходимо по произвольно написанному резюме определить основную информацию о работнике. Верни в формате json (не используя вставку кода) такую информацию, как: ФИО (ключ fio), адрес электронной почты (ключ email), возраст (ключ age, тип int), опыт (ключ exp (вернуть в формате количество месяцев)), стек технологий (массив строк, ключ stack), предыдущие места работы (ключ jobs) (массив словарей, содержащих название компаний (ключ name), должность (ключ post), начало работы (from, unix время), конец работы (to, unix время)). Если какой-то информации нет в тексте соответствующему ключу пустое значение",
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
            result = result["result"]["alternatives"][0]["message"]["text"]
            result = result.replace("#", "")
            result = result.replace("*", "")
    return filename, result


async def main():
    print(await parse(
        "https://files.biwork.tech/biwork/85988bc3-d004-4021-b89d-3b93bb5f0388_7b0905696fa3321ad19b102a2a5ff0c1.rtf?AWSAccessKeyId=tbdnQvks053pl55YRlm3&Signature=uniAO1unXuUFv3IAJl0UUzEDtFk%3D&Expires=1717271611"))

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
