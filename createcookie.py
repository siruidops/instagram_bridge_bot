from instagram_private_api import Client
import sys
import json
import codecs

username = sys.argv[1]
password = sys.argv[2]

settings_file = "credentials.json"

def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')

def onlogin_callback(api, settings_file):
    cache_settings = api.settings
    with open(settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)
    print("writed to {}".format(settings_file))

api = Client(username, password,
        on_login=lambda x: onlogin_callback(x, settings_file))


