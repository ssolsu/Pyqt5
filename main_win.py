# coding=utf-8

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QGridLayout, QVBoxLayout, QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
import sys
import urllib.request
import json


class main_win(QWidget):
    def __init__(self):
        super(main_win, self).__init__()
        self.initui()

    def initui(self):
        self.setWindowTitle('翻译窗口')
        # 创建三个布局,创建一个主布局
        self.wvl = QVBoxLayout()
        self.hl = QHBoxLayout()
        self.vl = QVBoxLayout()
        self.gl = QGridLayout()
        # 编辑gl布局
        self.ledit = QLineEdit()
        self.ledit.returnPressed.connect(self.stran)
        self.label1 = QLabel('查找的单词')
        self.label2 = QLabel('美式发音：')
        self.label2_1 = QLabel()
        self.label3 = QLabel('英式发音：')
        self.label3_1 = QLabel()
        self.gl.addWidget(self.label1, 1, 0)
        self.gl.addWidget(self.ledit, 1, 1)
        self.gl.addWidget(self.label2, 2, 0)
        self.gl.addWidget(self.label2_1, 2, 1)
        self.gl.addWidget(self.label3, 2, 2)
        self.gl.addWidget(self.label3_1, 2, 3)
        # 把gl布局添加到主布局中
        self.wvl.addLayout(self.gl)
        # 设置窗体布局为主布局
        self.setLayout(self.wvl)
        self.setGeometry(0, 0, 300, 100)
        self.setStyleSheet("QLabel{color:rgb(0,0,0,250);font-size:9px;font-family:Roman times;}"
                           "QLabel:hover{color:red;}")
        self.show()

    def stran(self):
        self.word = urllib.request.quote(self.ledit.text())
        req = urllib.request.Request('http://xtk.azurewebsites.net/BingDictService.aspx?Word=%s' % self.word)
        with urllib.request.urlopen(req) as response:
            the_page = response.read().decode('utf-8')
        print(the_page)
        jsondata = json.loads(the_page)
        if jsondata['pronunciation'] != None:
            self.label2_1.setText(jsondata['pronunciation']['AmE'])
            self.label3_1.setText(jsondata['pronunciation']['BrE'])


class tran():
    def request_data(self):
        print('fuck')
        req = urllib.request.Request('http://xtk.azurewebsites.net/BingDictService.aspx?Word=welcome')
        with urllib.request.urlopen(req) as response:
            the_page = response.read().decode('utf-8')
        jsondata = json.loads(the_page)
        print(jsondata)
        return jsondata


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwin = main_win()
    sys.exit(app.exec_())
