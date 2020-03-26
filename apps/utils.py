import hashlib
import time


def upload_name(f):
    fname = f.encode('utf-8')
    suffix = fname.split('.')[-1]
    stamp = int(time.time())
    md5 = hashlib.md5()
    md5.update(fname)
    return '.'.join([str(stamp), md5.hexdigest(), suffix])


def upload_to(path):
    return "uploads/%s/" % path
