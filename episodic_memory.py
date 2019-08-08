from __future__ import unicode_literals, print_function, division
from psychopy import gui, visual, event, core, monitors
from psychopy.tools.monitorunittools import posToPix

import random
import math
import os

random.seed()

# open a dialog window and promt for subject_nr
myDlg = gui.Dlg(title=" ")
myDlg.addText('Participant info')
myDlg.addField('Subject number:')
subject_nr = myDlg.show()[0]

#
# EXPERIMENT SETTINGS
#
nBlocks = 2                      # amount of study and test blocks
nTrialsPerBlock = 2              # amount of word location pairs per block
doPracticeTrials = False         # whether the experiment should start with practice trials

#
# TECHNICAL SETTINGS
#
resultDir = "results/"              # save results in this directory
resultFile = resultDir + str(subject_nr) + ".csv" # name of the file containing a participants results
wordFile = "words.txt"              # file containing the words
circleRadius = 300                  # radius of the presented circle
circleLineWidth = 10                # width of the circle outline
circleEdges = 128                   # amount of edges to draw the circle

#
# TEXT MESSAGES
#
instructionMessage = '''In diesem Experiment wird jeweils ein Wort mit einer Position auf einem Kreis verknüpft. Du musst dir merken, zu welchem Wort welche Position gehört.
Das Experiment besteht aus mehreren Blöcken. Pro Block werden Dir {nTrialsPerBlock} Positions-Wort-Verbindungen präsentierst. Anschließend wirst du abgefragt. Dazu wird dir das Wort gezeigt und du musst die Position auf dem Kreis bestimmen.
Wir beginnen mit ein paar Übungsdurchläufen.

Drücke eine beliebige Taste wenn du bereit bist.'''

studyBlockStartMessage = '''
                        Block {currentBlock}/{nBlocks}

                        >Lernphase<

Versuche Dir zu merken welches Wort mit welcher Position auf dem Kreis verknüpft war.

Drücke eine beliebige Taste wenn du bereit bist.'''

studyBlockCompleteMessage = '''
                        Block {currentBlock}/{nTrialsPerBlock}

                        >Testphase<

Erinnere Dich welche Position auf dem Kreis zu welchem Wort gehört. Du kannst die Position mit einem Mausklick festlegen. Die Position kannst Du beliebig oft korriegieren.
Um Deine Auswahl zu bestätigen musst Du die Enter-Taste drücken.

Drücke eine beliebige Taste wenn du bereit bist.'''

practiceCompleteMessage = '''Du hast die Übungsdurchläufe abgeschlossen. Falls Du noch Fragen haben solltest, wende dich an die Experimentleitung.
Ansonsten kannst du das Experiment durch Drücken einer beliebigen Taste starten.

Viel Spaß!'''

experimentCompleteMessage = '''Das Experiment ist abgeschlossen. 
Vielen Dank für Deine Teilnahme.'''

selectPointMessage = '''Wähle mit der Maus die mit dem gezeigten Wort verknüpfte Position auf dem Kreis aus.
Du kannst die Position beliebig oft korriegieren. 
Deine Auswahl kannst du mit der Enter-Taste bestätigen.'''

nextStudyTrialMessage = '''
                Lernphase Trial {currentTrial}/{nTrialsPerBlock}

Drücke eine beliebige Taste das Trial zu starten.'''


nextTestTrialMessage = '''
                Testphase Trial {currentTrial}/{nTrialsPerBlock}
                
Drücke eine beliebige Taste zum fortfahren.'''

retryVerification = '''Deine Antwort war zu ungenau. Probiere es nochmal.
Drücke eine beliebige Taste zum fortfahren.'''

#
# SETUP EXPERIMENT
#

m = monitors.Monitor("monitor", distance=90, autoLog=True)
m.save()
win = visual.Window(
                    size = [1920,1080],
                    monitor=m,
                    units='pix', 
                    winType='pyglet', 
                    color=-.5,
                    fullscr=True
                    #screen=1,
                    #allowGUI=False
                    )
clock = core.Clock()
win.winHandle.set_fullscreen(False) 
win.flip()
win.mouseVisible = False
win.fullscr=True
win.winHandle.set_fullscreen(True)
win.flip()

# These variables will keep track of the current block and trial number
currentBlock = 0
currentTrial = 0

# Create the results file and add the csv header containing the needed collumns
try:
    os.makedirs(resultDir)
except FileExistsError:
    # directory already exists
    pass
