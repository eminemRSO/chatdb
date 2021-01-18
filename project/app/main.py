from models import chat, Message
from typing import Optional
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config import TOKEN_URL, SECRET_KEY, ALGORITHM
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
import data

FAIL = False

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8083",
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


@app.get('/conversation_with/{user}', response_model=List[dict])
async def list_messages_with_user(user: str, username: str = Depends(get_current_user)):
    """
    :param user: username
    :param username: username of the one calling this with jwt token
    :return: conversation between two users
    """
    return data.find_conversation(chat, name_a=user, name_b=username)


@app.get('/messages', response_model=List[dict])
async def list_messages(username: str = Depends(get_current_user)):
    """
    :param username: username of the one calling this with jwt token
    :return: all messages from user username
    """
    return data.user_messages(chat, name=username)


@app.post('/message', response_model=dict)
async def create_message(text: str, receiver: str, username: str = Depends(get_current_user)):
    create = {"sender": username, "receiver": receiver, "text": text}
    ret = data.create_message(chat, create)
    return ret


@app.get("/v1/health/live_check", response_model=str)
async def live_check():
    return "OK"


@app.get("/v1/health/test_crash", response_model=str)
async def set_to_fail():
    global FAIL
    FAIL = True
    return "OK"


@app.get("/v1/health/db_ready", response_model=dict)
async def test_db():
    global FAIL
    if FAIL:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Intentional fail",
        )
    sender = str(uuid4())
    receiver = str(uuid4())
    text = str(uuid4())
    create = data.create_message(chat, {"sender": sender, "receiver": receiver, "text": text})
    messages = data.get_messages(chat, sender=sender, receiver=receiver, text=text)

    print(len(messages))
    if len(messages) != 1:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to retrieve message",
        )
    messages = data.delete_messages(chat, sender=sender, receiver=receiver, text=text)
    messages = data.get_messages(chat, sender=sender, receiver=receiver, text=text)

    print(len(messages))
    if len(messages) != 0:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to delete message",
        )
    return {"database_check": "ok"}

