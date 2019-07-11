from __future__ import unicode_literals, print_function, division
from psychopy import gui, visual, event, core, monitors

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



instructions.draw()
win.flip()
core.wait(.5)

win.close()
core.quit()
