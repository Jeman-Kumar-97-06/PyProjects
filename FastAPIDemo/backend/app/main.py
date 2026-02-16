#Import FastAPI from fastapi
from fastapi import FastAPI

#Create a FastAPI instance
app = FastAPI()

#Access '/' to see 'Hello World' as 'message':
@app.get('/')
async def root():
    return {"message":"Hello World"}

#Access '/items/{item_id}' to see a item detail:
@app.get('/items/{item_id}')
async def read_item(item_id):
    return {'item_id':item_id}



