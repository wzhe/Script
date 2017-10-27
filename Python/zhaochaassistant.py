#!Python
#coding=gbk
__version__ = "$Id$"

# ����ע��
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
    game_hwnd = 0           # ��Ϸ�Ĵ�����
    bgpixmap = None
    pixmap = None
    my_visible = False

    GAME_CLASS = "#32770"
    GAME_TITLE = "������Ҳ�"

    WIDTH = 500             # ��ͼ��
    HEIGHT = 450            # ��ͼ��
    ANCHOR_LEFT_X = 8       # ��ͼX���
    ANCHOR_RIGHT_X = 517    # ��ͼX���
    ANCHOR_Y = 190          # Y���
    CLIP_WIDTH = 1
    CLIP_HEIGHT = 1
    DIFF_LIMIT = 6000       # ���췧ֵ����Ƭͼ�ζԱȲ�����쳬����ֵ��Ϊ��һ��

    # ��������
    # ��ͼ�� 1024 x 738
    BIG_WIDTH = 498             # ��ͼ��
    BIG_HEIGHT = 448            # ��ͼ��
    BIG_ANCHOR_LEFT_X = 8       # ��ͼX���
    BIG_ANCHOR_RIGHT_X = 517    # ��ͼX���
    BIG_ANCHOR_Y = 190          # Y���
    BIG_CLIP_WIDTH = 1
    BIG_CLIP_HEIGHT = 1
    BIG_DIFF_LIMIT = 6000       # ���췧ֵ����Ƭͼ�ζԱȲ�����쳬����ֵ��Ϊ��һ��

    # Сͼ�� 800 x 600
    SMALL_WIDTH = 381             # ��ͼ��
    SMALL_HEIGHT = 286            # ��ͼ��
    SMALL_ANCHOR_LEFT_X = 10      # ��ͼX���
    SMALL_ANCHOR_RIGHT_X = 403    # ��ͼX���
    SMALL_ANCHOR_Y = 184          # Y���
    SMALL_CLIP_WIDTH = 1
    SMALL_CLIP_HEIGHT = 1
    SMALL_DIFF_LIMIT = 7000       # ���췧ֵ����Ƭͼ�ζԱȲ�����쳬����ֵ��Ϊ��һ��


    # �洢�ԱȽ�� ��λ���飬ӳ��ÿһ������
    result = []

    clock = 0

    def __init__(self, parent = None):
        QWidget.__init__(self, parent, flags = Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint)
        # ���ñ���͸����������ť����̫�ѿ�
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # ��Щ�����ó��������������ֱ���
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Popup | Qt.Tool);

        # ����
        self.icon = QIcon(":\icon.png")

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.icon)
        self.trayIcon.setToolTip(u"QQ�Ҳ�����")
        self.trayIcon.show()
        self.trayIcon.showMessage(u"QQ�Ҳ�����", u"QQ�Ҳ������Ѿ�������������Ϸ���ɼ���")

        self.action = QAction(u"�˳�QQ�Ҳ�����", self, triggered = sys.exit)
        self.menu = QMenu(self)
        self.menu.addAction(self.action)
        self.trayIcon.setContextMenu(self.menu)

        # ��ʱ̽����Ϸ
        self.stick_timer = QTimer()
        self.stick_timer.start(20)
        self.connect(self.stick_timer, SIGNAL('timeout()'), self.StickTarget)

        # ���QLabel��ʵ�����м��ͼ���ı���
        self.label = QLabel(self)

        self.pixmap = QPixmap(self.size())

        # ˢ�°�ť
        self.btn_compare = QPushButton(self)
        self.btn_compare.setText(u"�Ա�")
        self.connect(self.btn_compare, SIGNAL('clicked()'), self.Compare)

        # ����
        self.btn_toggle = QPushButton(self)
        self.btn_toggle .setText(u"����")
        self.connect(self.btn_toggle , SIGNAL('clicked()'), self.Clear)

        self.HideMe()


    def StickTarget(self):
        '''�ñ�����ճ����Ŀ�괰����'''
        # �ҵ�Ŀ�괰�ھ��
        game_hwnd = win32gui.FindWindow(self.GAME_CLASS, self.GAME_TITLE)
        if game_hwnd == 0:
            if self.my_visible:
                # �����Ϸ���岻�ɼ���������С�����ر��ˣ������Լ�
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
                # ��Ϸ��������ʱ��ͬʱ�����Ҳ�����
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
                    # ��һ�����㣬��������̫�ѿ�
                    base_l_x = self.ANCHOR_LEFT_X + self.CLIP_WIDTH * col
                    base_r_x = self.ANCHOR_RIGHT_X + self.CLIP_WIDTH * col
                    base_y = self.ANCHOR_Y + self.CLIP_HEIGHT * row

                    if row == 0 or self.result[row - 1][col] == 0:
                        # ����ǵ�һ�У���������ĸ���Ϊ�գ���һ���ϱ�
                        p.drawLine(base_l_x, base_y, base_l_x + self.CLIP_WIDTH, base_y)
                        p.drawLine(base_r_x, base_y, base_r_x + self.CLIP_WIDTH, base_y)
                    if row == len(self.result) - 1 or self.result[row + 1][col] == 0:
                        # ��������һ�У���������ĸ���Ϊ�գ���һ���±�
                        p.drawLine(base_l_x, base_y + self.CLIP_HEIGHT, base_l_x + self.CLIP_WIDTH, base_y + self.CLIP_HEIGHT)
                        p.drawLine(base_r_x, base_y + self.CLIP_HEIGHT, base_r_x + self.CLIP_WIDTH, base_y + self.CLIP_HEIGHT)
                    if col == 0 or self.result[row][col - 1] == 0:
                        # ����ǵ�һ�У�������ߵĸ���Ϊ�գ���һ�����
                        p.drawLine(base_l_x, base_y, base_l_x, base_y + self.CLIP_HEIGHT)
                        p.drawLine(base_r_x, base_y, base_r_x, base_y + self.CLIP_HEIGHT)
                    if col == len(self.result[0]) - 1 or self.result[row][col + 1] == 0:
                        # ����ǵ�һ�У������ұߵĸ���Ϊ�գ���һ���ұ�
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
        # �Ա�
        if self.stick_timer.isActive():
            self.FindAndShow()
        else:
            self.stick_timer.start()


    def ResetResult(self):
        # ���֮ǰ����Ľ��
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
            print "��Ϸ�����Сƥ�����"
            return

        self.pixmap = QPixmap(self.size())
        self.bgpixmap = QPixmap(self.width(), self.HEIGHT)
        self.bgpixmap.fill(QColor(0, 0, 255))
        self.label.setGeometry(0, self.ANCHOR_Y, self.width(), self.HEIGHT)
        self.label.setPixmap(self.bgpixmap)


    def FindAndShow(self):
        # ��ȡ��Ϸ��������
        self.my_visible = True
        self.DebugTime("init")

        ## �ü��õ����ҵ�����ͼƬ
        win32gui.ShowWindow(self.game_hwnd, win32con.SW_RESTORE)    # ǿ����ʾ�����źý�ͼ
        win32gui.SetForegroundWindow(self.game_hwnd)                # ����Ϸ�����ᵽ��ǰ
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
        self.DebugTime("��ͼ���")

 
        #�����Ҵ�ͼ�ü��ɶ��Сͼ�ֱ���жԱ�
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


        self.DebugTime("�Ա�")
        self.repaint()
        self.DebugTime("����")
       # print "----------------------"
       # for i in range(len(self.result)):        # Y��ѭ��
       #     for j in range(len(self.result[i])):    # X��ѭ��
       #         print self.result[i][j],
       #     print
       # print "----------------------"

    def compare(self, image_a, image_b):
        '''������ͼ�Ĳ���ֵ
        ������ͼ��������ֵ��ֱ�֮��'''
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
