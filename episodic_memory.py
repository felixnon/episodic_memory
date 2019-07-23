from __future__ import unicode_literals, print_function, division
from psychopy import gui, visual, event, core, monitors
from psychopy.tools.monitorunittools import posToPix

import random
import math

random.seed()

# open a dialog window and promt for subject_nr
myDlg = gui.Dlg(title=" ")
myDlg.addText('Participant info')
myDlg.addField('Subject number:')
subject_nr = 1# myDlg.show()[0]

#
# EXPERIMENT SETTINGS
#
nBlocks = 2                        # amount of study and test blocks
nTrialsPerBlock = 3                # amount of word location pairs per block

#
# TECHNICAL SETTINGS
#
continueKey = "right"               # the key to proceed in the experiment
resultDir = "results/"              # save results in this directory
resultFile = str(subject_nr) + ".csv" # name of the file containing a participants results
wordFile = "words.txt"              # file containing the words
circleRadius = 300                  # radius of the presented circle
circleLineWidth = 10                # width of the circle outline
circleEdges = 128                   # amount of edges to draw the circle

#
# TEXT MESSAGES
#
instructionMessage = '''In diesem Experiment wird jeweils ein Wort mit einer Position auf einem Kreis verknüpft. Du musst dir merken, zu welchem Wort welche Position gehört.
Das Experiment besteht aus mehreren Blöcken. Pro Block werden Dir {} Positions-Wort-Verbindungen präsentierst. Anschließend wirst du abgefragt. Dazu wird dir das Wort gezeigt und du musst die Position auf dem Kreis bestimmen.
Wir beginnen mit ein paar Übungsdurchläufen.

Drücke eine beliebige Taste wenn du bereit bist.'''

studyBlockStartMessage = '''Block {} / {}
>Lernphase<

Versuche Dir zu merken welches Wort mit welcher Position auf dem Kreis verknüpft war.

Drücke eine beliebige Taste wenn du bereit bist.'''

studyBlockCompleteMessage = '''Block {} / {}
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

nextStudyTrialMessage = '''Lernphase Trial {}/{}
Drücke eine beliebige Taste das Trial zu starten.'''


nextTestTrialMessage = '''Testphase Trial {}/{}
Drücke eine beliebige Taste zum fortfahren.'''

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

win.fullscr=True
win.winHandle.set_fullscreen(True)
win.flip()

# keep increasing these variables.
currentBlock = 0
currentTrial = 0

# Create the results file and add the csv header containing the needed collumns
with open(resultFile, "w") as f:
    print("subject_nr,id,block,trial,isTest,word,position,selectedPos,clickPosX,clickPosY,rt,rtFinal", file=f)

instructions = visual.TextStim(win, instructionMessage, wrapWidth=1000, alignVert='center')

# load the words from file and randomize them
words = []
with open(wordFile, "r") as f:
    words = f.read().splitlines()
random.shuffle(words)

# pair words with a random location on circle outline
stimuli = [(word, random.randint(0, 359)) for word in words]

practiceStimuli = [("word1", 15),
                   ("word2", 30),
                   ("word3", 45),
                   ("word4", 60)]
                   #("word5", 75),
                   #("word6", 90),
                   #("word7", 105),
                   #("word8", 120),
                   #("word9", 135)]

# make sure there are not more trials than words
if nBlocks * nTrialsPerBlock > len(stimuli):
    raise Exception("There are more trials than words. Use larger word list or less trials.")

#
#
#

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
    
    return degrees

    
def selectPointOnCircle():

    text = visual.TextStim(win, selectPointMessage)
            
    # get an instance of the mouse in order to get clicks and position
    mouse = event.Mouse()
    # 
    pos = (None, None)
    
    while True:
        check_esc()
        
        circle = getCircleStim()
        circle.draw()
        
        text.draw()
        
        buttons = mouse.getPressed()
        if buttons[0]:
            pos = degreesToPos(posToDegrees(mouse.getPos()))
        if pos[0] != None and pos[1] != None:
            cross = visual.Circle(win, 10, lineWidth=1, pos=pos, lineColor='Red', fillColor='Red')
            cross.draw()
            
            if "return" in event.getKeys():
                win.flip()
                break
        win.flip()
    return pos
    
    
def writeText(text, duration = None):
    '''
    displays an text on the screen.
    Parameters:
        text: the displayed text
        duration: the duration the text is displayed. if none, wait for key press
    '''
    textStim = visual.TextStim(win, text)
    textStim.draw()
    win.flip()
    
    if duration:
        core.wait(duration)
    else:
        event.waitKeys()
    
    check_esc()
    win.flip()

def studyTrial(word, angle):
    writeText(nextStudyTrialMessage)
    writeText("+", 2)
    core.wait(1)
    drawCircleWithCross(angle)
    core.wait(2)
    win.flip()
    writeText(word, 2)
    markerAngle = selectPointOnCircle()
    
def testTrial(word, angle):
    writeText(nextTestTrialMessage)
    writeText("+", 1)
    core.wait(0.5)
    writeText(word, 2)
    core.wait(1)
    markerAngle = selectPointOnCircle()
    
def startPracticeTrials():
    # study trials
    for stimulus in practiceStimuli:
        studyTrial(*stimulus)
        
    writeText(studyBlockCompleteMessage)
    # test trials
    random.shuffle(practiceStimuli)
    for stimulus in practiceStimuli:
        testTrial(*stimulus)
    
    writeText(practiceCompleteMessage)



#
# Experiment Procedure
# 

instructions.draw()
win.flip()
event.waitKeys()
# start the practice trials
#startPracticeTrials()

# start the experiment
for block in range(nBlocks):
    currentBlock = block

    # get the subset of stimuli that will be presented in the current block
    blockStimuli = stimuli[block*nTrialsPerBlock : (block+1)*nTrialsPerBlock]
    
    # study trials
    writeText(studyBlockStartMessage)
    #for stimulus in blockStimuli:
    #    studyTrial(*stimulus)
    for trial in range(nTrialsPerBlock):
        currentTrial = trial
        studyTrial(*blockStimuli[trial])
        
        
    writeText(studyBlockCompleteMessage)
    
    # test trials
    random.shuffle(blockStimuli)
    #for stimulus in blockStimuli:
    #    testTrial(*stimulus)
    for trial in range(nTrialsPerBlock):
        currentTrial = trial
        testTrial(*blockStimuli[trial])
        
writeText(experimentCompleteMessage)

win.close()
core.quit()
