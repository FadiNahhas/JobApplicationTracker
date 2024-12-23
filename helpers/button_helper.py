import constants as c
from PyQt6 import QtCore

def update_buttons(main_window, app=None, has_events=False):
    is_selected = app is not None
    main_window.editButton.setEnabled(is_selected)
    main_window.deleteApplicationButton.setEnabled(is_selected)
    main_window.newEventButton.setEnabled(is_selected and app and app.status != c.STATUS_CLOSED)
    
    selected_event = main_window.eventsTable.currentRow()
    is_event_selected = selected_event >= 0

    if is_event_selected:
        note_item = main_window.eventsTable.item(selected_event, 0)
        event_note = note_item.data(QtCore.Qt.ItemDataRole.UserRole + 1)
        main_window.viewNoteButton.setEnabled(bool(event_note))
    else:
        main_window.viewNoteButton.setEnabled(False)

    main_window.deleteEventButton.setEnabled(has_events and is_event_selected)