

import uvicorn
from fastapi import FastAPI, Response
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
    try:
        response.headers["x-total-count"] = str(len(img_links.dict_img[topic]))
        return img_links.dict_img[topic]
    except KeyError:
        return "Неверный ключ"


@app.get('/quiz')
def quiz():
    return quiz.quiz


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

