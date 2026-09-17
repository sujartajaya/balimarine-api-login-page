FREE = None

def init(path):
    global FREE
    with open(path) as f:
        FREE = set(line.strip() for line in f)

def check(domain):
    return domain in FREE