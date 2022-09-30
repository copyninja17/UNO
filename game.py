from src import button
import pygame_textinput as pti
from src import config, uno_client
from pages import hostPrompt, enterRoomSize, serverAddress, startGame
from src import clientConfig as cc

import pygame
import platform


config.platform = platform.system()

pygame.init()

# create display window
SCREEN_HEIGHT = 600 #450
SCREEN_WIDTH = 1000
TEXTBOX_WIDTH = 272
TEXTBOX_HEIGHT = 35
bPOsX = SCREEN_WIDTH/2
bPosY = SCREEN_HEIGHT/2

myFont = [None] * 3
myFont[0] = pygame.font.Font('assets/fonts/rimouski_sb.otf', 25)
myFont[1] = pygame.font.Font('assets/fonts/rimouski_sb.otf', 18)
myFont[2] = pygame.font.Font('assets/fonts/rimouski_sb.otf', 32)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('UNO')

# -----------------------------------
# Back Button
# -----------------------------------
backImg = pygame.image.load('assets/textures/back.png').convert_alpha()
backButton = button.Button(10, 10, backImg, 0.07)


# -----------------------------------
# Host Prompt
# -----------------------------------
createRoom = pygame.image.load(
    'assets/textures/createroom.png').convert_alpha()
joinRoom = pygame.image.load('assets/textures/joinroom.png').convert_alpha()

createButton = button.Button(SCREEN_WIDTH/6*2 - (createRoom.get_width()/2 * 0.4), SCREEN_HEIGHT/2.25, createRoom, 0.4)
joinButton = button.Button(SCREEN_WIDTH/6*4 - (joinRoom.get_width()/2 * 0.4), SCREEN_HEIGHT/2.25, joinRoom, 0.4)


# -----------------------------------
# Room size
# -----------------------------------

# loading images
sample_button = pygame.image.load(
    'assets/textures/buttons/2.png').convert_alpha()
enterRoomSize_ = pygame.image.load(
    'assets/textures/roomsize.png').convert_alpha()

# Creating butttons
enterRoomSizeHeader = button.Button(SCREEN_WIDTH/2-(enterRoomSize_.get_width()/2*0.4),
                                    SCREEN_HEIGHT/5,
                                    enterRoomSize_,
                                    0.4)

roomSizeButtons = [[] for _ in range(3)]
roomSizeButtonsFinal = [[] for _ in range(3)]
roomSizeNames = [[] for _ in range(3)]


# -----------------------------------
# Room size
# -----------------------------------

# making room buttons
count = 2
for i in range(3):
    for j in range(3):
        roomSizeButtons[i].append(pygame.image.load(
                                  f'assets/textures/buttons/{count}.png').convert_alpha())
        roomSizeButtonsFinal[i].append(pygame.image.load(
                                       f'assets/textures/buttons/{count}final.png').convert_alpha())
        roomSizeNames[i].append(str(count))
        count += 1

w, h = -1.5*sample_button.get_width()*0.45, 0

for i in range(3):
    for j in range(3):
        roomSizeButtons[i][j] = button.Button(bPOsX + w,
                                              bPosY + h,
                                              roomSizeButtons[i][j],
                                              0.4)
        roomSizeButtonsFinal[i][j] = button.Button(bPOsX + w,
                                                   bPosY + h,
                                                   roomSizeButtonsFinal[i][j],
                                                   0.4)
        w += sample_button.get_width()*0.45

    w = - 1.5*sample_button.get_width()*0.45
    h += sample_button.get_height()*0.45


# -----------------------------------
# Server address
# -----------------------------------
serverAddressImg = pygame.image.load(
    'assets/textures/serverAddress.png').convert_alpha()
serverAddressHeader = button.Button(SCREEN_WIDTH/2-serverAddressImg.get_width()/2*0.4,
                                    SCREEN_HEIGHT/4,
                                    serverAddressImg,
                                    0.4)

ngrokImg = pygame.image.load('assets/textures/ngrok.png').convert_alpha()
ngrokButton = button.Button(SCREEN_WIDTH/2 - ngrokImg.get_width()/2*2.8*0.27,
                            SCREEN_HEIGHT/2 + ngrokImg.get_height()/2*0.27,
                            ngrokImg,
                            0.27)

ngrokFinImg = pygame.image.load('assets/textures/ngrokFin.png').convert_alpha()
ngrokFinButton = button.Button(SCREEN_WIDTH/2 - ngrokFinImg.get_width()/2*2.8*0.27,
                               SCREEN_HEIGHT/2 + ngrokFinImg.get_height()/2*0.27,
                               ngrokFinImg,
                               0.27)

textInputManager = pti.TextInputManager(
    validator=lambda input: len(input) <= 24)
textinputCustom = pti.TextInputVisualizer(
    manager=textInputManager, font_object=myFont[0])
enteredAddress = ''


# -----------------------------------
# enter name
# -----------------------------------

enterNameImg = pygame.image.load(
    'assets/textures/entername.png').convert_alpha()
enterNameButton = button.Button(SCREEN_WIDTH/2-enterNameImg.get_width()/2*0.4,
                                SCREEN_HEIGHT/4,
                                enterNameImg,
                                0.4)

nameInputManager = pti.TextInputManager(
    validator=lambda input: len(input) <= 10)
textinputName = pti.TextInputVisualizer(
    manager=nameInputManager, font_object=myFont[0])


# -----------------------------------
# waiting lobby
# -----------------------------------

waitinglobbyImg = pygame.image.load(
    'assets/textures/waitinglobby.png').convert_alpha()
