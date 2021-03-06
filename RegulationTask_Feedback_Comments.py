#!/usr/bin/env python   #this is telling psychopy which virtual environment to use  -- in  my case it is an environment called python
# -*- coding: utf-8 -*-  # using unicode encoding (??? i have no idea what that actually means)

#Now we're importing a ton of packages - this is parallel to what you do with libraries in R
from __future__ import absolute_import, division  # gets the most updated version of our libraries
from psychopy import prefs # default preferences preloaded by psychopy
from psychopy import gui, visual, core, data, event, logging, clock, colors  # these are features of our stimuli that we'll be able to call on
from psychopy.constants import (NOT_STARTED, STARTED, STOPPED, FINISHED)  # these are status checks we can use
import numpy as np
from numpy.random import random, choice  # numpy is what we'll use to randomly select things
from psychopy.hardware import keyboard  # this lets us make keyboard responses
import random   # a different randomize package

#Give some information about the experiment
expName = "Probability Feedback"   #name of our experiment
expInfo = {"Participant" :"", "Date":""} # This is called a dictionary, it is a collection of keys (e.g., "Participant" and "Date") and values (e.g., whatever you type into those text boxes)

#define our window that we want the experiment to pop up in
win=visual.Window(units='height')

# create a dialogue box using a graphical user interface (gui) function called "Dialogue from dictionary"
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName) # in the dialogue box we will show our dictionary from line16 and our title from line 15
if dlg.OK == False: #if a person does not click okay in the dialogue box,
    core.quit()   # quit the Experiment

fileName =  u'Data/%s_%s' % (expInfo['Participant'], expName)  #this is going to name our output data file, the blue ""%s" are placeholders for what comes in the parentheses, in this case,
                                                       #       the participant number (that we get from the dialogue box, and our experiment name)
thisExp = data.ExperimentHandler(name=expName, extraInfo=expInfo, dataFileName = fileName)# this is using a function called "Experiment Handler" and it is going to wrap all of our data in a neat bow


#Now we can start declaring and initializing variables

'''
But first, to explain why we're using the variables we are, this task is going to have four parts:
    1) Instructions
    2) Choice trials
    3) Feedback screens
    4) End screen
For the instructions, we just need some text to appear on the screen, and we want to use the keyboard to have the screens move on
For the choice trials, we will have timed stimuli on screen, for which participants can make a keyboard response indicating a preference for one of the choices.
    In these trials, participants will be shown one risky and one sure decision on screen at the same time. For the risky decision, there will be either a 25, 50, or 75% chance of getting the desired outcome.
    For the sure decision, there will be a 100% chance of getting the desired outcome. The specific outcomes are going to be amount of time, in minutes, cuddling animals. So participants will be prompted to
    take a risk to win a lot of time cuddling animals, or a guaranteed amount of less time cuddling animals.
    In these trials, we will have one variable text stimulus for the probability (25, 50, or 75), two variable text stimuli for the amount of minutes (one for the risky decision and one for the sure decision),
    one static text stimuli for the sure probability (100%), and two image stimuli. We will also have a keyboard component to allow for a response.
For the feedback trials, participants will see how much time they earned cuddling animals, dependent on their prior choice. If participants chose the sure option, they will see a screen saying that they earned
that sure amount of time. If participants chose the risky option, they will see if they won the gamble, and if so, the amount of time they gambled for.
Lastly, the end screen will show participants how much time in total, they accumulated for cuddling animals.
There will also be timed fixation crosses throughout the task
'''
# Now we can really start declaring our variables

clock = core.Clock() # now we're using stimuli from psychopy that we called on in line 7, this one is going to be a clock
defaultKeyboard = keyboard.Keyboard() #this is a keyboard that we will use throughout the task to allow ppl to escape the window
spaceKey = keyboard.Keyboard()  # another keyboard stim that we'll use more specifically for pressing space
choiceKeys = keyboard.Keyboard()   # another keyboard stim that we'll use for making choices in the task itself

