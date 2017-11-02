

def funcname(start, end):
    for char in end["characters"]:
        return 0

def diffPoints(start, end):
    if start is None or end is None:
        return 0

    diff = 0
    if type(end) is dict:
        for key in end:
            diff += diffPoints(start[key], end[key])
        return diff

    if type(end) is list:
        for item in end:
            if not item in start:
                print(item)
                diff += 1
        return diff

    if start != end:
        print(end)
        return 1
    return 0

