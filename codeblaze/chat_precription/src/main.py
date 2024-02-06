from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI


class Query(BaseModel):
    text : str
    # lon : str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Allow specific origins (use ["*"] to allow all)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get('/')
def sayHi():
    return {'hello' : 'there'}

# @app.post("/coordinates")
# def get_coordinates(latitude: float, longitude: float):
#     return {"latitude": latitude, "longitude": longitude}

@app.post('/product')
def getResponse(data : Query):
    print(data.text)
    arr = data.text.split(',')
    print(arr)
    return {"message": f"{data.text}"}
