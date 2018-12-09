from sanic import response
class Status:

    def get_status(self,**kwargs):
        import itertools
        return response.json(itertools.chain.from_iterable(kwargs["completed"].values()))


    def get_status_id(self,id,**kwargs):


        if not kwargs["finished"][id]:
            status = "complete"
        elif not kwargs["completed"][id] and not kwargs["failed"][id]:
            status = "pending"
        else:
            status = "in-progress"



        result = {
            "id" : id,
            "created" : kwargs["created"][id],
            "finished" : kwargs["finished"][id],
            "status" : status,
            "uploaded" : {
                "pending" : kwargs["pending"][id],
                "completed" : kwargs["completed"][id],
                "failed" : kwargs["failed"][id]
            }
        }

        return response.json(result)