

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import img_links


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
def get_topics(topic: str):
    try:
        return img_links.dict_img[topic]
    except KeyError:
        return "Неверный ключ"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