waitinglobbyButton = button.Button(SCREEN_WIDTH/2-waitinglobbyImg.get_width()/2*0.4,
                                   SCREEN_HEIGHT/4,
                                   waitinglobbyImg,
                                   0.4)


# -----------------------------------
# game room
# -----------------------------------

tables = [0]*3
tables[0] = pygame.image.load('assets/textures/uno_table.png').convert_alpha()
tables[1] = pygame.image.load('assets/textures/uno_table_clockwise.png').convert_alpha()
tables[2] = pygame.image.load('assets/textures/uno_table_anticlockwise.png').convert_alpha()

colours = ['red', 'green', 'blue', 'yellow']
cardsList = {}
cardButtons = {}

for colour in colours:
    cardsList[colour[0].upper()] = []
    for num in range(10):
        cardsList[colour[0].upper()].append(pygame.image.load(
            f'assets/textures/cards/{colour}/{colour}{num}.png').convert_alpha())
    cardsList[colour[0].upper()].append(pygame.image.load(
        f'assets/textures/cards/{colour}/{colour}Plus2.png').convert_alpha())
    cardsList[colour[0].upper()].append(pygame.image.load(
        f'assets/textures/cards/{colour}/{colour}Rev.png').convert_alpha())
    cardsList[colour[0].upper()].append(pygame.image.load(
        f'assets/textures/cards/{colour}/{colour}Skip.png').convert_alpha())
    cardsList[colour[0].upper()].append(pygame.image.load(
        f'assets/textures/cards/{colour}/{colour}+4.png').convert_alpha())
    cardsList[colour[0].upper()].append(pygame.image.load(
        f'assets/textures/cards/{colour}/{colour}wild.png').convert_alpha())

cardsList['X'] = []
cardsList['X'].append(pygame.image.load(
    f'assets/textures/cards/others/X+4.png').convert_alpha())
cardsList['X'].append(pygame.image.load(
    f'assets/textures/cards/others/Xwild.png').convert_alpha())
cardsList['unoBack'] = pygame.image.load(
    f'assets/textures/cards/others/unoBack.png').convert_alpha()

gameplayImg = {}
gameplayImg['yourTurn'] = pygame.image.load(
    f'assets/textures/yourTurn.png').convert_alpha()
gameplayImg['notYourTurn'] = pygame.image.load(
    f'assets/textures/notYourTurn.png').convert_alpha()
gameplayImg['ok'] = pygame.image.load(
    f'assets/textures/ok.png').convert_alpha()
gameplayImg['pick'] = {}
for colour in colours:
    gameplayImg['pick'][colour] = pygame.image.load(
        f'assets/textures/pick{colour}.png').convert_alpha()


# -----------------------------------
# Game Loop
# -----------------------------------
run = True
config.buttonUpdate = 0
pygame.key.set_repeat(300, 25)

while run:

    screen.fill((202, 228, 241))
    events = pygame.event.get()

    # back button
    if config.Page < 5 and config.Page > 0:
        if backButton.draw(screen):
            if config.Page == 3:
                config.Page = config.lastPage
                config.lastPage = 0
            else:
                config.Page = 0

    # create/join room
    if config.Page == 0:
        hostPrompt.display(screen, createButton, joinButton)

    # enter room size
    elif config.Page == 1:
        enterRoomSizeHeader.draw(screen)
        enterRoomSize.display(screen, roomSizeButtons,
                              roomSizeButtonsFinal, roomSizeNames)

    # enter server address
    elif config.Page == 2:
        textinputCustom.update(events)
        serverAddressHeader.draw(screen)
        serverAddress.display(screen, ngrokButton, ngrokFinButton)

        screen.blit(textinputCustom.surface, (SCREEN_WIDTH/2 - 50,
                                              SCREEN_HEIGHT/2 + ngrokImg.get_height()/2*0.27 + 7,
                                              TEXTBOX_WIDTH,
                                              TEXTBOX_HEIGHT))

    # enter name
    elif config.Page == 3:
        enterNameButton.draw(screen)
        textinputName.update(events)
        screen.blit(textinputName.surface, (SCREEN_WIDTH/2 - 50,
                                            SCREEN_HEIGHT/2 + ngrokImg.get_height()/2*0.27 + 7,
                                            TEXTBOX_WIDTH,
                                            TEXTBOX_HEIGHT))

    elif config.Page == 4:
        waitinglobbyButton.draw(screen)
        if cc.top_card:
            config.Page = 5

    elif config.Page == 5:
        startGame.display(screen, tables, cardsList, gameplayImg, myFont)

    if config.waitingTime:
        pygame.time.wait(config.waitingTime)
        config.waitingTime = 0

    # event handler
    for event in events:
        # quit game
        if event.type == pygame.QUIT:
            run = False

        if config.buttonUpdate == 1:
            if config.Page == 1:
                pygame.display.update()
                pygame.time.wait(250)
                config.lastPage = config.Page
                config.Page = 3
                config.buttonUpdate = 0

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if config.Page == 3:
                cc.playerName = textinputName.value
                print(f"Name = {cc.playerName}")
                config.Page = 4
                # textinputName.value = ''
                uno_client.start()
                # print("aage")

            elif config.Page == 2:
                config.settings = textinputCustom.value
                print(f"Entered Address = {enteredAddress}")
                config.lastPage = config.Page
                config.Page = 3
                textinputCustom.value = ''

    pygame.display.update()
    clock.tick(60)

pygame.quit()