#Now we're creating a bunch of visual stimuli:
# First we have a bunch of text that's going to appear on the screen
# Each "TextStim" has a bunch of parameters we can work with to customize the stimuli so it looks the way we want it to
instText = visual.TextStim(win=win, text='', pos=[0,0], height=0.08, wrapWidth = 1.15, color='#34a8eb') # first, always specify the window you want the text to appear in, if you don't it will not show up
isi = visual.TextStim(win=win, text='+', pos=[0,0], height=0.22, color='white') # then say what you want your stimulus to say, that is, what text will appear on screen?
cue = visual.TextStim(win=win, text='', pos=[0,0], height=0.16, wrapWidth=1.3, color='#d3b8ff')  # pos is position and refers to the x,y plane of your computer screen, so you'll need to always put in two arguments
leftProbability = visual.TextStim(win=win, text='', height=0.09, pos=[-0.36, 0.35], color="white") # height is the size of your text, usually 0.1 is a pretty normal size, 0.05 is quite small and 0.2 is quite big
rightProbability = visual.TextStim(win=win, text='100% Chance', height=0.09, pos=[0.36,0.35], color="white")  # color is the color of your text, you can use words (e.g., 'white', 'blue', 'pink'), but psychopy doesn't recognize everything (e.g., 'mets blue' wouldn't work); you can also use rgb color codes
leftTimeBottom = visual.TextStim(win=win, text='', height=0.065, wrapWidth=0.8, pos=[-0.36, -0.40], color="white") # wrapWidth is how wide you want your text to be on screen; if you're just showing one word you don't really have to worry about this, but if you're showing sentences you'll want to adjust this
rightTimeBottom = visual.TextStim(win=win, text='', height=0.065,wrapWidth=0.8, pos=[0.36, -0.40], color="white")
feedbackText = visual.TextStim(win=win, text="You won ", height = 0.12, wrapWidth=0.95, color="white")
#As you can see from the above TextStims, only some of my stimuli have text in the text argument -- the ones that are blank are going to be changing throughout the task

#Add a couple of image stimuli
leftImage = visual.ImageStim(win=win, image=None, pos=[-0.36,0], size=(0.35,0.35)) # again, say what window we're using
sureImage = visual.ImageStim(win=win, image=None, pos=[0.36,0], size=(0.35, 0.35)) # then position is the same as before (x,y) and size takes two arguments, for width and height

#Lastly add a line
lineStim = visual.Line(win=win,start=(-2.5, 0), end=(2.5, 0), ori=90.0, lineWidth=10.0, lineColor='black') # for lines we're also going to add where we want the line to start (x,y) and where we want it to end (x,y)
#There are a bunch more arguments we can add to all of the above stim, like 'opacity', 'depth' (where things appear in relation to each other), 'bold' and 'italic' for text, etc..
# The psychopy website has great documentation! : https://www.psychopy.org/api/visual/index.html




# Now we're going to actually build the task! Everything we did so far was just creating a dialogue box and delaring our stimuli, but now we get to call on it and have it appear and do things!!

