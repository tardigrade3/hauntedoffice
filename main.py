"""
Haunted Office
J Kirney
A game where the user tries to collect items before the time runs out while being chased by ghosts.
"""

import pgzrun
import pygame
import random

WIDTH = 1000
HEIGHT = 600

# player
player = Actor('stickmanyellow')

# ghosts
ghosts = [] # the ghosts
ghostXdirection = [] # horizontal movement for each ghost: if the value of an item is positive, the corresponding ghost will move right; if it is negative, the ghost will move left
ghostYdirection = [] # vertical movement for each ghost: if the value of an item is positive, the corresponding ghost will move up; if negative, the ghost will move down
ghostOverlapping = [] # stores whether each ghost should move away from the other ghosts to prevent overlap

# obstacles
obstacles = [] # player can't move through obstacles

# tasks
taskObject = Actor('pinksquare') # touch to earn a point
completed = -1 # how many points earned/tasks completed
currentTaskType = 'simple' # type of task ('simple', 'multi', 'hidden', or 'final')
taskObjects = [] # items for 'multi' tasks
gathered = 0 # if currentTaskType == 'multi' --> how many items have been collected?
hiddenIndex = -1 # if currentTaskType == 'hidden' --> index of obstacles where task object is hidden; for all other task types, hiddenIndex = -1

# colours
darkBlue = 0, 0, 32
gray = 191, 185, 195
loudPink = 247, 23, 121
lightGray = 238, 238, 238
darkPink = 109, 23, 56
ghostBlue = 230, 251, 255
yellow = 255, 167, 0
lightYellow = 255, 211, 128

# other variables & lists
playerFrozen = False # has the player been frozen by a ghost?
inLevel = False # is the player currently playing a level?
timeLeft = 0 # how much time is left in the level
level = 0 # current level (the value of level is 1 less that the actual level, for example level = 0 during level 1)
toComplete = 0 # how many points are needed to win the level?
whatsHappening = 'intro' # if not currently in level, what's happening?
levelStartBg = ['levelo', 'leveli', 'levelio', 'levelii', 'levelioo', 'levelioi', 'leveliio', 'leveliii', 'leveliooo', 'leveliooi'] # image to use at start of level
pauseImage = 'pause' # what image to use for pause button

