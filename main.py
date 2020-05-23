import matplotlib.pyplot as plt
import pygame
import pygame.draw as draw
import math
from time import sleep

pygame.init()  # 初始化
display = pygame.display
screen = display.set_mode((640, 480), 0, 32)
display.set_caption("物理: 弹簧实验")

fontObj = pygame.font.Font('ZKST.ttf', 48)  # 通过字体文件获得字体对象
fontObj2 = pygame.font.Font('ZKST.ttf', 20)  # 通过字体文件获得字体对象
text_M = fontObj.render('M', True, (100, 255, 255))  # 配置要显示的文字

v_list = []  # v-t图像的v
t_list = []  # v-t图像和s-t图像的t
s_list = []  # s-t图像的s
dh_list = []  # dh-t图像的dh
a_list = []  # a-t图像的a

g = 9.8  # 重力加速度
k = 0.4  # 弹簧劲度系数
v = 0  # 物体速度
m = 1  # 物体质量
F = 0  # 物体受力
h = 0  # 物体距离原来高度位置(弹簧伸缩量)
gh = 8  # 距离弹簧对高度
times = 0

get_g = lambda m: g * m  # 获取重力(重力方向为正方向)
get_n = lambda h: 0 if h < gh else k * (h - gh)  # 计算弹力
get_f = lambda f1, f2: f1 + f2  # 计算力

get_a = lambda f, m: f / m  # 计算加速度
get_v = lambda v, a, t: v + a * t  # 计算速度
get_s = lambda v, a, t: v * t + 0.5 * a * t ** 2  # 计算位移

to_ypos = lambda y: int((y / 100) * 470 + 30) # 100是虚拟环境的高度，470是画布高度, 10是向下偏移

time = 0.001
now_draw = 0

def sin():  # get sin
    a = 0
    for i in range(100):
        yield math.sin(a), a
        a += 1


def draw_font(x, y, text, screen):
    tmp_text = fontObj2.render(text, True, (0, 0, 0))  # 配置要显示的文字
    tmp = tmp_text.get_rect()  # 获得要显示的对象的rect
    tmp.center = (x, y)  # 设置显示对象的坐标
    screen.blit(tmp_text, tmp)  # 绘制字体


