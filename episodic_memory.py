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
nBlocks = 15                        # amount of study and test blocks
nTrialsPerBlock = 16                # amount of word location pairs per block

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

# Create the results file and add the csv header containing the needed collumns
with open(resultFile, "w") as f:
    print("subject_nr,id,action,object,correct_answer,answer,rt", file=f)

instructions = visual.TextStim(win,'''In this experiment bla bla bla...''', wrapWidth=1000, alignVert='center')

# load the words from file and randomize them
words = []
with open(wordFile, "r") as f:
    words = f.read().splitlines()
random.shuffle(words)

# pair words with a random location on circle outline
pairs = [(word,random.randint(0,359)) for word in words]

# make sure there are not more trials than words
if nBlocks * nTrialsPerBlock > len(pairs):
    raise Exception("There are more trials than words. Use larger word list or less trials.")

#
#
#

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

    text = visual.TextStim(win, 
                            "An welcher Stelle hast Du das Kreuz gesehen? \n" +
                            "Klicke auf den Kreis um eine Markierung zu setzen. \n" +
                            "Du kannst beliebig oft die Position ändern. \n" +
                            "Wenn Du Dich entschieden hast, drücke die Enter-Taste."
                            )
            
    # get an instance of the mouse in order to get clicks and position
    mouse = event.Mouse()
    # 
    pos = (None, None)
    
    while True:
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
    win.flip()

def studyTrial(word, angle):
    writeText("Press any key to proceed...")
    writeText("+", 2)
    core.wait(1)
    drawCircleWithCross(angle)
    core.wait(2)
    win.flip()
    writeText(word, 2)
    markerAngle = selectPointOnCircle()
    
def testTrial(word, angle):
    writeText("+", 1)
    core.wait(0.5)
    writeText(word, 2)
    core.wait(1)
    markerAngle = selectPointOnCircle()
    

#
#
#






#instructions.draw()
win.flip()
#event.waitKeys()
win.flip()
core.wait(.5)

studyTrial("wort",1)
#for block in range(nBlocks):
    
    # study trials
    

win.close()
core.quit()
