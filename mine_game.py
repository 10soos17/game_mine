#!/usr/bin/python3
import pygame
import pyaudio, wave
import playsound as pls

import os, sys, time
import random
import threading

import textinput
import mine_input as mi
import mine_sound as ms

white = (255,255,255)
black = (0,0,0)
red = (110,0,0)
deepred = (70,0,0)
lightred = (200,0,0)

baseDir = os.getcwd()
imgDir = os.path.join(baseDir,"mine_imgs/NanumBrush") #이미지 폴더 위치 반환
fontDir = os.path.join(baseDir, "mine_font")
soundDir = os.path.join(baseDir, "mine_sound")
effectMineDir = os.path.join(baseDir, "mine_effect/mine")
effectVoiceDir = os.path.join(baseDir, "mine_effect/voice")

mineFont=f'{fontDir}/SSShinb7.ttf'
song = f'{soundDir}/Examine_Spider Man.wav'
replay = 'loop'
#mineFont=f'{fontDir}/SangSangFlowerRoad.otf'
#mineFont=f'{fontDir}/NanumBrush.otf'
#############################get mine_code values###############################
x, y, mine, matrix = mi.matrix_count()
##############################screen size setting###############################
score_bar = 50
frame_gap = 1  # space between two mines
screen_width = (y * 20) + (frame_gap * (y+1))
screen_height = (x * 20) + (frame_gap * (x+1)) + score_bar

def main():
    global CLOCK, STARTCLOCK, GAMEFONT, TEXTFONT, SCOREFONT,SCREEN # global variables

    pygame.init()
    #======================================================== title setting ====
    SCREEN = pygame.display.set_mode((screen_width,screen_height))
    screen_back = pygame.Rect((0, 0), (screen_width, screen_height))
    pygame.draw.rect(SCREEN, deepred, screen_back)
    pygame.display.set_caption("Mine Game")
    #============================================================game font =====
    SCOREFONT = pygame.font.Font(mineFont,25)
    GAMEFONT = pygame.font.Font(mineFont,30)
    TEXTFONT =  pygame.font.Font(mineFont,20)
    #================================================================== FPS ====
    STARTCLOCK = pygame.time.get_ticks() #get start time
    CLOCK = pygame.time.Clock()

    runGame()

