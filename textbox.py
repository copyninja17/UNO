import pygame
from src import button
import subprocess, sys
import pygame_textinput

pygame.init()

# create display window
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800
TEXTBOX_WIDTH = 272
TEXTBOX_HEIGHT = 35

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('UNO')

#load button images
start_img = pygame.image.load('assets/textures/createroom.png').convert_alpha()
exit_img = pygame.image.load('assets/textures/joinroom.png').convert_alpha()

base_font = pygame.font.Font('assets/fonts/Minecraft.ttf', 25)
# userText = '0.tcp.in.ngrok.io:11632'
userText = ''

inputBox = pygame.Rect(SCREEN_WIDTH/2-TEXTBOX_WIDTH/2,
					   SCREEN_HEIGHT/2-TEXTBOX_HEIGHT/2,
					   TEXTBOX_WIDTH,
					   TEXTBOX_HEIGHT)

textinput = pygame_textinput.TextInputVisualizer()

#game loop
run = True

while run:

	screen.fill((202, 228, 241))
	events = pygame.event.get()
	textinput.update(events)
	screen.blit(textinput.surface, (SCREEN_WIDTH/2-TEXTBOX_WIDTH/2,
									SCREEN_HEIGHT/2-TEXTBOX_HEIGHT/2,
									TEXTBOX_WIDTH,
									TEXTBOX_HEIGHT))

	# pygame.draw.rect(screen,(255,255,255), inputBox)

	# textSurface = base_font.render(userText, True, (0,0,0))
	# screen.blit(textSurface, (inputBox.x + 8, inputBox.y + 6))

	for event in events:
		# quit game
		if event.type == pygame.QUIT:
			run = False
		# text box
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				userText = userText[:-1]
			elif event.key == pygame.K_RETURN:
				finalText = userText
			else:
				userText += event.unicode

	pygame.display.update()
	clock.tick(60)

pygame.quit()