# we are defining a function called 'instructionsFunction' with one argument called 'textArg'
# you can name functions whatever you want, and you can call your arguments whatever you want! Just make sure to have the command 'def' before them!
def instructionsFunction(textArg): # you can define functions without adding arguments, but when we do add args, we can use the function in different contexts
    continueRoutine = True # tells the experiement to keep going!
    instructionComponents= [instText, spaceKey] # you don't have to do this, but creating a list, or something in brackets, will allow us to loop through that list quickly
    # so line 89 is just creating a LIST called 'instructionsComponents' and giving it two values, instKey and spaceKey
    for i in instructionComponents: # now we're using a 'for' loop, so this is saying, for each item (i) in our list (instructionsComponents), do something
        i.status = STARTED  # and that something, is to change the status of each item to be "STARTED"
    while continueRoutine: # Now we're outside of the for loop, but we're creating something else called a 'while' statement - so now this is saying, as long as 'continueRoutine' is TRUE (which we declared in line 88), do something
                 #         and what we're doing is calling on our stimuli, having it appear on screen, and also allowing a keyboard response!
        instText.setText(text) # This line is important because we're using the argument that we first acknowledge in our function in line 87! So this current line is telling the text variable (instText) to have the input of the value of our argument (textArg)
        # when we initialized our variable instText on line61, we gave it the parameter value of text='', if we left it like that, we wouldn't see any text appear on the screen -- however, we also will not straight up see "textArg" on the screen.... more on that later
        instText.setAutoDraw(True) # have this stimuli appear on screen!
        win.flip() # and show the window!
        if spaceKey.status == STARTED: # now we're going to be using a conditional 'if' statement, which says that if some condition is met, do something -- in our case, if the status of our spaceKey stimuli (this was a keyboard stim) is 'STARTED' (which we made happen in line92), then:
            theseKeys = spaceKey.getKeys(keyList=['1', '2', 'space']) # let us press space, 1, or 2, on our keyboard
            if len(theseKeys): # if we pressed any of these ^ keys
                continueRoutine = False # stop this part of the task!!!
                instText.setAutoDraw(False) # make the text disappear from the screen
                spaceKey.rt = theseKeys[-1].rt # and lastly, collect reaction time for when we pressed any of the allowed keys
        if defaultKeyboard.getKeys(keyList=["escape"]): #this is a safety measure that I highly recommend adding to all of your routines , it is saying that if we press 'escape':
            core.quit() # quit the experiment entirely
    thisExp.addData("Instructions Text", instText.text) # now we can add some data to our output file; using our experiment handler from line 28, we're going to create a column called "Instructions Text" and we're doing to add whatever text appeared on screen, so instText.text refers to line 96 when we gave our stimuli some value
    thisExp.addData("Space RT", spaceKey.rt) # we are also creating a column called "Space RT" and adding in our reaction time of pressing any of the allowed keys
    thisExp.nextEntry() # move on to the next part of the task!

# Again, what we just defined is a function, and although we added in a lot of commands into it (e.g., having text appear, collecting keyboard responses), if we were to run the script right now - nothing would happen!
#This is because we need to call on the function for it to run -- more on that later

#for now, we're creating another function!
def isiFunc(time): # this one is going to have a fixation cross appear on the screen for a specific time -- 'time' is our argument that we can specify when we run the function
    continueRoutine = True # keep the experiment going
    isi.status = STARTED # have our text stimulus, which is just a "+" sign, start
    isi.setAutoDraw(True) # and have it appear on scree
    win.flip() # keep the window open
    core.wait(time) # have the isi appear on screen for x amount of time - again dependent on the argument 'time'
    if defaultKeyboard.getKeys(keyList=["escape"]): 3=# this is that safety measure again, if we press escape at any point, quit the task entirely
        core.quit()
    isi.setAutoDraw(False) # after our specified amount of time is up, get the "+" sign off the screen
    isi.status = FINISHED # change its status to FINISHED
    thisExp.addData("ISI Time", time) # and add some more data to our output file - we created a new column called "ISI Time" and we're inputting the amount of time specified from our "time" argument
    thisExp.nextEntry() # on to the next thing!


 # This next function is going to be very similar to the two previous functions - in this one we're going to show varied regulation cues for a specified amount of time
 # So similar to the first function, our argument will refer to the text on screen, but similar to the second function, we're only going to show this text for some time before the screen moves on
def regulationCues(cueText): # now our argument is called "cueText"
    continueRoutine = True # keep going
    cue.status = STARTED # change the status of our text stimuli "cue" to started
    cue.setText(cueText) # set the text of our text stim to be whatever our argument is
    cue.setAutoDraw(True) # and have the text appear
    win.flip() # keep the window open
    core.wait(3.00) # wait three seconds
    if defaultKeyboard.getKeys(keyList=["escape"]): # our nifty safety measure
        core.quit()
    cue.setAutoDraw(False) # after 3 seconds, have the text disappear
    thisExp.addData("Cue Presented", cueText) # add data to our output file - we're creating a column called "Cue Presented" and adding whatever text appeared on screen, as given by our argument
    thisExp.nextEntry() # and move on to the next thing!


