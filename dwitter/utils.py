
def length_of_code(code):
    """
    Centralize the character counting to one place
    """
    return len(code.replace('\r\n', '\n'))
