import pygame
from pygame.locals import *
#import time
import configparser
#import requests
import socket
from time import sleep

#HOST = "127.0.0.1"  # The server's hostname or IP address
#PORT = 65432  # The port used by the server

config = configparser.ConfigParser()
config.read('data/client.cfg')
HOST = config['HOST']['IP']
PORT = int(config['HOST']['PORT'])
FULLSCREEN = config.getboolean('GENERAL','FULLSCREEN')
OFFLINE = config.getboolean('GENERAL','OFFLINE')

from lib.widgets import *

class App:

    windowWidth = 1920
    windowHeight = 1080
    bg = pygame.image.load(r'.\data\background.png')
    buttons = []
    fullscreen = False
    

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.display_surf = None
        self.bg = pygame.image.load(r'.\data\background.png')
        self.image_surf = None
        self.btns = []
        self.page_load = True
        self.connected = False
        self.fullscreen = FULLSCREEN
        self.offline = OFFLINE

    def connect_to_server(self):
        try:
            self.netsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.netsocket.connect((HOST, PORT))
            self.connected = True
        except:
            print("Couldnt connect to server")
            sleep( 1 )

    def on_init(self):
        pygame.init()
        pygame.font.init()
        if self.fullscreen:
            self.display_surf = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        else:
            self.display_surf = pygame.display.set_mode((0,0), pygame.RESIZABLE)

        pygame.display.set_caption('CSD Elite Dangerous Control Panel')

        #self.sprites = pygame.sprite.Group()

        self.menu = 'WELCOME'
        self.lastMenu = 'NONE'
        self.font_sm = pygame.font.SysFont('Gautami', 26)
        self.font_med = pygame.font.SysFont('Gautami', 32)
        self.font_lg = pygame.font.SysFont('Gautami', 62)
        return True

        #self.sprites.add(self.player)

        # load sounds
        #self.task_complete_sound = pygame.mixer.Sound(r'data/audio/task_complete.wav')
        #self.spawn_sound = pygame.mixer.Sound(r'data/audio/spawn.wav')
        #self.round_start_sound = pygame.mixer.Sound(r'data/audio/round_start.wav')
        #self.task_incomplete_sound = pygame.mixer.Sound(r'data/audio/task_incomplete.wav')

    def on_event(self, event):
        if event.type == QUIT:
            self.running = False

    def on_loop(self):
        if not self.connected and not self.offline:
            self.connect_to_server()

    def on_render(self):
        # 1920 x 1280 screen can hold 12 x 8 grid of buttons (each being 160px sq)
        if(self.page_load):
            self.page_load = False
            self.buttons.clear()
            _h = 160
            _w = 160

            row1 = 0
            row2 = _h
            row3 = _h * 2
            row4 = _h * 3
            row5 = _h * 4
            row6 = _h * 5
            row7 = _h * 6
            row8 = _h * 7
            
            col1 = 0
            col2 = _w
            col3 = _w * 2
            col4 = _w * 3
            col5 = _w * 4
            col6 = _w * 5
            col7 = _w * 6
            col8 = _w * 7
            col9 = _w * 8
            col10 = _w * 9
            col11 = _w * 10
            col12 = _w * 11
            
            self.addWidget(Button('systemmap_vsm', 'sysmap',  col1,  row1, _h, _w))
            self.addWidget(Button('galmap_vsm', 'galmap',     col1,  row2, _h, _w))
            self.addWidget(Button('headlights_vsm', 'hdlts',  col1,  row3, _h, _w))
            self.addWidget(Button('nightvision_vsm', 'nvg',   col1,  row4, _h, _w))

            self.addWidget(Button('comms_vsm', 'comms', col2, row1, _h, _w))
            self.addWidget(Button('quit_vsm', 'quit',   col12, row8, _h, _w))
            
        self.display_surf.blit(self.bg, (0, 0))
        # Render Welcome Screen
        if self.menu == 'WELCOME':
            self.display_surf.blit(self.bg, (0, 0))
            #self.display_surf.blit(self.font_lg.render('CSD ED Controls', False, orange), (10,10))
            for _b in self.buttons:
                _b.draw(self.display_surf)
 
        pygame.display.flip()


    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self.running = False
        while( self.running ):
            pygame.event.pump()
            ev = pygame.event.get()
            
            mspos = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()
            if (keys[K_ESCAPE]):
                self.netsocket.close()
                self.running = False
                break

            # Mouse over button highlighted
            for _b in self.buttons:
                if _b.get_rect().collidepoint(mspos):
                    _b.active = True
                    #print("mouse detected")
                else:
                    _b.active = False

            btn_action = None

            for event in ev:
                if event.type == pygame.QUIT:
                    self.running = False
                # handle MOUSEBUTTONUP
                if event.type == pygame.MOUSEBUTTONUP:
                    mspos = pygame.mouse.get_pos()
                    for b in self.buttons:
                        if b.get_rect().collidepoint(mspos):
                            #b.active = True
                            btn_action = b.desc
                            print(btn_action)
                            if btn_action == "quit":
                                self.netsocket.close()
                                self.running = False
                                btn_action = None
                            
            if btn_action and not self.offline:
                try:
                    self.netsocket.sendall(bytes(btn_action, 'utf-8'))
                    data = self.netsocket.recv(1024)
                    print(f"Received {data!r}")
                    sent = True
                except:
                    self.connect_to_server()

            self.on_loop()
            self.on_render()
            self.clock.tick(30)
        self.on_cleanup()

    def addWidget(self, widget):
        if type(widget) == Button:
            self.buttons.append(widget)


if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
