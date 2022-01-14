"""
Emirhan Yılmaz
10.09.2020
"""
import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRegExp

import sqlite3
from PIL import Image
from PyQt5.QtWidgets import QMessageBox

con = sqlite3.connect("emp.db")
cur = con.cursor()
defaultImage = "person.png"
currentImage = ""
person_id = None
class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ÇALIŞANLARIM")
        self.setGeometry(350, 150, 650, 500)
        #self.setStyleSheet("QMainWindow{background-color: orange} QFrame { border: 50px solid black } ");
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()
        self.getEmp()
        if self.employeelist.count() > 0:
            self.displayFirst()
    def layouts(self):
        # #########LAYOUTLAR################
        self.mainlayout = QHBoxLayout()

        self.form = QFormLayout()
        #self.form.setStyleSheet("background-color:grey;")
        self.rightbox = QVBoxLayout()
        self.list = QHBoxLayout()
        self.hbox = QHBoxLayout()
        #self.form.setStyleSheet("background-color:grey;")
        # adding child layouts to main layout
        self.rightbox.addLayout(self.list)
        self.rightbox.addLayout(self.hbox)
        self.mainlayout.addLayout(self.form,40)
        self.mainlayout.addLayout(self.rightbox,60)
        # #adding widgets to layouts
        self.list.addWidget(self.employeelist)
        self.hbox.addWidget(self.btnNew)
        self.hbox.addWidget(self.btnUpdate)
        self.hbox.addWidget(self.btnDel)

        # setting main window layout
        self.setLayout(self.mainlayout)
    def mainDesign(self):
        self.setStyleSheet("font-size:13pt;font-family:Ariel;")
        self.employeelist = QListWidget()
        self.employeelist.itemClicked.connect(self.showPerson)
        self.employeelist.setStyleSheet("background-color:rgb(204,255,255);")
        self.btnNew = QPushButton("Ekle")
        self.btnNew.setStyleSheet("background-color:orange;")
        self.btnNew.clicked.connect(self.addEmp)
        self.btnUpdate = QPushButton("Güncelle")
        self.btnUpdate.setStyleSheet("background-color:orange;")
        self.btnUpdate.clicked.connect(self.updateEmp)
        self.btnDel = QPushButton("Sil")
        self.btnDel.setStyleSheet("background-color:orange;")
        self.btnDel.clicked.connect(self.deleteEmp)

    def updateEmp(self):
        global person_id
        if self.employeelist.selectedItems():
            person = self.employeelist.currentItem().text()
            person_id = person.split("-")[0]
            self.updateWindow = UpdateWindow()
            self.close()
    def deleteEmp(self):
        if self.employeelist.selectedItems():
            person = self.employeelist.currentItem().text()
            id = person.split("-")[0]
            mbox = QMessageBox.question(self, "Uyarı!", "Bu kişiyi silmek istediğine emin misin?", QMessageBox.Yes |QMessageBox.No, QMessageBox.No)
            if mbox == QMessageBox.Yes:
                try:
                    query = "DELETE FROM emp WHERE id=?"
                    cur.execute(query, (id,))
                    con.commit()
                    QMessageBox.information(self, "Bilgi!", "Kişi silindi")
                    self.close()
                    self.main = Main()
                except:
                    QMessageBox.information(self, "Uyarı!", "Kişi silinemedi")

    def showPerson(self):
        for i in reversed(range(self.form.count())):
            widget = self.form.takeAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.displayFirst()

    def addEmp(self):
        self.newEmp = AddEmployee()
        self.close()
    def getEmp(self):
        query = "SELECT id,name,surname FROM emp"
        employees = cur.execute(query).fetchall()
        for employee in employees:
            self.employeelist.addItem(str(employee[0])+"-"+employee[1]+" "+employee[2])
            
    def displayFirst(self):
        try:
            employee = self.employeelist.currentItem().text()
            id = employee.split("-")[0]
            query = "SELECT * FROM emp WHERE id=?"
            employee = cur.execute(query, (id,)).fetchone()
        except:
            query = "SELECT * FROM emp ORDER BY ROWID ASC LIMIT 1"
            employee = cur.execute(query).fetchone()

        img = QLabel()
        img.setPixmap(QPixmap("images/"+employee[5]))
        
        self.form.setVerticalSpacing(20)
        self.form.addRow("", img)
        self.form.setAlignment(Qt.AlignCenter)
        self.form.addRow("İsim :", QLabel(employee[1]))
        self.form.addRow("Soy isim :", QLabel(employee[2]))
        self.form.addRow("Telefon Numarası :", QLabel(employee[3]))
        self.form.addRow("E-posta :", QLabel(employee[4]))
        self.form.addRow("Adres :", QLabel(employee[6]))

        

class UpdateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Çalışan Güncelle")
        self.setStyleSheet("background-color:rgb(204,255,255);")
        self.setGeometry(450, 150, 350, 600)

        self.UI()
        self.show()

    def UI(self):
        self.getPerson()
        self.mainDesign()
        self.layouts()
    def closeEvent(self, event):
        self.main = Main()

    def getPerson(self):
        global person_id
        query = "SELECT * FROM emp WHERE id=?"
        employee = cur.execute(query,(person_id,)).fetchone()
        self.namee = employee[1]
        self.surnamee = employee[2]
        self.phonee = employee[3]
        self.emaill = employee[4]
        self.imgg = employee[5]
        self.adres = employee[6]
    def layouts(self):
        # main layouts
        self.main = QVBoxLayout()
        self.top = QVBoxLayout()
        self.bottom = QFormLayout()
        # adding child layouts
        self.main.addLayout(self.top)
        self.main.addLayout(self.bottom)
        # adding top layout widgets
        self.top.addWidget(self.title)
        self.top.addWidget(self.img)
        self.img.setAlignment(Qt.AlignCenter)
        self.top.addStretch()
        self.top.setAlignment(Qt.AlignCenter)
        # adding bottom layout widgets
        self.bottom.addRow(self.name, self.nameEntry)
        self.bottom.addRow(self.surname, self.surnameEntry)
        self.bottom.addRow(self.phone, self.phoneEntry)
        self.bottom.addRow(self.email, self.emailEntry)
        self.bottom.addRow(self.imglbl, self.imgbtn)
        self.bottom.addRow(self.adreslbl, self.adressEditor)
        self.bottom.addRow("", self.upbtn)
        # setting main layout for window
        self.setLayout(self.main)

    def mainDesign(self):
        regex = QRegExp("[a-z-A-Z_]+")
        validator = QRegExpValidator(regex)

        regexInt = QRegExp("[0-9_]+")
        validatorInt = QRegExpValidator(regexInt)

        regexEmail = QRegExp("\\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,4}\\b", Qt.CaseInsensitive)
        validatorEmail = QRegExpValidator(regexEmail)
       
        # Top layout widgets
        self.title = QLabel("Çalışan Güncelle")
        self.title.setStyleSheet('font-size:24pt;font-family:Arial Bold')
        self.img = QLabel()
        self.img.setPixmap(QPixmap("images/{}".format(self.imgg)))
        # bottom layout widgets
        self.name = QLabel("İsim :")
        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.namee)
        self.nameEntry.setValidator(validator)
        self.nameEntry.setMaxLength(30)
        self.surname = QLabel("Soy isim :")
        self.surnameEntry = QLineEdit()
        self.surnameEntry.setText(self.surnamee)
        self.surnameEntry.setValidator(validator)
        self.surnameEntry.setMaxLength(30)
        self.phone = QLabel("Telefon Numarası :")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setText(self.phonee)
        self.phoneEntry.setValidator(validatorInt)
        self.phoneEntry.setMaxLength(11)
        self.email = QLabel("E-posta :")
        self.emailEntry = QLineEdit()
        self.emailEntry.setText(self.emaill)
        self.emailEntry.setMaxLength(35)
        self.emailEntry.setValidator(validatorEmail)
        self.imglbl = QLabel("Fotoğraf :")
        self.imgbtn = QPushButton("Seçiniz")
        self.imgbtn.setStyleSheet("background-color:orange;font-size:10pt")
        self.imgbtn.clicked.connect(self.uploadim)
        self.adreslbl = QLabel("Adres :")
        self.adressEditor = QTextEdit()
        self.adressEditor.setText(self.adres)
        self.upbtn = QPushButton("Güncelle")
        self.upbtn.setStyleSheet("background-color:orange;font-size:10pt")
        self.upbtn.clicked.connect(self.updatePer)

    def updatePer(self):
        global defaultImage
        global person_id
        check = True
        name = self.nameEntry.text()
        surname = self.surnameEntry.text()
        phone = self.phoneEntry.text()
        email = self.emailEntry.text()
        img = currentImage
        address = self.adressEditor.toPlainText()
        if(self.emailEntry.hasAcceptableInput() == False):
            self.emailEntry.setStyleSheet("QLineEdit { color: red;}")
            check = False
        if(len(phone) < 11):
            self.phoneEntry.setStyleSheet("QLineEdit { color: red;}")
            check = False
        if (name and surname and phone != "" and check):
            try:
                query = "UPDATE emp set name=?,surname=?,phone=?,email=?,img=?,adress=? WHERE id=?"
                cur.execute(query, (name, surname, phone, email, img, address, person_id))
                con.commit()
                QMessageBox.information(self, "Başarılı!", "Kişi Güncellendi")
                self.close()
                self.main = Main()
            except:
                QMessageBox.information(self, "Uyarı!", "Kişi Güncellenemedi")
        elif(check == False):
            QMessageBox.information(self, "Uyarı", "Kişi Güncellenemedi")
        else:
            QMessageBox.information(self, "Uyarı", "Alanlar boş bırakılamaz")

    def uploadim(self):
        global currentImage
        size = (128, 128)
        self.fileName, ok = QFileDialog.getOpenFileName(self, "Fotoğraf Yükle", '', 'Image Files (*.jpg *.png)' )
        if ok:
            currentImage = os.path.basename(self.fileName)
            img = Image.open(self.fileName)
            img = img.resize(size)
            img.save("images/{}".format(currentImage))
            self.img.setPixmap(QPixmap("images/{}".format(currentImage)))

