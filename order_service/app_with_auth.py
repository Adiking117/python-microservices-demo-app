from fastapi import FastAPI, Request, HTTPException, Depends
from producer import send_order
from breaker import rabbitmq_breaker
# from auth import create_access_token, verify_token
import asyncio
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# security = HTTPBearer()
app = FastAPI()

# # 🔐 Dummy user
# fake_user = {
#     "username": "aditya",
#     "password": "1234"
# }

# # 🔐 LOGIN
# @app.post("/login")
# async def login(request: Request):
#     data = await request.json()
#     if data["username"] == fake_user["username"] and data["password"] == fake_user["password"]:
#         token = create_access_token({
#             "sub": data["username"]
#         })
#         return {"access_token": token}
#     raise HTTPException(status_code=401, detail="Invalid credentials")


# def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     token = credentials.credentials
#     payload = verify_token(token)
#     if payload is None:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     return payload

import py_eureka_client.eureka_client as eureka_client

@app.on_event("startup")
async def register_service():

    eureka_client.init(
        eureka_server="http://eureka:8761/eureka/",
        app_name="order-service",
        instance_port=8000
    )

@app.post("/create-order")
async def create_order(
    request: Request,
    #user=Depends(get_current_user)  # 🔐 PROTECTED
):
    order = await request.json()

    def sync_send(o):
        asyncio.run(send_order(o))

    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            rabbitmq_breaker.call,
            sync_send,
            order
        )
        return {
            "message": "Order placed",
            #"user": user,
            "order": order
        }
    except Exception as e:
        print("Circuit breaker:", e)
        return {"message": "RabbitMQ unavailable"}