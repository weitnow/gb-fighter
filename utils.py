import json
import pygame

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

if __name__ == '__main__':
   aseprite.anim_import(path_to_jsonfile='./graphics/gbFighter.json', path_to_pngfile='./graphics/gbFighter.png', zoomfactor=6)
   aseprite.get_animation('Idle')



   