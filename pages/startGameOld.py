'''
THIS SCRIPT IS CURRENTLY NOT IN USE

[TODO] add shell=True for platform != 'windows'
'''

from src import config
import subprocess, sys

def start():
    subprocess.Popen([sys.executable,
                      f'src/uno_client.py', 
                      f'{config.host}', 
                      f'{config.settings}', 
                      f'{config.playerName}'],
                     creationflags=subprocess.CREATE_NEW_CONSOLE)
    print("sent")