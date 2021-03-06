'''
'''
import json
import socket
import os
import subprocess
import time
import logging

logging.getLogger(__name__)

# consider merging eaccess here
from lib import eaccess


def loadconfig(configfile):
    with open(configfile) as f:
        return json.load(f)

def setup_game_connection(server_addr, server_port, key, frontend_settings):
    ''' initialize the connection and return the game socket
    '''

    gamesock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = (server_addr, int(server_port))
    gamesock.connect(server)

    time.sleep(1) # would be better to get an ACK of some sort before sending the token...
    gamesock.sendall(key)
    gamesock.sendall(b'\n')
    gamesock.sendall(frontend_settings)
    gamesock.sendall(b'\n')

    # needs a second to connect or else it hangs, then you need to send a newline or two...
    time.sleep(1)
    gamesock.sendall(b'\n')
    gamesock.sendall(b'\n')

    return gamesock

def _open_game_socket(jsonconfig, GAME_KEY=''):
    ''' method is a cleanliness abstraction, relies on parent/enclosed variables
    '''
    if not GAME_KEY:
        GAME_KEY = eaccess.get_game_key(
                jsonconfig['eaccess_host'],
                jsonconfig['eaccess_port'],
                jsonconfig['username'].encode('ascii'),
                jsonconfig['password'].encode('ascii'),
                jsonconfig['character'].encode('ascii'),
                jsonconfig['gamestring'].encode('ascii'),
                jsonconfig['keyfile'])

    lichprocess = subprocess.Popen(["./lichlauncher.sh"], shell=True)
    time.sleep(1)

    gamesock = setup_game_connection(
            jsonconfig['server_addr'],
            jsonconfig['server_port'],
            GAME_KEY,
            jsonconfig['frontend_settings'].encode('ascii'))

    return gamesock, lichprocess

def game_connection_controller():
    ''' controller gets its values from this module
    '''
    configfile = os.getenv('PYLANTHIA_CONFIG', 'config.json')
    jsonconfig = loadconfig(configfile)

    GAME_KEY = ''
    if os.path.isfile(jsonconfig['keyfile']):
        with open(jsonconfig['keyfile']) as f:
            GAME_KEY = f.read().encode('utf-8')

    if GAME_KEY:
        try:
            gamesock, lichprocess = _open_game_socket(jsonconfig, GAME_KEY)
        # cached game key was expired
        except BrokenPipeError as e:
            logging.debug('Game socket broke on cached GAME_KEY: {}'.format(e))
            gamesock, lichprocess = _open_game_socket(jsonconfig)
    # no cached game key
    else:
        gamesock, lichprocess = _open_game_socket(jsonconfig)

    return gamesock, lichprocess
