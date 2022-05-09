#導入模組
import pygame
import math
import time
import random
import numpy as np
import os
import sys
import json
import tkinter

# 讀取json檔
with open('data.json', "r", encoding="utf8") as file:
    data = json.load(file)

#變數設定
fps = data['fps']                           #每秒執行多少次
probability = data['probability']           #生成機率
width = data['width']                       #視窗寬度
height = data['height']                     #視窗高度
block_count = data['block_count']           #視窗邊的方塊數量
if block_count<=0:                          #數字校正
    block_count=10
space_size = width//block_count             #區塊大小
x_block = width//space_size                 #計算寬有多少格
y_block = height//space_size                #計算高有多少格
execute = True                              #執行
run = False                                 #是否運行中
global life_cycle                           #生命週期
life_cycle = 0
message = "Life cycle:" + str(life_cycle)   #遊戲資訊
#細胞存活狀態設定
cell_state = np.ndarray(shape=(9,1))
cell_state = data['cell_state']
for number in range(0,8):
    if cell_state[number]<-1 or cell_state[number]>1:
        cell_state[number] = 0

#介面與初始設定
pygame.init()
conway = pygame.display.set_mode((width,height+50))
pygame.display.set_caption('康威生命遊戲')
#圖片導入
icon = pygame.image.load("img/icon.png")
icon.set_colorkey((255,255,255))
#設定icon
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
conway.fill(data['color_background'])


#區塊分區與座標設定
space_x_count = math.ceil(width/space_size)
space_y_count = math.ceil(height/space_size)
space_data = np.ndarray(shape=(space_x_count,space_y_count))
for x in range(0,space_x_count):
    for y in range(0,space_y_count):
        space_data[x][y] = False
#暫存區
storage_cache = np.ndarray(shape=(space_x_count,space_y_count))
for x in range(0,space_x_count):
    for y in range(0,space_y_count):
        storage_cache[x][y] = 0


#滑鼠點擊偵測(設置)
def mouse_click_event_setting(mouseX,mouseY):
    block_x_choose = mouseX//space_size
    block_y_choose = mouseY//space_size
    pygame.draw.rect(surface=conway, color=data['cell_color'], rect=((block_x_choose*space_size, block_y_choose*space_size),(space_size,space_size)))
    space_data[block_x_choose][block_y_choose]=True

#滑鼠點擊偵測(移除)
def mouse_click_event_remove(mouseX,mouseY):
    block_x_choose = mouseX//space_size
    block_y_choose = mouseY//space_size
    pygame.draw.rect(surface=conway, color=data['color_background'], rect=((block_x_choose*space_size, block_y_choose*space_size),(space_size,space_size)))
    space_data[block_x_choose][block_y_choose]=False

#細胞變化控制
def cell():
    for i in range(0,space_x_count):
        for j in range(0,space_y_count):
            cell_count = 0
            #座標校正
            if i+1 > space_x_count-1:
                i_up = i
            else:
                i_up = i+1
            if i-1 < 0:
                i_down = i
            else:
                i_down = i-1
                        
            if j+1 > space_y_count-1:
                j_up = j
            else:
                j_up = j+1
            if j-1 < 0:
                j_down = j
            else:
                j_down = j-1
            #偵測周圍
            if i_up != i and space_data[i_up][j]==True:
                cell_count+=1
            if i_down != i and space_data[i_down][j]==True:
                cell_count+=1

            if j_up != j and space_data[i][j_up]==True:
                cell_count+=1
            if j_down != j and space_data[i][j_down]==True:
                cell_count+=1

            if i_up != i and j_up != j and space_data[i_up][j_up]==True:
                cell_count+=1
            if i_down != i and j_down != j and space_data[i_down][j_down]==True:
                cell_count+=1

            if i_up != i and j_down != j and space_data[i_up][j_down]==True:
                cell_count+=1
            if i_down != i and j_up != j and space_data[i_down][j_up]==True:
                cell_count+=1
            storage_cache[i][j] = cell_state[cell_count]

#隨機
def random_number():
    for x in range(0,space_x_count):
            for y in range(0,space_y_count):
                number = math.ceil(random.random()*100)
                if number <= probability:
                    space_data[x][y] = True
                else:
                    space_data[x][y] = False
    #細胞狀態
    for i in range(0,space_x_count):
        for j in range(0,space_y_count):
            if space_data[i][j]==True:
                pygame.draw.rect(surface=conway, color=data['cell_color'], rect=((i*space_size, j*space_size),(space_size,space_size)))
            elif space_data[i][j]==False:
                pygame.draw.rect(surface=conway, color=data['color_background'], rect=((i*space_size, j*space_size),(space_size,space_size)))
    #更新畫面
    pygame.display.update()
    
