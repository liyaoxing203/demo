import pygame
from pygame.locals import *
import sys

class Bullet:
    def __init__(self,window,ele):
        self.window = window
        self.image = pygame.image.load('./img/bullet_10.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        #相当于开始执行lambda表达式  lambda self.width,self.height :(self.__x+self.width/2-w/2,self.__y-h)
        #然后lambda表达式结果为元组  解包 赋值给self.x,self.y
        self.x,self.y=ele(self.width,self.height)
    def display(self):
        self.window.blit(self.image,(self.x,self.y))
    def move(self):
        self.y -= 5


class Plane:
    def __init__(self, x, y, window):
        self.__x = x
        self.__y = y
        self.window = window
        # 设置为控件
        self.image = pygame.image.load('./img/hero2.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.window_width = window.get_width()
        self.window_height = window.get_height()
        self.bullets = []

    def display(self):
        self.window.blit(self.image, (self.__x, self.__y))
        for bullet in self.bullets:
            bullet.display()
            bullet.move()

    def moveL(self):
        self.__x -= 5
        if self.__x < 0:
            self.__x = 0

    def moveR(self):
        self.__x += 5
        if self.__x > (self.window_width - self.width):
            self.__x = self.window_width - self.width

    def moveU(self):
        self.__y -= 5
        if self.__y < 0:
            self.__y = 0

    def moveD(self):
        self.__y += 5
        if self.__y > (self.window_height - self.height):
            self.__y = self.window_height - self.height

    def fire(self):
        bullet = Bullet(self.window,lambda w,h:(self.__x+self.width/2-w/2,self.__y-h))
        self.bullets.append(bullet)

def start():
    # 初始化pygame
    pygame.init()

    # 加载背景图片
    bgImage = pygame.image.load('./img/img_bg_level_1.jpg')
    WINDOW_WIDTH = bgImage.get_width()
    WINDOW_HEIGHT = bgImage.get_height()
    # 设置窗体大小
    window = pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT))

    # 设置标题
    pygame.display.set_caption('飞机大战')

    # 加载图标文件
    iconImage = pygame.image.load('./img/app.ico')
    pygame.display.set_icon(iconImage)

    heroPlane = Plane(200, 600, window)

    while True:
        # 背景图片
        window.blit(bgImage, (0, 0))
        heroPlane.display()
        # 刷新窗口
        pygame.display.flip()

        # 点击x号 可停止程序
        eventList = pygame.event.get()

        for event in eventList:
            if event.type == QUIT:
                # print('点击了退出按钮')
                # pygame.quit()
                # 退出界面
                pygame.quit()
                # python 程序退出
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_j:
                    heroPlane.fire()


        status = pygame.key.get_pressed()
        if 1 in status:
            if status[K_a]:
                heroPlane.moveL()
            elif status[K_d]:
                heroPlane.moveR()
            elif status[K_w]:
                heroPlane.moveU()
            elif status[K_s]:
                heroPlane.moveD()



if __name__ == '__main__':
    start()