def draw_(screen, display, h, v, a, n, mg, f, time):  # 绘制受力分析图
    mh = 50
    mw = 60

    # 清空
    screen.fill((255, 255, 255))

    pygame.draw.line(screen, (0, 0, 0), (0, to_ypos(0)), (640, to_ypos(0)), 2)  # 绘制最高线h

    pygame.draw.line(screen, (0, 0, 0), (0, to_ypos(h)), (640, to_ypos(h)), 1)  # 绘制物体高度线:h

    draw_font(590, to_ypos(h) + 12, f'h = {h:4.2f}m', screen)
    draw_font(640 // 2, to_ypos(h) - 12, f'v = {v:4.2f}m/s, a = {a:4.2f}m/s^2', screen)

    pygame.draw.rect(screen, (0, 0, 0), (int(640 / 2 - mw / 2), to_ypos(h), mw, mh), 0)
    tmp = text_M.get_rect()  # 获得要显示的对象的rect
    tmp.center = (640 // 2, to_ypos(h) + mh // 2)  # 设置显示对象的坐标
    screen.blit(text_M, tmp)  # 绘制字体

    if h > gh:
        max_h = h
    else:
        max_h = gh
    point_list = []
    for i in sin():
        x = int(i[0] / 2 * mw / 2 + (640 / 2 - 10) + mw / 8) # 换算,  + mw / 8是让弹簧居中
        y = int(i[1] / 100 * (400 - to_ypos(max_h) - mh) + to_ypos(max_h) + mh)  # 换算
        point_list.append((x,y))

    pygame.draw.lines(screen, (min(max_h / 60 * 255, 255), 0, 0), False, point_list, 2)  # 绘制最高线h

    x = 60
    base_y = 270
    pygame.draw.circle(screen, (0,0,255), (x, base_y), 5)

    y = int(base_y + (mg / 20 * 150))
    pygame.draw.line(screen, (0, 0, 0), (x, base_y), (x, y), 3)  # 绘制mg
    pygame.draw.lines(screen, (0, 0, 0), False, [(x-5,y-5), (x,y), (x+5,y-5)], 3)

    draw_font(x, y + 12, f'mg = {mg:4.2f}N', screen)


    if n < 0:
        y = int(base_y + (n / 20 * 150))
        pygame.draw.line(screen, (0, 0, 0), (x, base_y), (x, y), 3)  # 绘制n
        pygame.draw.lines(screen, (0, 0, 0), False, [(x - 5, y + 5), (x, y), (x + 5, y + 5)], 3)
        draw_font(x, y - 12, f'N = {-n:4.2f}N', screen)
    else:
        draw_font(x, base_y - 12, f'N = 0N', screen)

    y = int(base_y + (f / 20 * 150))
    pygame.draw.line(screen, (250, 0, 0), (x, base_y), (x, base_y + int(f / 20 * 150)), 3)  # 绘制最高线h
    pygame.draw.lines(screen, (0, 0, 0), False, [(x - 5, (y + 5) if f < 0 else (y - 5)), (x, y),
                                                 (x + 5, (y + 5) if f < 0 else (y - 5))], 3)
    draw_font(x + x, y - 5, f'F = {f:4.2f}N', screen)

    draw_font(320, 440 - 12, f'time = {time:4.2f}s, g = {g}m/s^2, m(M) = {m}kg, k = {k}', screen)
    draw_font(320, 460 - 12, f'power by SuperHuan (https://www.songzh.website)', screen)
    display.update()
    # pygame.draw.rect(screen, (0, 0, 0), (5, a, 50, 50), 0)


def is_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            get_new()
    return True


def get_new():  # 获取新的数据
    try:
        type = int(input('''1)重力加速度g
2)劲度系数k
3)M的质量
Please Enter The Number: '''))
        n = int(input("Please Enter The New Value: "))
    except ValueError:
        return False

    if type == 1:
        global g
        g = n
    elif type == 2:
        global k
        k = n
    elif type == 3:
        global m
        m = n
    return True


if __name__ == "__main__":
    try:
        while is_quit():
            the_g = get_g(m)
            the_n = -get_n(h)  # 重力方向为正方向
            the_f = get_f(the_n, the_g)
            the_a = get_a(the_f, m)  # 获取当前的加速度

            times += time
            dh = get_s(v, the_a, time)  # 计算位移增量
            new_v = get_v(v, the_a, time)

            # print(f"h = {h}, dh = {dh}, h + dh = {h + dh}, a = {the_a}, v = {v}, n = {the_n}, time = {times}s, count = {i}")
            if now_draw == 30:
                draw_(screen, display, h, v, the_a, the_n, the_g, the_f, times)
                now_draw = 0
            else:
                sleep(time)
                now_draw += 1
            v_list.append(v)
            s_list.append(dh + h)
            dh_list.append(dh)
            t_list.append(times)
            a_list.append(the_a)

            v = new_v
            h += dh

        plt.figure()
        size = (3,2)
        dh_t = plt.subplot2grid(size, (0, 0), colspan=1, rowspan=1)
        s_t = plt.subplot2grid(size, (0, 1), colspan=1, rowspan=1)
        v_t = plt.subplot2grid(size, (1, 0), colspan=2, rowspan=1)
        a_t = plt.subplot2grid(size, (2, 0), colspan=2, rowspan=1)

        def set_plot(plot, title, ylabel, xlabel, line, y_list, x_list):
            plot.set_title(title)
            plot.set_ylabel(ylabel)
            plot.set_xlabel(xlabel)
            plot.plot(x_list, y_list, line, label=title)


        set_plot(v_t, 'v-t', 'v(m/s)', 't(s)', 'r', v_list, t_list)
        set_plot(s_t, 'h-t', 'h(m)', 't(s)', 'b', s_list, t_list)
        set_plot(dh_t, f'dh-t(dt = {time}s)', 'dh(m)', 't(s)', 'y', dh_list, t_list)
        set_plot(a_t, 'a-t', 'a(m/s^2)', 't(s)', 'g', a_list, t_list)

        v_t.grid()
        s_t.grid()
        dh_t.grid()
        a_t.grid()
        plt.show()
    except KeyboardInterrupt:
        pass
    print("Bye Bye(power by SuperHuan)!")