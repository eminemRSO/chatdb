from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from config import DB_PASSWORD, DB_USER, DB_AUTH_SOURCE, AUTH_MECHANISM, DB_URL

client = MongoClient("mongodb+srv://" + DB_USER + ":"+DB_PASSWORD+"@"+DB_URL+"/chat?retryWrites=true&w=majority")

#client = MongoClient(DB_URL,
#                      username=DB_USER,
#                      password=DB_PASSWORD,
#                      authSource=DB_AUTH_SOURCE,
#                      authMechanism=AUTH_MECHANISM)

db = client["chat"]
#db.authenticate('admin', 'admin')
chat = db["messages"]


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Message(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    sender: str
    receiver: str
    text: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
