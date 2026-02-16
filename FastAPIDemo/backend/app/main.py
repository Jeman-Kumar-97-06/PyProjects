from enum import Enum
#Import FastAPI from fastapi
from fastapi import FastAPI
from pydantic import BaseModel

#----------------------------------------------------------
class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet  = 'resnet'
    lenet   = 'lenet'

fake_items_db = [{"item_name":"Foo"},{"item_name":"Bar"},{"item_name":"Baz"}]


class Item(BaseModel):
    name:str
    description:str | None = None #Optional
    price:float
    tax:float | None = None       #Optional

#------------------------------------------------------------

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

#Only 'int' allowed as path parameter:
@app.get('/items_int/{item_id}')
async def read_item(item_id:int):
    return {'item_id':item_id}

#Order of routes: Order matters :
@app.get('/users/me')
async def read_user_me():
    return {'user_id':"Current User Yo"}

@app.get('/users/{user_id}')
async def read_user(user_id:str):
    return {'User_id': user_id}

#The following makes sure the 'model_name' passed is a part of ModelName:
@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {'model_name':model_name,'message':'Deep Learning FTW!'}
    
    if model_name.value == 'lenet':
        return {'model_name':model_name, 'message': 'LeCNN all the images!'}
    
    return {'model_name':model_name, 'message':"Have some residuals"}

#If you want the path parameter to be a path:
@app.get('/files/{file_path:path}')
async def read_file(file_path:str):
    return {"file_path":file_path}

#Query Parameters: When you include parameters in route function that are not a part of path parameters, they are automatically interpreted
#... as query parameters.
@app.get('/items/') #In this line, there's no path parameters. So the parameters in the below function are treated as query params.
async def read_item(skip:int=0,limit:int=0):
    return fake_items_db[skip : skip+limit]
#the above shit is dealt as : http://127.0.0.1:8000/items/?skip=0&limit=10

@app.get('/items/{item_id}')
async def read_item(item_id:str, q:str | None = None):
    if q:
        return {"item_id":item_id,"q":q}
    return {"item_id":item_id}

#multiple path and query parameters:
@app.get('/users/{user_id}/items/{item_id}')
async def read_user_item(user_id:int, item_id:str, q:str | None = None, short:bool = False):
    item = {"item_id":item_id,"owner_id":user_id}
    if q:
        item.update({'q':q})
    if not short:
        item.update(
            {"description":"This is an amazing item that has a long description"}
        )
    return item

#Required Query Params : 
@app.get('/items/{item_id}')
async def read_user_item(item_id:str, needy:str):#here 'needy' is a required query parameter: It you don't include 'needy' you will see error.
    item = {"item_id":item_id, "needy":needy}
    return item

#REQUEST BODY: DATA SENT BY CLIENT TO AN API:
#Defining a Request body : ie., rules about what the fuck API accepts from a client:
#Reads the 'item' as JSON.
@app.post('/items/')
async def create_item(item:Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax':price_with_tax})
    return item_dict

#-----------------------------------------------------------
@app.post('/items/{item_id}')
async def update_item(item_id:int, item:Item):
    return {"item_id":item_id,**item.model_dump()}




#RESPONSE BODY: DATA SENT BY AN API BACK TO A CLIENT: