import md5

def genmd5(s):
    m = md5.new()
    m.update(s)
    return m.hexdigest()