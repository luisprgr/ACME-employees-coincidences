class Hour:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __eq__(self, __o: object) -> bool:
        if self.start == __o.start and self.end == __o.end:
            return True
        else:
            return False
