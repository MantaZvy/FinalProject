import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import get_db
from models import DataModel
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

@app.get("/dataResponse", response_model=DataResponse)
async def get_data_response(db: AsyncSession = Depends(get_db)):#endpoint to get data response
    result = await db.execute(select(DataModel)) #query all data from DataModel table
    items = result.scalars().all()
    return DataResponse(data=[Data(name=item.name)for item in items]) 

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}


@app.post("/dataResponse", response_model=Data)
async def add_data_response(data: Data, db: AsyncSession = Depends(get_db)):
    item = DataModel(name=data.name)
    db.add(item)
    await db.commit() #save
    await db.refresh(item) #return
    return Data(name=item.name)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)#fastest way to run ASGI server