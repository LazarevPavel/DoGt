# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mvideo\PycharmProjects\Graph_Alogrithm\Interface\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(526, 525)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.FileOperationsLayout = QtWidgets.QVBoxLayout()
        self.FileOperationsLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.FileOperationsLayout.setContentsMargins(-1, -1, 0, -1)
        self.FileOperationsLayout.setObjectName("FileOperationsLayout")
        self.Path_start_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.Path_start_label.setFont(font)
        self.Path_start_label.setObjectName("Path_start_label")
        self.FileOperationsLayout.addWidget(self.Path_start_label)
        self.FileInputLayout = QtWidgets.QHBoxLayout()
        self.FileInputLayout.setObjectName("FileInputLayout")
        self.File_url_input = QtWidgets.QTextEdit(self.centralwidget)
        self.File_url_input.setEnabled(True)
        self.File_url_input.setMinimumSize(QtCore.QSize(0, 0))
        self.File_url_input.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.File_url_input.setFont(font)
        self.File_url_input.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.File_url_input.setReadOnly(True)
        self.File_url_input.setObjectName("File_url_input")
        self.FileInputLayout.addWidget(self.File_url_input)
        self.File_input_button = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.File_input_button.setFont(font)
        self.File_input_button.setAutoFillBackground(False)
        self.File_input_button.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.File_input_button.setObjectName("File_input_button")
        self.FileInputLayout.addWidget(self.File_input_button)
        self.FileOperationsLayout.addLayout(self.FileInputLayout)
        self.Calculate_button = QtWidgets.QPushButton(self.centralwidget)
        self.Calculate_button.setObjectName("Calculate_button")
        self.FileOperationsLayout.addWidget(self.Calculate_button)
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setEnabled(False)
        self.stop_button.setObjectName("stop_button")
        self.FileOperationsLayout.addWidget(self.stop_button)
        self.Finish_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Finish_label.setFont(font)
        self.Finish_label.setStyleSheet("color: rgb(0, 170, 0);")
        self.Finish_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Finish_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Finish_label.setLineWidth(1)
        self.Finish_label.setObjectName("Finish_label")
        self.FileOperationsLayout.addWidget(self.Finish_label)
        self.ProblemsBoxLayout = QtWidgets.QVBoxLayout()
        self.ProblemsBoxLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.ProblemsBoxLayout.setContentsMargins(0, 0, -1, 6)
        self.ProblemsBoxLayout.setObjectName("ProblemsBoxLayout")
        self.Problems_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.Problems_text.setEnabled(True)
        self.Problems_text.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.Problems_text.setFont(font)
        self.Problems_text.setObjectName("Problems_text")
        self.ProblemsBoxLayout.addWidget(self.Problems_text)
        self.FileOperationsLayout.addLayout(self.ProblemsBoxLayout)
        self.Make_visual_button = QtWidgets.QPushButton(self.centralwidget)
        self.Make_visual_button.setEnabled(False)
        self.Make_visual_button.setObjectName("Make_visual_button")
        self.FileOperationsLayout.addWidget(self.Make_visual_button)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.FileOperationsLayout.addLayout(self.verticalLayout)
        self.Path_result_lable = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.Path_result_lable.setFont(font)
        self.Path_result_lable.setObjectName("Path_result_lable")
        self.FileOperationsLayout.addWidget(self.Path_result_lable)
        self.FileOutputLayout = QtWidgets.QHBoxLayout()
        self.FileOutputLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.FileOutputLayout.setContentsMargins(0, -1, -1, -1)
        self.FileOutputLayout.setSpacing(6)
        self.FileOutputLayout.setObjectName("FileOutputLayout")
        self.File_url_output = QtWidgets.QTextEdit(self.centralwidget)
        self.File_url_output.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.File_url_output.setFont(font)
        self.File_url_output.setObjectName("File_url_output")
        self.FileOutputLayout.addWidget(self.File_url_output)
        self.File_output_button = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.File_output_button.setFont(font)
        self.File_output_button.setAutoFillBackground(False)
        self.File_output_button.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.File_output_button.setObjectName("File_output_button")
        self.FileOutputLayout.addWidget(self.File_output_button)
        self.FileOperationsLayout.addLayout(self.FileOutputLayout)
        self.Label_filename_output = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.Label_filename_output.setFont(font)
        self.Label_filename_output.setObjectName("Label_filename_output")
        self.FileOperationsLayout.addWidget(self.Label_filename_output)
        self.Edit_filename_output = QtWidgets.QTextEdit(self.centralwidget)
        self.Edit_filename_output.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.Edit_filename_output.setFont(font)
        self.Edit_filename_output.setObjectName("Edit_filename_output")
        self.FileOperationsLayout.addWidget(self.Edit_filename_output)
        self.out_result_button = QtWidgets.QPushButton(self.centralwidget)
        self.out_result_button.setEnabled(False)
        self.out_result_button.setObjectName("out_result_button")
        self.FileOperationsLayout.addWidget(self.out_result_button)
        self.horizontalLayout.addLayout(self.FileOperationsLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Path_start_label.setText(_translate("MainWindow", "Введите путь до файла:"))
        self.File_input_button.setText(_translate("MainWindow", "Browse..."))
        self.Calculate_button.setText(_translate("MainWindow", "Выполнить расчёт"))
        self.stop_button.setText(_translate("MainWindow", "Остановить расчёт"))
        self.Finish_label.setText(_translate("MainWindow", "Статус"))
        self.Make_visual_button.setText(_translate("MainWindow", "Провести визуализацию"))
        self.Path_result_lable.setText(_translate("MainWindow", "Укажите путь для сохранения результата:"))
        self.File_output_button.setText(_translate("MainWindow", "Browse..."))
        self.Label_filename_output.setText(_translate("MainWindow", "Укажите имя файла результата (без указания расширения):"))
        self.out_result_button.setText(_translate("MainWindow", "Вывести результат в файл"))