# A little heftier function now - but this is the good stuff that will make up most of our task!
# In this function, we're going to have a lot of things going on - we'll have text stimuli, image stimuli, keyboard responses, and it's all going to be timed
def choiceFunc(leftImg, sureImg, leftTime, leftProb, rightTime): #So we have a bunch of arguments for our different stim!
    continueRoutine = True # keep going
    choiceFuncComponents= [lineStim, leftProbability, rightProbability, leftTimeBottom, rightTimeBottom, leftImage, sureImage, choiceKeys, clock] # we're bringing back our components list, this helps us use for statements in the next couple of lines
    choiceKeys.keys=[] #we're creating an empty list here that will help us keep track of what keys people pressed in this task (we'll use this list when we save our data)
    choiceKeyPress=[] # this will track the same key presses as well as their reaction time
    choiceKeys.rt=[] # this will just track reaction time (we'll use this list when we save our data)
    textComponents = [leftTimeBottom, rightTimeBottom, rightProbability, leftProbability] # we're creating two more lists out of some of the same items from our list in line 149 - we're making separate lists because not all of our stimuli can be called on the same way
    imgComponents = [leftImage, sureImage, lineStim] # and thus having separate lists allows us to use different for loops (our line operates the same as a picture, so we're including it here)
    clock.reset() # we're using a clock to keep track of time, resetting it means setting it to 0, and clocks count upwards
    for i in choiceFuncComponents: # our first for loop is changing the status of ALL of our stimuli to be STARTED
        i.status = STARTED
    for i in textComponents: # our next for loop is only using the items from our list in line 153, which is all of the text stim
        i.setAutoDraw(True) # so we're telling all of our text to appear on screen
    for i in imgComponents: # we're doing the same thing for our image stimuli - the reason we're not using our list of everything (line149) is because we want to use this setAutoDraw command to make things appear on screen - however, we can't make the clock or keyboard appear because they are internal elements
        i.setAutoDraw(True) # so if we ran these for loops with choiceFuncComponents, we would get error messages that the screen can't draw "clock" or 'choiceKeys' (these things don't have visual components)
    while clock.getTime() < 5.0: # the clock is counting up, so as long as the clock is less than 5 seconds...:
        leftProbability.setText(str(leftProb) + "% Chance") #we're using one of our arguments to set the text of a text stimuli - as you can see, we have a little extra command within our text - str() - this means 'convert to string' - and more plainly means - turn non-text things so they are readable and can be considered text
        # the reason we need that str() command is because one of our arguments, leftProb, is going to be an INTEGER - python can't read integers the same way as strings, so by converting an integer into a string, we are able to set the text of our stimuli with the number value of our argument, while still being considered a string
        #lines 163, 166, 167 look a bit different to our normal way of setting text because of the "+" signs in the middle of our parentheses - we're using this + sign to concatenate, or smush together, different strings
        rightTimeBottom.setText(rightTime + " minutes \ncuddling animals") # so in this line, we are first entering one of our arguments, then we want it to say "minutes cuddling animals" after it - you'll also notice a weird "\n" hanging out in our phrase - this is how we represent a break while staying in a string
        leftTimeBottom.setText(leftTime + " minutes \ncuddling animals") # when this text will appear on screen, we'll see a variable number for our argument, then right next to that number we'll see 'minutes' and on the next line right below it, we'll see 'cuddling animals'
        leftImage.setImage(leftImg) # now we're using some more arguments to set the images for our two image stimuli
        sureImage.setImage(sureImg)
        theseKeys = choiceKeys.getKeys(keyList=['1', '2']) # and telling the script what keys we're allowed to use to respond, in this case, keys '1' and '2'
        choiceKeyPress.extend(theseKeys) # this line is telling our script to add on to our list 'choiceKeyPress' (which is empty, as per line151) by appending the different keys we pressed
        # so if the task was running and I pressed '1', our list choiceKeyPress, which was initially empty, would now look like: ['1']
        # if the task kept going and I pressed '2', then '2' again, then '1', our list choiceKeyPress would then look like ['1', '2', '2', '2']
        if len(choiceKeyPress): # this if statement is saying that if our list, choiceKeyPress, is NOT empty, then...:
            choiceKeys.keys = choiceKeyPress[-1].name # get the name of the last key we pressed, so when we say the name of a list and [-1] right after it (choiceKeyPress[-1]), that means get the last item in the list
            choiceKeys.rt = choiceKeyPress[-1].rt # and get the reaction time of the last key we pressed
        if choiceKeys.keys == '1': # Now we're doing a couple more conditional statements! If the last key we pressed was a '1'...:
            leftTimeBottom.setColor("yellow") # then change the color of our left-bottom text to be yellow
            leftProbability.setColor("yellow") # and also change the color of our left - probability text to be yellow
        if choiceKeys.keys == '2': # if instead, the last key we pressed was a '2':
            rightTimeBottom.setColor("yellow") # make the text on the right-bottom turn yellow
            rightProbability.setColor("yellow") # and make the text of the right-probability text to be yellow
        if continueRoutine # while the routine is still going:
            win.flip() # keep the window open
    if defaultKeyboard.getKeys(keyList=["escape"]): # our safety measure again
        core.quit()
    for i in textComponents: # now this for loop is happening outside of our while statement, so these following loops are occurring AFTER the clock in line162 reached a time of 5 seconds
        i.setAutoDraw(False) # have all of our text disappear
    for i in imgComponents: # have all of our images disappear ( and our line stim)
        i.setAutoDraw(False)
    for i in textComponents: # change back the color of all of our text to white!
        i.setColor("white") # this is important, because if we did not change it, all of the text would remain yellow following every trial, and therefore we would not be able to see which choice was selected (the keys would still respond, we just wouldn't get the visual feedback of the text turning from white to yellow)
    continueRoutine = False # stop this part of the task
    thisExp.addData("Choice RT", choiceKeys.rt) # and add a bunch of data, including the reaction time of our choice
    thisExp.addData("Choice Made", choiceKeys.keys) # which choice we selected, we will get this information from choice.keys because if they pressed '1', that changed the left text yellow, hence they selected the choice on the left hand side (same for '2' with the right hand choices)
    thisExp.addData("Gamble Probability", leftProb) # we're also adding the probability that appeared on screen
    thisExp.addData("Gamble Time", leftTime) # as well as the amount of time that appeared on screen on the left side
    thisExp.addData("Sure Time", rightTime) # and the amount of time that appeared on the right side
    thisExp.nextEntry()

