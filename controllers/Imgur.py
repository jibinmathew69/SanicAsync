from sanic import response
from sanic.exceptions import ServerError
from settings.settings import imgur_config

class Imgur:
    def __init__(self):

        try:
            config          = imgur_config()
            self.url        = config["IMGURURL"]
            self.client_id  = config["CLIENTID"]

        except:
            raise ServerError("Internal Server Error",status_code=500)
