#Uebung 5

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import urllib.parse


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.createLayout()
        self.createConnects()

    def createLayout(self):
        # Fenster-Titel definieren:
        self.setWindowTitle("GUI-Programmierung")

        # Layout erstellen:
        layout = QFormLayout()
        self.setMinimumSize(800,500)

        # Widget-Instanzen erstellen:

        menubar = self.menuBar()
        filemenu1 = menubar.addMenu("File")
        filemenu2 = menubar.addMenu("View")
        
        self.save = QAction("Save", self)
        self.quit = QAction("Quit", self)


        self.vornameLineEdit = QLineEdit()
        self.nameLineEdit = QLineEdit()
        self.geburtstagLineEdit = QDateEdit()
        self.geburtstagLineEdit.setDisplayFormat("dd/MM/yyyy")
        self.adresseLineEdit = QLineEdit()
        self.plzLineEdit = QLineEdit()
        self.ortLineEdit = QLineEdit()
        self.countries = QComboBox()
        self.countries.addItems(["Schweiz", "Deutschland", "Österreich"])

        
        self.button1 = QPushButton("Auf Karte Anzeigen")
        self.button2 = QPushButton("Laden")
        self.button3 = QPushButton("Save")
        

        # Layout füllen:
        layout.addRow("Vorname:", self.vornameLineEdit)
        layout.addRow("Name:", self.nameLineEdit)
        layout.addRow("Geburtstag:", self.geburtstagLineEdit)
        layout.addRow("Adresse:", self.adresseLineEdit)
        layout.addRow("Postleitzahl:", self.plzLineEdit)
        layout.addRow("Ort:", self.ortLineEdit)
        layout.addRow("Land:" , self.countries)
        
        layout.addRow(self.button1)
        layout.addRow(self.button2)
        layout.addRow(self.button3)

        filemenu1.addAction("save", self.speichern)
        filemenu1.addSeparator()
        filemenu1.addAction("quit", self.ende)

        filemenu2.addAction("Karte", self.aufKarte)
        filemenu2.addSeparator()
        filemenu2.addAction("Laden", self.laden)

        # Zentrales Widget erstellen und layout hinzufügen
        center = QWidget()
        center.setLayout(layout)

        # Zentrales Widget in diesem Fenster setzen
        self.setCentralWidget(center)

        # Fenster anzeigen
        self.show()

    def createConnects(self):
        
        self.button1.clicked.connect(self.aufKarte)
        self.button2.clicked.connect(self.laden)
        self.button3.clicked.connect(self.speichern)

    def aufKarte(self):
        addresse = f"{self.adresseLineEdit.text()}+{self.plzLineEdit.text()}+{self.ortLineEdit.text()}+{self.countries.currentText()}"
        query = urllib.parse.quote(addresse)
        link = f"https://www.google.ch/maps/place/{query}"
        QDesktopServices.openUrl(QUrl(link))

    def laden(self):
        filename, type = QFileDialog.getOpenFileName(self, "Datei öffnen",
                                                     "", 
                                                     "Textfile (*.txt)")
        file = open(filename, "r")
        daten = file.read().split(", ")
        print(daten)
        self.vornameLineEdit.setText(daten[0])
        self.nameLineEdit.setText(daten[1])
        self.geburtstagLineEdit.setDate(QDate.fromString(daten[2], "dd/MM/yyyy"))
        self.adresseLineEdit.setText(daten[3])
        self.plzLineEdit.setText(daten[4])
        self.ortLineEdit.setText(daten[5])
        index = self.countries.findText(daten[6], Qt.MatchFixedString)
        self.countries.setCurrentIndex(index)




    def speichern(self):
        filename, typ= QFileDialog.getSaveFileName(self, "Datei Speichern",
                                                   "",
                                                   "Txt (*.txt)")
        file = open(filename, "w")
        daten = [self.vornameLineEdit.text(), 
                 self.nameLineEdit.text(), 
                 self.geburtstagLineEdit.text(), 
                 self.adresseLineEdit.text(), 
                 self.plzLineEdit.text(), 
                 self.ortLineEdit.text(), 
                 self.countries.currentText()
                 ]
        daten_2= ", ".join(str(i) for i in daten)
        file.write (daten_2)
        file.close()
        QMessageBox.information(self, "Speichern", "Daten wurden erfolgreich gespeichert!", QMessageBox.Ok)
        
        
    def ende(self):
        sys.exit()
        #self.close() geht auch  
        






def main():
    app = QApplication(sys.argv)  # Qt Applikation erstellen
    mainwindow = MyWindow()       # Instanz Fenster erstellen
    mainwindow.raise_()           # Fenster nach vorne bringen
    app.exec_()                   # Applikations-Loop starten

if __name__ == '__main__':
    main()