with open(resultFile, "w") as f:
    print("subject_nr,id,block,trial,isTest,word,angle,selectedAngle,error,clickPosX,clickPosY,rt,rtFinal", file=f)

# load the words from file and randomize them
words = []
with open(wordFile, "r") as f:
    words = f.read().splitlines()
random.shuffle(words)

# create the stimuli pairs.
# to do so, pair words with a random location on circle outline
stimuli = [(word, random.randint(0, 359)) for word in words]

# the stimuli used for the practice trials
practiceStimuli = [("word1", 15),
                   ("word2", 30),
                   ("word3", 45),
                   ("word4", 60)]

# make sure there are not more trials than words
if nBlocks * nTrialsPerBlock > len(stimuli):
    raise Exception("There are more trials than words. Use larger word list or less trials.")

#
# HELPER FUNCTIONS
#

def evaluateText(text):
    text = text.format(nBlocks=nBlocks,
                       nTrialsPerBlock=nTrialsPerBlock,
                       currentBlock=currentBlock+1, # add 1 so counting starts with 1 instead of 0
                       currentTrial=currentTrial+1)                       
    return text

def check_esc():
    if event.getKeys(['escape']):
        win.close()
        core.quit()

def getCircleStim():
    circle = visual.Circle(win, 
                           circleRadius, 
                           lineWidth=circleLineWidth, 
                           edges=circleEdges)
    return circle

def drawCircle():
    getCircleStim().draw()
    win.flip()
    
def drawCircleWithCross(degrees):
    circle = getCircleStim()
    circle.draw()
    
    posX, posY = degreesToPos(degrees)
    
    cross = visual.Circle(win, 10, lineWidth=1, pos=(posX,posY), lineColor='Black', fillColor='Black')
    cross.draw()
    
    win.flip()
    
    
def calculateError(alpha, beta):
    '''
    calculates the distance in degrees of the angles alpha and beta
    Parameters:
        alpha: angle in degrees
        beta:  angle in degrees
    '''
    phi = abs(beta-alpha) % 360
    distance = phi if phi < 180 else 360 - phi
    
    return distance

def degreesToPos(degrees):
    # calculate the position of the cross using the radius and angle
    rad = degrees * (math.pi/180)
    xRelative = circleRadius * math.cos(rad)
    yRelative = circleRadius * math.sin(rad)    
    posX = xRelative #+ posToPix(circle)[0]
    posY = yRelative #+ posToPix(circle)[1]
    
    return posX, posY
    
def posToDegrees(pos):
    rad = math.atan2(pos[1], pos[0])
    degrees = rad * 180 / math.pi
    degrees = (degrees + 360) % 360
    return degrees

    
def selectPointOnCircle():
    
    text = visual.TextStim(win, selectPointMessage)
            
    # get an instance of the mouse in order to get clicks and position
    mouse = event.Mouse()
    mouse.clickReset()
    mouse.setPos((0, 0))
    clock.reset()
    
    win.mouseVisible = True
    
    rts = []
    rtFinal = None
    pos = (None, None)
    clickX = 0
    clickY = 0
    
    while True:
        check_esc()
        
        circle = getCircleStim()
        circle.draw()
        
        text.draw()
        
        buttons, rt = mouse.getPressed(getTime=True)
        if buttons[0]:
            event.clearEvents("keyboard")
            pos = degreesToPos(posToDegrees(mouse.getPos()))
            clickX, clickY = mouse.getPos()
            rts.append(rt[0])
        if pos[0] != None and pos[1] != None:
            cross = visual.Circle(win, 10, lineWidth=1, pos=pos, lineColor='Red', fillColor='Red')
            cross.draw()
            
            keypresses = event.getKeys(keyList=["return"], timeStamped=clock)
            if keypresses:
                key, rt = keypresses[0]
                if key == "return" :
                    rtFinal = rt
                    win.flip()
                    break
        win.flip()
        
    angle = posToDegrees(pos)
    
    win.mouseVisible = False
    
    return angle, rts[0], rtFinal, clickX, clickY
    
    
