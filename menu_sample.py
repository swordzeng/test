# -*- coding: utf-8 -*-
# Created by PCITZDF on 2018/4/8 15:36.
# FileName: menuandtools.py

import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp, QMenu


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.menuInit()
        self.toolMenuInit()

        self.statusBar().showMessage("Ready")  # 设置状态栏
        self.setGeometry(300, 300, 250, 150)  # 设置窗体位置及大小
        self.setWindowTitle("Statusbar")  # 设置标题
        self.show()

    def menuInit(self):
        exitAct = QAction(QIcon('icons/node.png'), "exit", self)
        exitAct.setShortcut("Ctrl+Q")
        exitAct.setStatusTip("Exit Application")
        exitAct.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")
        filemenu.addAction(exitAct)

        impMenu = QMenu("Import", self)

        newActioni = QAction("New", self, checkable=True)
        impMenu.addAction(newActioni)

        filemenu.addMenu(impMenu)

    def contextMenuEvent(self, e):
        """右键菜单"""
        cmenu = QMenu(self)

        newAct = cmenu.addAction("new")
        openAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(e.pos()))
        if action == quitAct:
            qApp.quit()

    def toolMenuInit(self):
        """工具栏菜单"""
        exitAct = QAction(QIcon('icons/node.png'), "exit", self)
        exitAct.setShortcut("Ctrl+Q")
        exitAct.triggered.connect(qApp.quit)
        exitAct.setToolTip("退出应用")

        self.toolbar = self.addToolBar("Exit")
        self.toolbar.addAction(exitAct)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())