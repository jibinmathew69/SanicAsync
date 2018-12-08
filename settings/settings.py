import dotenv
from os.path import join,dirname

def imgur_config():
    try:
        dotenv.load(join(dirname(__file__), '.env'))
        imgurconfig = {
            'IMGURURL' : dotenv.get('IMGURURL'),
            'CLIENTID' : dotenv.get('CLIENTID'),
        }
        return imgurconfig
    except:
        return None