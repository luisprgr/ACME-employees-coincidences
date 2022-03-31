class Employee:
    def __init__(self, name, schedule):
        self.name = name
        self.schedule = schedule

    def __eq__(self, __o: object) -> bool:
        if self.name == __o.name and self.schedule == __o.schedule:
            return True
        else:
            return False