leftProbArray = [25, 50, 75, 50] # This is a list of all of our gambles - I only added two 50s to have an equal number as the items in our time/images lists that we will create soon
FiftyGamble = [1,0]  # This is a list that will represent a gamble with a 50% chance of winning
SeventyGamble = [1,1,1,0]  # This is a list that will represent a gamble with a 75% chance of winning
TwentyGamble = [1,0,0,0] # This is a list that will represent a gamble with a 25% chance of winning
resultStr=[] # create an empty list that we will fill up later
totalTime = [] # create another empty list that we will fill up later!


# This part is a bit more complicated, but it just builds off of everything we've seen so far - most of the following code chunk is more python than psychopy, meaning we're not so much using psychopy functions and stimuli as much as we are using variables and functions that we'll define
# We are now creating a "class"; a class can be used for a bunch of different things, but we're going to be using it to hold together functions
# Notably, we're using a class to hold together RELATED functions
# Normally, if we were to define two functions that use the same variable, the second function would ot be able to know what was happening within the first function, so if a shared variable was changed in the first function, the second function would still be using the original, unchanged variable
# This is because functions are considered LOCAL instead of GLOBAL; in other words, changes that occur within a function stay therefore
#But we need to change variables and call on those changed variables! So we're going to use a class to hold two functions together -
class Spam(): # like our functions, we can call our class anything we want, this one I'm calling Spam
    def randomProbabilitySelection(self, y, z): # now we're defining a function within our class, and telling it that we need three arguments - this is a bit of a trick however, because when we call on this function later, we're only going to give it TWO arguments
    # this is because we need to add 'self' as an argument in our function to BIND our object (in this case, our function 'randomProbabilitySelection') with our class (Spam)
        if choiceKeys.keys  == '1': # we're using a conditional if statement now, that says if we pressed '1' in the trial...:
            if '50' in leftProbability.text: # Oh no! Another if statement! This is considered a NESTED if statement, because we had one if (line 218) and now another, so you can read this as - if we pressed '1' in the trial AND if the probability shown on screen was 50, then...:
                result=random.choice(FiftyGamble) # we're going to create a variable called random and assign it to the outcome of a random selection function
                #  random.choice() is a function that randomly selects one thing from a list; if our script is reading this line it means that the above two if conditions were met, and the participant chose the gamble choice, which had a 50% probability
                # so we're going to randomly select from our list that represent a 50% chance (FiftyGamble)
                # Because our list consists of 0 and 1 , we will either get an output of 0 OR 1
                if result == 1: # And more nested if statements! After we randomly selected from our FiftyGamble list, if the outcome was a 1...:
                    print("won the 50% gamble") # That means we won the gamble! This print statement will appear in the terminal, but NOT on screen -- print statements are very useful for workshopping more complex code, because you can see if your script is working!
                    resultStr.append("Won") # Now we're adding a string, "Won" to our initially empty list that we defined in line 205
                    self.timeEarned = y # and we're creating a new variable called "timeEarned", BINDING IT, using 'self' and assigning it the value of an argument that we input when we call on the function -  when we call on this function, this argument is going to represent the time shown on screen for the gamble option
                if result == 0: # So instead when we randomly selected something from our list, if we got a 0..:
                    print("Lost the 50% gamble") # we lost the gamble!
                    resultStr.append("Lost") # and now we're adding a different string, "Lost" to our list resultStr
                    self.timeEarned = '0' # and assigning the value of that binded variable, timeEarned, to 0, meaning we did not earn any time cuddling animals
                    # so we're going to continually update the value of this variable depending on if we won or lost gambles, and we'll see why we had to bind it in a second

             # but for now, we have to cover our bases with the rest of the gamble probabilities
            if '25' in leftProbability.text: # Because this is still nested within the for loop on line 218, this if statement will run if the gamble was chosen (i.e., they pressed the 1 key) and the gamble on screen was 25%..:
                result=random.choice(TwentyGamble) # we're going to randomly select from our OTHER list, this time, from the list representing a probability of 25%
                if result == 1: #Again, if 1 was the randomly selected item, we won the gamble!
                    print("Won the 25% gamble")
                    resultStr.append("Won") # and we're adding 'Won' to our list that tracks our gamble results
                    self.timeEarned = y # and again assigning the BINDED variable to the time in our argument ( we won some amount of time cuddling animals, the specific amount of time depends on that argument)
                if result == 0: # If 0 was randomly selected from our 25% chance list, we lost the gamble
                    print("Lost the 25% gamble")
                    resultStr.append("Lost") # Add 'Lost' to the list keeping track of our outcomes
                    self.timeEarned = '0' # Assign the binded variable to 0, meaning we did not earn any time cuddling animals

            if '75' in leftProbability.text: #this is still nested within the for loop on line 218, so this if statement will run if the gamble was chosen (i.e., they pressed the 1 key) and the gamble on screen was 75%..:
                result=random.choice(SeventyGamble) # now randomly select from our list representing a 75% chance, and assign the outcome to the variable result
                if result == 1: # If 1 was randomly selected...
                    print("Won the 75% gamble") # We won!
                    resultStr.append("Won") # Add 'Won' to our list
                    self.timeEarned = y # And again assigning the BINDED variable to the time in our argument ( we won some amount of time cuddling animals, the specific amount of time depends on that argument)
                if result == 0: # If 0 was randomly selected
                    print("Lost the 75% gamble") # We lost
                    resultStr.append("Lost") # Add "lost" to the list
                    self.timeEarned = '0' # And assign the binded variable to 0, meaning we did not earn any time cuddling animals
        if choiceKeys.keys == '2': # Now, notice where this if statement is -- we are lined up with the first if statement -- so we are NO LONGER NESTED; this if statement means - if the participant pressed 2 on their keyboard, then ...:
            resultStr.append("Chose sure option") # That means they did not gamble, and chose the sure option, so now we're adding a new string to that same list that tracks all of our outcomes
            self.timeEarned = z # We are still using the same binded variable, but now we're assigning the value to OUR OTHER ARGUMENT - when we call on this function, this argument is going to represent the time shown on screen for the sure option
            print("Chose sure option")
        thisExp.addData("Feedback Results", resultStr[-1]) # Now we're adding some data to the output file - we want to have the outcome of each trial, whether it was winning a gamble, losing a gamble, or choosing the sure option. So we're going to use the list that we've been appending, grab the last item in the list (the [-1] that we've seen before), and add that to our data
        thisExp.addData("Time Earned", self.timeEarned) # We're also saving the data for the time that's been earned in that trial

    def feedbackFunc(self): # We are now defining a new function, which is still located in the class - so it's going to be related to that first function. While we don't have a regular argument in the parentheses, we do have 'self' again - this is because we'll be using that binded variable from the first function
        continueRoutine = True # keep it going
        feedbackText.setText("You won " + self.timeEarned + " minutes cuddling animals") # In this routine, we're giving participants feedback and telling them how much time they earned from the previous trial. We're going to set the text of a text stimulus to concatenate a regular string with the BINDED VARIABLE, so we can give accurate feedback!
        totalTime.append(int(self.timeEarned)) # Now, we are adding the time that was earned to an initially empty list, so we'll eventually have a list of all of the minutes that were earned
        feedbackText.setAutoDraw(True) # display the text
        win.flip() # keep the window open
        core.wait(3.500) # have the feedback stay on screen for 3.5 seconds
        if defaultKeyboard.getKeys(keyList=["escape"]): # and keep our safety measure handy
            core.quit()
        feedbackText.setAutoDraw(False) # after 3.5 seconds, make the text disappear
        print("Total Time List", totalTime) # this is just another print statement that allows us to see if  our list is being updated
        return totalTime # this is making sure we're having the most updated version of our list, which we're going to call on later
        thisExp.nextEntry() # move on to the next part in the script!
