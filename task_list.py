import requests # type: ignore
import json
from typing import TypedDict
from PySide6 import QtCore, QtWidgets, QtGui
from plyer import notification

from client import CLIENT

class TaskListWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)

        self.tasks = CLIENT.fetch_tasks()
        overdue = CLIENT.get_overdue()

        if overdue != 0:
            notification.notify(title="Kairo: Overdue Tasks!", message=f"You have {len(overdue)} tasks which need to be completed!")

        self.magic()

    @QtCore.Slot()
    def magic(self):
        # Create a QScrollArea
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # Container for the scroll area
        container = QtWidgets.QWidget()
        container_layout = QtWidgets.QVBoxLayout(container)
        container_layout.addLayout(self.layout)  # Add the layout to the container

        for task in self.tasks:
            container_layout.addWidget(QtWidgets.QLabel(task['title']))
        
        scroll_area.setWidget(container)  # Set the container as the widget for scroll area

        # Add the scroll area to the main layout
        self.layout.addWidget(scroll_area)
