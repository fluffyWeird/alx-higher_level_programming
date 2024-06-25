class something():
    def hello(self):
        print("Hello")

class something1(something):
    def hello(self):
        print("bye")

class something2(something1):
    pass
if __name__ == __main__:
    a = something1
    a.hello()