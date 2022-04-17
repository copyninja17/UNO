# UNO
UNO is a fun card game where players put down matching cards and the one with 0 cards in the end wins.

We are bringing this multiplayer card game to PC with support for more than 4 players.
> The official android version of **[Mattel UNO](https://play.google.com/store/apps/details?id=com.matteljv.uno&hl=en_IN&gl=US)** supports only 4 players

## v0.7 beta

### Features
- Playable over LAN or internet using [ngrok](https://ngrok.com/)
- Game ends when any player has 0 cards


### Bugs
- AI player temporarily removed
- ngrok button disabled

### Upcoming Features
- Party rules
- Full Graphics
- Broadcasting

# Installation
Install [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/) from [pip](https://pip.pypa.io/en/stable/)
```powershell
# in powershell
pip install pyinstaller

# in bash
pip3 install pyinstaller
```
Make the game into a windows executable by running
```bash
pyinstaller --onefile -c "game.py"
```

Install [ngrok](https://ngrok.com/) to play with friends over internet

# Usage
One player(Host) creates the room and enters the room size. 

Host runs [ngrok](https://ngrok.com/) and enter:
```powershell
ngrok tcp -region in 5555
```
Other players can join by entering the address in their game.

# Gameplay
Play a card by entering the serial number of "Playable Cards". If none, press enter. Winner gets decided by getting to 0 cards first.

Refer to [unorules.com](https://www.unorules.com/) for standard uno rules.

# Contributors
- [Ayush Gupta](https://github.com/AyushGupta57)
- [Akanksha](https://github.com/itsjustakanksha)
- [Astitva Singh](https://github.com/astitva-s)

# Author 
- [Mohit Pradhan](https://github.com/copyninja17)

# License
Copyright © 2021 Mohit Pradhan.
This project is [MIT](/LICENSE.md) licensed.