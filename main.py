from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork
import csv, sys, datetime, time
from FLBasicModule import CONFIG,LSS

app_name = "DesktopTips"
c=CONFIG.Config(
    app_name=app_name,
    format2={
                "isOut":["on"], #["on"]/["off"]/[""]/["on","off"]
                "isShowLast":["on"],
                "Debug":False, #True/False
                "Thing":"中考",
                "Date":"2023.6.18"
             },
    is_json=True,
    is_log=False
    )

def ex_fun(s):
    try:
        print(s.data())
        st = s.data().decode()
        if st == 'exit':
            app.exit()

        elif 'ST' in st and c.c["Debug"]==True:#if "set time" command in st
                tstring=st[2:]
                tt=time.strptime(tstring,"%H:%M:%S")
                dtobj=datetime.datetime(timer.t.year,timer.t.month,timer.t.day,tt.tm_hour,tt.tm_min,tt.tm_sec)
                timer.t=dtobj
                
    except Exception as e:
        print(e.__class__.__name__,e)



class Timer(QtCore.QTimer):
    def __init__(self):
        super().__init__()
        self.sub = None
        self.Now = 0
        self.t = datetime.datetime.now()
        self.eachSecond()
        self.timeout.connect(self.eachSecond)
        self.start(1000)

    def _sub(self, da: datetime.time, db: datetime.time) -> int:
        return (da.hour * 60 * 60 + da.minute * 60 + da.second) - (db.hour * 60 * 60 + db.minute * 60 + db.second)

    def eachSecond(self):
        if c.c["Debug"]:
            self.t = datetime.datetime.fromtimestamp(self.t.timestamp()+1)
        else:
            self.t = datetime.datetime.now()
        self.tododay=datetime.date.fromtimestamp(time.mktime(time.strptime(c.c["Date"],"%Y.%m.%d"))) - datetime.date(self.t.year,self.t.month,self.t.day)
        self.lessons = csvRowList[self.t.weekday()]
        dt_now = datetime.time(self.t.hour, self.t.minute, self.t.second)
        for i in csvDictTimes:
            # st=time.strptime(i[:s.index('-')],'%m:%d')
            st = time.strptime(i[i.index('-') + 1:], '%H:%M')
            dt = datetime.time(st.tm_hour, st.tm_min)
            if dt_now >= dt:
                continue
            self.sub = self._sub(dt, dt_now)
            self.nowLessonTime = i
            self.nowLessonTimeii = csvDictTimes.index(i)
            self.print()
            break
        else:
            self.refresh()

    def print(self):
        if self.lessons[self.nowLessonTime] == '下课' or self.lessons[self.nowLessonTime] == '午休':
            try:
                LL = self.lessons[csvDictTimes[self.nowLessonTimeii - 1]]
            except:
                LL = None
            try:
                NL = self.lessons[csvDictTimes[self.nowLessonTimeii + 1]]
            except:
                NL = None
            ui.setText('''<html>
  <body>
    <p align="center" style="line-height: 0.8;">
      <span style="font-size: 30pt">上节课: </span
      ><span style="font-size: 40pt; font-weight: 600; color: #ff0000"
        >{LL}</span
      >
    </p>
    <p align="center" style="line-height: 0.65;">
      <span style="font-size: 30pt">{isthis}节课: </span
      ><span style="font-size: 40pt; font-weight: 600; color: #0000ff"
        >{NL}</span
      ></p>
      <p align="center" style="line-height: 0.6;">
      <span style="font-size: 20pt; color: #000000;">还有{d}{Th}</span>
    </p>
    <p align="center">
      <span style="font-size: 22pt; color: #000000;">{T}</span>
    </p>
  </body>
</html>'''.format(LL=LL, NL=NL, T=time.strftime('%y/%m/%d %H:%M:%S', self.t.timetuple()),
                  isthis='这' if self.sub <= 60 else '下',d=str(self.tododay.days)+"天",Th=c.c["Thing"]))
        else:
            ui.setText('''<html>
  <body>
    <p align="center">
      <span style="font-size: 30pt; color: #0000ff">这节课: </span
      ><span style="font-size: 40pt; font-weight: 600; color: #ff0000"
        >{}</span
      >
    </p>
    <p align="center">
    <span style="font-size: 20pt; color: #000000;">还有{d}{Th}</span></p>
    <p align="center">
      <span style="font-size: 22pt; color: #000000">{}</span>
    </p>
  </body>
</html>'''.format(self.lessons[self.nowLessonTime], time.strftime('%y/%m/%d %H:%M:%S', self.t.timetuple()),
                  d=str(self.tododay.days)+"天",Th=c.c["Thing"]))

    def refresh(self):
        if c.c["Debug"]:
            self.t = self.t+datetime.time(second=1)
        else:
            self.t = datetime.datetime.now()
        self.lessons = csvRowList[self.t.weekday()]


class Ui_classShowing(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.m_flag = False

    def setupUi(self, classShowing):
        classShowing.setObjectName("classShowing")
        classShowing.resize(400, 300)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.9)
        # self.setStyleSheet(".QWidget{background-color: rgb(255, 245, 238);border: 2px solid blue;}")
        d = app.desktop()
        self.move(d.width() - 420, 10)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        classShowing.setFont(font)
        classShowing.setWindowOpacity(0.8)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(36)
        self.setFont(font)
        self.setTextFormat(QtCore.Qt.RichText)
        self.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.setWordWrap(True)
        self.setObjectName("label")

        self.retranslateUi(classShowing)
        QtCore.QMetaObject.connectSlotsByName(classShowing)

    def retranslateUi(self, classShowing):
        _translate = QtCore.QCoreApplication.translate
        classShowing.setWindowTitle(_translate("classShowing", "Form"))
        self.setText(_translate("classShowing",
                                "<html><head/><body><p align=\"center\"><span style=\" font-size:30pt;\">上节课: "
                                "</span><span style=\" font-size:40pt; font-weight:600; "
                                "color:#ff0000;\">语文</span></p><p align=\"center\"><span style=\" "
                                "font-size:30pt;\">下节课: </span><span style=\" font-size:40pt; font-weight:600; "
                                "color:#0000ff;\">数学</span></p><p align=\"center\"><span style=\" "
                                "font-size:22pt; color:#000000;\">22/11/5 12:20:02</span></p></body></html>"))

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
        painter.setPen(QtCore.Qt.transparent)
        rect = self.rect()
        rect.setHeight(rect.height())
        rect.setWidth(rect.width())
        painter.drawRoundedRect(rect, 15, 15)
        # p = QtGui.QPainter(self)
        # opt=QtWidgets.QStyleOption()
        # opt.initFrom(self)
        # self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget,opt,p)
        # QtWidgets.QStyle.drawPrimitive(self,)
        super().paintEvent(a0)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))


app = QtWidgets.QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
lss = LSS.LocalSocSer(app_name,ex_fun)

with open('lessons.csv', 'r', newline='', encoding='gbk') as f:
    csvDictReader = csv.DictReader(f)
    csvRowList = [row for row in csvDictReader]
    csvDictTimes = csvDictReader.fieldnames
    # print(csvRowList[0][csvDictTimes[0]])
    #   csvRowList[星期数-1]==当天课程与时间对应表
    #   csvDictTimes[row]==某一时间
    #   csvRowList[星期数-1][csvDictTimes[row]]==此时课程

ui = Ui_classShowing()
timer = Timer()
ui.show()

app.exec_()
c.save()