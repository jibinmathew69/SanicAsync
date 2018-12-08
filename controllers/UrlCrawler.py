from sanic import response
from sanic.exceptions import ServerError
from settings.settings import url_config

class UrlCrawler:
    def __init__(self):
        try:
            config = url_config()
            self.upload_folder = config["upload_folder"]
            self.max_connect = config["max_connect"]
        except:
            raise ServerError("Internal Server Error",status_code=500)


