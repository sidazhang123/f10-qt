import hmac
from datetime import datetime, timedelta
from hashlib import sha256

import requests


def makeHeader():
    headers = {"accept": "*/*", "accept-encoding": "gzip,deflate,br", "connection": "keep-alive"}
    nonce = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M")
    m = hmac.new(
        bytearray([25 ..., 51]),
        digestmod=sha256
    )
    m.update(nonce.encode(encoding='utf8'))
    headers["..."] = sha256(bytearray(
        [...]) + m.digest()).hexdigest()
    return headers


def fetch(path, args_list):
    for args in args_list:
        tag, raw_body, store_dir = args
        try:
            yield 'starting %s' % tag
            r = requests.post(path, data=raw_body, headers=makeHeader())
            open(store_dir, 'wb').write(r.content)
        except Exception as e:
            yield "Err" + str(e)
            continue

        yield 'done %s' % tag


