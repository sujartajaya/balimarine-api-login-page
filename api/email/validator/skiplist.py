SKIPLIST = None
def init(path):
    global SKIPLIST
    with open(path) as f:
        SKIPLIST = set(line.strip() for line in f)

def check(domain):
    return domain in SKIPLIST