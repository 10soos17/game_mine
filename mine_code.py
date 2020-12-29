#!/usr/bin/python3
import random

def matrix_set(x,y,mine):

    matrix = [[0]*y for i in range(x)]
    shell = [[0]*(y+2) for i in range(x+2)]
    rx = 0
    ry = 0
    count = 0
    while count != mine:
        rx=random.randint(0,x-1)
        ry=random.randint(0,y-1)
        if matrix[rx][ry] != "9":
            matrix[rx][ry] = "9"
            count+=1
    a=0
    b=0

    for i in range(x):
        for j in matrix[a]:
            shell[a+1][b+1]=j
            b+=1
        a+=1
        b=0
    a=1
    b=1
    mineCount = 0

    for i in range(x):
        for j in matrix[0]:
            if shell[a][b] != "9":
               if shell[a-1][b-1] == "9":
                   mineCount +=1
               if shell[a-1][b] == "9":
                   mineCount +=1
               if shell[a-1][b+1] == "9":
                   mineCount +=1
               if shell[a][b-1] == "9":
                   mineCount +=1
               if shell[a][b+1] == "9":
                   mineCount +=1
               if shell[a+1][b-1] == "9":
                   mineCount +=1
               if shell[a+1][b] == "9":
                   mineCount +=1
               if shell[a+1][b+1] == "9":
                   mineCount +=1
               shell[a][b] = mineCount
               mineCount = 0
            b+=1
        a+=1
        b=1
    a=0
    b=0

    for i in range(x):
        for j in matrix[a]:
            matrix[a][b] = shell[a+1][b+1]
            b+=1
        a+=1
        b=0
    a=0
    b=0

    for i in range(x):
        for j in matrix[b]:
            print(matrix[b][a], end = "")
            a+=1
        print("\n")
        a=0
        b+=1

    return x, y, mine, matrix
"""
def matrix_question():

    x = int(input("x?"))
    while x > 30:
        x = int(input("Try again! x?"))
    y = int(input("y?"))
    while y > 50:
        y = int(input("Try again! y?"))
    limit = x*y

    mine = int(input("mine?"))
    while limit <= mine:
          mine = int(input("Try again! mine?"))

    return matrix_set(x,y,mine)
"""
