from src import config

def display(screen, createButton, joinButton):
	if createButton.draw(screen):
		config.host = True
		config.Page = 1
		config.waitingTime = 200

	if joinButton.draw(screen):
		config.host = False
		config.Page = 2
		config.waitingTime = 200
