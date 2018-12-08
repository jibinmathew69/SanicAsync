from sanic import response
from sanic.exceptions import ServerError
from settings.settings import url_config
from contextlib import closing
from urllib.parse import urlsplit,unquote
import posixpath
import os
import requests
import aiohttp
import asyncio


class UrlCrawler:
    def __init__(self):
        try:
            config = url_config()
            self.upload_folder = config["upload_folder"]
            self.max_connect = config["max_connect"]
            self.allowed_formats = config["allowed_formats"]
            self.max_size = config["max_size"]
            self.chunk_size = config["chunk_size"]
        except:
            raise ServerError("Internal Server Error",status_code=500)


    async def is_valid_url(self,url):

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


    async def fetch_urls(self,urls,id,imgur):
        loop = asyncio.get_event_loop()
        semaphore = asyncio.BoundedSemaphore(self.max_connect)
        async with aiohttp.ClientSession(loop=loop) as session:
            await asyncio.wait([
                self.get_image(url,session,semaphore,id,imgur) for url in urls
            ])



    async def create_response(self,id):
        return response.json({
            "jobId" : id
        },status=200)



    async def get_image(self,url,session,semaphore,id,imgur,**kwargs):
        with(await semaphore):
            file_name = self.create_filename(url)
            image_header = await self.is_valid_url(url)

            if not image_header:
                kwargs["failed"][id].append(url) #todo log

            file_name = os.path.join(self.upload_folder,file_name)
            image_data = await session.get(url)

            with closing(image_data), open(file_name, 'wb') as file:
                while True:
                    chunk = await image_data.content.read(self.chunk_size)
                    if not chunk:
                        break
                    file.write(chunk)

                imgur_result = await imgur.image_upload(file_name)
                if imgur_result == None:
                    kwargs["failed"][id].append(url)  # todo log
                    kwargs["pending"].remove(url)
                else:
                    kwargs["completed"]["id"].append(imgur_result["data"]["link"])
                    kwargs["pending"].remove(url)

                os.remove(file_name)

        return url


    def create_filename(self,url):

        urlpath = urlsplit(url).path
        basename = posixpath.basename(unquote(urlpath))
        if (os.path.basename(basename) != basename or
                    unquote(posixpath.basename(urlpath)) != basename):
            return None

        return basename
