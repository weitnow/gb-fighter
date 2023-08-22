import json
import pygame
import text

class Aseprite():

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Aseprite, cls).__new__(cls)
        else:
            print("Aseprite is a singelton and already instanciated")
        return cls.instance

    def __init__(self) -> None:
        self.frameobj = None
        self.frameTags = None
        self.anim_names = []

    def anim_import(self, path_to_jsonfile : str, path_to_pngfile: str, zoomfactor: int) -> list:
        """imports a jsonfile and pngfile from asesprite, applies the zoomfactor and returns a list like this  [list of pygame-surfaces, list of dict with animationnames and corresponding indexes in list of pygame-surfaces]""" 

        with open(path_to_jsonfile, 'r') as f:
            animation_data = json.load(f)

        _frames = animation_data['frames']
        frameTags = animation_data['meta']['frameTags'] 

        framelist = []
        spritesheet = pygame.image.load(path_to_pngfile)

        frameobj = []   #contains pygame-surfaces as a list

        for key, value in _frames.items():
            #print(key, value)
            x = value['frame']['x']
            y = value['frame']['y']
            w = value['frame']['w']
            h = value['frame']['h']
            new_dict = {"name" : key,
                        "x" : x,
                        "y" : y,
                        "w" : w,
                        "h" : h}
            framelist.append(new_dict)

        for frame in framelist:
            sprite_rect = pygame.Rect(frame['x'], frame['y'], frame['w'], frame['h'])
            sprite_image = pygame.Surface(sprite_rect.size, pygame.SRCALPHA)
            sprite_image.blit(spritesheet, (0, 0), sprite_rect)
            sprite_image = pygame.transform.scale(sprite_image, (32 * zoomfactor, 32 * zoomfactor))
            frameobj.append(sprite_image)

        self.frameobj = frameobj
        self.frameTags = frameTags

        self.store_animation_names()

        return [frameobj, frameTags]
    

    def store_animation_names(self) -> None:
        for anim_dict in self.frameTags:
            self.anim_names.append(anim_dict['name'])

    def get_animation(self, anim_name: str) -> list[pygame.Surface]:
        """expects the name of the aseprite animation and returns a list with all the frames for the animation as pygame-surfaces"""
        
        if anim_name not in self.anim_names:
            raise Exception(f'{anim_name} is not a valid anim_name')
        
        new_anim_list = []
        for anim_dict in self.frameTags:
            if anim_dict['name'] == anim_name:
                for i in range(anim_dict['from'], anim_dict['to']+1):
                    new_anim_list.append(self.frameobj[i])
                return new_anim_list
                    


aseprite = Aseprite()

class Joystick():

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Joystick, cls).__new__(cls)
        else:
            print("Joystick is a singelton and already instanciated")
        return cls.instance

    def __init__(self):
        

        self.x_pressed = False
        self.a_pressed = False
        self.y_pressed = False
        self.b_pressed = False

        self.dpad_right = False
        self.dpad_left = False
        self.dpad_up = False
        self.dpad_down = False

        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]



    def update(self):

        self.x_pressed = False
        self.a_pressed = False
        self.y_pressed = False
        self.b_pressed = False

        self.dpad_right = False
        self.dpad_left = False
        self.dpad_up = False
        self.dpad_down = False

        for joystick in self.joysticks:
            if joystick.get_button(0):
                self.a_pressed = True
            if joystick.get_button(1):
                self.b_pressed = True
            if joystick.get_button(2):
                self.x_pressed = True
            if joystick.get_button(3):
                self.y_pressed = True
            if (joystick.get_hat(0))[1] == -1:
                self.dpad_down = True
            if (joystick.get_hat(0))[1] == 1:
                self.dpad_up = True
            if (joystick.get_hat(0))[0] == -1:
                self.dpad_left = True
            if (joystick.get_hat(0))[0] == 1:
                self.dpad_right = True

        
joystick = Joystick()          

if __name__ == '__main__':
   aseprite.anim_import(path_to_jsonfile='./graphics/gbFighter.json', path_to_pngfile='./graphics/gbFighter.png', zoomfactor=6)
   aseprite.get_animation('Idle')



   