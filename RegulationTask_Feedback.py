#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
from psychopy import prefs
from psychopy import gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, STOPPED, FINISHED)
import numpy as np
from numpy.random import random, choice
from psychopy.hardware import keyboard
import random
expName = "Probability Feedback"
expInfo = {"Participant" :"", "Date":""}

win=visual.Window(units='height')
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()
fileName =  u'Data/%s_%s' % (expInfo['Participant'], expName)
thisExp = data.ExperimentHandler(name=expName, extraInfo=expInfo, dataFileName = fileName)

clock = core.Clock()
defaultKeyboard = keyboard.Keyboard()
spaceKey = keyboard.Keyboard()
choiceKeys = keyboard.Keyboard()
instText = visual.TextStim(win=win, text='', pos=[0,0], height=0.08, wrapWidth = 1.15, color='#34a8eb')
isi = visual.TextStim(win=win, text='+', pos=[0,0], height=0.22, color='white')
cue = visual.TextStim(win=win, text='', pos=[0,0], height=0.16, wrapWidth=1.3, color='#d3b8ff')
leftImage = visual.ImageStim(win=win, image=None, pos=[-0.36,0], size=(0.35,0.35))
sureImage = visual.ImageStim(win=win, image=None, pos=[0.36,0], size=(0.35, 0.35))
leftProbability = visual.TextStim(win=win, text='', height=0.09, pos=[-0.36, 0.35], color="white")
rightProbability = visual.TextStim(win=win, text='100% Chance', height=0.09, pos=[0.36,0.35], color="white")
leftTimeBottom = visual.TextStim(win=win, text='', height=0.065, wrapWidth=0.8, pos=[-0.36, -0.40], color="white")
rightTimeBottom = visual.TextStim(win=win, text='', height=0.065,wrapWidth=0.8, pos=[0.36, -0.40], color="white")
lineStim = visual.Line(win=win,start=(0, -1.0), end=(0, 1.0), lineWidth=10.0, lineColor='black')
feedbackText = visual.TextStim(win=win, text="You won ", height = 0.12, wrapWidth=0.95, color="white")

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

def choiceFunc(leftImg, sureImg, leftTime, leftProb, rightTime):
    continueRoutine = True
    choiceFuncComponents= [lineStim, leftProbability, rightProbability, leftTimeBottom, rightTimeBottom, leftImage, sureImage, choiceKeys, clock]
    choiceKeys.keys=[]
    choiceKeyPress=[]
    choiceKeys.rt=[]
    textComponents = [leftTimeBottom, rightTimeBottom, rightProbability, leftProbability]
    imgComponents = [leftImage, sureImage]
    clock.reset()
    for i in choiceFuncComponents:
        i.status = STARTED
    for i in textComponents:
        i.setAutoDraw(True)
    for i in imgComponents:
        i.setAutoDraw(True)
    lineStim.setAutoDraw(True)
    while clock.getTime() < 5.0:
        leftProbability.setText(str(leftProb) + "% Chance")
        rightTimeBottom.setText(rightTime + " minutes" + "\ncuddling animals")
        leftTimeBottom.setText(leftTime + " minutes" + "\ncuddling animals")
        leftImage.setImage(leftImg)
        sureImage.setImage(sureImg)
        theseKeys = choiceKeys.getKeys(keyList=['1', '2'])
        choiceKeyPress.extend(theseKeys)
        if len(choiceKeyPress):
            choiceKeys.keys = choiceKeyPress[-1].name
            choiceKeys.rt = choiceKeyPress[-1].rt
        if choiceKeys.keys == '1':
            leftTimeBottom.setColor("yellow")
            leftProbability.setColor("yellow")
        if choiceKeys.keys == '2':
            rightTimeBottom.setColor("yellow")
            rightProbability.setColor("yellow")
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
    thisExp.addData("Gamble Probability", leftProb)
    thisExp.addData("Gamble Time", leftTime)
    thisExp.addData("Sure Time", rightTime)
    thisExp.nextEntry()

leftProbArray = [25, 50, 75, 50]
FiftyGamble = [1,0]
SeventyGamble = [1,1,1,0]
TwentyGamble = [1,0,0,0]
resultStr=[]
totalTime = []

class Spam():
    def randomProbabilitySelection(self, y, z):
        if choiceKeys.keys  == '1':
            if '50' in leftProbability.text:
                result=random.choice(FiftyGamble)
                if result == 1:
                    print("won the 50% gamble")
                    resultStr.append("Won")
                    self.timeEarned = y
                if result == 0:
                    print("Lost the 50% gamble")
                    resultStr.append("Lost")
                    self.timeEarned = '0'

            if '25' in leftProbability.text:
                result=random.choice(TwentyGamble)
                if result == 1:
                    print("Won the 25% gamble")
                    resultStr.append("Won")
                    self.timeEarned = y
                if result == 0:
                    print("Lost the 25% gamble")
                    resultStr.append("Lost")
                    self.timeEarned = '0'

            if '75' in leftProbability.text:
                result=random.choice(SeventyGamble)
                if result == 1:
                    print("Won the 75% gamble")
                    resultStr.append("Won")
                    self.timeEarned = y
                if result == 0:
                    print("Lost the 75% gamble")
                    resultStr.append("Lost")
                    self.timeEarned = '0'
        if choiceKeys.keys == '2':
            resultStr.append("Chose sure option")
            self.timeEarned = z
            print("Chose sure option")
        if resultStr[-1] == "Won":
            print("won the gamble")
        thisExp.addData("Feedback Results", resultStr[-1])
        thisExp.addData("Time Earned", self.timeEarned)

    def feedbackFunc(self):
        continueRoutine = True
        feedbackText.setText("You won " + self.timeEarned + " minutes cuddling animals")
        totalTime.append(int(self.timeEarned))
        feedbackText.setAutoDraw(True)
        win.flip()
        core.wait(3.500)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        feedbackText.setAutoDraw(False)
        print("Total Time List", totalTime)
        return totalTime
        thisExp.nextEntry()
s = Spam()

cueArray = ["RISKS ARE FUN", "BETTER SAFE THAN SORRY", "CHOICE"]
leftImgArray = ["deer.jpg", "el.jfif", "alli.jpg", "tiger.jpg"]
sureImgArray = ["ducks.jpg", "lion.jfif", "squ.jpg", "bun.jpg"]
rightTimeArray = ["5", "3", "4", "9"]
leftTimeArray = ["16", "18", "13", "15"]

random.shuffle(leftImgArray)
random.shuffle(sureImgArray)

instructionsArray = ["Welcome!", "In this task, you will be making risky decisions about how you might spend your time."]
for i in instructionsArray:
    instructionsFunction(i)

isiFunc(2.00)

for i in cueArray:
    regulationCues(i)
    isiFunc(1.500)
    for (a, b, c, d, e) in zip(leftImgArray, sureImgArray, leftTimeArray, leftProbArray, rightTimeArray):
        choiceFunc(a, b, c, d, e)
        isiFunc(1.50)
        s.randomProbabilitySelection(c, e)
        isiFunc(1.50)
        s.feedbackFunc()
        isiFunc(3.00)

sumTime = sum(totalTime)
instructionsFunction("Thank you for participating! Your total amount of time earned to cuddle animals is " + str(sumTime) + " minutes!")
