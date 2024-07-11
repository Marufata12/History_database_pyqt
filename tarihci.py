import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class HistoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Historian - Historical Events Database")
        self.setGeometry(100, 100, 500, 400)

        self.initUI()
        self.events = {}

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.setStyleSheet("background-color: #f5f5dc; font-family: Arial;")

        self.label_title = QLabel("Historian - Historical Events Database")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setFont(QFont("Arial", 16, QFont.Bold))
        self.layout.addWidget(self.label_title)

        self.label_event_name = QLabel("Event Name:")
        self.edit_event_name = QLineEdit()
        self.layout.addWidget(self.label_event_name)
        self.layout.addWidget(self.edit_event_name)

        self.label_event_date = QLabel("Event Date:")
        self.edit_event_date = QLineEdit()
        self.layout.addWidget(self.label_event_date)
        self.layout.addWidget(self.edit_event_date)

        self.label_event_description = QLabel("Event Description:")
        self.edit_event_description = QLineEdit()
        self.layout.addWidget(self.label_event_description)
        self.layout.addWidget(self.edit_event_description)

        self.btn_add_event = QPushButton("Add Event")
        self.btn_add_event.setStyleSheet("background-color: #8b4513; color: white; border-radius: 5px;")
        self.btn_add_event.clicked.connect(self.addEvent)
        self.layout.addWidget(self.btn_add_event)

        self.label_events = QLabel("Added Events")
        self.label_events.setFont(QFont("Arial", 12, QFont.Bold))
        self.layout.addWidget(self.label_events)

        self.list_events = QListWidget()
        self.list_events.setStyleSheet("background-color: #d2b48c; border-radius: 5px;")
        self.layout.addWidget(self.list_events)

        self.label_query_event = QLabel("Query Event:")
        self.layout.addWidget(self.label_query_event)

        self.edit_query_event = QLineEdit()
        self.layout.addWidget(self.edit_query_event)

        self.btn_query_event = QPushButton("Query Event")
        self.btn_query_event.setStyleSheet("background-color: #8b4513; color: white; border-radius: 5px;")
        self.btn_query_event.clicked.connect(self.queryEvent)
        self.layout.addWidget(self.btn_query_event)

        self.label_query_date = QLabel("Query Date:")
        self.layout.addWidget(self.label_query_date)

        self.edit_query_date = QLineEdit()
        self.layout.addWidget(self.edit_query_date)

        self.btn_query_date = QPushButton("Query Date")
        self.btn_query_date.setStyleSheet("background-color: #8b4513; color: white; border-radius: 5px;")
        self.btn_query_date.clicked.connect(self.queryDate)
        self.layout.addWidget(self.btn_query_date)

    def addEvent(self):
        event_name = self.edit_event_name.text()
        event_date = self.edit_event_date.text()
        event_description = self.edit_event_description.text()

        if event_name in self.events:
            QMessageBox.warning(self, "Warning", "This event is already added.")
            return

        person_name, ok = QInputDialog.getText(self, "Add Person", "Enter the name of the person associated with the event:")
        if not ok:
            return

        if event_name not in self.events:
            self.events[event_name] = {"Date": event_date, "Description": event_description, "People": []}
            self.list_events.addItem(f"Event: {event_name} - {event_date} - {event_description}")

        self.events[event_name]["People"].append(person_name)

        self.list_events.clear()
        for event, info in self.events.items():
            self.list_events.addItem(f"Event: {event} - {info['Date']} - {info['Description']}")
            for person in info["People"]:
                self.list_events.addItem(f"    Person: {person}")

    def queryEvent(self):
        event_name = self.edit_query_event.text()
        if event_name in self.events:
            info = self.events[event_name]
            people = ", ".join(info["People"])
            QMessageBox.information(self, "Event Information", f"Event Date: {info['Date']}\nEvent Description: {info['Description']}\nPeople: {people}")
        else:
            QMessageBox.warning(self, "Warning", "This event is not found in the database.")

    def queryDate(self):
        date = self.edit_query_date.text()
        found_events = []
        for event, info in self.events.items():
            if info["Date"] == date:
                found_events.append((event, info))

        if found_events:
            message = ""
            for event, info in found_events:
                people = ", ".join(info["People"])
                message += f"Event Name: {event}\nDate: {info['Date']}\nDescription: {info['Description']}\nPeople: {people}\n\n"
            QMessageBox.information(self, "Date Information", message)
        else:
            QMessageBox.warning(self, "Warning", "No events found on the specified date.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HistoryApp()
    window.show()
    sys.exit(app.exec_())