# functions
def draw():
    """
    Draws the game on the screen
	Args
		None
	Returns
		None
    """

    # gameplay
    if whatsHappening == 'gameplay':
        # background colour
        screen.fill(gray)
        # player
        player.draw()
        # task items (hidden task items will be hidden behind obstacles)
        if currentTaskType == 'multi':
            for i in taskObjects:
                screen.draw.filled_rect(i, loudPink)
        else:
            taskObject.draw()
        # obstacles
        for i in obstacles:
            screen.draw.filled_rect(i, darkBlue)
        # ghosts (ghosts are visible in front of obstacles)
        for ghost in ghosts:
            ghost.draw()
        # time remaining in level
        screen.draw.text('Time left: {:02d}:{:02d}'.format(timeLeft // 60, timeLeft % 60), (20, 20), fontname = "barlow", fontsize = 20, color = yellow) # time formatting from https://stackoverflow.com/questions/134934/display-number-with-leading-zeros
        # score
        screen.draw.text('Score: {}/{}'.format(completed, toComplete), (20, 50), fontname = "barlow", fontsize = 20, color = yellow)
        # pause button
        if 950 <= mouse[0] <= 990 and 10 <= mouse[1] <= 50:
            screen.blit(pauseImage + 'select', (950, 10)) # change colour if mouse is over pause button
        else:
            screen.blit(pauseImage, (950, 10))

    # intro screen
    elif whatsHappening == 'intro':
        if 424 <= mouse[0] <= 576 and 425 <= mouse[1] <= 477: # highlight continue button
            screen.blit('introselect', (0, 0))
        else:
            screen.blit('intro', (0, 0))

    # start screen
    elif whatsHappening == 'start':
        if 420 <= mouse[0] <= 580 and 300 <= mouse[1] <= 350:
            screen.blit('startscreenstart', (0, 0)) # highlight start button
        elif 420 <= mouse[0] <= 580 and 350 <= mouse[1] <= 400:
            screen.blit('startscreeninstructions', (0, 0)) # highlight instructions button
        else:
            screen.blit('startscreen', (0, 0))
        screen.draw.text("Haunted Office", center = (500, 225), fontname = 'doctorglitch', fontsize = 68, color = ghostBlue)

    # instructions screen
    elif whatsHappening == 'instructions':
        if 420 <= mouse[0] <= 580 and 472 <= mouse[1] <= 535: # highlight start button
            screen.blit('instructionsselect', (0, 0))
        else:
            screen.blit('instructions', (0, 0))

    # start of level screen
    elif whatsHappening == 'level start':
        if 420 <= mouse[0] <= 580 and 464 <= mouse[1] <= 527: # highlight start button
            screen.blit(levelStartBg[level] + 'select', (0, 0))
        else:
            screen.blit(levelStartBg[level], (0, 0))

    # lose level screen
    elif whatsHappening == 'level end' and completed < toComplete:
        screen.fill(darkPink)

        screen.draw.text("Time's up!", center = (500, 120), fontname = "barlow", fontsize = 60, color = lightGray)
        screen.draw.text("You got {} of {} needed points".format(completed, toComplete), center = (500, 200),
                         fontname = 'barlow', fontsize=26, color = ghostBlue)
        screen.draw.text("You lose :((", center = (500, 300), fontname = "barlow", fontsize = 48, color = yellow)
        screen.draw.text("You didn't finish your tasks on time. Your coworkers' annoyance is\nsignificantly heightened by the fact that there are LITERALLY\nACTUAL GHOSTS EVERYWHERE.",
            center=(500, 400), align='center', fontname='barlow', color=gray, fontsize=18)
        # highlight replay level button
        if 710 <= mouse[0] <= 990 and 10 <= mouse[1] <= 60:
            screen.draw.text("Replay level ->", (720, 20), color = lightYellow, fontname = 'barlow', fontsize=35)
        else:
            screen.draw.text("Replay level ->", (720, 20), color = yellow, fontname = 'barlow', fontsize=35)

    # level won screen
    elif whatsHappening == 'level end':
        screen.fill(lightGray)
        screen.draw.text("Level {} completed".format(level), center = (500, 120), fontname = "barlow", fontsize = 60, color = loudPink)
        screen.draw.text("You got {} of {} needed points".format(completed, toComplete), center = (500, 200), fontname = 'barlow', fontsize = 26, color = darkBlue) # score
        screen.draw.text("You win! :D", center = (500, 300), fontname = "barlow", fontsize = 48, color = darkPink)
        screen.draw.text("You met all your deadlines despite all the ghosts in your office! Your\ncoworkers are astounded by your inhuman levels of productivity.", center = (500, 400), align = 'center', fontname = 'barlow', color = darkBlue, fontsize = 18)
        # highlight next level button
        if 710 <= mouse[0] <= 990 and 10 <= mouse[1] <= 60:
            screen.draw.text("Play next level ->", (720, 20), color = lightYellow, fontname = 'barlow', fontsize = 35)
        else:
            screen.draw.text("Play next level ->", (720, 20), color = yellow, fontname = 'barlow', fontsize=35)

    # I suppose this could be called a cutscene, but it's literally just two sentences of text
    elif whatsHappening == 'literally the worst cutscene':
        if 424 <= mouse[0] <= 576 and 348 <= mouse[1] <= 400: # highlight continue button
            screen.blit('blehselect', (0, 0))
        else:
            screen.blit('bleh', (0, 0))

    # player finished all levels (end of game screen)
    elif whatsHappening == 'entire game won':
        screen.fill(darkBlue)
        screen.draw.text('The end.', center = (500, 200), fontname = 'doctorglitch', fontsize = 68, color = loudPink)
        screen.draw.text('You give the doughnut to the ghosts, and they seem\nsatisfied. Hopefully they’ll finally leave you alone now.', center = (500, 300), fontname = 'barlow', align = 'center', color = lightGray, fontsize = 21)
        ghosts[0].draw()
        ghosts[1].draw()

def playerMove(ghosts, keepGhostDirection):
    """
    Allows the player to move, updates ghost movement direction, and checks if the player has completed a task
    Args
        ghosts: list of Actors
        The ghosts for this level
        keepGhostDirection: list of bools
        Whether each ghost will update its direction to move towards the player
    Returns
        ghostXdirection: list of ints
        1 for right, -1 for left, 0 for no horizontal movement
        ghostYdirection: list of ints
        1 for up, -1 for down, and 0 for no vertical movement
    """

    global taskObjects
    global gathered
    global hiddenIndex
    global obstacles

    # update ghost direction to move towards player
    for i in range(len(ghosts)):
        # don't go more than 5 px of the edge of the screen - horizontal
        if ghosts[i].midleft[0] < -5:
            ghostXdirection[i] = 1
        elif ghosts[i].midright[0] > WIDTH + 5:
            ghostXdirection[i] = -1

        # don't go more than 5 px off the edge of the screen - vertical
        if ghosts[i].midtop[1] < -5:
            ghostYdirection[i] = 1
        elif ghosts[i].midbottom[1] > HEIGHT + 5:
            ghostYdirection[i] = -1

        # go towards player
        if not keepGhostDirection[i]:
            if player.x - 0.5 <= ghosts[i].x <= player.x + 0.5:
                ghostXdirection[i] = 0
            else:
                ghostXdirection[i] = (player.x - ghosts[i].x) / abs(player.x - ghosts[i].x)
            if player.y - 0.5 <= ghosts[i].y <= player.y + 0.5:
                ghostYdirection[i] = 0
            else:
                ghostYdirection[i] = (player.y - ghosts[i].y) / abs(player.y - ghosts[i].y)

        # update each ghost's image to match the direction it is moving
        if ghostXdirection[i] == 1:
            # face right if going right
            ghosts[i].image = 'ghostr'
        elif ghostXdirection[i] == -1:
            # face left if going left
            ghosts[i].image = 'ghostl'

    # move player, don't go past edges
    if (keyboard.A or keyboard.LEFT) and player.midleft[0] > 0:
        player.x -= 3
        # can't go through  obstacles (except to find hidden task item)
        if player.collidelist(obstacles) not in [hiddenIndex, -1]:
            player.x += 3
    if (keyboard.D or keyboard.RIGHT) and player.midright[0] < WIDTH:
        player.x += 3
        # can't go through  obstacles (except to find hidden task item)
        if player.collidelist(obstacles) not in [hiddenIndex, -1]:
            player.x -= 3
    if (keyboard.W or keyboard.UP) and player.midtop[1] > 0:
        player.y -= 3
        # can't go through  obstacles (except to find hidden task item)
        if player.collidelist(obstacles) not in [hiddenIndex, -1]:
            player.y += 3
    if (keyboard.S or keyboard.DOWN) and player.midbottom[1] < HEIGHT:
        player.y += 3
        # can't go through  obstacles (except to find hidden task item)
        if player.collidelist(obstacles) not in [hiddenIndex, -1]:
            player.y -= 3

    # check if task is completed
    # multiple task items
    if currentTaskType == 'multi':
        if player.collidelist(taskObjects) > -1:
            taskObjects = taskObjects[:player.collidelist(taskObjects)] + taskObjects[player.collidelist(taskObjects) + 1:] # remove item from taskObjects
            gathered += 1 # record that the item has been found
            if gathered == 5:
                # new task once task is completed
                newTask(obstacles, 'multi')
    # check if player has found hidden item
    elif hiddenIndex > -1:
        if player.colliderect(obstacles[hiddenIndex]):
            # remove obstacle the task was hiding behind
            obstacles.remove(obstacles[hiddenIndex])
            hiddenIndex = -1
    # check if task has been completed (task types other than 'multi')
    elif currentTaskType in ['simple', 'hidden', 'final'] and taskObject.colliderect(player):
        newTask(obstacles, currentTaskType)

    return ghostXdirection, ghostYdirection

def unfreeze():
    """
    Ends ghost freeze effect (scheduled in update())
    Args
        None
    Returns
        None
    """
    global playerFrozen
    playerFrozen = False

def levelDone():
    """
    Ends the level
    Args
        None
    Returns
        None
    """
    global inLevel
    global whatsHappening
    global level
    global ghosts

    if inLevel: # prevent the pause button from breaking everything
        inLevel = False # no longer in level
        # if the last level has been completed
        if level == 9 and completed > 0:
            whatsHappening = 'entire game won'
            # prepare ghost animation
            ghosts = [Actor('ghostr'), Actor('ghostl')]
            ghosts[0].pos = (-100, 100)
            ghosts[1].pos = (1100, 450)

        else: # first 9 levels
            whatsHappening = 'level end'
            clock.unschedule(countdown) # stop countdown

        # go to next level if level won
        if completed >= toComplete:
            level += 1

def ghostContinue():
    """
    Makes all ghosts start following the player again (scheduled when ghosts get too close and start avoiding each other to avoid overlapping)
    Args
        None
    Returns
        None
    """
    # all ghosts will follow player again (could probably be more efficient)
    global ghostOverlapping
    ghostOverlapping = [False] * len(ghostOverlapping)

def newTask(noOverlap, taskType):
    """
    Makes a new task for the player
    Args
        noOverlap: list of Rects
        The list of level obstacles (so the task items don't generate inside obstacles)
        taskType: string ('simple', 'multi', 'hidden', or 'final')
        What type of task this level has
    Returns
        None
    """
    global completed
    global taskObjects
    global gathered
    global currentTaskType
    global hiddenIndex

    completed += 1 # give player a point
    currentTaskType = taskType # update currentTaskType if this is the first task in a level

    # single task item
    if taskType == 'simple':
        # randomly position taskObject
        taskObject.pos = random.randint(0, 999), random.randint(0, 599)
        # don't overlap with obstacles
        while taskObject.collidelist(noOverlap) > -1:
            taskObject.pos = random.randint(0, 999), random.randint(0, 599)

    # many task items
    elif taskType == 'multi':
        taskObjects = [] # get rid of any leftover task items
        # randomly place new task items
        for i in range(5):
            taskObjects.append(Rect((random.randint(-10, 990), random.randint(-10, 590)), (20, 20)))
            # don't overlap or generate in obstacles
            while taskObjects[i].collidelist(taskObjects) != i or taskObjects[i].collidelist(noOverlap) > -1: #([Rect((taskObjects[j][0][0] - 20, taskObjects[j][0][1] - 20), (60, 60)) for j in len(taskObjects)]) > -1:
                taskObjects[i] = Rect((random.randint(-10, 990), random.randint(-10, 590)), (20, 20))
        gathered = 0 # reset number of task items gathered

    # hidden item
    elif taskType == 'hidden':
        if noOverlap == []:
            # avoid breaking everything at the end of level 7
            currentTaskType = 'multi'
        else:
            # hide task behind a random Rect in obstacles
            hiddenIndex = random.randint(0, len(noOverlap) - 1)
            taskObject.center = noOverlap[hiddenIndex].center

    # final level
    elif taskType == 'final':
        hiddenIndex = -1 # clean up from previous levels with hidden items
        taskObject.pos = (500, 100)
        taskObject.image = 'doughnut'

def levelStart():
    """
    Gets everything ready for a new level
    Args
        None
    Returns
        newGhosts: list of Actors
        The ghosts for this level
        newGhostXdirection: list ([0] * number of ghosts)
        The X direction of each ghost
        newGhostYdirection: list ([0] * number of ghosts)
        The Y direction of each ghost
        newGhostOverlapping: list ([False] * number of ghosts)
        Whether each ghost should move away from the other ghosts to prevent overlap
        levelObstacles[level]: list of Rects
        The obstacles for this level
        levelTime[level]: int
        The duration of this level in seconds
        levelTaskTypes[level]: string ('simple', 'multi', 'hidden' or 'final')
        What type of task this level has
        levelTaskNum[level]: int
        The score needed to win this level
    """

    levelObstacles = [[Rect((0, 0), (1000, 200)), Rect((0, 400), (1000, 200))], [Rect((200, 200), (600, 200))], [Rect((100, 50), (200, 200)), Rect((400, 50), (200, 200)), Rect((700, 50), (200, 200)), Rect((100, 350), (200, 200)), Rect((400, 350), (200, 200)), Rect((700, 350), (200, 200))], [Rect((550, 250), (450, 100)), Rect((0, 250), (450, 100))], [Rect((250, 0), (100, 300)), Rect((500, 350), (500, 100))], [Rect((150, 100), (100, 300)), Rect((450, 150), (100, 300)), Rect((750, 200), (100, 300))], [Rect((450, 250), (100, 100))], [Rect((50, 50), (100, 100)), Rect((250, 50), (100, 100)), Rect((450, 50), (100, 100)), Rect((650, 50), (100, 100)), Rect((850, 50), (100, 100)), Rect((50, 250), (100, 100)), Rect((250, 250), (100, 100)), Rect((450, 250), (100, 100)), Rect((650, 250), (100, 100)), Rect((850, 250), (100, 100)), Rect((50, 450), (100, 100)), Rect((250, 450), (100, 100)), Rect((450, 450), (100, 100)), Rect((650, 450), (100, 100)), Rect((850, 450), (100, 100))], [Rect((0, i * 40), (60, 40)) for i in range(15)] + [Rect((940, i * 40), (60, 40)) for i in range(15)] + [Rect((440, i * 40), (60, 40)) for i in range(7)] + [Rect((500, i * 40), (60, 40)) for i in range(7)] + [Rect((440, i * 40), (60, 40)) for i in range(8, 15)] + [Rect((500, i * 40), (60, 40)) for i in range(8, 15)], [Rect((0, 0), (300, 600)), Rect((700, 0), (300, 600)), Rect((300, 450), (300, 80)), Rect((400, 300), (300, 80)), Rect((300, 150), (300, 80))]] # list of obstacles for each level
    ghostNum = [2, 3, 4, 4, 3, 5, 5, 3, 4, 15] # number of ghosts for each level
    levelTime = [29, 59, 119, 89, 59, 104, 44, 69, 134, 12] # time limit for each level
    playerStartPos = [(500, 300), (20, 300), (20, 20), (500, 100), (500, 300), (30, 500), (20, 300), (300, 25), (700, 300), (500, 560)] # player starting location for each level
    levelTaskNum = [5, 8, 15, 12, 4, 6, 1, 5, 4, 1] # points needed for each level
    levelTaskTypes = ['simple', 'simple', 'simple', 'simple', 'multi', 'multi', 'hidden', 'hidden', 'hidden', 'final'] # task type for each level

    # place the player
    player.center = (playerStartPos[level])

    # prepare new ghosts
    newGhosts = []
    newGhostXdirection = [0] * ghostNum[level]
    newGhostYdirection = [0] * ghostNum[level]
    newGhostOverlapping = [False] * ghostNum[level]
    # place the ghosts
    for i in range(ghostNum[level]):
        # make a new ghost
        newGhosts.append(Actor('ghostl'))

        # place the ghost
        newGhosts[i].pos = random.randint(0, 1000), random.randint(0, 600)
        while not newGhosts[i].collidelist([Rect((player.left - 80, player.top - 80), (player.width + 160, player.height + 160))] + [Rect((j.left - 20, j.top - 20), (j.width + 40, j.height + 40)) for j in newGhosts]) > -1:
            newGhosts[i].pos = random.randint(0, 1000), random.randint(0, 600)

    # new task
    newTask(levelObstacles[level], levelTaskTypes[level])

    # the level will finish at the time limit
    clock.schedule_unique(levelDone, levelTime[level] + 1)
    clock.schedule_interval(countdown, 1) # count down time left in level

    # returns correspond to: ghosts, ghostXdirection, ghostYdirection, ghostOverlapping, obstacles, timeLeft, currentTaskType, toComplete
    return newGhosts, newGhostXdirection, newGhostYdirection, newGhostOverlapping, levelObstacles[level], levelTime[level], levelTaskTypes[level], levelTaskNum[level]

def update():
    """
    Updates game every frame
    Args
        None
    Returns
        None
    """
    global playerFrozen
    global ghostXdirection
    global ghostYdirection
    global inLevel
    global ghostOverlapping
    global mouse

    # get mouse position - source: https://pythonprogramming.net/making-interactive-pygame-buttons/?completed=/pygame-buttons-part-1-button-rectangle/
    mouse = pygame.mouse.get_pos()

    if inLevel:
        # end level if level won
        if completed >= toComplete:
            clock.unschedule(levelDone)
            levelDone()

        # can't move if player is frozen, ghost won't continue to move towards player
        if not playerFrozen:
            ghostXdirection, ghostYdirection = playerMove(ghosts, ghostOverlapping)

        # move ghosts
        for i in range(len(ghosts) - 1, -1, -1): # iterate over ghosts backwards
            ghosts[i].x += ghostXdirection[i] * 1.5
            ghosts[i].y += ghostYdirection[i] * 1.5

            # prevent ghosts from all going to the same spot and overlapping for the rest of the level
            for j in range(i): # iterate over every ghost in ghosts before ghosts[i]
                # is ghosts[i] touching a rectangle slightly bigger than ghosts[j]?
                if ghosts[i].colliderect(Rect((ghosts[j].left - 20, ghosts[j].top - 20), (ghosts[j].width + 40, ghosts[j].height + 40))):
                    # go in opposite direcction to ghosts[j], or if ghosts[j] is going perfectly verically, go randomly left or right
                    if ghostXdirection[j] == 0:
                        if random.randint(0, 1) == 0:
                            ghostXdirection[i] = -1
                        else:
                            ghostXdirection[i] = 1
                    else:
                        ghostXdirection[i] = ghostXdirection[j] * -1

                    # go in opposite direcction to ghosts[j], or if ghosts[j] is going perfectly horizontally, go randomly up or down
                    if ghostYdirection[j] == 0:
                        if random.randint(0, 1) == 0:
                            ghostYdirection[i] = -1
                        else:
                            ghostYdirection[i] = 1
                    else:
                        ghostYdirection[i] = ghostYdirection[j] * -1

                    ghostOverlapping[i] = True # record that the ghost is overlapping
                    clock.schedule(ghostContinue, 5) # all ghosts will follow the player again in 5 seconds

        # freeze player for 2 seconds if touching ghost
        if player.collidelist(ghosts) > -1:
            playerFrozen = True
            clock.schedule(unfreeze, 2)

    # do the ghost animation in the screen at the end of the game
    elif whatsHappening == 'entire game won':
        if ghosts[0].x > 1100:
            ghosts[0].x = -100
        else:
            ghosts[0].x += 2
        if ghosts[1].x < -100:
            ghosts[1].x = 1100
        else:
            ghosts[1].x -= 2

def countdown():
    """
    Counts down time left in the level (called every second while the level is in progress)
    Args
        None
    Returns
        None
    """
    global timeLeft
    if inLevel: # don't count down if game is paused
        timeLeft -= 1

def on_mouse_down():
    """
    Called when mouse is clicked. Controls buttons and cheat codes.
    Args
        None
    Returns
        None
    """
    global whatsHappening

    global inLevel
    global ghosts
    global ghostXdirection
    global ghostYdirection
    global ghostOverlapping
    global obstacles
    global timeLeft
    global completed
    global playerFrozen
    global currentTaskType
    global toComplete
    global pauseImage

    # instantly win level
    if keyboard.z:
        clock.unschedule(levelDone)
        completed = toComplete
        levelDone()

    # teleport player to mouse
    elif keyboard.x:
        player.pos = mouse

    # pause button
    elif whatsHappening == 'gameplay' and 950 <= mouse[0] <= 990 and 10 <= mouse[1] <= 50:
        pauseUnpause()

    # intro screen continue button --> go to start screen
    elif whatsHappening == 'intro' and 424 <= mouse[0] <= 576 and 425 <= mouse[1] <= 477:
        whatsHappening = 'start'

    # start screen
    elif whatsHappening == 'start':
        # start button --> go to level 1
        if 420 <= mouse[0] <= 580 and 300 <= mouse[1] <= 350:
            whatsHappening = 'level start'
        # instructions button --> go to instructions
        elif 420 <= mouse[0] <= 580 and 350 <= mouse[1] <= 400:
            whatsHappening = 'instructions'

    # instructions screen start button --> go to level 1
    elif whatsHappening == 'instructions' and 420 <= mouse[0] <= 580 and 472 <= mouse[1] <= 535:
        whatsHappening = 'level start'

    # start of level screen start button --> start level
    elif whatsHappening == 'level start' and 420 <= mouse[0] <= 580 and 464 <= mouse[1] <= 527:
        whatsHappening = 'gameplay'
        ghosts, ghostXdirection, ghostYdirection, ghostOverlapping, obstacles, timeLeft, currentTaskType, toComplete = levelStart()
        inLevel = True # game will play
        completed = 0 # reset number of points
        playerFrozen = False # player is not frozen
        pauseImage = 'pause' # set pause button to the right image (only necessary if a cheat code is used while the level is paused)

    # level failed screen replay level button --> go to start of current level
    elif whatsHappening == 'level end' and completed < toComplete and 710 <= mouse[0] <= 990 and 10 <= mouse[1] <= 60:
        whatsHappening = 'level start'

    # level won screen next level button --> go to next level
    elif whatsHappening == 'level end' and 710 <= mouse[0] <= 990 and 10 <= mouse[1] <= 60:
        if level == 9: # screen between 9th and 10th level
            whatsHappening = 'literally the worst cutscene'
        else: # normal level
            whatsHappening = 'level start'

    # continue button in the screen before the last level --> start of level 10
    elif whatsHappening == 'literally the worst cutscene' and 424 <= mouse[0] <= 576 and 348 <= mouse[1] <= 400:
        whatsHappening = 'level start'

def pauseUnpause():
    """
    Pauses or unpauses the game
    Args:
        None
    Returns:
        None
    """
    global inLevel
    global pauseImage

    if inLevel:
        pauseImage = 'unpause' # change image to play button
        # prevent level from ending (pause the game)
        clock.unschedule('levelDone')

    else:
        pauseImage = 'pause' # change image to pause button
        # reschedule end of level (unpause the game)
        clock.schedule_unique(levelDone, timeLeft)

    # unpause if game was paused or vice versa
    inLevel = not inLevel

# start game
pgzrun.go()
