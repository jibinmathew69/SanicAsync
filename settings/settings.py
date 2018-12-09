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
            'upload_folder'     : dotenv.get('TEMPUPLOAD'),
            'max_connect'       : dotenv.get('MAXCONNECT'),
            'allowed_formats'   : ("image/png", "image/jpeg", "image/jpg","image/gif","image/apng","image/tiff"),
            'max_size'          : 2e+7,
            'chunk_size'        : 1<<15,
            'log_folder'        : dotenv.get('LOGFOLDER'),
            'log_file'          : dotenv.get('LOGFILE')
        }
        return urlconfig
    except:
        return None
