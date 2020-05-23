import pygame, sys  # 声明 导入需要的模块

from pygame.locals import *

pygame.init()  # 初始化pygame

DISPLAYSURF = pygame.display.set_mode((400, 300))  # 设置窗口的大小，单位为像素

pygame.display.set_caption('Font')  # 设置窗口的标题

# 定义几个颜色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

fontObj = pygame.font.Font('ZKST.ttf', 48)  # 通过字体文件获得字体对象
textSurfaceObj = fontObj.render('Hello world!', True, (0,0,0))  # 配置要显示的文字
textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect
textRectObj.center = (200, 150)  # 设置显示对象的坐标

DISPLAYSURF.fill(WHITE)  # 设置背景

DISPLAYSURF.blit(textSurfaceObj, textRectObj)  # 绘制字体

while True:  # 程序主循环

    for event in pygame.event.get():  # 获取事件

        if event.type == QUIT:  # 判断事件是否为退出事件

            pygame.quit()  # 退出pygame

            sys.exit()  # 退出系统

    pygame.display.update()  # 绘制屏幕内容
