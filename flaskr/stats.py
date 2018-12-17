import PyQt5.QtWidgets as qw
from PyQt5.QtCore import pyqtSlot
from conn import DBWrapper, RegistrationDesk

import sys


# Using RegistrationDesk
class Field():
    def __init__(self, num, name, dbw, ted, needField, query=''):
        self.num = num
        self.name = name
        self.ted = ted
        self.textline = qw.QLineEdit()
        self.textline.setDisabled(not needField)
        self.button = qw.QPushButton(name)
        self.button.clicked.connect(lambda x: self.on_click())
        self.dbw = dbw
        self.query = query

    def on_click(self):
        print("Looking " + self.name + "=" + self.textline.text())
        ret = self.dbw.query(self.query, (self.textline.text(),))
        s = ''
        if not ret is None:
            if len(ret) > 0:
                for elem in ret:
                    s += ' '.join(list(map(str, elem)))
                    s += '\n'

        self.textline.setText("")
        self.ted.setText(s)


# PyQT application class

class Dialog(qw.QDialog):
    NumGridRows = 3
    NumButtons = 3

    def __init__(self):
        super(Dialog, self).__init__()
        self.dbw = DBWrapper(
            host='40.85.80.197',
            dbname='aero',
            user='aero',
            password='domodedovo',
            port='5432')

        # You need to properly connect the database
        self.dbw.connect()
        self.reg = RegistrationDesk(1, self.dbw)
        self.ted = qw.QTextEdit()

        self.createFormGroupBox()

        buttonBox = qw.QDialogButtonBox(qw.QDialogButtonBox.Close)
        buttonBox.rejected.connect(self.reject)

        mainLayout = qw.QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        mainLayout.addWidget(self.ted)
        self.ted.setText("Query results will be displayed here")
        self.setLayout(mainLayout)

        self.setWindowTitle("Statistics")

    def createFormGroupBox(self):
        self.formGroupBox = qw.QGroupBox("queries:")
        layout = qw.QFormLayout()
        # Creating rows
        field_names = ['Passenger by passport', 'Passengers by flight', 'Count arrivals',
                       'All flights', 'Connected cities', 'Flights by status', 'Companies and flights']

        queries = [
            "SELECT name, surname, birthdate FROM dpassengers WHERE passport_id = %s",

            "SELECT DISTINCT dp.name, dp.surname FROM dpassengers dp \
            JOIN epassenger ep ON ep.passport_id = dp.passport_id WHERE ep.flight = %s",

            "SELECT ea.name, COUNT(fa.code) \
            FROM daeroports ea\
            LEFT JOIN eflight fa\
            ON ea.code = fa.loc_to\
            LEFT JOIN eflight fd\
            ON ea.code = fd.loc_from\
            GROUP BY ea.name",

            "SELECT c.name, f.code, d.city AS departure, a.city AS arrival\
            FROM rcompany2flight r2f\
            RIGHT JOIN eflight f\
            ON r2f.flight_code = f.code\
            JOIN dcompnames c\
            ON r2f.comp_code = c.iata_code\
            JOIN daeroports d\
            ON d.code = f.loc_from\
            JOIN daeroports a\
            ON a.code = f.loc_to",

            "SELECT DISTINCT r.city\
            FROM eflight f\
            JOIN daeroports a\
            ON a.code = f.loc_from\
            JOIN daeroports r\
            ON r.code = f.loc_to\
            WHERE a.city = %s",

            "SELECT dc.name, f.code from eflight f\
            join daeroports d on f.loc_from = d.code\
            join rcompany2flight c on c.flight_code = f.code\
            join dcompnames dc on dc.iata_code = c.comp_code\
            where status = %s",

            "SELECT c.name, COUNT(f.code) AS flights FROM rcompany2flight r2f \
            JOIN eflight f ON r2f.flight_code = f.code \
            RIGHT JOIN dcompnames c ON c.iata_code = r2f.comp_code \
            GROUP BY c.name",
        ]
        needField = [1, 1, 0, 0, 1, 1, 0]
        rows = [Field(i, field_names[i], self.dbw, self.ted, needField[i], queries[i]) for i in range(7)]

        for field in rows:
            layout.addRow(field.textline, field.button)

        self.formGroupBox.setLayout(layout)


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    dialog = Dialog()
    dialog.exec_()
