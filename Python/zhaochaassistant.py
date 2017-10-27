#!Python
#coding=gbk
__version__ = "$Id$"

# 中文注释
import sys
reload(sys)
sys.setdefaultencoding("gbk")

import os
import time

from PIL import Image
from PIL import ImageChops
from PIL import ImageGrab
from PIL import ImageDraw

import win32gui
import win32api
import win32con

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import resources

class ZhaoChaFrame(QWidget):
    game_hwnd = 0           # 游戏的窗体句柄
    bgpixmap = None
    pixmap = None
    my_visible = False

    GAME_CLASS = "#32770"
    GAME_TITLE = "大家来找茬"

    WIDTH = 500             # 大图宽
    HEIGHT = 450            # 大图高
    ANCHOR_LEFT_X = 8       # 左图X起点
    ANCHOR_RIGHT_X = 517    # 右图X起点
    ANCHOR_Y = 190          # Y起点
    CLIP_WIDTH = 1
    CLIP_HEIGHT = 1
    DIFF_LIMIT = 6000       # 差异阀值，两片图形对比差异差异超过此值视为不一样

    # 查找区域
    # 大图版 1024 x 738
    BIG_WIDTH = 498             # 大图宽
    BIG_HEIGHT = 448            # 大图高
    BIG_ANCHOR_LEFT_X = 8       # 左图X起点
    BIG_ANCHOR_RIGHT_X = 517    # 右图X起点
    BIG_ANCHOR_Y = 190          # Y起点
    BIG_CLIP_WIDTH = 1
    BIG_CLIP_HEIGHT = 1
    BIG_DIFF_LIMIT = 6000       # 差异阀值，两片图形对比差异差异超过此值视为不一样

    # 小图版 800 x 600
    SMALL_WIDTH = 381             # 大图宽
    SMALL_HEIGHT = 286            # 大图高
    SMALL_ANCHOR_LEFT_X = 10      # 左图X起点
    SMALL_ANCHOR_RIGHT_X = 403    # 右图X起点
    SMALL_ANCHOR_Y = 184          # Y起点
    SMALL_CLIP_WIDTH = 1
    SMALL_CLIP_HEIGHT = 1
    SMALL_DIFF_LIMIT = 7000       # 差异阀值，两片图形对比差异差异超过此值视为不一样


    # 存储对比结果 二位数组，映射每一个基块
    result = []

    clock = 0

    def __init__(self, parent = None):
        QWidget.__init__(self, parent, flags = Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint)
        # 设置背景透明，这样按钮不会太难看
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 这些属性让程序不在任务栏出现标题
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Popup | Qt.Tool);

        # 托盘
        self.icon = QIcon(":\icon.png")

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.icon)
        self.trayIcon.setToolTip(u"QQ找茬助手")
        self.trayIcon.show()
        self.trayIcon.showMessage(u"QQ找茬助手", u"QQ找茬助手已经待命，进入游戏即可激活")

        self.action = QAction(u"退出QQ找茬助手", self, triggered = sys.exit)
        self.menu = QMenu(self)
        self.menu.addAction(self.action)
        self.trayIcon.setContextMenu(self.menu)

        # 定时探测游戏
        self.stick_timer = QTimer()
        self.stick_timer.start(20)
        self.connect(self.stick_timer, SIGNAL('timeout()'), self.StickTarget)

        # 这个QLabel其实就是中间绘图区的背景
        self.label = QLabel(self)

        self.pixmap = QPixmap(self.size())

        # 刷新按钮
        self.btn_compare = QPushButton(self)
        self.btn_compare.setText(u"对比")
        self.connect(self.btn_compare, SIGNAL('clicked()'), self.Compare)

        # 开关
        self.btn_toggle = QPushButton(self)
        self.btn_toggle .setText(u"擦除")
        self.connect(self.btn_toggle , SIGNAL('clicked()'), self.Clear)

        self.HideMe()


    def StickTarget(self):
        '''让本窗体粘附在目标窗体上'''
        # 找到目标窗口句柄
        game_hwnd = win32gui.FindWindow(self.GAME_CLASS, self.GAME_TITLE)
        if game_hwnd == 0:
            if self.my_visible:
                # 如果游戏窗体不可见，比如最小化、关闭了，隐藏自己
                self.HideMe()
            return
        else:
            self.game_hwnd = game_hwnd

        try:
            window_rect = win32gui.GetWindowRect(self.game_hwnd)
            if self.game_hwnd == win32gui.GetForegroundWindow() and window_rect[0] > 0:
                point = QPoint(window_rect[0], window_rect[1])
                size = QSize(window_rect[2] - window_rect[0], window_rect[3] - window_rect[1])

                if self.size() != size:
                    self.SyncSize(size)

                if self.pos() != point:
                    self.move(point)

                if not self.my_visible:
                    self.ShowMe()
                    #self.FindAndShow()
            elif win32gui.GetForegroundWindow() != int(self.winId()) and self.my_visible:
                # 游戏窗口隐藏时，同时隐藏找碴助手
                self.HideMe()
        except:
            if self.my_visible:
                self.HideMe()


    def paintEvent(self, event):
        if not self.my_visible:
            self.move(-2000, -2000)

        self.pixmap.fill()
        p = QPainter(self.pixmap)
        p.setPen(QPen(QBrush(QColor(0, 0, 0)), 2))

        for row in xrange(len(self.result)):
            for col in xrange(len(self.result[0])):
                if self.result[row][col] != 0:
                    # 定一个基点，避免算数太难看
                    base_l_x = self.ANCHOR_LEFT_X + self.CLIP_WIDTH * col
                    base_r_x = self.ANCHOR_RIGHT_X + self.CLIP_WIDTH * col
                    base_y = self.ANCHOR_Y + self.CLIP_HEIGHT * row

                    if row == 0 or self.result[row - 1][col] == 0:
                        # 如果是第一行，或者上面的格子为空，画一条上边
                        p.drawLine(base_l_x, base_y, base_l_x + self.CLIP_WIDTH, base_y)
                        p.drawLine(base_r_x, base_y, base_r_x + self.CLIP_WIDTH, base_y)
                    if row == len(self.result) - 1 or self.result[row + 1][col] == 0:
                        # 如果是最后一行，或者下面的格子为空，画一条下边
                        p.drawLine(base_l_x, base_y + self.CLIP_HEIGHT, base_l_x + self.CLIP_WIDTH, base_y + self.CLIP_HEIGHT)
                        p.drawLine(base_r_x, base_y + self.CLIP_HEIGHT, base_r_x + self.CLIP_WIDTH, base_y + self.CLIP_HEIGHT)
                    if col == 0 or self.result[row][col - 1] == 0:
                        # 如果是第一列，或者左边的格子为空，画一条左边
                        p.drawLine(base_l_x, base_y, base_l_x, base_y + self.CLIP_HEIGHT)
                        p.drawLine(base_r_x, base_y, base_r_x, base_y + self.CLIP_HEIGHT)
                    if col == len(self.result[0]) - 1 or self.result[row][col + 1] == 0:
                        # 如果是第一列，或者右边的格子为空，画一条右边
                        p.drawLine(base_l_x + self.CLIP_WIDTH, base_y, base_l_x + self.CLIP_WIDTH, base_y + self.CLIP_HEIGHT)
                        p.drawLine(base_r_x + self.CLIP_WIDTH, base_y, base_r_x + self.CLIP_WIDTH, base_y + self.CLIP_HEIGHT)
        p.fillRect(self.btn_compare.geometry(), QBrush(QColor(0, 0, 0)))
        p.fillRect(self.btn_toggle.geometry(), QBrush(QColor(0, 0, 0)))
        self.setMask(QBitmap(self.pixmap))


    def Clear(self):
        self.ResetResult()
        self.repaint()


    def ShowMe(self):
        self.my_visible = True
        self.repaint()


    def HideMe(self):
        self.my_visible = False
        self.repaint()


    def Compare(self):
        # 对比
        if self.stick_timer.isActive():
            self.FindAndShow()
        else:
            self.stick_timer.start()


    def ResetResult(self):
        # 清楚之前计算的结果
        self.result = [[0 for a in range(0, self.WIDTH / self.CLIP_WIDTH)] for b in range(0, self.HEIGHT / self.CLIP_HEIGHT)]


    def SyncSize(self, size):
        self.resize(size);

        if self.width() == 1024 and self.height() == 738:
                self.WIDTH           = self.BIG_WIDTH
                self.HEIGHT          = self.BIG_HEIGHT
                self.ANCHOR_LEFT_X   = self.BIG_ANCHOR_LEFT_X
                self.ANCHOR_RIGHT_X  = self.BIG_ANCHOR_RIGHT_X
                self.ANCHOR_Y        = self.BIG_ANCHOR_Y
                self.CLIP_WIDTH      = self.BIG_CLIP_WIDTH
                self.CLIP_HEIGHT     = self.BIG_CLIP_HEIGHT
                self.DIFF_LIMIT      = self.BIG_DIFF_LIMIT
                self.btn_compare.setGeometry(611, 650, 100, 40)
                self.btn_toggle.setGeometry(715, 650, 100, 40)
        elif self.width() == 800 and self.height() == 600:
                self.WIDTH           = self.SMALL_WIDTH
                self.HEIGHT          = self.SMALL_HEIGHT
                self.ANCHOR_LEFT_X   = self.SMALL_ANCHOR_LEFT_X
                self.ANCHOR_RIGHT_X  = self.SMALL_ANCHOR_RIGHT_X
                self.ANCHOR_Y        = self.SMALL_ANCHOR_Y
                self.CLIP_WIDTH      = self.SMALL_CLIP_WIDTH
                self.CLIP_HEIGHT     = self.SMALL_CLIP_HEIGHT
                self.DIFF_LIMIT      = self.SMALL_DIFF_LIMIT
                self.btn_compare.setGeometry(472, 496, 100, 40)
                self.btn_toggle.setGeometry(576, 496, 100, 40)
        else:
            print "游戏窗体大小匹配错误"
            return

        self.pixmap = QPixmap(self.size())
        self.bgpixmap = QPixmap(self.width(), self.HEIGHT)
        self.bgpixmap.fill(QColor(0, 0, 255))
        self.label.setGeometry(0, self.ANCHOR_Y, self.width(), self.HEIGHT)
        self.label.setPixmap(self.bgpixmap)


    def FindAndShow(self):
        # 截取游戏窗口内容
        self.my_visible = True
        self.DebugTime("init")

        ## 裁剪得到左右的内容图片
        win32gui.ShowWindow(self.game_hwnd, win32con.SW_RESTORE)    # 强行显示界面后才好截图
        win32gui.SetForegroundWindow(self.game_hwnd)                # 将游戏窗口提到最前
        src_image = ImageGrab.grab((self.x(), self.y() + self.ANCHOR_Y, self.x() + self.ANCHOR_RIGHT_X + self.WIDTH, self.y() + self.ANCHOR_Y + self.HEIGHT))
        print "Get the Picture"
        #src_image.show()
        left_box = (self.ANCHOR_LEFT_X, 0, self.ANCHOR_LEFT_X + self.WIDTH, self.HEIGHT)
        right_box = (self.ANCHOR_RIGHT_X, 0, self.ANCHOR_RIGHT_X + self.WIDTH, self.HEIGHT)
        image_left = src_image.crop(left_box)
        image_right = src_image.crop(right_box)
        print "show the left"
        #image_left.show()
        print "----------------------"
        print "----------------------"
        print "show the right"
        print "----------------------"
        print "----------------------"
        #image_right.show()
        image_cover = ImageChops.invert(image_right)
        image_diff = Image.blend(image_left,image_cover,0.5)
        image_left.save("left.bmp","bmp")
        image_right.save("right.bmp","bmp")
        image_diff.save("diff.bmp","bmp")
        #image_diff.show()
        #image_diff.convert('1').show()
        #Image.composite(image_left,image_cover,1).show()
        self.DebugTime("拆图完成")

 
        #将左右大图裁剪成多个小图分别进行对比
        self.ResetResult()
        for col in xrange(0, self.WIDTH / self.CLIP_WIDTH):
            for row in xrange(0, self.HEIGHT / self.CLIP_HEIGHT - 1):
                clip_box_left = (col * self.CLIP_WIDTH, row * self.CLIP_HEIGHT, (col + 1) * self.CLIP_WIDTH, (row + 1) * self.CLIP_HEIGHT)
                clip_box_right = (col * self.CLIP_WIDTH, (row + 1) * self.CLIP_HEIGHT, (col + 1) * self.CLIP_WIDTH, (row + 2) * self.CLIP_HEIGHT)
                clip_image_left = image_diff.crop(clip_box_left)
                clip_image_right = image_diff.crop(clip_box_right)
                clip_diff = self.compare(clip_image_left, clip_image_right)

                if sum(clip_diff) > 2500:
                    self.result[row][col] = 1


        self.DebugTime("对比")
        self.repaint()
        self.DebugTime("绘制")
       # print "----------------------"
       # for i in range(len(self.result)):        # Y轴循环
       #     for j in range(len(self.result[i])):    # X轴循环
       #         print self.result[i][j],
       #     print
       # print "----------------------"

    def compare(self, image_a, image_b):
        '''返回两图的差异值
        返回两图红绿蓝差值万分比之和'''
        print "Start Compare"
        histogram_a = image_a.histogram()
        histogram_b = image_b.histogram()
        if len(histogram_a) != 768 or len(histogram_b) != 768:
            return None

        red_a = 0
        red_b = 0
        for i in xrange(0, 256):
            #print "red:i:%d"%i + " Left:%d"%histogram_a[i] +" Right:%d"%histogram_b[i]
            red_a += histogram_a[i + 0] * i
            red_b += histogram_b[i + 0] * i
        diff_red = 0
        if red_a + red_b > 0:
            diff_red = abs(red_a - red_b) * 10000 / max(red_a, red_b)

        green_a = 0
        green_b = 0
        for i in xrange(0, 256):
           # print "green:i:" + i + " Left:" + histogram_a[i +256] +" Right:"+ histogram_b[i+256]
            green_a += histogram_a[i + 256] * i
            green_b += histogram_b[i + 256] * i
        diff_green = 0
        if green_a + green_b > 0:
            diff_green = abs(green_a - green_b) * 10000 / max(green_a, green_b)

        blue_a = 0
        blue_b = 0
        for i in xrange(0, 256):
           # print "bule:i:" + i + " Left:" + histogram_a[i+512] +" Right:"+ histogram_b[i+512]
            blue_a += histogram_a[i + 512] * i
            blue_b += histogram_b[i + 512] * i
        diff_blue = 0
        if blue_a + blue_b > 0:
            diff_blue = abs(blue_a - blue_b) * 10000 / max(blue_a, blue_b)

        return diff_red, diff_green, diff_blue

    def DebugTime(self, text = ""):
        return

        if self.clock > 0:
            print time.clock() - self.clock, text
        self.clock = time.clock()


def main():
    app = QApplication(sys.argv)
    qb = ZhaoChaFrame()
    qb.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
