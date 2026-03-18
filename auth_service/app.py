from fastapi import FastAPI, Request, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
import threading
import time
import py_eureka_client.eureka_client as eureka_client

app = FastAPI()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


# 🔹 Eureka Registration
@app.on_event("startup")
async def register_service():

    def register():
        while True:
            try:
                eureka_client.init(
                    eureka_server="http://eureka:8761/eureka/",
                    app_name="auth-service",
                    instance_port=8002,
                    instance_host="auth_service"
                )
                print("✅ Auth Service registered with Eureka")
                break
            except Exception as e:
                print("❌ Eureka not ready (Auth), retrying...", e)
                time.sleep(5)

    threading.Thread(target=register).start()


# 🔐 LOGIN
@app.post("/login")
async def login(request: Request):

    data = await request.json()

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