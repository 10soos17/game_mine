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
soundDir = os.path.join(baseDir, "mine_sound")
effectMineDir = os.path.join(baseDir, "mine_effect/mine")
effectVoiceDir = os.path.join(baseDir, "mine_effect/voice")

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

            while STOP_FLAG == True:
                STREAM.stop_stream()
                if STOP_FLAG == False:
                    STREAM.start_stream()

            data = WF.readframes(CHUNK)


        PLAYNUM -=1

        if PLAYNUM == 3:
            PLAYNUM +=1

    return 0

def play_stop(flag):
    global STOP_FLAG
    STOP_FLAG = flag

def play_restart():
    global STOP_FLAG
    STOP_FLAG = False

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
        pls.playsound(f'{effectMineDir}/mine2.mp3', False)
        pls.playsound(f'{effectVoiceDir}/lose.mp3', False)
        duration = cal_duration(f"{effectVoiceDir}/lose.mp3")
        time.sleep(duration)

    elif msg == "Mission Complete":
        pls.playsound(f'{effectMineDir}/mine2.mp3', False)
        pls.playsound(f'{effectVoiceDir}/win.mp3', False)
        duration = cal_duration(f"{effectVoiceDir}/win.mp3")
        time.sleep(duration)

    elif msg == "Time Over":
        pls.playsound(f'{effectMineDir}/mine2.mp3', False)
        pls.playsound(f'{effectVoiceDir}/timeover.mp3', False)
        duration = cal_duration(f"{effectVoiceDir}/timeover.mp3")
        time.sleep(duration)

    elif msg == "No flags left":
        play_stop(True)
        pls.playsound(f'{effectMineDir}/mine13.mp3', False)
        pls.playsound(f'{effectVoiceDir}/overflag.mp3', False)

        duration = cal_duration(f'{effectMineDir}/mine13.mp3')
        time.sleep(duration)
        play_restart()

    elif msg == "Would you like to try again?":
        #pls.playsound(f'{effectDir}/sinewave.mp3', False)
        pls.playsound(f'{effectVoiceDir}/question.mp3', False)

    elif msg == "YES":
        pls.playsound(f'{effectMineDir}/mine4.mp3', False)
        pls.playsound(f'{effectVoiceDir}/restart.mp3', False)

    elif msg == "NO":
        pls.playsound(f'{effectVoiceDir}/bye.mp3', False)

    elif msg == "Enter the number of rows":
        pls.playsound(f'{effectVoiceDir}/row.mp3', False)

    elif msg == "Enter the number of columns":
        pls.playsound(f'{effectVoiceDir}/column.mp3', False)

    elif msg == "Enter the number of mines":
        pls.playsound(f'{effectVoiceDir}/minenum.mp3', False)

    elif msg == "Game Start":
        pls.playsound(f'{effectVoiceDir}/start.mp3', False)

    elif msg == "Please try again.":
        #pls.playsound(f'{effectDir}/sinewave.mp3', False)
        pls.playsound(f'{effectVoiceDir}/tryagain.mp3', False)
