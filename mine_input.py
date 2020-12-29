#!/usr/bin/python3
import pygame
import time, sys, os
import playsound as pls

import textinput
import mine_code as mc
import mine_sound as ms

white = (255,255,255)
black = (0,0,0)
red = (110,0,0)
deepred = (70,0,0)
lightred = (200,0,0)

baseDir = os.getcwd()
fontDir = os.path.join(baseDir, "mine_font")
soundDir = os.path.join(baseDir, "mine_sound")
effectMineDir = os.path.join(baseDir, "mine_effect/mine")
effectVoiceDir = os.path.join(baseDir, "mine_effect/voice")

mineFont=f'{fontDir}/SSShinb7.ttf'
#mineFont=f'{fontDir}/SangSangFlowerRoad.otf'
#mineFont=f'{fontDir}/NanumBrush.otf'
pygame.init()

screen_width = 200
screen_height = 100
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("setting Q")
clock = pygame.time.Clock()
TEXTFONT =  pygame.font.Font(mineFont,15)
questionList = ["Enter the number of rows","Enter the number of columns","Enter the number of mines","Game Start"]
#soundList = ["mine1","mine3","mine11","mine13", "mine12"]
def matrix_count():

    ti = textinput.TextInput()
    ti.text_color = lightred
    ti.font_family=mineFont
    ti.font_size=20

    count=0
    num=[2]*3
    running = True
    pls.playsound(f'{effectMineDir}/mine1.mp3', False)
    ms.play_msg(questionList[count])
    while running:

        screen.fill((black))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if ti.update(events):
            try:
                text = int(ti.get_text())
                num[count] = text
                ti.clear_text()
                if num[0] < 1:
                    pls.playsound(f'{effectMineDir}/mine2.mp3', False)
                    ms.play_msg("Please try again.")

                elif num[1] < 1:
                    pls.playsound(f'{effectMineDir}/mine2.mp3', False)
                    ms.play_msg("Please try again.")

                elif num[0] * num[1] <= num[2] or num[2] < 1:
                    pls.playsound(f'{effectMineDir}/mine2.mp3', False)
                    ms.play_msg("Please try again.")

                else:
                    count+=1

                    ms.play_msg(questionList[count])
                    if count == 3:
                        running = False

            except Exception as msg:
                ms.play_msg("Please try again.")
                ti.clear_text()

        screen.blit(ti.get_surface(), (10, 10))
        #left, top, width, height
        question_rect = pygame.Rect((0,screen_height//2.2),(screen_width,screen_height-(screen_height//1.8)))
        question = questionList[count]

        pygame.draw.rect(screen, lightred, question_rect)
        question_msg = TEXTFONT.render(question,True,black)
        question_msg_rect = question_msg.get_rect(center=(int(screen_width//2),int(screen_height//1.5)))
        screen.blit(question_msg,question_msg_rect)

        pygame.display.update()
        clock.tick(30)

    return mc.matrix_set(num[0],num[1],num[2])
