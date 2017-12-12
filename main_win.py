# coding=utf-8

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QGridLayout, QVBoxLayout, QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
import urllib.request
import json


class main_win(QWidget):
    def __init__(self):
        super(main_win, self).__init__()
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
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
        self.label4 = QLabel('翻译区域：')
        self.label4_1 = QLabel()
        # self.label4_1.setGeometry(QRect(80, 5, 20, 20))
        self.label4_1.setWordWrap(True)
        self.gl.addWidget(self.label1, 0, 0)
        self.gl.addWidget(self.ledit, 0, 1, 1, 2)
        self.gl.addWidget(self.label2, 1, 0)
        self.gl.addWidget(self.label2_1, 1, 1)
        self.gl.addWidget(self.label3, 1, 2)
        self.gl.addWidget(self.label3_1, 1, 3)
        self.gl.addWidget(self.label4, 2, 0, 4, 1)
        self.gl.addWidget(self.label4_1, 2, 1, 4, 3)
        # 把gl布局添加到主布局中
        self.wvl.addLayout(self.gl)
        # 设置窗体布局为主布局
        self.setLayout(self.wvl)
        self.setGeometry(0, 0, 300, 200)
        self.setStyleSheet("QLabel{color:rgb(0,0,0,250);font-size:10px;font-family:Roman times;}"
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

        else:
            self.label2_1.setText('')
            self.label3_1.setText('')
        tran_text = ""
        for i in jsondata['defs']:
            # print(i['pos'], i['def'])
            tran_text += i['pos'] + i['def'] + '\n'
        self.label4_1.setText(tran_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwin = main_win()
    sys.exit(app.exec_())
