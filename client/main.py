import pygame
from pygame.locals import *
#import time
import configparser
#import requests
import socket
from time import sleep

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

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
        config = configparser.ConfigParser()
        config.read('.\data\csdedif.cfg')
        self.ip = config['network']['server_ip']
        self.port = config['network']['server_port']
        self.btns = []
        self.page_load = True
        self.connected = False
        while self.connected == False:
            self.connect_to_server()
            

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
        fullscreen = False
        if fullscreen:
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
        pass
        #self.sprites.update()
        #if self.menu != self.lastMenu:
        #    self.lastMenu = self.menu
        #    self.buttons.clear()
        #    self.addWidget(Button('comms_sm', 'Comms', 20, 80, 320, 320))
            #if self.menu == 'WELCOME':
                
                #self.addWidget(Button('common', 'Common', 760, 660))
                #self.addWidget(Button('tasks', 'Progress', 970, 660))
                #self.addWidget(Button('exit', 'Exit', 100, 900))

                #self.addWidget(Button('exit', 'Back', 100, 900))

    def on_render(self):
        
        if(self.page_load):
            self.page_load = False
            self.buttons.clear()

            _h = 160
            _x = _h
            _x2 = _h * 2
            _x3 = _h * 3
            
            _w = 160
            _y = _w
            _y2 = _w * 2
            _y3 = _w * 3
            _y4 = _w * 4
            _y5 = _w * 5

            
            self.addWidget(Button('systemmap_vsm', 'sysmap',  0,   0, _h, _w))
            self.addWidget(Button('galmap_vsm', 'galmap',     0,  _y, _h, _w))
            self.addWidget(Button('headlights_vsm', 'hdlts',  0, _y2, _h, _w))
            self.addWidget(Button('nightvision_vsm', 'nvg',   0, _y3, _h, _w))

            self.addWidget(Button('comms_vsm', 'comms', _x, 0, _h, _w))
            self.addWidget(Button('quit_vsm', 'quit', _x2, _y5, _h, _w))
            
            
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
                            
            if btn_action:
                try:
                    self.netsocket.sendall(bytes(btn_action, 'utf-8'))
                    data = self.netsocket.recv(1024)
                    print(f"Received {data!r}")
                    sent = True
                except:
                    self.connect_to_server()
                    retry_counter -= 1

                #if event.type == pygame.MOUSEBUTTONUP:
                #    mspos = pygame.mouse.get_pos()
                #    if self.menu == 'WELCOME':
                #        # PLAYER SELECT BUTTONS
                #        _plyrclkd = False
                #        for _pb in self.plyrbtns:
                #            if _pb.get_rect().collidepoint(mspos):
                #                self.sprites.remove(self.player)
                #                self.setPlayer(_pb.name)
                #                self.sprites.add(self.player)
                #                _plyrclkd = True
                #        if(_plyrclkd):
                #            _plyrclkd = False
                #            for pn, po in self.players.items():
                #                po.chosen = False
                #                if po.name == self.player.name:
                #                    po.chosen = True
                #                    self.spawn_sound.play()
                #            self.menu = 'TASKS'
                #            self.bg = pygame.image.load(r'.\data\images\bg_empty.png')
                #
                #        # OTHER BUTTONS
                #        for _b in self.buttons:
                #            if _b.rect.collidepoint(mspos):
                #                #print(_b.action)
                #                if _b.action == 'common':
                #                    self.setPlayer('Common')
                #                    self.menu = 'TASKS'
                #                    self.spawn_sound.play()
                #                    self.bg = pygame.image.load(r'.\data\images\bg_empty.png')
                #                if _b.action == 'exit':
                #                    # EXIT
                #                    print('Exit!')
                #                    self.running = False
                #
                #    elif self.menu == 'TASKS':
                #        # TASK CHECKBOXES
                #        idx = 0
                #        for tb in self.tskbtns:
                #            _tbrect = pygame.Rect(tb.x, tb.y, tb.w, tb.h)
                #            if _tbrect.collidepoint(mspos):
                #                if tb.id == self.players['Common'].id:
                #                    self.players['Common'].tasks[idx].completed = not self.players['Common'].tasks[idx].completed
                #                    self.db.updateOccurrence(self.players['Common'].tasks[idx], self.player.id)
                #                else:
                #                    #self.task_incomplete_sound.play()
                #                    self.player.tasks[idx].completed = not self.player.tasks[idx].completed
                #                    self.db.updateOccurrence(self.player.tasks[idx], self.player.id)
                #                    self.lastMenu = 'NONE'
                #                    #break;
                #            idx += 1
                #        for _b in self.buttons:
                #        # BACK
                #            if _b.rect.collidepoint(mspos):
                #                if _b.action == 'exit':
                #                    for t in self.taskstosave:
                #                        print("Task to save " + t.title)
                #                        #self.db.updateOccurrence(t, self.player.id)
                #                    self.menu = 'WELCOME'
                #                    self.bg = pygame.image.load(r'.\data\images\bg_title.png')
                #    print(mspos)
                #elif event.type == pygame.KEYDOWN:
##              #      if event.key == pygame.K_RIGHT:
##              #          self.player.moveRight()
##              #          #print('right')
##              #      if event.key == pygame.K_LEFT:
##              #          self.player.moveLeft()
##              #          #print('left')
##              #      if event.key == pygame.K_UP:
##              #          self.player.moveUp()
##              #          #print('up')
##              #      if event.key == pygame.K_DOWN:
##              #          self.player.moveDown()
##              #          #print('down')
                #    if event.key == pygame.K_SPACE:
                #        self.player.stop()
                #    if event.key == pygame.K_ESCAPE:
                #        self.fullscreen = not self.fullscreen
                #        if self.fullscreen:
                #            self.display_surf = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                #        else:
                #            self.display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.RESIZABLE)

            #if (keys[K_RIGHT]):
            #    self.player.moveRight()
            #if (keys[K_LEFT]):
            #    self.player.moveLeft()
            #if (keys[K_UP]):
            #    self.player.moveUp()
            #if (keys[K_DOWN]):
            #    self.player.moveDown()
            #if (keys[K_SPACE]):
            #    self.player.stop()

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
