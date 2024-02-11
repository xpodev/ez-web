import ez

@ez.get("/test")
def test():
    return "This is a test plugin"