#清除
def clear():
    for x in range(0,space_x_count):
            for y in range(0,space_y_count):
                space_data[x][y] = False
    #細胞狀態
    for i in range(0,space_x_count):
        for j in range(0,space_y_count):
            if space_data[i][j]==True:
                pygame.draw.rect(surface=conway, color=data['cell_color'], rect=((i*space_size, j*space_size),(space_size,space_size)))
            elif space_data[i][j]==False:
                pygame.draw.rect(surface=conway, color=data['color_background'], rect=((i*space_size, j*space_size),(space_size,space_size)))
    font = pygame.font.SysFont('freesansbold.ttf',30)
    global life_cycle
    life_cycle = 0
    #更新畫面
    pygame.display.update()


   
#遊戲執行
while execute:
    clock.tick(fps)
    #遊戲資訊
    font = pygame.font.SysFont('freesansbold.ttf',30)
    text = font.render(message, True, (255,0,0),data['color_background'])
    text_display = text.get_rect()
    text_display.center=(width/2,height+25)
    message = "Life cycle: " + str(life_cycle)
    pygame.draw.rect(conway,data['color_background'],[0,height+1,width,height+50])
    conway.blit(text,text_display)
    #按鍵偵測
    for event in pygame.event.get():
        #離開遊戲
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        #滑鼠偵測
        if event.type == pygame.MOUSEMOTION:
            #偵測滑鼠按下
            mouse_click_type = pygame.mouse.get_pressed()
            if mouse_click_type[0]:
                mouseX,mouseY = pygame.mouse.get_pos()
                if mouseX <= width and mouseY < height and mouseX >= 0 and mouseY >= 0:
                    mouse_click_event_setting(mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #偵測滑鼠按下
            mouse_click_type = pygame.mouse.get_pressed()
            if mouse_click_type[0]:
                mouseX,mouseY = pygame.mouse.get_pos()
                if mouseX <= width and mouseY < height and mouseX >= 0 and mouseY >= 0:
                    mouse_click_event_setting(mouseX, mouseY)
        if event.type == pygame.MOUSEMOTION:
            #偵測滑鼠按下
            mouse_click_type = pygame.mouse.get_pressed()
            if mouse_click_type[2]:
                mouseX,mouseY = pygame.mouse.get_pos()
                if mouseX <= width and mouseY < height and mouseX >= 0 and mouseY >= 0:
                    mouse_click_event_remove(mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #偵測滑鼠按下
            mouse_click_type = pygame.mouse.get_pressed()
            if mouse_click_type[2]:
                mouseX,mouseY = pygame.mouse.get_pos()
                if mouseX <= width and mouseY < height and mouseX >= 0 and mouseY >= 0:
                    mouse_click_event_remove(mouseX, mouseY)
        #鍵盤偵測
        if event.type == pygame.KEYDOWN:
            #離開遊戲
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                break
            #執行隨機生成
            if event.key == pygame.K_TAB:
                run = False
                random_number()
                #執行隨機生成
            if event.key == pygame.K_DELETE:
                run = False
                clear()
            #控制是否要運行
            if event.key == pygame.K_SPACE:
                run = not run
    #細胞演化
    if run == True:
        cell()
        #細胞狀態
        for i in range(0,space_x_count):
            for j in range(0,space_y_count):
                if storage_cache[i][j]==-1:
                    pygame.draw.rect(surface=conway, color=data['color_background'], rect=((i*space_size, j*space_size),(space_size,space_size)))
                    space_data[i][j]=False
                elif storage_cache[i][j]==1:
                    pygame.draw.rect(surface=conway, color=data['cell_color'], rect=((i*space_size, j*space_size),(space_size,space_size)))
                    space_data[i][j]=True
        life_cycle+=1
    #畫格子
    for line in range(0,width+1,space_size):
        pygame.draw.line(conway , data['line_color'], (line,0), (line,height))
    for line in range(0,height+1,space_size):
        pygame.draw.line(conway , data['line_color'], (0,line), (width,line))
    #更新畫面
    pygame.display.update()