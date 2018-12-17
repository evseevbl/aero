from PyQt5 import QtWidgets as qw
from PyQt5.QtCore import pyqtSlot
from conn import DBWrapper, RegistrationDesk

import sys

# PyQT application class

class Dialog(qw.QDialog):
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

        self.createFormGroupBox()

        buttonBox = qw.QDialogButtonBox((qw.QDialogButtonBox.Ok | qw.QDialogButtonBox.Close))
        buttonBox.rejected.connect(self.reject)
        buttonBox.accepted.connect(self.changeStatus)

        mainLayout = qw.QVBoxLayout()
        self.combo = qw.QComboBox()
        self.combo.addItems(["scheduled", "departed","arrived", "delayed"])
        self.combo.setDisabled(True)
#        self.combo.currentIndexChanged.connect(lambda x: self.changeStatus())
        

        self.setWindowTitle("Airplanes app")
        mainLayout.addWidget(qw.QLabel('Диспетчер'))
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.combo)
        self.status = qw.QLabel()
        mainLayout.addWidget(self.status)
        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)

 
    def updateStatus(self):
        ok, status = self.getStatus(self.flight_line.text())
        print(status)
        self.ok = ok
        if ok:
            self.combo.currentIndex = self.combo.findText(status[0][0])
            self.status.setText('Рейс найден. Измените статус и нажмите Ок.')
            self.combo.setDisabled(False)
        else:
            self.combo.setDisabled(False)
            alert = qw.QMessageBox()
            alert.setText('Рейс не найден!')
            alert.setWindowTitle("Airplanes app")
            alert.exec_()
    
    def changeStatus(self):
        new_status = self.combo.currentText()
        # Here is a query to update the value in a table
        if self.ok:
            self.dbw.query('UPDATE eflight SET status = %s WHERE code = %s', (new_status, self.flight_line.text(),))
            self.status.setText('Статус рейса обновлён.')


    def getStatus(self, code):
        statuses = self.dbw.query('SELECT status FROM eflight WHERE code = %s', (code,))
        ok = True
        if len(statuses) == 0:
            ok = False
        return ok, statuses

    def createFormGroupBox(self):

        self.formGroupBox = qw.QGroupBox("Выберите рейс:")
        layout = qw.QFormLayout()

        self.flight_line = qw.QLineEdit()
        choose_button = qw.QPushButton('Выбрать')
        choose_button.clicked.connect(lambda x: self.updateStatus())

        layout.addRow(self.flight_line, choose_button)

        self.formGroupBox.setLayout(layout)
 
if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    dialog = Dialog()
    dialog.exec_()
