class Event:
    __slots__ = ("event_id", "amount")
    def __init__(self, event_id, amount):
        self.event_id, self.amount = event_id, amount
event = Event(1, 100)
assert event.amount == 100 and not hasattr(event, "__dict__")
