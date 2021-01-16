from models import chat, Message
from typing import Optional
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config import TOKEN_URL, SECRET_KEY, ALGORITHM
from fastapi.middleware.cors import CORSMiddleware

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = str(payload.get("sub"))
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


@app.get('/conversation_with/{user}', response_model=List[Message])
async def list_users(user: str, username: str = Depends(get_current_user)):
    """
    :param user: username
    :param username: username of the one calling this with jwt token
    :return: conversation between two users
    """
    messages = []
    for message in chat.find({
        "$or": [
            {
                "$and": [
                    {
                        "receiver": {"$eq": user}
                    },
                    {
                        "sender": {"$eq": username}
                    }
                ]
            },
            {
                "$and": [
                    {
                        "receiver": {"$eq": username}
                    },
                    {
                        "sender": {"$eq": user}
                    }
                ]
            }
        ]
    }):
        messages.append(Message(**message))
    return messages


@app.get('/messages', response_model=List[Message])
async def list_users(username: str = Depends(get_current_user)):
    """
    :param username: username of the one calling this with jwt token
    :return: all messages from user username
    """
    messages = []
    for message in chat.find({
        "$or": [
            {
                "sender": {"$eq": username}
            },
            {
                "receiver": {"$eq": username}

            }
        ]
    }):
        messages.append(Message(**message))
    return messages


@app.post('/message', response_model=Message)
async def create_user(text: str, receiver: str, username: str = Depends(get_current_user)):
    create = {"sender": username, "receiver": receiver, "text": text}
    ret = chat.insert_one(create)
    create["id"] = ret.inserted_id
    return Message(**create)
