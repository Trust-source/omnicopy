from fastapi import FastAPI, HTTPException, Request, Response
from datetime import datetime
from random import randint
from sqlmodel import create_engine

app = FastAPI(root_path = "/api/v1")

data = [
    {"campaign_id": 1,
     "name": "Summer Launch",
     "due_date": datetime.now(),
     "created_at": datetime.now()
     },
    {"campaign_id": 2,
     "name": "Black Friday",
     "due_date": datetime.now(),
     "created_at": datetime.now()
     },

    
]

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args = connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.get("/")
async def root():
    return {"message": "Hello world!"}

@app.get("/campaigns")
async def read_campaigns():
    return {"campaigns": data}

@app.get("/campaign/{id}")
async def read_campaign(id: int):
    for campaign in data:
        if campaign.get("campaign_id") == id:
            return campaign
    raise HTTPException(status_code = 404)

@app.post("/campaigns", status_code = 201)
async def create_campaign(body: dict):
    if not body.get("name"):
        raise HTTPException(status_code = 403, detail = "Forbidden: Name is required..")
    new = {
        "campaign_id": randint(100, 1000),
        "name": body.get("name"),
        "due_date": body.get("due_date"),
        "created_at": datetime.now()
    }

    data.append(new)
    return {"campaign": new}


@app.put("/campaigns")
async def update_campaign(id: int, body: dict):
    for index, campaign in enumerate(data):
        if campaign.get("campaign_id") == id:
            updated = {
                "campaign_id": id,
                "name": body.get("name"),
                "due_date": body.get("due_date"),
                "created_at": campaign.get("created_at")
            }

            data[index] = updated
            return {"campaign": updated}
    raise HTTPException(status_code = 404)


@app.delete("/campaigns/id")
def delete_campaign(id: int):
    for index, campaign in enumerate(data):
        if campaign.get("campaign_id") == id:
            data.pop(index)
            return Response(status_code = 204)
    raise HTTPException(status_code = 404)