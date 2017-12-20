# coding=utf-8

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QGridLayout, QVBoxLayout, QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from bs4 import BeautifulSoup
import sys, re
import urllib.request
import json


class main_win(QWidget):
    def __init__(self):
        super(main_win, self).__init__()
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint|Qt.MSWindowsFixedSizeDialogHint )

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
        self.ledit.returnPressed.connect(self.stran1)
        self.label1 = QLabel('查找的单词')
        self.label2 = QLabel('英式发音：')
        self.label2_1 = QLabel()
        self.label4 = QLabel('翻译区域：')
        self.label4_1 = QLabel()
        self.label4_1.setStyleSheet('color:green')
        # self.label4_1.setGeometry(QRect(80, 5, 20, 20))
        self.label4_1.setWordWrap(True)
        self.gl.addWidget(self.label1, 0, 0)
        self.gl.addWidget(self.ledit, 0, 1, 1, 1)
        self.gl.addWidget(self.label2, 1, 0)
        self.gl.addWidget(self.label2_1, 1, 1)
        self.gl.addWidget(self.label4_1, 2, 0, 4, 2)
        # 把gl布局添加到主布局中
        self.wvl.addLayout(self.gl)
        # 设置窗体布局为主布局
        self.setLayout(self.wvl)
        self.setGeometry(0, 0, 200, 200)
        self.setStyleSheet("QLabel{color:rgb(0,0,0,250);font-size:10px;font-family:Roman times;}"
                           "QLabel:hover{color:red;}")
        self.show()

    def stran1(self):
        self.word = urllib.request.quote(self.ledit.text())
        req = urllib.request.Request(
            'http://cn.bing.com/dict/search?q=%s&qs=n&form=Z9LH5&sp=-1&pq=%s&sc=3-12&sk=&cvid=BE4372C421374C658F9CC629DF84F6E9' % (
                self.word, self.word))
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
        self.soup = BeautifulSoup(the_page, "lxml")
        dict_stran = {'Ame': ''}
        try:
            tags = self.soup.find('div', id="headword")
            for tag in tags:
                if tag.get_text() != None:
                    dict_stran['word'] = tag.get_text()
            tags = self.soup.find_all('div', class_="hd_pr")
            for tag in tags:
                if tag.get_text() != None:
                    dict_stran['Ame'] = tag.get_text()
        except TypeError as e:
            print(e)
            self.label2_1.setText('没有读音')
        t2 = self.soup.find_all('li')
        yisi = ''
        for i in t2:
            if i.find(class_='pos') != None:
                yisi = yisi + i.get_text() + "\n"
                # print(i,i.name,i.attrs,i.find(class_='pos'))

        self.label2_1.setText(dict_stran['Ame'])
        self.label4_1.setText(yisi)

    def del_content_blank(s):
        clean_str = re.sub(r'\n|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020', '', str(s))
        return clean_str


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwin = main_win()
    sys.exit(app.exec_())
