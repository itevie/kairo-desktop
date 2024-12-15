import sys
import signal
from PySide6 import QtGui, QtWidgets

from client import Client
from task_list import TaskListWidget

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)

        self.layout.addWidget(QtWidgets.QLabel(text="Your Tasks"))

        self.layout.addWidget(TaskListWidget())

    def closeEvent(self, event):
        self.hide()
        event.ignore()

if __name__ == "__main__":
    # Setup app
    app = QtWidgets.QApplication([])

    # Check if tray is allowed
    if not QtWidgets.QSystemTrayIcon.isSystemTrayAvailable():
        print("System tray is not available on this system.")
        sys.exit(1)
    
    # Setup tray
    tray_icon = QtWidgets.QSystemTrayIcon()
    tray_icon.setIcon(QtGui.QIcon("./logo512.png"))
    tray_icon.activated.connect(lambda: widget.show())

    # Create tray context menu
    tray_menu = QtWidgets.QMenu()

    # Add actions to the context menu
    label = QtGui.QAction("Kairo Desktop")
    label.setEnabled(False)
    tray_menu.addAction(label)

    show_action = QtGui.QAction("Show")
    show_action.triggered.connect(lambda: widget.show())
    tray_menu.addAction(show_action)

    quit_action = QtGui.QAction("Quit")
    quit_action.triggered.connect(lambda: sys.exit(0))
    tray_menu.addAction(quit_action)

    # Finish tray icon setup
    tray_icon.setContextMenu(tray_menu)
    tray_icon.show()

    # Allow CTRL + C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    # Create main widget
    widget = MyWidget()
    widget.resize(800, 600)
    # widget.show()

    sys.exit(app.exec())