class AddEmployee(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Çalışan Ekle")
        self.setStyleSheet("background-color:rgb(204,255,229);")
        self.setGeometry(450, 150, 350, 600)
        self.UI()
        self.show()
        self.check = False
    def closeEvent(self, event):
        self.main = Main()
    def UI(self):
        self.mainDesign()
        self.layouts()
    def layouts(self):
        # main layouts
        self.main = QVBoxLayout()
        self.top = QVBoxLayout()
        self.bottom = QFormLayout()
        # adding child layouts
        self.main.addLayout(self.top)
        self.main.addLayout(self.bottom)
        # adding top layout widgets
        self.top.addWidget(self.title)
        self.img.setAlignment(Qt.AlignCenter)
        self.top.addWidget(self.img)
        self.top.addStretch()
        self.top.setAlignment(Qt.AlignCenter)
        # adding bottom layout widgets
        self.bottom.addRow(self.name, self.nameEntry)
        self.bottom.addRow(self.surname, self.surnameEntry)
        self.bottom.addRow(self.phone, self.phoneEntry)
        self.bottom.addRow(self.email, self.emailEntry)
        self.bottom.addRow(self.imglbl, self.imgbtn)
        self.bottom.addRow(self.adreslbl, self.adressEditor)
        self.bottom.addRow("", self.addbtn)
        # setting main layout for window
        self.setLayout(self.main)
    def mainDesign(self):
        regex = QRegExp("[a-z-A-Z_]+")
        validator = QRegExpValidator(regex)

        regexInt = QRegExp("[0-9_]+")
        validatorInt = QRegExpValidator(regexInt)

        regexEmail = QRegExp("\\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,4}\\b", Qt.CaseInsensitive)
        validatorEmail = QRegExpValidator(regexEmail)

        # Top layout widgets
        self.title = QLabel("Çalışan Ekle")
        self.title.setStyleSheet('font-size:24pt;font-family:Arial Bold')
        self.img = QLabel()
        self.img.setPixmap(QPixmap("icons\person.png"))
        # bottom layout widgets
        self.name = QLabel("İsim :")
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Çalışan ismini giriniz")
        self.nameEntry.setValidator(validator)
        self.nameEntry.setMaxLength(30)
        self.surname = QLabel("Soy isim :")
        self.surnameEntry = QLineEdit()
        self.surnameEntry.setPlaceholderText("Çalışan soy ismini giriniz")
        self.surnameEntry.setValidator(validator)
        self.surnameEntry.setMaxLength(30)
        self.phone = QLabel("Telefon Numarası :")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setPlaceholderText("Çalışan telefon numarasını giriniz")
        self.phoneEntry.setValidator(validatorInt)
        self.phoneEntry.setMaxLength(11)
        self.email = QLabel("E-posta :")
        self.emailEntry = QLineEdit()
        self.emailEntry.setPlaceholderText("Çalışan e-posta adresini giriniz")
        self.emailEntry.setMaxLength(20)
        self.emailEntry.setValidator(validatorEmail)
        self.imglbl = QLabel("Fotoğraf :")
        self.imgbtn = QPushButton("Seçiniz")
        self.imgbtn.clicked.connect(self.uploadim)
        self.imgbtn.setStyleSheet("background-color:orange;font-size:10pt")
        self.adreslbl = QLabel("Adres :")
        self.adressEditor = QTextEdit()
        self.addbtn = QPushButton("Ekle")
        self.addbtn.clicked.connect(self.addEmp)
        self.addbtn.setStyleSheet("background-color:orange;font-size:10pt")
        self.adreslbl = QLabel("Adres :")
    def addEmp(self):
        global defaultImage
        global currentImage
        name = self.nameEntry.text()
        surname = self.surnameEntry.text()
        phone = self.phoneEntry.text()
        email = self.emailEntry.text()
        check = True
        if(self.check):
            img = currentImage
        else:
            img = defaultImage
        adress = self.adressEditor.toPlainText()
        if(self.emailEntry.hasAcceptableInput() == False):
            self.emailEntry.setStyleSheet("QLineEdit { color: red;}")
            check = False
        if(len(phone) < 11):
            self.phoneEntry.setStyleSheet("QLineEdit { color: red;}")
            check = False
        if (name and surname and phone != "" and check):
            try:
                query = "INSERT INTO emp (name,surname,phone,email,img,adress) VALUES(?,?,?,?,?,?)"
                cur.execute(query, (name,surname,phone,email,img,adress))
                con.commit()
                QMessageBox.information(self, "Başarılı!", "Kişi Eklendi")
                self.close()
                self.main = Main()
            except:
                QMessageBox.information(self, "Uyarı!", "Kişi Eklenemedi")
        elif(name and surname and phone != "" and check == False):
            QMessageBox.information(self, "Uyarı", "Kişi Eklenemedi")
        else:
            self.nameEntry.setStyleSheet("QLineEdit { color: red;}")
            self.surnameEntry.setStyleSheet("QLineEdit { color: red;}")
            QMessageBox.information(self, "Uyarı", "Alanlar boş bırakılamaz")

    def uploadim(self):
        global currentImage
        size = (128, 128)
        self.fileName, ok = QFileDialog.getOpenFileName(self, "Fotoğraf Yükle", '', 'Image Files (*.jpg *.png)' )
        if ok:
            self.check = True
            currentImage = os.path.basename(self.fileName)
            img = Image.open(self.fileName)
            img = img.resize(size)
            img.save("images/{}".format(currentImage))
            self.img.setPixmap(QPixmap("images/{}".format(currentImage)))
def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()