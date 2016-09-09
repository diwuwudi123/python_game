# -*- coding: utf-8 -*-
import pygame
from sys import exit
from pygame.locals import *
from gameRole import *
import random


# 初始化游戏
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, 600))
pygame.display.set_caption('飞机大战')

# 载入背景图
background = pygame.image.load('resources/image/background.png').convert()
game_over = pygame.image.load('resources/image/gameover.png')

filename = 'resources/image/shoot.png'
plane_img = pygame.image.load(filename)

# 设置玩家相关参数
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))        # 玩家精灵图片区域
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸精灵图片区域
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))

#初始化玩家位置
player_pos = [200, 600]
player = Player(plane_img, player_rect, player_pos)

# 定义子弹对象使用的surface相关参数
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# 定义敌机对象使用的surface相关参数
enemy_rect = pygame.Rect(534, 612, 57, 43)
enemy_img = plane_img.subsurface(enemy_rect)
enemy_down_imgs = []
enemy_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies = pygame.sprite.Group()

# 存储被击毁的飞机，用来渲染击毁精灵动画
enemies_down = pygame.sprite.Group()

shoot_frequency = 0
enemy_frequency = 0

player_down_index = 16

score = 0

clock = pygame.time.Clock()

font = pygame.font.Font('xingkai.ttf', 20)
while True:
    # 控制游戏最大帧率为60
    clock.tick(60)

    # 控制发射子弹频率,并发射子弹
    if not player.is_hit:
        if shoot_frequency % 15 == 0:
            player.shoot(bullet_img)
        shoot_frequency += 1
        if shoot_frequency >= 15:
            shoot_frequency = 0

    # 生成敌机
    if enemy_frequency % 50 == 0:
        enemy_pos = [random.randint(0, SCREEN_WIDTH - enemy_rect.width), 0]
        enemy = Enemy(enemy_img, enemy_down_imgs, enemy_pos)
        enemies.add(enemy)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0

    # 移动子弹，若超出窗口范围则删除
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    # 移动敌机，若超出窗口范围则删除
    for enemy in enemies:
        enemy.move()
        # 判断玩家是否被击中
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies.remove(enemy)
            player.is_hit = True
            break
        if enemy.rect.top > SCREEN_HEIGHT:
            enemies.remove(enemy)

    # 将被击中的敌机对象添加到击毁敌机Group中，用来渲染击毁动画
    enemies_down_list = pygame.sprite.groupcollide(enemies, player.bullets, 1, 1)
    for enemy_down in enemies_down_list:
        enemies_down.add(enemy_down)

    # 绘制背景
    screen.fill(0)
    screen.blit(background, (0, 0))

    # 绘制玩家飞机
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        # 更换图片索引使飞机有动画效果
        player.img_index = shoot_frequency // 8
    else:
        player.img_index = player_down_index // 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            #绘制gameover
            screen.blit(game_over, (0, 0))
            runing = pygame.event.wait()
            if runing.type == pygame.QUIT:
                exit()
    # 绘制击毁动画
    for enemy_down in enemies_down:
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    # 绘制子弹和敌机
    player.bullets.draw(screen)
    enemies.draw(screen)

    # 绘制得分
    text_content = font.render(u'你真厉害,你已经打下了'+str(score)+u'架飞机', True, (128, 128, 128))
    text_rect = text_content.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(text_content, (0,0))

    # 更新屏幕
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            
    # 监听键盘事件
    key_pressed = pygame.key.get_pressed()
    # 若玩家被击中，则无效
    if not player.is_hit:
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()