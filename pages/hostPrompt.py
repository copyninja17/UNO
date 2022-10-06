from src import clientConfig as cc


def display(screen, createButton, joinButton):
	if createButton.draw(screen):
		cc.host = True
		cc.page = 1
		cc.waitingTime = 200

	if joinButton.draw(screen):
		cc.host = False
		cc.page = 2
		cc.waitingTime = 200
