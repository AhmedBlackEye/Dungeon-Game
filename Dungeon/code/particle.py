import pygame as pg
from support import *
from random import choice

class AnimationPlayer():
    def __init__(self):
        self.frames = {
            # magic
            'flame': import_images('../graphics/particles/flame/frames'),
            'aura': import_images('../graphics/particles/aura'),
            'heal': import_images('../graphics/particles/heal/frames'),
            
            # attacks 
            'claw': import_images('../graphics/particles/claw'),
            'slash': import_images('../graphics/particles/slash'),
            'coin': import_images('../graphics/particles/coin'),
            }

    def reflect_images(self, frames):
        new_frames = []
        for frame in frames:
            flipped_frame = flip(frame, True, False)
            new_frames.append(flipped_frame)

        return new_frames
    
    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)
    
    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pg.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = "magic"
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
        
    def update(self):
        self.animate()