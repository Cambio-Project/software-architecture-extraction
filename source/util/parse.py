def bool_from_string(arg: str):
    arg = arg.lower()
    return True if bool(arg) and not arg.startswith('f') else False
