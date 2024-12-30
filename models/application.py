class Application:
    def __init__(self, id, company, job_title, application_date, status, location=None, latitude=None, longitude=None):
        self.id = id
        self.company = company
        self.job_title = job_title
        self.application_date = application_date
        self.status = status
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.events = []  # List of associated events

    def add_event(self, event):
        self.events.append(event)
        
    def __repr__(self):
        return (
            f"Application(id={self.id}, company='{self.company}', "
            f"job_title='{self.job_title}', application_date='{self.application_date}', "
            f"status='{self.status}')"
        )