import json
from .util import parse_line


if __name__ == '__main__':
    path = "D:\\los alamos\\auth.txt"
    # path = "auth_short.txt"
    f = open(path)
    limit = 5000
    count = 0
    for line in f:
        if count > limit:
            break
        try:
            values = parse_line(line)
        
            f_write = open(f"D:\\los alamos\\auths\\auth_{values['src_user']}.txt", 'a')
            f_write.write(line)
            f_write.close()
            count += 1
        except:
            continue
