def load(path):
    with open(path) as f:
        return set(line.strip() for line in f)

DISPOSABLE = None

def init(path):
    global DISPOSABLE
    DISPOSABLE = load(path)

def check(domain):
    return domain in DISPOSABLE