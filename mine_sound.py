#!/usr/bin/python3
# -*- coding:utf-8 -*-
import time, os, sys, subprocess
import threading
import random

import pyaudio, wave
import playsound as pls
from gtts import gTTS

baseDir = os.getcwd()
soundDir = os.path.join(baseDir, "mine_sound")
effectDir = os.path.join(baseDir, "mine_effect")

CHUNK=1024
AUDIO = pyaudio.PyAudio()

def play_sound(song, replay):
    global STREAM, PLAYNUM, STOP_FLAG
    STOP_FLAG = False
    PLAYNUM = replay
    if PLAYNUM == "loop":
        PLAYNUM = 3

    WF = wave.open(song,'rb')
    HZ = WF.getframerate()
    CHANNELS = WF.getnchannels()
    BITDEPTH = WF.getsampwidth()
    LENGTH = WF.getnframes()

    STREAM = AUDIO.open(format=AUDIO.get_format_from_width(BITDEPTH),
                        channels=CHANNELS,rate=HZ,output=True)

    RUN_DURATION = float(LENGTH / HZ)

    while PLAYNUM > 0:

        data = WF.readframes(CHUNK)

        while len(data) > 0:

            STREAM.write(data)

            data = WF.readframes(CHUNK)

            if STOP_FLAG == True:
                STREAM.stop_stream()

        PLAYNUM -=1

        if PLAYNUM == 3:
            PLAYNUM +=1

    return 0

def play_stop(flag):
    global STOP_FLAG
    STOP_FLAG = flag

def play_restart():
    STREAM.start_stream()

def cal_duration(song):
    args=("ffprobe","-show_entries", "format=duration","-i",song)
    popen = subprocess.Popen(args, stdout = subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()

    textOutput = str(output)
    textOutput=textOutput.split('=')
    textOutput=textOutput[1].split('\\')

    return float(textOutput[0])

def play_msg(msg):

    flag = False

#    tts = gTTS(text=f"{msg}",lang="en",tld="com")
#    tts.save(f"{effectDir}/tryagain.mp3")

    if msg == "Mission Failure":
        #pls.playsound(f'{effectDir}/sinewave.mp3', False)
        pls.playsound(f'{effectDir}/lose.mp3', False)
        duration = cal_duration(f"{effectDir}/lose.mp3")
        time.sleep(duration)

    elif msg == "Mission Complete":
        #pls.playsound(f'{effectDir}/horror.mp3', False)
        pls.playsound(f'{effectDir}/win.mp3', False)
        duration = cal_duration(f"{effectDir}/win.mp3")
        time.sleep(duration)

    elif msg == "Time Over":
        #pls.playsound(f'{effectDir}/sinewave.mp3', False)
        pls.playsound(f'{effectDir}/timeover.mp3', False)
        duration = cal_duration(f"{effectDir}/timeover.mp3")
        time.sleep(duration)

    elif msg == "No flags left":
        #pls.playsound(f'{effectDir}/sinewave.mp3', False)
        pls.playsound(f'{effectDir}/overflag.mp3', False)

    elif msg == "Would you like to try again?":
        #pls.playsound(f'{effectDir}/sinewave.mp3', False)
        pls.playsound(f'{effectDir}/question.mp3', False)

    elif msg == "YES":
        pls.playsound(f'{effectDir}/restart.mp3', False)

    elif msg == "NO":
        pls.playsound(f'{effectDir}/bye.mp3', False)

    elif msg == "Enter the number of rows":
        pls.playsound(f'{effectDir}/row.mp3', False)

    elif msg == "Enter the number of columns":
        pls.playsound(f'{effectDir}/column.mp3', False)

    elif msg == "Enter the number of mines":
        pls.playsound(f'{effectDir}/no.mp3', False)

    elif msg == "Game Start":
        pls.playsound(f'{effectDir}/start.mp3', False)

    elif msg == "Please try again.":
        #pls.playsound(f'{effectDir}/sinewave.mp3', False)
        pls.playsound(f'{effectDir}/tryagain.mp3', False)
