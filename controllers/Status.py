from sanic import response
class Status:

    def get_status(self,**kwargs):
        import itertools
        return response.json(itertools.chain.from_iterable(kwargs["completed"].values()))

