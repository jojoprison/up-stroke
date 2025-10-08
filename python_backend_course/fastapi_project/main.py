from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# Serve minimal static UI at /ui
static_dir = (Path(__file__).parent / "static")
app.mount("/ui", StaticFiles(directory=str(static_dir), html=True), name="ui")

@app.get('/test')
def test():
    dict_f = {'name': 'serg', 'adress': 'moscow', 'house': 7, 'data': '26:09:2025'}
    print('сказать повару: быстрее')
    return dict_f