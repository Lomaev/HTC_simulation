log = []


def print_to_log(*args):
    global log
    try:
        log.append(' '.join(str(i) for i in args))
    except Exception:
        log.append('Incorrect log message.')


def get_log():
    return log

def clear_log():
    log = []