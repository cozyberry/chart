from hashlib import md5
from time import localtime

def add_prefix(filename):
  return "%s_%s" % (md5(str(localtime())).hexdigest(), filename)
