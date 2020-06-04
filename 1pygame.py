#导入pygame框架
#注意不要将文件命名为包同名文件  导致导入失败
import pygame
from pygame.locals import *
import sys
import time

def start():
    #初始化pygame
    pygame.init()

    #设置窗体大小
    window=pygame.display.set_mode(size=(400,400))

    #加载图标文件
    iconImage = pygame.image.load('./img/app.ico')
    #设置图标
    pygame.display.set_icon(iconImage)

    #背景音乐/只有一份
    pygame.mixer.music.load('./snd/bomb.wav')
    #音效/可以多份叠加
    s1 = pygame.mixer.Sound('./snd/bomb.wav')
    s2 = pygame.mixer.Sound('./snd/bg2.ogg')
    #字体
    font = pygame.font.Font("./font/happy.ttf", 42)
    #渲染文字
    txt = font.render('黑马程序员',True,(255,255,255))

    #加载图片
    heroImage=pygame.image.load('./img/hero2.png')
    #设置标题
    pygame.display.set_caption('飞机大战')
    x=200
    y=200
    #让程序不结束
    #界面开发 pyqt qt pygame 阻塞方式阻止界面结束
    while True:
        startTime = time.time()
        #每次开始前，需要涂成黑色背景
        window.fill((0,0,0))
        window.blit(txt,(100,100))
        window.blit(heroImage,(x,y))
        #刷新窗口
        pygame.display.flip()
        #点击x号 可停止程序
        eventList = pygame.event.get()


        for event in eventList:
            if event.type == QUIT:
                # print('点击了退出按钮')
                # pygame.quit()
                #退出界面
                pygame.quit()
                #python 程序退出
                sys.exit()
            elif event.type == KEYDOWN:
                #事件类型是键盘按下的事件
                #判断键盘值
                if event.key == K_a:
                    # print('点击了A')
                    x-=5
                elif event.key == K_d:
                    # print('点击了D')
                    x+=5
                elif event.key == K_RETURN:
                    #循环参数控制音乐播放的次数。播放(5)将使音乐播放一次，然后重复5次，总共是6次。
                    # pygame.mixer.music.play(loops=2)
                    s1.play(-1)
                    s2.play(-1)
                elif event.key == K_SPACE:
                    # pygame.mixer_music.stop()
                    s1.stop()
                    s2.stop()

        #降低fps  减小cpu消耗
        time.sleep(0.01)
        endTime = time.time()
        offsetTime = endTime-startTime
        try:
            fps = 1//offsetTime
            print(fps)
        except:
            pass
if __name__ == '__main__':
    start()
