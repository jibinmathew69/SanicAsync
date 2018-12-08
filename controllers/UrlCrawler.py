from sanic import response
from sanic.exceptions import ServerError
from settings.settings import url_config

class UrlCrawler:
    def __init__(self):
        try:
            config = url_config()
            self.upload_folder = config["upload_folder"]
            self.max_connect = config["max_connect"]
            self.allowed_formats = config["allowed_formats"]
            self.max_size = config["max_size"]
        except:
            raise ServerError("Internal Server Error",status_code=500)


    async def is_valid_url(self,url):
        import requests

        valid_request = requests.head(url)
        if valid_request.headers["content-type"] not in self.allowed_formats or valid_request.headers["content-length"] > 20480:
            return False

        return True
