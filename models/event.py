class Event:
    def __init__(self, id, application_id, event_type, event_date, note=None):
        self.id = id
        self.application_id = application_id
        self.event_type = event_type
        self.event_date = event_date
        self.note = note