s=Spam() # this is doing something called instantiating our class, Spam, and assigning it to a variable called 's'
#this is going to allow us to access our functions within our class using a 'dot operator'; we'll see that in a little bit


# We're almost ready to run the script! Just a few more things to set up -
cueArray = ["RISKS ARE FUN", "BETTER SAFE THAN SORRY", "CHOICE"] # We're creating lists of text that will be used in our regulationCues function
leftImgArray = ["deer.jpg", "el.jfif", "alli.jpg", "tiger.jpg"] # And lists of images that will be used in our choiceFunc function, but specifically for our variable leftImage, these images are going to be associated with the risky choice
sureImgArray = ["ducks.jpg", "lion.jfif", "squ.jpg", "bun.jpg"] # another list of images that will be used in our choiceFunc function, but this time for our variable rightImage, these are going to be the images associated with the "sure" choice
rightTimeArray = ["5", "3", "4", "9"] # A list of the times in minutes that will appear on the right side of the screen
leftTimeArray = ["16", "18", "13", "15"] # A list of the times in minutes that will appear on the left side of the screen - as the left side is going to be the gamble side, we're going to have greater time amounts in this list to encourage risk-taking!

random.shuffle(leftImgArray) # as good practice, we're going to shuffle the order of the images in our list
random.shuffle(sureImgArray)

