# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mvideo\PycharmProjects\Graph_Alogrithm\Interface\GraphicsFrame.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GraphicsFrame(object):
    def setupUi(self, GraphicsFrame):
        GraphicsFrame.setObjectName("GraphicsFrame")
        GraphicsFrame.resize(749, 656)
        self.verticalLayout = QtWidgets.QVBoxLayout(GraphicsFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setHorizontalSpacing(10)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.GraphicsView = QtWidgets.QGraphicsView(GraphicsFrame)
        self.GraphicsView.setObjectName("GraphicsView")
        self.gridLayout_2.addWidget(self.GraphicsView, 1, 0, 1, 1)
        self.ParametersScrollArea = QtWidgets.QScrollArea(GraphicsFrame)
        self.ParametersScrollArea.setMinimumSize(QtCore.QSize(150, 0))
        self.ParametersScrollArea.setMaximumSize(QtCore.QSize(150, 16777215))
        self.ParametersScrollArea.setWidgetResizable(True)
        self.ParametersScrollArea.setObjectName("ParametersScrollArea")
        self.ParametersScrollAreaWidget = QtWidgets.QWidget()
        self.ParametersScrollAreaWidget.setGeometry(QtCore.QRect(0, 0, 148, 576))
        self.ParametersScrollAreaWidget.setObjectName("ParametersScrollAreaWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.ParametersScrollAreaWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ParametersVerticalLayout = QtWidgets.QVBoxLayout()
        self.ParametersVerticalLayout.setSpacing(10)
        self.ParametersVerticalLayout.setObjectName("ParametersVerticalLayout")
        self.verticalLayout_2.addLayout(self.ParametersVerticalLayout)
        self.ParametersScrollArea.setWidget(self.ParametersScrollAreaWidget)
        self.gridLayout_2.addWidget(self.ParametersScrollArea, 1, 1, 1, 1)
        self.SavePicture_button = QtWidgets.QPushButton(GraphicsFrame)
        self.SavePicture_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.SavePicture_button.setObjectName("SavePicture_button")
        self.gridLayout_2.addWidget(self.SavePicture_button, 0, 0, 1, 1)
        self.Print_button = QtWidgets.QPushButton(GraphicsFrame)
        self.Print_button.setObjectName("Print_button")
        self.gridLayout_2.addWidget(self.Print_button, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.Recalculate_button = QtWidgets.QPushButton(GraphicsFrame)
        self.Recalculate_button.setObjectName("Recalculate_button")
        self.verticalLayout.addWidget(self.Recalculate_button)

        self.retranslateUi(GraphicsFrame)
        QtCore.QMetaObject.connectSlotsByName(GraphicsFrame)

    def retranslateUi(self, GraphicsFrame):
        _translate = QtCore.QCoreApplication.translate
        GraphicsFrame.setWindowTitle(_translate("GraphicsFrame", "Graphics form"))
        self.SavePicture_button.setText(_translate("GraphicsFrame", "Сохранить изображение"))
        self.Print_button.setText(_translate("GraphicsFrame", "Печать изображения"))
        self.Recalculate_button.setText(_translate("GraphicsFrame", "Пересчитать"))
