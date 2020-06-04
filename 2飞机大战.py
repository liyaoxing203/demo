import pygame
from pygame.locals import *
import sys
import random
class Enemy:
    def __init__(self,window):
        self.window = window
        self.window_height = self.window.get_height()
        self.window_width = self.window.get_width()

        self.__reset()
        # self.width = self.image.get_width()
        # self.height = self.image.get_height()
        # self.x=x
        # self.y=y
        # self.image = pygame.image.load('./img/img-plane_1.png')


    def display(self):
        self.window.blit(self.image,(self.x,self.y))
    def move(self):
        self.y+=2
        #判断是否越界 如果越界  重置
        if self.y>self.window_height:
            self.__reset()

    def __reset(self):
        self.image = pygame.image.load('./img/img-plane_{}.png'.format(random.randint(1,7)))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = random.randint(0,self.window_width-self.width)
        self.y = -random.randint(self.height,self.height*10)
    def recycle(self):
        self.__reset()

class Bullet:
    def __init__(self,x,y,window):
        self.window = window
        self.image = pygame.image.load('./img/bullet_10.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        #重新计算子弹位置
        self.x = x - self.width/2
        self.y = y - self.height
    def display(self):
        self.window.blit(self.image,(self.x,self.y))
    def move(self):
        self.y -= 5
    def needDestroy(self):
        return self.y<-self.height
    def hasCollision(self,enemy):
        #子弹矩形
        bulletRect = pygame.Rect(self.x,self.y,self.width,self.height)
        #飞机矩形
        enemyRect = pygame.Rect(enemy.x,enemy.y,enemy.width,enemy.height)
        return bulletRect.colliderect(enemyRect)


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
        self.__blood = 5

    def depressBlood(self):
        self.__blood-=1

    def display(self):
        # 判断是否需要销毁  需要倒序遍历才能删除干净列表
        for index in range(len(self.bullets)-1,-1,-1):
            if self.bullets[index].needDestroy():
                # self.bullets.pop(index)
                del self.bullets[index]

        # for ele in self.bullets:
        #     if ele.needDestory():
        #         self.bullets.remove(ele)
        # print('数量',len(self.bullets))
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
        bullet = Bullet(self.__x+self.width/2,self.__y,self.window)
        self.bullets.append(bullet)
    def hasCollision(self,enemy):
        #飞机矩形
        planeRect = pygame.Rect(self.__x,self.__y,self.width,self.height)
        #飞机矩形
        enemyRect = pygame.Rect(enemy.x,enemy.y,enemy.width,enemy.height)
        return planeRect.colliderect(enemyRect)
    def isGame(self):
        return self.__blood<=0

def start():
    # 初始化pygame
    pygame.init()

    # 加载背景图片
    bgImage = pygame.image.load('./img/img_bg_level_1.jpg')
    WINDOW_WIDTH = bgImage.get_width()
    WINDOW_HEIGHT = bgImage.get_height()
    # 设置窗体大小
    window = pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.mixer.music.load('./snd/bg2.ogg')
    #设置音效
    s1 = pygame.mixer.Sound('./snd/bomb.wav')
    s1.set_volume(10)
    s2 = pygame.mixer.Sound('./snd/bg2.ogg')
    s2.set_volume(2)
    # 设置标题
    pygame.display.set_caption('飞机大战')

    # 加载图标文件
    iconImage = pygame.image.load('./img/app.ico')
    pygame.display.set_icon(iconImage)

    heroPlane = Plane(200, 600, window)
    enemyList=[]
    for index in range(1,6):
        enemyList.append(Enemy(window))

    font = pygame.font.Font('./font/happy.ttf',50)
    overGame=font.render('游戏结束',True,(255,255,255))
    fontWidth=overGame.get_width()
    fontHeight=overGame.get_height()
    pygame.mixer.music.play()

    while True:
        #事件处理
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
        #检测游戏结束
        if heroPlane.isGame():
            window.blit(overGame,(WINDOW_WIDTH/2-fontWidth/2,WINDOW_HEIGHT/2-fontHeight/2))
            pygame.display.flip()
            continue
        for index in range(len(heroPlane.bullets)-1,-1,-1):
            bullet = heroPlane.bullets[index]
            for enemy in enemyList:
                #判断子弹是否和飞机相交
                if bullet.hasCollision(enemy):
                    del heroPlane.bullets[index]
                    s1.play()
                    #刷新飞机
                    enemy.recycle()
                    #停止循环
                    break
        for enemy in enemyList:
            if heroPlane.hasCollision(enemy):
                heroPlane.depressBlood()
                enemy.recycle()
                #发生循环跳出运行
                break

        # 背景图片
        window.blit(bgImage, (0, 0))
        heroPlane.display()
        #循环展示所有飞机
        for enemy in enemyList:
            enemy.display()
            enemy.move()

        # 刷新窗口
        pygame.display.flip()


            # elif event.type == KEYDOWN:
            #     #事件类型是键盘按下的事件
            #     #判断键盘值
            #     if event.key == K_a:
            #         heroPlane.moveL()
            #     elif event.key == K_d:
            #         heroPlane.moveR()
            #     elif event.key == K_w:
            #         heroPlane.moveU()
            #     elif event.key == K_s:
            #         heroPlane.moveD()


if __name__ == '__main__':
    start()
