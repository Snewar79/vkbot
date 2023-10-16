from fastapi import FastAPI, Request, Response
from vkbot.common.conf import config
import vk
import logging

logging.basicConfig(level = logging.INFO)
logging.info("Call main.py of VkBot")
logging.debug("this will get printed")

app = FastAPI()
vk_api_version = config["vk_api_version"]

def decorator_function(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Some error happend: {e}")

    return wrapper


class VkBot:
    api = None

    @decorator_function
    def __init__(self):
        self.makeAuth()
        self.sendInitMessage()

    @decorator_function
    def makeAuth(self):
        access_token = config["access_token"]
        self.api = vk.API(access_token=access_token)

    @decorator_function
    def sendMessage(self, user_id, message):
        self.api.messages.send(v=vk_api_version, message=message, user_id=user_id, random_id=0)

    @decorator_function
    def sendInitMessage(self):
        admins = config["ADMIN_USERS"]
        for admin in admins:
            self.api.messages.send(v=vk_api_version, message="Привет, бот начал работать!", user_id=admin, random_id=0)

    @decorator_function
    def getUid(self, body):
        user_id = None
        try:
            user_id = body["object"]["user_id"]
            return user_id
        except Exception as e:
            logging.error(f"Error happend in getUid: {e}")
            return None
    
    @decorator_function
    def getName(self, user_id):
        try:
            logging.info(f"get name by uid: {user_id}")
            name = self.api.users.get(user_ids=user_id, v=vk_api_version)[0]["first_name"]
            return name
        except Exception as e:
            logging.error(f"Error happend in getName: {e}")
            return None

    @decorator_function
    def answerToJoin(self, body):
        user_id = self.getUid(body)
        if not user_id:
            return

        name = self.getName(user_id)
        if not name:
            return
        
        message = config["JOINING_A_GROUP_TEXT"].format(name=name)
        self.sendMessage(user_id, message=message)

    @decorator_function
    def answerToOrder(self, body):
        user_id = self.getUid(body)
        if not user_id:
            return

        name = self.getName(user_id)
        if not name:
            return
        
        message = config["PLACING_AN_ORDER_TEXT"].format(name=name)
        self.sendMessage(user_id, message=message)

    @decorator_function
    def isGroupJoinType(self, body: dict):
        if "type" in body and body["type"] == "group_join":
            return True

        return False

    @decorator_function
    def isOrderType(self, body: dict):
        if "type" in body and body["type"] == "market_order_new":
            return True
        
        return False

bot = VkBot()

@app.post("/callback")
async def post_callback(request: Request):
    body = None

    try:
        body = await request.json()
    except Exception as e:
        logging.error(f"Some error happend: {e}")

        return Response(
            content=b'ok',
            media_type="text/plain"
        )
    
    logging.info(body)
    
    if bot.isGroupJoinType(body):
        logging.info("is it group join request, lets send a hello message")
        bot.answerToJoin(body)

    if bot.isOrderType(body):
        logging.info("is it order request, lets send a help message")
        bot.answerToOrder(body)

    return Response(
            content=b'ok',
            media_type="text/plain"
        )