##################################### Game #####################################
def runGame():
    mineFrame_width, mineFrame_height,mineFrame, hide_images, mines, yes_check = MineFrame.image_setting()
    mines = MineFrame.firstScreen(mineFrame_width, mineFrame_height,mineFrame, hide_images, mines, yes_check)

    yes_count = 0
    correct_count = 0
    openArray = []
    yesArray = []

    LEFT = 1
    RIGHT = 3
    running = True

    th = threading.Thread(target=ms.play_sound, args=(song,replay), daemon=True)
    th.start()

    while running:

        dt = CLOCK.tick(30) #게임화면의 초당프레임수 설정
        event = pygame.event.poll()

        if event.type == pygame.QUIT: # click exit window button
            quit()
        #=============================================== mouse click event =====
        # click & left
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT :
            print("You released the left mouse button at ({}, {})".format(*event.pos))

        # release & left : show hide_images, change to hide_images, decrease yes_count & show yes_count
        elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT :
            get_x = event.pos[0] # clicked x coordinate
            get_y = event.pos[1] # clicked y coordinate

            temp_x = (get_x)// mineFrame_width  # 좌표에 해당하는 mines list 인덱스 값 찾는 과정
            get_mine_col = (get_x -(temp_x * frame_gap))// mineFrame_width

            temp_y = (get_y) // mineFrame_height
            get_mine_row = (get_y - score_bar - (temp_y * frame_gap)) // mineFrame_height

            get_img = mines[get_mine_row][get_mine_col]["hide_imgs"] # get values
            put_x = mines[get_mine_row][get_mine_col]["pos_x"]
            put_y = mines[get_mine_row][get_mine_col]["pos_y"]

            # 스코어 바 제외한 부분 클릭 시, 화면 변화 적용
            if get_y > score_bar and mines[get_mine_row][get_mine_col] not in yesArray :
                SCREEN.blit(hide_images[get_img],(put_x,put_y))

                openArray.append(mines[get_mine_row][get_mine_col])

                MineFrame.openRange(get_mine_row, get_mine_col, mines, hide_images, yesArray, openArray)
                MineFrame.openRangeSec(get_mine_row, get_mine_col, mines, hide_images, yesArray, openArray)
                MineFrame.openRangeThird(get_mine_row, get_mine_col, mines, hide_images, yesArray, openArray)

            # 클릭 값이 지뢰인 경우, 글자 표시 및  게임 종료
            if mines[get_mine_row][get_mine_col]["hide_imgs"] == 9 and mines[get_mine_row][get_mine_col] not in yesArray:
                game_result = "Mission Failure"
                ms.play_msg(game_result)
                running = False

            # 깃발 표시했던 부분 클릭 시, yes_count 감소(yesArray 에 있는 지 여부로 체크) & 지뢰였을 경우 correct_count 감소
            if mines[get_mine_row][get_mine_col] in yesArray :
                SCREEN.blit(mineFrame,(put_x,put_y))
                yesArray.remove(mines[get_mine_row][get_mine_col])
                yes_count -= 1
                if mines[get_mine_row][get_mine_col]["hide_imgs"] == 9 :
                    correct_count -= 1

            print("You pressed the left mouse button at ({}, {}) and yes: {},correct: {}.".format(get_x,get_y,yes_count,correct_count))

        # click & left :
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT :
            print("You released the right mouse button at ({}, {})".format(*event.pos))

        #release & right : yes(깃발)이미지로 변, yesArray 저장, yes_count 증가 및 화면 표시
        elif event.type == pygame.MOUSEBUTTONUP and event.button == RIGHT :
            get_x = event.pos[0] #클릭된 x좌표 값
            get_y = event.pos[1] #클릭된 y좌표 값


            temp_x = (get_x)// mineFrame_width# 좌표에 해당하는 mines list 인덱스 값 찾는 과정

            get_mine_col = (get_x -(temp_x * frame_gap))// mineFrame_width
            temp_y = (get_y) // mineFrame_height
            get_mine_row = (get_y - score_bar - (temp_y * frame_gap)) // mineFrame_height

            put_x = mines[get_mine_row][get_mine_col]["pos_x"] # 해당 값 얻어오기
            put_y = mines[get_mine_row][get_mine_col]["pos_y"]

            if yes_count < mine and mines[get_mine_row][get_mine_col] not in yesArray and mines[get_mine_row][get_mine_col] not in openArray: #깃발 수 < 지뢰 경우, yes(깃발) 화면에 표시,yes_count 증가
                SCREEN.blit(yes_check,(put_x,put_y))
                yes_count +=1
                if mines[get_mine_row][get_mine_col]["hide_imgs"] == 9: # 깃발 표시 값이 지뢰인 경우, correct_count 증가시킴
                    correct_count +=1
                    if correct_count == mine: # 깃발 표시 값이 지뢰이며 correct_count 값 = 지뢰수이면, 성공 메시지 & 게임 종료
                        game_result = "Mission Complete"
                        ms.play_msg(game_result)
                        running = False
            elif yes_count == mine: # yes_count 가 지뢰 수 같으면(깃발 표시한 것 중에 지뢰 아닌 것이 포함된 경우임), 안내 문구 표시
                game_result = "No flags left"
                ms.play_msg(game_result)
                print("limit")

            yesArray.append(mines[get_mine_row][get_mine_col]) #yesArray 에 해당 mines값 저장

            print("You pressed the left mouse button at ({}, {}) and yes: {},correct: {}.".format(get_x,get_y,yes_count,correct_count))
        #======================================================= time count ====
        elapsed_time, total_time = MineFrame.draw_bar_time(yes_count)
        pygame.display.update()
        #시간 초과했다면, 메시지 표시, 게임 종료
        if total_time - elapsed_time <= 0:
            game_result = "Time Over"
            ms.play_msg(game_result)

            running = False

    #============================================================ restart? =====
    if correct_count == mine: #마지막 지뢰 찾기 성공 시, 루프 벗어나기에. 루프 밖에서 마지막 깃발 표시 후 종료.
        SCREEN.blit(yes_check,(put_x,put_y))
        pygame.time.delay(2000)

    MineFrame.answer_set(mines)
    MineFrame.popup_restart(game_result)
#============================================================== game exit ======
def quit():
    #========================================================== 2sec sleep =====
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()


