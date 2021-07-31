def safe_div(n, d):
    try:
        r = n / d
    except ZeroDivisionError:
        return 0
    return r
