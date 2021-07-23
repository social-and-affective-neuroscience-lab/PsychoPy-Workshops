#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
from psychopy import prefs
from psychopy import gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, STOPPED, FINISHED, PRESSED)
from psychopy.hardware import keyboard
import os
import sys
import itertools
_thisDir=os.path.dirname(os.path.abspath(__file__))
expName = "Regulating Responses"
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
instText = visual.TextStim(win=win, text='', pos=[0,0], height=0.08, wrapWidth = 1.15, color='#34a8eb')
isi = visual.TextStim(win=win, text='+', pos=[0,0], height=0.22, color='white')
cue = visual.TextStim(win=win, text='', pos=[0,0], height=0.16, wrapWidth=1.3, color='#d3b8ff')
picStim = visual.ImageStim(win=win, image=None, pos=[0,0], size=(0.7,0.7))
emoScale = visual.Slider(win=win, size=(0.85, 0.07), pos=(0,-0.14), ticks=(1,2,3,4,5,6,7), style='rating', color='LightGray', fillColor="Red",labels=("Small bundles", "I could cry"), borderColor="white", labelHeight=0.03, readOnly=False)
scaleQ = visual.TextStim(win=win, text='How much joy do you feel?', pos=[0, 0.35], height=0.08, color="white")

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
instructionsArray = ["Welcome!", "In this task, you will be looking at pictures and assessing your emotional responses."]
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

isiFunc(2.00)

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

def imageFunc(img):
    continueRoutine = True
    picStim.status = STARTED
    picStim.setImage(img)
    picStim.setAutoDraw(True)
    win.flip()
    core.wait(5.00)
    if defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    picStim.setAutoDraw(False)
    thisExp.addData("Image Presented", img)
    thisExp.nextEntry()

def emoResponse():
    continueRoutine = True
    emoResponseComponents= [emoScale, scaleQ]
    for i in emoResponseComponents:
        i.status = STARTED
    while continueRoutine:
        emoScale.setAutoDraw(True)
        scaleQ.setAutoDraw(True)
        win.flip()
        if spaceKey.status == STARTED:
            theseKeys = spaceKey.getKeys(keyList=['space'])
            if len(theseKeys):
                continueRoutine = False
                emoScale.setAutoDraw(False)
                scaleQ.setAutoDraw(False)
                spaceKey.rt = theseKeys[-1].rt
        if defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()

    thisExp.addData("Emotion Response", emoScale.getRating())
    emoScale.reset()
    thisExp.nextEntry()

cueArray = ["EMPHASIZE", "LOOK", "DE-EMPHASIZE", "LOOK", "EMPHASIZE", "LOOK", "DE-EMPHASIZE"]
imgArray = ["dog1.jpg", "dog2.jpeg", "dog3.jpg", "dog4.jpg", "dog5.jpg", "dog6.jpg", "dog7.jpg"]

for (i, b) in zip(cueArray, imgArray):
    regulationCues(i)
    isiFunc(1.500)
    imageFunc(b)
    isiFunc(1.500)
    emoResponse()
    isiFunc(3.00)
instructionsFunction("Thank you for participating!")
