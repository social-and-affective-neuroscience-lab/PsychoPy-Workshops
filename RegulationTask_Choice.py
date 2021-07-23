#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
from psychopy import prefs
from psychopy import gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, STOPPED, FINISHED, PRESSED)
import numpy as np
from numpy.random import random, randint, shuffle, choice
from psychopy.hardware import keyboard
import os
import sys
import random
_thisDir=os.path.dirname(os.path.abspath(__file__))
expName = "Making Regulatory Decisions"
expInfo = {"Participant" :""}

win=visual.Window(units='height')
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()
fileName = _thisDir + os.sep + u'Data/%s_%s' % (expInfo['Participant'], expName)
thisExp = data.ExperimentHandler(name=expName, extraInfo=expInfo, originPath = _thisDir, dataFileName = fileName)

#declare variables
defaultKeyboard = keyboard.Keyboard()
spaceKey = keyboard.Keyboard()
choiceKeys = keyboard.Keyboard()
instText = visual.TextStim(win=win, text='', pos=[0,0], height=0.08, wrapWidth = 1.15, color='#34a8eb')
isi = visual.TextStim(win=win, text='+', pos=[0,0], height=0.22, color='white')
cue = visual.TextStim(win=win, text='', pos=[0,0], height=0.15, wrapWidth=1.3, color='#d3b8ff')
leftImage = visual.ImageStim(win=win, image=None, pos=[-0.36,0.3], size=(0.28,0.31))
rightImage = visual.ImageStim(win=win, image=None, pos=[0.36,0.3], size=(0.28,0.31))
leftTimeTop = visual.TextStim(win=win, text='', height=0.05, pos=[-0.36, 0.08], color="white")
rightTimeTop = visual.TextStim(win=win, text='', height=0.05, pos=[0.36,0.08], color="white")
leftTimeBottom = visual.TextStim(win=win, text='', height=0.05, pos=[-0.36, -0.40], color="white")
rightTimeBottom = visual.TextStim(win=win, text='', height=0.05, pos=[0.36, -0.40], color="white")
leftJournalImg = visual.ImageStim(win=win, image="jpsp.jpg", size=(0.28,0.28), pos=[-0.36, -0.19])
rightJournalImg = visual.ImageStim(win=win, image="jpsp.jpg", size=(0.28,0.28), pos=[0.36, -0.19])
lineStim = visual.Line(win=win,start=(-2.5, 0), end=(2.5, 0), ori=90.0, lineWidth=10.0, lineColor='black', fillColor='black')
#Define Instructions Function
def instructionsFunction(text):
    continueRoutine = True
    instructionComponents= [instText, spaceKey]
    for i in instructionComponents:
        i.status = STARTED
    while continueRoutine:
        instText.setText(text)
        instText.setAutoDraw(True)
        win.flip()
        if spaceKey.status == STARTED:
            theseKeys = spaceKey.getKeys(keyList=['space'])
            if len(theseKeys):
                continueRoutine = False
                instText.setAutoDraw(False)
                spaceKey.rt = theseKeys[-1].rt
        if defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
    thisExp.addData("Instructions Text", instText.text)
    thisExp.addData("Space RT", spaceKey.rt)
    spaceKey.keys=[]
    spaceKey.rt=[]
    thisExp.nextEntry()

#Run Instructions Function
instructionsArray = ["Welcome!", "In this task, you will be making decisions in which you will indicate how you would like to allocate your time between two activities."]
for i in instructionsArray:
    instructionsFunction(i)

#Define ISI Function
def isiFunc(time):
    continueRoutine = True
    isi.status = STARTED
    isi.setAutoDraw(True)
    win.flip()
    core.wait(time)
    if defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    isi.setAutoDraw(False)
    isi.status = FINISHED
    thisExp.addData("ISI Time", time)
    thisExp.nextEntry()

def regulationCues(cueText):
    continueRoutine = True
    cue.status = STARTED
    cue.setText(cueText)
    cue.setAutoDraw(True)
    win.flip()
    core.wait(3.00)
    if defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    cue.setAutoDraw(False)
    thisExp.addData("Cue Presented", cueText)
    thisExp.nextEntry()

clock = core.Clock()
def choiceFunc(leftImg, rightImg, leftTimeTopText, leftTimeBotText, rightTimeTopText, rightTimeBotText):
    continueRoutine = True
    choiceFuncComponents= [lineStim, leftTimeTop, rightTimeTop, leftTimeBottom, rightTimeBottom, leftImage, rightImage, leftJournalImg, rightJournalImg, choiceKeys, clock]
    choiceKeys.keys=[]
    choiceKeyPress=[]
    choiceKeys.rt=[]
    textComponents = [leftTimeTop, rightTimeTop, leftTimeBottom, rightTimeBottom]
    imgComponents = [leftImage, rightImage, leftJournalImg, rightJournalImg]
    clock.reset()
    for i in choiceFuncComponents:
        i.status = STARTED
    for i in textComponents:
        i.setAutoDraw(True)
    for i in imgComponents:
        i.setAutoDraw(True)
    lineStim.setAutoDraw(True)
    while clock.getTime() < 5.0:
        rightTimeTop.setText(rightTimeTopText + " minutes" + "\npetting a dog")
        leftTimeTop.setText(leftTimeTopText + " minutes" + "\npetting a dog")
        rightTimeBottom.setText(rightTimeBotText + " minutes" + "\nwriting a manuscript")
        leftTimeBottom.setText(leftTimeBotText + " minutes" + "\nwriting a manuscript")
        leftImage.setImage(leftImg)
        rightImage.setImage(rightImg)
        theseKeys = choiceKeys.getKeys(keyList=['1', '2'], waitRelease=False)
        choiceKeyPress.extend(theseKeys)
        if len(choiceKeyPress):
            choiceKeys.keys = choiceKeyPress[-1].name
            choiceKeys.rt = choiceKeyPress[-1].rt
        if choiceKeys.keys == '1':
            print("pressed 1")
            leftTimeTop.setColor("yellow")
            leftTimeBottom.setColor("yellow")
        if choiceKeys.keys == '2':
            print("pressed 2")
            rightTimeBottom.setColor("yellow")
            rightTimeTop.setColor("yellow")
        if continueRoutine:
            win.flip()
    if defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    for i in textComponents:
        i.setAutoDraw(False)
    for i in imgComponents:
        i.setAutoDraw(False)
    lineStim.setAutoDraw(False)
    for i in textComponents:
        i.setColor("white")
    continueRoutine = False
    thisExp.addData("Choice RT", choiceKeys.rt)
    thisExp.addData("Choice Made", choiceKeys.keys)
    thisExp.nextEntry()

cueArray = ["FUTURE", "CHOICE", "PRESENT"]
leftImgArray = ["dog8.jpg", "dog10.jpeg", "dog12.jpg", "dog14.jpg"]
rightImgArray = ["dog9.jpg", "dog11.jpg", "dog13.jpg", "dog15.jpg"]
leftTopArray = ["12", "17", "14", "11"]
leftBotArray = ["8", "3", "6", "9"]
rightTopArray = ["4", "2", "7", "5"]
rightBotArray = ["16", "18", "13", "15"]


isiFunc(2.00)
random.shuffle(leftImgArray)
random.shuffle(rightImgArray)

for i in cueArray:
    regulationCues(i)
    isiFunc(1.500)
    for (a, b, c, d, e, f) in zip(leftImgArray, rightImgArray, leftTopArray, leftBotArray, rightTopArray, rightBotArray):
        choiceFunc(a, b, c, d, e, f)
        isiFunc(3.00)

instructionsFunction("Thank you for participating!")
