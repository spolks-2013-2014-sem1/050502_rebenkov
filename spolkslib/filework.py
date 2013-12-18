import os
import time


def get_fsize(f):
    try:
        old_file_position = f.tell()
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(old_file_position, os.SEEK_SET)
    except Exception as e:
        print ("exception occured %s" % e)
    else:
        return size


def random_name():
    return 'F' + str(int(time.time() * 10))[4:]
