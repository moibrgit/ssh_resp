""" 
>pip install uvicorn
>pip install fastapi
>pip install python-multipart 


> uvicorn 01_post:app --reload

> http://127.0.0.1:8000/docs
> http://127.0.0.1:8000/redoc
>


@app.post()
@app.put()
@app.delete()
@app.options()
@app.head()
@app.patch()
@app.trace()

GET: Retrieves data from the server. Should have no other effect.
PUT: Replaces target resource with the request payload. Can be used to update or create a new resource.
PATCH: Similar to PUT, but used to update only certain fields within an existing resource.
POST: Performs resource-specific processing on the payload. Can be used for different actions including creating a new resource, uploading a file, or submitting a web form.
DELETE: Removes data from the server.
TRACE: Provides a way to test what the server receives. It simply returns what was sent.
OPTIONS: Allows a client to get information about the request methods supported by a service. The relevant response header is Allow with supported methods. Also used in CORS as preflight request to inform the server about actual the request method and ask about custom headers.
HEAD: Returns only the response headers.

"""


from pydoc import describe
from fastapi import Request

from fastapi import FastAPI, Request

from pydantic import BaseModel
from typing import Optional


    
    


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}



# http://127.0.0.1:8000/items/1  --> good
# http://127.0.0.1:8000/items/a  --> error
@app.get("/items/{item_id}")
async def read_item(item_id: int): 
    return {"item_id": item_id}


#########################################################################
# THE URL is:  http://localhost:8000/getUserInfo?id=1&name=thomas  ---> good
# THE URL is:  http://localhost:8000/getUserInfo?id=a&name=thomas  ---> error because id should be integer
# THE URL is:  http://127.0.0.1:8000/getUserInfo?id=1&name=100  ---> good, because 100 can be also string interprated


@app.get("/getUserInfo")
def getUserInfo(id: int, name: str):
      return [{
          "id" : id,
          "firstName" : name
      }]

# The return is: [{"id":100,"firstName":"tom"}]
   
      

###########################################################################
# Posting data to the server

"""  Try to post to the URL a json file
{
	"id" : 100,
	"name" : "Jay",
    "city" : "Kochi"
}
"""
@app.post("/getInformation")
async def getInformation(info : Request):
    
    req_info = await info.json() # dictionary
    print(type(req_info))  # dictionary
    
    return {
        "status" : "SUCCESS",
        "author" : "Mohamed",
        "data" : req_info
    }


######################################################################
# Posting data to the server # Usiing pydantic
""" 
{
	"id" : 100,
	"name" : "Jay"
}
""" # ---> good

""" 
{
	"id" : 100
}
"""  # ---> error : missing value


# Use pydantic
class Info(BaseModel):
    id : int
    name : str
    
    
@app.post("/getInformation2")
def getInformation(info : Info):
    
    return {
        "status" : "SUCCESS",
        "author" : "M.Ibrahim",
        "data" : info
    }


##########################################################


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


""" 
{
	"name" : 100,
	"description" : "abcd",
	"price": 100,
	"tax": 4
}
"""
@app.post("/items1")
async def create_item1(item: Item):
    return item




""" 
{
	"name" : 105,
	"description" : "abcdefgh",
	"price": 100,
	"tax": 4
}
"""
@app.post("/items2")
async def create_item2(item: Item):
    new_item = Item(name = item.name, 
                    description = item.description, 
                    price = item.price, 
                    tax=item.tax)
    
    return new_item


""" 
{
	"name" : 210,
	"description" : "abcdefgh",
	"price": 200,
	"tax": 6
}
"""
@app.post("/items3")
async def create_item3(item: Item):
    item_dict = item.dict()
    
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
        
    return item_dict

############################################

# Put --> the param will be in the url
# Post --> the data will be sent as a part of the header (like JSON)

list_of_usernames = []

@app.put("/putdata/{username}")
async def put_data(username:str):
   print(username)
   list_of_usernames.append(username)
   return {
       "data": username,
       "list_of": list_of_usernames
   }
   
        
@app.post("/postdata")
async def post_data(username:str):
   print(username)
   list_of_usernames.append(username)
   return {
       "data": username,
       "list_of": list_of_usernames
   }

@app.delete("/deletedata")
async def post_data(username:str):
   print(username)
   list_of_usernames.remove(username)
   return {
       "data": username,
       "list_of": list_of_usernames
   }
   
   
@app.api_route("/homedata", methods=["GET", "POST", "PUT", "DELETE"])
async def hand_data(username:str):
   print(username)   
   return {
       "data": username,
       "list_of": list_of_usernames
   }
   