# Almost ready! Last thing we need is some text for our instructions! If you remember when we defined our function, we had a textArg argument that was acting as a placeholder for text that would eventually appear on screen
# So we're going to create yet another list, with the different text we want to have in our instructions function:
instructionsArray = ["Welcome!", "In this task, you will be making risky decisions about how you might spend your time."]


# IT'S SHOWTIME!!!!
# Now we're actually going to run the task!
# First, we're going to call on our instructionsFunction that we made all the way in the beginning - BUT - we're going to do so within a 'for' loop
#So, we're going to say, for each item in our list (instructionsArray), run our instructionsFunction with that item as the text that appears
for i in instructionsArray:
    instructionsFunction(i)
#Because we had two items in our list, it is going to loop through our instructionsFunction twice!

#Then, we're going to have our fixation cross appear
isiFunc(2.00) # Call on our ISI function, and using our time argument, we're going to tell it to run for 2 seconds

# Now this is the main part of our task!
# We're starting with another for loop, this time saying for each item in our list cueArray (there are three items in that list, so we know it's going to loop through the following code three times)
for i in cueArray:
    regulationCues(i) # run our regulation Cues function, using the item in the cueArray list as the regulation text that appears on screen
    isiFunc(1.500) # run our isi function again, this time only showing the fixation cross for 1.5 seconds
    for (a, b, c, d, e) in zip(leftImgArray, sureImgArray, leftTimeArray, leftProbArray, rightTimeArray): # now we're using ANOTHER for loop, but this one is a bit more complex
    # instead of just saying, for each item in a list..., we're doing that for multiple lists -- so line 311 is saying - for each item in list leftImgArray AND for each item in list sureImgArray AND for each item in leftTimeArray AND for each item in leftProbArray AND LASTLY for each item in rightTimeArray
    # because we now have a NESTED for loop , meaning a for loop within a foor loop, we're going to be looping through each item in the above lists (there are 4 in each list) for the below functions AND THEN coming back to the first loop, and doing that two more times
    # So in total, we're going to have 12 iterations - 4 choice trials for each of the three regulation cues
        choiceFunc(a, b, c, d, e) # Now we're calling on that relatively big choice function, making sure to add variables for each argument - you can see the arguments in in line 147 - we have to make sure we are matching up the right arguments!!
        isiFunc(1.50) # call our isi function again, using 1.5 seconds as our time argument
        s.randomProbabilitySelection(c, e) # Now we're using that dot operator we talked about in line 277 to call the first function of our class Spam, which played out the probability of the gamble - note that this only has two arguments!
        isiFunc(1.50)# call our isi function again, using 1.5 seconds as the time
        s.feedbackFunc() # Now we're using the SECOND function our our Spam class, which is showing us the result of our choice -- if we gambled, did we win or lose? and if we did not gamble, how much time did we get?
        isiFunc(3.00) # call our isi function one last time, showing the fixation for 3 seconds

sumTime = sum(totalTime) # We will want to know how much time the participants accumulated throughout the task, so we're going to sum up everything in that list we made


# We're going to call on our instructionsFunction one last time to have an ending screen where we tell participants how much total time they earned cuddling animals
#The function is going to operate exactly the same as before, but our argument is just going to look a bit different
#We're going to have some regular text in quotes, then we want to add in that total time earned, BUT, it is currently a number, not a string! Python won't allow non-strings to act as the text parameter in a text stimuli, so we have to convert it to a string using str()
#We're also going to surround that with + signs, which will smush our text and newly converted string together to make one sentence
instructionsFunction("Thank you for participating! Your total amount of time earned to cuddle animals is " + str(sumTime) + " minutes!")
# AND THE EXPERIMENT IS DONE!!!! WOOOOOOOOOOO!!
