from os.path import normpath, join


def path(first: str, *other):
    return normpath(join(first, *other))
