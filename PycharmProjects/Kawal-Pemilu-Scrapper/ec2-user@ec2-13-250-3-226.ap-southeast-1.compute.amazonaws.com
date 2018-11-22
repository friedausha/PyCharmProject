import requests
import boto
from urllib3.exceptions import ProtocolError
for i in range(10):
    requested_pic = requests.get("http://scanc1.kpu.go.id/viewp.php?f=000000400104.jpg", stream = True)
    if requested_pic.status_code == 200:
        print('got the image')
        try:
            connection = boto.connect_s3('AKIAIQ2PJXOKYG3NNPYQ', 'UtfaTqkf6Ub4bNlaZN5HCCBrX9bxDbbImZhg9eLn')
            bucket = connection.get_bucket('kawal-pemilu-frieda', validate=False)
            key = bucket.new_key("{filename}".format(filename=i))
            key.set_contents_from_string(requested_pic.content, replace=True,
                                       policy='authenticated-read',
                                       reduced_redundancy=True)
            key.generate_url(expires_in=0, force_http=True)
        except ProtocolError:
            print('error protocol')
