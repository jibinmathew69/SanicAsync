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


def url_config():
    try:
        dotenv.load(join(dirname(__file__), '.env'))
        urlconfig = {
            'upload_folder' : dotenv.get('TEMPUPLOAD'),
            'max_connect' : dotenv.get('MAXCONNECT'),
        }
        return urlconfig
    except:
        return None