class MineFrame():
    #========================================================= back screen =====
    def draw_screen():
        screen_back = pygame.Rect((0, 0), (screen_width, screen_height))
        pygame.draw.rect(SCREEN, deepred, screen_back)
    #======================================================== score & time =====
    def draw_bar_time(yes_count):
        total_time = 1000 # time limit
        setting_back = pygame.Rect((0, 0), (screen_width, score_bar)) # bar location
        pygame.draw.rect(SCREEN, black, setting_back) # bar setting
        elapsed_time = (pygame.time.get_ticks() - STARTCLOCK) / 1000 # ms -> s
        timer = SCOREFONT.render(" Time: {} Flag: {}".format(int(total_time - elapsed_time),int(yes_count)),True,lightred)
        SCREEN.blit(timer,(0,0))

        return elapsed_time, total_time

    #========================================================== image load =====
    def image_setting():
        mineFrame = pygame.image.load(os.path.join(imgDir,"mine_frame.png")) # 프레임
        yes_check = pygame.image.load(os.path.join(imgDir,"yes.png")) # 깃발

        hide_images=[  # 클릭 시 보여 줄 이미지 저장(matrix 값(근처지뢰수) = hide_images indext번호)
            pygame.image.load(os.path.join(imgDir,"nothing.png")), # 0(근처지뢰수) = hide_images[0] = nothing img
            pygame.image.load(os.path.join(imgDir,"one.png")), # 1 = hide_images[1] = one img
            pygame.image.load(os.path.join(imgDir,"two.png")), # 2 = hide_images[2] = two img
            pygame.image.load(os.path.join(imgDir,"three.png")), # 3 = hide_images[3] = three img
            pygame.image.load(os.path.join(imgDir,"four.png")), # 4 = hide_images[4] = four img
            pygame.image.load(os.path.join(imgDir,"five.png")), # 5 = hide_images[5] = five img
            pygame.image.load(os.path.join(imgDir,"six.png")), # 6 = hide_images[6] = six img
            pygame.image.load(os.path.join(imgDir,"seven.png")), # 7 = hide_images[7] = seven img
            pygame.image.load(os.path.join(imgDir,"eight.png")), # 8 = hide_images[8] = eight img
            pygame.image.load(os.path.join(imgDir,"no.png")) # 9(지뢰를 의미) = hide_images[9] = no img
            ]

        mineFrame_size = mineFrame.get_rect().size #프레임 넓이, 높이 얻기
        mineFrame_width = mineFrame_size[0]
        mineFrame_height = mineFrame_size[1]

        mines=[[0]*y for i in range(x)]

        return mineFrame_width, mineFrame_height,mineFrame, hide_images, mines, yes_check

    #===================================== mine frame start screen setting =====
    def firstScreen(mineFrame_width, mineFrame_height,mineFrame, hide_images, mines, yes_check):
        a=0
        b=0
        mine_x = frame_gap
        mine_y = score_bar + frame_gap
        for i in range(x):
            for j in matrix[a]:
                matrix_val = int(matrix[a][b]) # matrix에 저장된 값 불러오기
                mines[a][b]={ #mines list 에 이미지 설정할 x,y 위치,matrix row,col idx 값, 불러올 hide_images 인덱스번호 저장
                        "pos_x" : mine_x,
                        "pos_y" : mine_y,
                        "idx_row":a,
                        "idx_col":b,
                        "hide_imgs": matrix_val,
                        "hide_imgs_set": hide_images[matrix_val],
                        }
                SCREEN.blit(mineFrame,(mines[a][b]["pos_x"],mines[a][b]["pos_y"])) # 화면에 그리기
                mine_x += mineFrame_width + frame_gap # col증가할 때마다, x 위치 (프레임 넓이 + 간격만큼) 더하기
                b+=1
            mine_x = frame_gap # row 변경 시, x 위치 초기값으로 바꾸기
            mine_y += mineFrame_height + frame_gap # row 증가할 때마다, y 위치 (프레임 높이 + 간격만큼) 더하기
            a+=1
            b=0

        return mines
    #======================================================= answer screen =====
    def answer_set(mines):
        for i in range(len(mines)):
            for j in range(len(mines[i])):
                SCREEN.blit(mines[i][j]["hide_imgs_set"],(mines[i][j]["pos_x"],mines[i][j]["pos_y"])) # 화면에 그리기

        return mines

    #========================================================== open range =====
    def openRange(get_mine_row, get_mine_col, mines, hide_images, yesArray, openArray):
        #"hide_imgs": matrix_val,
        #"hide_imgs_set": hide_images[matrix_val]
        temp_row = get_mine_row
        temp_col = get_mine_col
        range = min(x,y)//15 + 2

        #range = 3
        count = 0
        while temp_row > 0 and count != range :#-1
            temp_row -= 1
            range_get_img = mines[temp_row][temp_col]["hide_imgs"] # get values
            range_put_x = mines[temp_row][temp_col]["pos_x"]
            range_put_y = mines[temp_row][temp_col]["pos_y"]
            if range_get_img == 0 and mines[temp_row][temp_col] not in openArray and mines[temp_row][temp_col] not in yesArray:
                openArray.append(mines[temp_row][temp_col])
                SCREEN.blit(hide_images[range_get_img],(range_put_x,range_put_y))
            else:
                break
            count +=1

        count = 0
        temp_row = get_mine_row

        while temp_row < len(mines)-2 and count != range :#+1
            temp_row += 1
            range_get_img = mines[temp_row][temp_col]["hide_imgs"] # get values
            range_put_x = mines[temp_row][temp_col]["pos_x"]
            range_put_y = mines[temp_row][temp_col]["pos_y"]
            if range_get_img == 0 and mines[temp_row][temp_col] not in openArray and mines[temp_row][temp_col] not in yesArray:
                openArray.append(mines[temp_row][temp_col])
                SCREEN.blit(hide_images[range_get_img],(range_put_x,range_put_y))
            else:
                break
            count +=1

        count = 0
        temp_row = get_mine_row


        while temp_col > 0 and count != range :#-1
            temp_col -= 1
            range_get_img = mines[temp_row][temp_col]["hide_imgs"] # get values
            range_put_x = mines[temp_row][temp_col]["pos_x"]
            range_put_y = mines[temp_row][temp_col]["pos_y"]

            if range_get_img == 0 and mines[temp_row][temp_col] not in openArray and mines[temp_row][temp_col] not in yesArray:
                openArray.append(mines[temp_row][temp_col])
                SCREEN.blit(hide_images[range_get_img],(range_put_x,range_put_y))
            else:
                break
            count +=1

        temp_col = get_mine_col
    #===============================open range_sec
    def openRangeSec(get_mine_row, get_mine_col, mines, hide_images, yesArray, openArray):
        #"hide_imgs": matrix_val,
        #"hide_imgs_set": hide_images[matrix_val]
        temp_row = get_mine_row
        temp_col = get_mine_col
        range = min(x,y)//15 + 1
        #range = 2
        count = 0
        while temp_row > 0 and temp_col > 0 and count != range :#-1
            temp_row -= 1
            temp_col -= 1
            range_get_img = mines[temp_row][temp_col]["hide_imgs"] # get values
            range_put_x = mines[temp_row][temp_col]["pos_x"]
            range_put_y = mines[temp_row][temp_col]["pos_y"]
            if range_get_img == 0 and mines[temp_row][temp_col] not in openArray and mines[temp_row][temp_col] not in yesArray:
                openArray.append(mines[temp_row][temp_col])
                SCREEN.blit(hide_images[range_get_img],(range_put_x,range_put_y))
            else:
                break
            count +=1

        count = 0
        temp_row = get_mine_row
        temp_col = get_mine_col

        while temp_row < len(mines)-2 and temp_col < len(mines[0])-2 and count != range :#+1
            temp_row += 1
            temp_col += 1
            range_get_img = mines[temp_row][temp_col]["hide_imgs"] # get values
            range_put_x = mines[temp_row][temp_col]["pos_x"]
            range_put_y = mines[temp_row][temp_col]["pos_y"]
            if range_get_img == 0 and mines[temp_row][temp_col] not in openArray and mines[temp_row][temp_col] not in yesArray:
                openArray.append(mines[temp_row][temp_col])
                SCREEN.blit(hide_images[range_get_img],(range_put_x,range_put_y))
            else:
                break
            count +=1

    #===============================open range_third
    def openRangeThird(get_mine_row, get_mine_col, mines, hide_images, yesArray, openArray):
        #"hide_imgs": matrix_val,
        #"hide_imgs_set": hide_images[matrix_val]
        temp_row = get_mine_row
        temp_col = get_mine_col
        range = min(x,y)//15 + 1
        #range = 2
        count = 0
        while temp_row > 0 and temp_col < len(mines[0])-2 and count != range :#-1
            temp_row -= 1
            temp_col += 1
            range_get_img = mines[temp_row][temp_col]["hide_imgs"] # get values
            range_put_x = mines[temp_row][temp_col]["pos_x"]
            range_put_y = mines[temp_row][temp_col]["pos_y"]
            if range_get_img == 0 and mines[temp_row][temp_col] not in openArray and mines[temp_row][temp_col] not in yesArray:
                openArray.append(mines[temp_row][temp_col])
                SCREEN.blit(hide_images[range_get_img],(range_put_x,range_put_y))
            else:
                break
            count +=1

        count = 0
        temp_row = get_mine_row
        temp_col = get_mine_col

        while temp_row < len(mines)-2 and temp_col > 0 and count != range :#+1
            temp_row += 1
            temp_col -= 1
            range_get_img = mines[temp_row][temp_col]["hide_imgs"] # get values
            range_put_x = mines[temp_row][temp_col]["pos_x"]
            range_put_y = mines[temp_row][temp_col]["pos_y"]
            if range_get_img == 0 and mines[temp_row][temp_col] not in openArray and mines[temp_row][temp_col] not in yesArray:
                openArray.append(mines[temp_row][temp_col])
                SCREEN.blit(hide_images[range_get_img],(range_put_x,range_put_y))
            else:
                break
            count +=1

    #=========================================================== restart Q =====
    def popup_restart(game_result):
        #left, top, width, height

        msg = "Would you like to try again?"
        ms.play_msg(msg)

        pop_restart = pygame.Rect((screen_width//6,screen_height//4),(screen_width//1.5,screen_height//4))
        restart_text = "Would you like to try again?"

        yes_box = pygame.Rect(((screen_width//6)*1.5,(screen_height//4)*1.4),(screen_width//6,(screen_height//4)*0.5))
        yes_text = "YES"
        no_box = pygame.Rect(((screen_width//6)*3.5,(screen_height//4)*1.4),(screen_width//6,(screen_height//4)*0.5))
        no_text = "NO"

        # game result message
        msg = GAMEFONT.render(game_result,True,lightred)
        msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 1.5)))
        SCREEN.blit(msg,msg_rect)

        pygame.draw.rect(SCREEN, lightred, pop_restart)
        restart_msg = TEXTFONT.render(restart_text,True,black)
        restart_msg_rect = restart_msg.get_rect(center=(int(screen_width //2),int(screen_height//3.4)))

        pygame.draw.rect(SCREEN, black, yes_box)
        yes_msg = TEXTFONT.render(yes_text,True,lightred)
        yes_msg_rect = yes_msg.get_rect(center=(int((screen_width//6)*2),int((screen_height//4)*1.7)))

        pygame.draw.rect(SCREEN,black, no_box)
        no_msg = TEXTFONT.render(no_text,True,lightred)
        no_msg_rect = no_msg.get_rect(center=(int((screen_width//6)*4),int((screen_height//4)*1.7)))

        SCREEN.blit(restart_msg,restart_msg_rect)
        SCREEN.blit(yes_msg,yes_msg_rect)
        SCREEN.blit(no_msg,no_msg_rect)

        pygame.display.update() #게임화면을 다시그리기(매 프레임마다 화면그려줘야하기에)

        yes_x  = (screen_width//6)*1.5
        yes_y = (screen_height//4)*1.4
        yes_x_limit = yes_x + (screen_width//6)
        yes_y_limit = yes_y + (screen_height//4)*0.5
        no_x = (screen_width//6)*3.5
        no_y = (screen_height//4)*1.4
        no_x_limit = no_x + (screen_width//6)
        no_y_limit = no_y + (screen_height//4)*0.5

        popLEFT = 1
        popRIGHT = 3
        popRunning = True

        while popRunning:

            popEvent = pygame.event.poll()
            if popEvent.type == pygame.QUIT: # 창이 닫히는 이벤트 발생 시
                quit()
            elif popEvent.type == pygame.MOUSEBUTTONDOWN and popEvent.button == popLEFT :
                get_x = popEvent.pos[0] #클릭된 x좌표 값
                get_y = popEvent.pos[1] + 10 #클릭된 y좌표 값
                if yes_x_limit  >= get_x >= yes_x and yes_y_limit >= get_y >= yes_y:
                    msg = "YES"
                    ms.play_msg(msg)
                    popRunning = False
                elif no_x_limit >= get_x >= no_x and no_y_limit >= get_y >= no_y:
                    msg = "NO"
                    ms.play_msg(msg)
                    quit()

        print(yes_x,get_x,yes_x_limit,"and y" ,yes_y,get_y,yes_y_limit)
        print("You pressed the left mouse button at ({}, {})".format(get_x,get_y))

        MineFrame.draw_screen()
        main()


if __name__ == '__main__':
    main()
