from sanic import Sanic
from sanic.config import Config
Config.KEEP_ALIVE = False

completed = {}
pending = {}
failed = {}
created = {}
finished = {}


def make_app():
    app = Sanic(__name__)

    @app.route('/v1/images/upload',methods=["POST"])
    async def upload(request):
        from controllers.UrlCrawler import UrlCrawler
        from controllers.Imgur import Imgur

        return await UrlCrawler().fetcher(request,Imgur(),
                                    completed=completed,
                                    pending=pending,
                                    failed=failed,
                                    created=created,
                                    finished=finished
                                    )

    @app.route('/v1/images')
    async def get_uploaded(request):
        from controllers.Status import Status

        return Status.get_status(request,
                                 completed=completed,
                                 pending=pending,
                                 failed=failed,
                                 created=created,
                                 finished=finished
                                 )

    @app.route('/v1/images/upload/<jobId>')
    async def get_uploaded_id(request,jobId):
        from controllers.Status import Status

        return Status.get_status_id(request,jobId,
                                 completed=completed,
                                 pending=pending,
                                 failed=failed,
                                 created=created,
                                 finished=finished
                                 )

    return app


if __name__ == '__main__':
    app = make_app()

    app.run(debug=False, host='0.0.0.0', port='8001')