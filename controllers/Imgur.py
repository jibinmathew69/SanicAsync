from sanic import response
from sanic.exceptions import ServerError
from settings.settings import imgur_config
import asyncio

class Imgur:
    def __init__(self):

        try:
            config          = imgur_config()
            self.url        = config["IMGURURL"]
            self.client_id  = config["CLIENTID"]

        except:
            raise ServerError("Internal Server Error",status_code=500)


    async def image_upload(self,file_name,log):
        import aiohttp
        import os.path

        if not os.path.isfile(file_name):
            return None


        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.url,
                data={
                    'image' : open(file_name,'rb')
                },
                headers={
                    'Authorization' : 'Client-ID {}'.format(self.client_id)
                }
            ) as imgur_request:
                imgur_response = await imgur_request.json()
                if imgur_request.status == 200:
                    return imgur_response
                else:
                    asyncio.ensure_future(self.logger(log,imgur_response["data"]["error"]))
                    return None


    async def logger(self,log,exception):
        log.error('%s raised an error', exception)
