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


    async def fetcher(self,request,**kwargs):
        if 'urls' not in request.json:
            raise ServerError("Insufficient parameters",status_code=400)

        urls = request.json["urls"]

        from uuid import uuid4
        id = str(uuid4())

        kwargs["pending"][id] = urls[:]

        return await self.create_response(id)


    async def create_response(self,id):
        return response.json({
            "jobId" : id
        },status=200)