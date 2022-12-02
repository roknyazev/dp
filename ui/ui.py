# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerDZEXRR.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
                          QRect, QSize, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                         QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
                         QRadialGradient)
from PyQt5.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1920, 1000)
        self.scrollArea = QScrollArea(Dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(10, 69, 371, 841))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 369, 839))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayoutWidget = QWidget(Dialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(380, 30, 1531, 881))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutWidget = QWidget(Dialog)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 910, 1871, 81))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.startstopButton = QPushButton(self.horizontalLayoutWidget)
        self.startstopButton.setObjectName(u"startstopButton")
        self.startstopButton.setMinimumSize(QSize(0, 60))
        font = QFont()
        font.setPointSize(25)
        self.startstopButton.setFont(font)

        self.horizontalLayout.addWidget(self.startstopButton)

        self.pauseButton = QPushButton(self.horizontalLayoutWidget)
        self.pauseButton.setObjectName(u"pauseButton")
        self.pauseButton.setMinimumSize(QSize(0, 60))
        self.pauseButton.setFont(font)

        self.horizontalLayout.addWidget(self.pauseButton)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.startstopButton.setText(QCoreApplication.translate("Dialog", u"Start", None))
        self.pauseButton.setText(QCoreApplication.translate("Dialog", u"Pause", None))
    # retranslateUi


