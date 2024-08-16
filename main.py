import os
import shutil
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Response, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import img_links
import quiz

app = FastAPI(title="ImgSite")
app.mount("/static", StaticFiles(directory="static"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("")
@app.get("/")
def test():
    return "ok"


@app.get('/get_topics')
def get_topics():
    return img_links.topics


@app.get('/get_topic/{topic}')
def get_topics(topic: str, response:Response):
    # Выложенные пользователями артинки попадают в отдельную папку для дальнейшей проверки
    if topic == "НаПроверку":
        print("Проверяемые файлы")
        # Необходимо составить список файлов во временной папке.
        # Указываем путь к папке.
        directory = "static/img/temp"
        # Получаем список файлов.
        files = os.listdir(directory)
        try:
            response.headers["x-total-count"] = str(len(files))
            new_files = []
            for i in files:
                new_files.append(f"static/img/temp/{i}")
            return new_files
        except KeyError:
            return "Неверный ключ"
    else:
        try:
            response.headers["x-total-count"] = str(len(img_links.dict_img[topic]))
            return img_links.dict_img[topic]
        except KeyError:
            return "Неверный ключ"


@app.get('/quiz')
def quiz():
    return quiz.quiz


@app.get('/check_user')
def check_user():
    return "Неавторизованный"


@app.post('/upload')
async def upload(file: UploadFile):
    try:
        print(file.size)
        date_now = datetime.strftime(datetime.now(), "%H:%M:%S")
        file_location = f"static/img/temp/{date_now}_{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

        return {"Result": "OK"}
    except:
        return {"Result": "Error"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

