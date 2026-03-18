from fastapi import FastAPI, Request, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


# 🔐 LOGIN
@app.post("/login")
async def login(request: Request):

    data = await request.json()

    # dummy user
    if data["username"] == "aditya" and data["password"] == "1234":

        payload = {
            "sub": data["username"],
            "exp": datetime.utcnow() + timedelta(minutes=60)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {"access_token": token}

    raise HTTPException(status_code=401, detail="Invalid credentials")


# 🔐 VALIDATE TOKEN
@app.get("/validate")
async def validate(request: Request):

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"user": payload["sub"]}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")