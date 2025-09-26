from fastapi import FastAPI, APIRouter
app = FastAPI()

@app.get('/test')
def test():
    dict_f = {'name': 'serg', 'adress': 'moscow', 'house': 7, 'data': '26:09:2025'}
    return dict_f