import spider
from MainGUI import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

# app = QApplication(sys.argv)
# MainWindow = QMainWindow()
# # ui = spider.Ui_Form()
# ui = MainGUI.Ui_MainText()
# ui.setupUi(MainWindow)
# MainWindow.show()
# sys.exit(app.exec_())


class MainScreen(QMainWindow,Ui_MainText):
    def setUi(self,MainText):
        Ui_MainText.setupUi(MainText)
        Ui_MainText.toolButton.setFixedSize(0)

    def __init__(self,parent= None):
        super(MainScreen, self).__init__(parent)
        self.setupUi(self)
        self.toolButton.setFixedSize(0,0)

def main():
    app = QApplication(sys.argv)
    ui = MainScreen()
    ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


