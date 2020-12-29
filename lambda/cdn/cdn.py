import base64
from OpenSSL.crypto import sign, load_privatekey, FILETYPE_PEM
import time
from urllib import parse

def get_cloudfront_signed_url(key_pair_id, key_data, resource, timeout):
    """
    Sign a CloudFront url
    @param key_pair_id: id of the key pair from AWS
    @param key_data: content of the .pem private key file from AWS
    @param resource: url of resource on CloudFront
    @param timeout: duration of the signed url in seconds
    @return: signed url
    """
    expires = int(time.time()) + timeout
    json = '{"Statement":[{"Resource":"%s","Condition":{"DateLessThan":' \
           '{"AWS:EpochTime":%d}}}]}' % (resource, expires)
    key = load_privatekey(FILETYPE_PEM, key_data)
    signature = base64.b64encode(sign(key, str.encode(json), 'sha1'))
    return '%s?Expires=%d&Signature=%s&Key-Pair-Id=%s' \
           % (resource, expires, bytes.decode(signature), key_pair_id)


key_pair_id = ''

key_data = open('key_file.pem').read()

object_name = parse.quote('')

resource = 'cdn_url' + object_name

timeout = 600

cdn_url = get_cloudfront_signed_url(key_pair_id, key_data, resource, timeout)