from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QFrame, QLabel, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
from sudokuMain import solve_sudoku
import cv2
import numpy as np


class DocScanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Sudoku Solver'
        self.left = 50
        self.top = 50
        self.width = 500
        self.coords = []
        self.filename = ""
        self.check_empty = True
        self.height = 550
        self.setFixedSize(self.width, self.height)
        self.setObjectName("main_window")
        with open("design.qss", "r") as fopen:
            stylesheet = fopen.read()
        self.setStyleSheet(stylesheet)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #---------------------------------------first window-----------------------------------------------------

        self.win1 = QFrame(self)
        self.win1.setObjectName("windows")

        self.upload_btn = QPushButton(self.win1)
        self.upload_btn.setObjectName("btns")
        self.upload_btn.move(200, 12)
        self.upload_btn.setText("Upload Image")
        self.upload_btn.clicked.connect(self.upload_img)

        self.pic_label = QLabel(self.win1)
        self.pic_label.setObjectName("picLabel")
        pixmap = QPixmap("empt.jpg")
        self.pic_label.setPixmap(pixmap)
        self.pic_label.move(100, 70)
        self.pic_label.setScaledContents(True)

        self.select_roi = QPushButton(self.win1)
        self.select_roi.setObjectName("btns")
        self.select_roi.move(200, 450)
        self.select_roi.setText("Solve Sudoku")
        self.select_roi.clicked.connect(self.solve_game)


        self.del_pic = QLabel(self.pic_label)
        self.del_pic.move(278, 5)
        self.del_pic.setVisible(False)
        self.del_pic.setObjectName("crossBtn")
        self.del_pic.setTextFormat(Qt.RichText)
        self.del_pic.mousePressEvent = self.remove_pic




        #---------------------------------------Second window-----------------------------------------------------

        self.win2 = QFrame(self)
        self.win2.setObjectName("windows")
        self.win2.setVisible(False)

        self.back_arrow = QLabel(self.win2)
        self.back_arrow.move(15, 0)
        self.back_arrow.setObjectName("back_arrow")
        self.back_arrow.setTextFormat(Qt.RichText)
        self.back_arrow.setText("&#8592;")
        self.back_arrow.mousePressEvent = self.back_arrow_clicked

        self.pic_label_ouput = QLabel(self.win2)
        self.pic_label_ouput.setObjectName("picLabel")
        self.pic_label_ouput.move(100, 70)
        self.pic_label_ouput.setScaledContents(True)

        self.output_label = QLabel(self.win2)
        self.output_label.setText("Solved Sudoku")
        self.output_label.move(180, 430)
        self.output_label.setObjectName("labels")



        self.show()


    # -----------------------------------------------Functions-----------------------------------------------

    def upload_img(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);; JPG (*.jpg);; PNG (*.png)")
        pixmap = QPixmap(self.filename)
        self.filename1 = self.filename
        self.pic_label.setPixmap(pixmap)
        self.del_pic.setVisible(True)
        self.del_pic.setText("&#10005;")
        self.del_pic.adjustSize()
        self.check_empty = False

    def solve_game(self):
        if self.check_empty == False:
            output = solve_sudoku(self.filename)
            if output != False:
                pixmap = QPixmap(output)
                self.pic_label_ouput.setPixmap(pixmap)
                self.win2.setVisible(True)
                self.win1.setVisible(False)
            else:
                self.cant_solve()
        else:
            self.no_any_image()



    def back_arrow_clicked(self, event):
        self.win1.setVisible(True)
        self.win2.setVisible(False)

    def show_pop_up(self):
        msg = QMessageBox()
        msg.setWindowTitle("Opps!")
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Could not find any document. Please select the roi manually.")
        x = msg.exec_()

    def no_any_image(self):
        msg = QMessageBox()
        msg.setWindowTitle("No Image!")
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Please upload an image first.")
        msg.exec_()

    def cant_solve(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Could not solve the sudoku.")
        msg.exec_()




    def remove_pic(self, event):
        pixamp = QPixmap("empt.jpg")
        self.pic_label.setPixmap(pixamp)
        self.del_pic.setVisible(False)
        self.check_empty = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    docScan = DocScanner()
    sys.exit(app.exec_())

