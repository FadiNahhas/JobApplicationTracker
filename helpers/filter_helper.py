import constants as c

def filter_applications(applications, filter_mode):
    if filter_mode == c.FilterMode.ALL:
        return applications
    elif filter_mode == c.FilterMode.ACTIVE:
        return [app for app in applications if app.status in (c.STATUS_PENDING, c.STATUS_ACTIVE)]
    elif filter_mode == c.FilterMode.CLOSED:
        return [app for app in applications if app.status == c.STATUS_CLOSED]
    else:
        raise ValueError(f"Unknown filter mode: {filter_mode}")