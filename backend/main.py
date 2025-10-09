import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

class Data(BaseModel):#Pydantic model for data validation
    name: str
    
class DataResponse(BaseModel):#Pydantic model for response structure
    data: List[Data]
    
app = FastAPI()#initialize FastAPI app

origins = [
    "http://localhost:5173",
]

app.add_middleware(#block unauthorized access
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_db = {"dataResponse": []}

@app.get("/dataResponse", response_model=DataResponse)
def get_data_response():#endpoint to get data response
    return DataResponse(data=memory_db["dataResponse"])

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}


@app.post("/dataResponse", response_model=Data)
def add_data_response(data: Data):
    memory_db["dataResponse"].append(data)
    return data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)#fastest way to run ASGI server