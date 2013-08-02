from hashlib import md5
from time import localtime
import os

def add_suffix(filename):
  filenames=os.path.splitext(filename)
  return "%s_%s%s" % (filenames[0],md5(str(localtime())).hexdigest(),filenames[1])
