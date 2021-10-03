from src import config
import subprocess, sys

def display(screen, createButton, joinButton):
	if createButton.draw(screen):
		print('CREATE SCRIPT')
		# subprocess.Popen([sys.executable, 'src/uno_client.py', '1'],
		#                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
		config.Page = 1

	if joinButton.draw(screen):
		print('JOIN SCRIPT HERE')
		# subprocess.Popen([sys.executable, 'src/uno_client.py', '0'],
		#                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
		config.Page = 2