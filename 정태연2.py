from bangtal import *
import random
import time

STONE = {'black':1, 'white':2}
gameTOKEN = 0

# index를 x,y좌표로
def indexTOxy(index):
    return ((index%8) * 80 + 40, (index//8) * 80 + 40)

# 돌의 가능한 위치 출력
def POSSIBLE(index, stone1, stone2): # stone1 : possible한지 출력하고 싶은 돌, stone2 : stone1이 아닌 돌
    dx = [-9, -8, -7, 1, 9, 8, 7, -1]
    li = [-1, -1, -1, 0, 1, 1, 1, 0]

    count = 0
    if MATRIX2[index] == 0:
        for d, l in zip(dx, li):
            token = False
            temp = index
            cc = 0
            while True:
                temp += d
                if temp < 0 or temp > 63 or (temp//8) - ((temp-d)//8) != l:       
                    break
                if MATRIX2[temp] == 0: # 빈(빈)
                    break
                elif MATRIX2[temp] == stone2 and token == False: # 빈(백)
                    token = True
                    cc += 1
                elif MATRIX2[temp] == stone2 and token == True: # 빈백(백)
                    cc += 1
                elif MATRIX2[temp] == stone1 and token == False: # 빈(흑)
                    break
                elif MATRIX2[temp] == stone1 and token == True: # 빈백(흑), 빈백백(흑) ...
                    count += cc
                    break
    else:
        return -1, -1
    return index, count

# 돌 뒤집기
def CHANGESTONE(index):
    global MATRIX1, MATRIX2
    stone1 = MATRIX2[index]
    if MATRIX2[index] == 1:
        stone1 = 'black'
        stone2 = 'white'
    else:
        stone1 = 'white'
        stone2 = 'black'

    dx = [-9, -8, -7, 1, 9, 8, 7, -1]
    li = [-1, -1, -1, 0, 1, 1, 1, 0]
    for d, l in zip(dx, li):
        temp = index
        candidates = []
        token = False
        while True:
            temp += d
            if temp < 0 or temp > 63 or (temp//8) - ((temp-d)//8) != l :
                break
            if MATRIX2[temp] == STONE[stone1] and token == True: # 흑백백(흑)
                for i in candidates:
                    MATRIX1[i].setImage('Images/{}.png'.format(stone1))
                    MATRIX2[i] = STONE[stone1]
                break
            elif MATRIX2[temp] == STONE[stone1] and token == False: # 흑(흑)
                break
            elif MATRIX2[temp] == STONE[stone2]: # 흑(백) or 흑백(백)
                candidates.append(temp)
                token = True
                continue
            else:
                break

# 총 돌의 수 계산
def totalSTONE():
    global MATRIX2, black_num1, black_num2, white_num1, white_num2

    b = [x for x in MATRIX2 if x == 1]
    w = [x for x in MATRIX2 if x == 2]

    black = len(b)
    white = len(w)

    black_num1.setImage('Images/L{}.png'.format(black//10))
    black_num2.setImage('Images/L{}.png'.format(black%10))
    white_num1.setImage('Images/L{}.png'.format(white//10))
    white_num2.setImage('Images/L{}.png'.format(white%10))

# possible list 출력  
def possiblelist(possible, m, n):
    for i in range(64):
        pos, cou = POSSIBLE(i, m, n)
        if cou == 0 or cou == -1: continue
        else : possible.append([pos, cou])

# 컴퓨터 차례
def computer(possible):
    try:
        tt = max(possible, key=lambda x:x[1])
    except ValueError as e:
        print(e)
        return
    ttt = [x[0] for x in possible if x[1] == tt[1]]
    random_index = random.sample(ttt, 1)
    
    MATRIX2[random_index[0]] = 2
    MATRIX1[random_index[0]].setImage('Images/white.png')

    CHANGESTONE(random_index[0]) # 백돌을 흑돌로 바꾸기

# 게임 종료 확인
def gameEND():
    global gameTOKEN
    black = []
    white = []
    possiblelist(black, 1, 2)
    possiblelist(white, 2, 1)

    if len(black) == 0 and len(white) == 0:
        gameTOKEN = 1
        showMessage('게임 종료')
    if 0 not in MATRIX2:
        gameTOKEN = 1
        showMessage('게임 종료')
    return 

'''------------------ 
INITIATE (초기 설정) 
------------------'''
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
scene = Scene('Othello', 'Images/background.png')
board = Object('Images/board.png')
board.locate(scene, 40, 40)
board.show()
MATRIX1 = [Object('Images/blank.png') for _ in range(64)] # 상황판 오브젝트 매특릭스
for i in range(64):
    MATRIX1[i].locate(scene, indexTOxy(i)[0], indexTOxy(i)[1])
    MATRIX1[i].show()
MATRIX2 = [0 for _ in range(64)] # 상황판 돌 매트릭스
possible = [[26,1], [19,1], [37,1], [44,1]]
MATRIX2[27] = 2
MATRIX1[27].setImage('Images/white.png')
MATRIX2[28] = 1
MATRIX1[28].setImage('Images/black.png')
MATRIX2[35] = 1
MATRIX1[35].setImage('Images/black.png')
MATRIX2[36] = 2
MATRIX1[36].setImage('Images/white.png')
MATRIX1[26].setImage('Images/black possible.png')
MATRIX1[19].setImage('Images/black possible.png')
MATRIX1[37].setImage('Images/black possible.png')
MATRIX1[44].setImage('Images/black possible.png')
black_num1 = Object('Images/L0.png')
black_num1.locate(scene, 750, 220)
black_num1.show()
black_num2 = Object('Images/L2.png')
black_num2.locate(scene, 830, 220)
black_num2.show()
white_num1 = Object('Images/L0.png')
white_num1.locate(scene, 1070, 220)
white_num1.show()
white_num2 = Object('Images/L2.png')
white_num2.locate(scene, 1150, 220)
white_num2.show()

def objectTOindex(object):
    global MATRIX1
    for index in range(64):
        if MATRIX1[index] == object: return index

def onMouseAction_stone(object, x, y, action):
    global possible, MATRIX1, MATRIX2, gameTOKEN
    index = objectTOindex(object)
    
    while True:
        if index in [x[0] for x in possible]: # 올바르게 흑이 놓아야할 위치를 클릭했을 경우
            for i in [x[0] for x in possible]: # 빈칸으로 다시 만들어 놓기
                MATRIX1[i].setImage('Images/blank.png')
                    
            MATRIX2[index] = 1
            MATRIX1[index].setImage('Images/black.png') # 흑돌 놓기
            
            CHANGESTONE(index) # 백돌을 흑돌로 바꾸기
            
            gameEND()
            if gameTOKEN == 1:
                return

            # 백이 놓을 수 있는 위치 찾기 (컴퓨터 차례)
            possible = []
            possiblelist(possible, 2, 1)
            
            if len(possible) != 0: # 컴퓨터가 놓을 자리가 있을 경우
                while True:
                    computer(possible) # <컴퓨터의 돌 놓기>
                    gameEND()
                    if gameTOKEN == 1:
                        return
 
                    possible = []
                    possiblelist(possible, 1, 2) # 흑이 놓을 수 있는 위치 찾기
            
                    if len(possible) != 0: # 흑돌이 놓을자리가 있을 경우
                        for pos, cou in possible: # 흑이 놓을 수 있는 위치 이미지 바꾸기
                            MATRIX1[pos].setImage('Images/black possible.png')

                        # total 돌의 수
                        totalSTONE()
                        token  = 1
                        break
                    else: # 흑돌이 놓을자리가 없는 경우 > 컴퓨터가 계속 놓아야함
                        gameEND()
                        if gameTOKEN == 1:
                            return
                        possible = []
                        possiblelist(possible, 2, 1) # 백이 놓을 수 있는 위치 찾기
                        continue

            else: # 컴퓨터가 놓을 자리가 없는 경우
                gameEND()
                if gameTOKEN == 1:
                    return
                possible = []
                possiblelist(possible, 1, 2)
                for pos, cou in possible:
                    MATRIX1[pos].setImage('Images/black possible.png')

                totalSTONE()
                break
        else:
            continue

        if token == 1:
            break
Object.onMouseActionDefault = onMouseAction_stone

startGame(scene)