def writeText(text, duration = None, font='', pos=(0.0, 0.0), depth=0, rgb=None, color=(1.0, 1.0, 1.0), 
                colorSpace='rgb', opacity=1.0, contrast=1.0, units='', ori=0.0, height=None, antialias=True, 
                bold=False, italic=False, alignHoriz='center', alignVert='center', fontFiles=(), wrapWidth=None, 
                flipHoriz=False, flipVert=False, languageStyle='LTR', name=None, autoLog=None):
    '''
    displays an text on the screen.
    Parameters:
        text: the displayed text
        duration: the duration the text is displayed. if none, wait for key press
    '''
    text = evaluateText(text)
    textStim = visual.TextStim(win, text, font, pos, depth, rgb, color, 
                colorSpace, opacity, contrast, units, ori, height, antialias, 
                bold, italic, alignHoriz, alignVert, fontFiles, wrapWidth, 
                flipHoriz, flipVert, languageStyle, name, autoLog)
    textStim.draw()
    win.flip()
    
    if duration:
        core.wait(duration)
    else:
        event.waitKeys()
    
    check_esc()
    win.flip()

def addTrialToCSV(subject_nr=subject_nr,
                  id=-1,
                  block=-1,
                  trial=-1,
                  isTest=None,
                  word=None,
                  angle=None,
                  selectedAngle=None,
                  error=None,
                  clickPosX=None,
                  clickPosY=None,
                  rt=-1,
                  rtFinal=-1):
    
    if id == -1:
        id = currentBlock*nTrialsPerBlock+currentTrial
    if block == -1:
        block = currentBlock
    if trial == -1:
        trial = currentTrial
    
    preparedString = "{},{},{},{},{},{},{},{},{},{},{},{},{}".format(subject_nr,id,block,trial,isTest,word,angle,selectedAngle,error,clickPosX,clickPosY,rt,rtFinal)
    with open(resultFile, "a") as f:
        print(preparedString, file=f)


def studyTrial(word, angle, isPractice=False):
    writeText(nextStudyTrialMessage)
    writeText("+", 2)
    core.wait(1)
    drawCircleWithCross(angle)
    core.wait(2)
    win.flip()
    writeText(word, 2)
    markerAngle, rt, rtFinal, clickPosX, clickPosY = selectPointOnCircle()
    error = calculateError(angle, markerAngle)
    
    while error > 6:
        writeText(retryVerification)
        drawCircleWithCross(angle)
        core.wait(0.25)
        win.flip()
        markerAngle, rt, rtFinal, clickPosX, clickPosY = selectPointOnCircle()
        error = calculateError(angle, markerAngle)
        
    addTrialToCSV(isTest=False,
                  word=word,
                  angle=angle,
                  selectedAngle=markerAngle,
                  error=error,
                  clickPosX=clickPosX,
                  clickPosY=clickPosY,
                  rt=rt,
                  rtFinal=rtFinal)
    
def testTrial(word, angle, isPractice=False):
    writeText(nextTestTrialMessage)
    writeText("+", 1)
    core.wait(0.5)
    writeText(word, 2)
    core.wait(1)
    markerAngle, rt, rtFinal, clickPosX, clickPosY = selectPointOnCircle()
    error = calculateError(angle, markerAngle)
    
    addTrialToCSV(isTest=True,
                  word=word,
                  angle=angle,
                  selectedAngle=markerAngle,
                  error=error,
                  clickPosX=clickPosX,
                  clickPosY=clickPosY,
                  rt=rt,
                  rtFinal=rtFinal)
    
def startPracticeTrials():
    # study trials
    for stimulus in practiceStimuli:
        studyTrial(*stimulus, isPractice=True)
        
    writeText(studyBlockCompleteMessage)
    # test trials
    random.shuffle(practiceStimuli)
    for stimulus in practiceStimuli:
        testTrial(*stimulus, isPractice=True)
    
    writeText(practiceCompleteMessage)


#
# Experiment Procedure
# 

writeText(instructionMessage, wrapWidth=1000)

# start the practice trials
if doPracticeTrials:
    startPracticeTrials()

# start the actual experiment
for block in range(nBlocks):
    currentBlock = block

    # get the subset of stimuli that will be presented in the current block
    blockStimuli = stimuli[block*nTrialsPerBlock : (block+1)*nTrialsPerBlock]
    
    # study trials
    writeText(studyBlockStartMessage)
    
    
    for trial in range(nTrialsPerBlock):
        currentTrial = trial
        studyTrial(*blockStimuli[trial])
        
        
    writeText(studyBlockCompleteMessage)
    
    # test trials
    random.shuffle(blockStimuli)
    
    for trial in range(nTrialsPerBlock):
        currentTrial = trial + nTrialsPerBlock
        testTrial(*blockStimuli[trial])
        
writeText(experimentCompleteMessage)

win.close()
core.quit()
