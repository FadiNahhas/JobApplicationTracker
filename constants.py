from enum import Enum

STATUS_PENDING = "Pending"
STATUS_ACTIVE = "Active"
STATUS_CLOSED = "Closed"

TABLE_COLUMN_COMPANY = 0
TABLE_COLUMN_JOB_TITLE = 1
TABLE_COLUMN_DATE_APPLIED = 2
TABLE_COLUMN_STATUS = 3

class FilterMode(Enum):
    ALL = "all"
    ACTIVE = "active"
    CLOSED = "closed"