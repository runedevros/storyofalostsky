from lostsky.battle.bullet_sys import Emitter, Bullet, BulletScript
import os
import pygame
from random import randint
from lostsky.core.linalg import Vector2

class Beam(Bullet):

    def __init__(self, initial_position, color, angle):
        self.base_spark = self.generate_spark(color)

        self.base_spark = pygame.transform.rotate(self.base_spark, angle)

        Bullet.__init__(self, initial_position, self.base_spark, 0, 0)

        self.starting_position = Vector2(initial_position)
        self.lhs_position = initial_position
        self.rhs_position = (840-initial_position[0], initial_position[1])
        self.rect.topleft = initial_position
        self.frame_counter = 0

        # How many frames until spark reaches max length
        self.max_length_frame = 60


    def generate_spark(self, color):

        width = 800
        height = 75
        canvas_surface = pygame.Surface((width, height)).convert_alpha()
        canvas_surface.fill((0, 0, 0, 0))

        # Sets up MS to follow a mirrored sqrt(x) function
        spacing = 5

        # Outer spark layer (more transparent)
        point_list = [(spacing*x, height/2+height/2*(x**0.5)/(width**0.5)) for x in xrange(0, width/spacing)]
        point_list_reversed = list(point_list)
        point_list_reversed.reverse()
        for point in point_list_reversed:
            point_list.append((point[0], height-point[1]))

        pygame.draw.polygon(canvas_surface, color+(150,), point_list)

        # Inner spark layer (less transparent)
        point_list = [(spacing*x, height/2+height/4*(x**0.5)/(width**0.5)) for x in xrange(0, width/spacing)]

        point_list_reversed = list(point_list)
        point_list_reversed.reverse()
        for point in point_list_reversed:
            point_list.append((point[0], height-point[1]))

        pygame.draw.polygon(canvas_surface, (255,255,255, 200), point_list)


        return canvas_surface

    def update(self, delta_t, rhs_source):

        # Jitter
        #
        # new_position = Vector2(self.lhs_position)+Vector2((randint(-1, 1), randint(-1, 1)))
        # if (new_position - self.starting_position).get_magnitude() < 7:
        #     self.lhs_position = new_position
        #     self.rhs_position = (840-new_position.x, new_position.y)


        # Controls stretching of MS image during first half of animation
        if self.frame_counter < self.max_length_frame:
            if rhs_source:

                self.image = pygame.transform.smoothscale(self.rhs_image,
                                                          (self.rhs_image.get_width()*self.frame_counter/self.max_length_frame,
                                                           self.rhs_image.get_height()))
                self.rect = self.image.get_rect()
                self.rect.topright = self.rhs_position
            else:
                self.image = pygame.transform.smoothscale(self.lhs_image,
                                                          (self.lhs_image.get_width()*self.frame_counter/self.max_length_frame,
                                                           self.lhs_image.get_height()))
                self.rect = self.image.get_rect()
                self.rect.topleft = self.lhs_position

        # Spark remains at full size
        else:
            if rhs_source:

                self.image = self.rhs_image
                self.rect = self.image.get_rect()
                self.rect.topright = self.rhs_position

            else:
                self.image = self.lhs_image
                self.rect = self.image.get_rect()
                self.rect.topleft = self.lhs_position

        self.frame_counter += 1

class SparkEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):
        self.num_bullets = 1
        delay = 0
        max_emissions = 1
        start_delay = 0

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

    def emit(self):
        self.bullets.add(Beam((270, 50), (255, 0, 255), 10))
        self.bullets.add(Beam((300, 150), (0, 200, 255),  5))
        self.bullets.add(Beam((300, 230), (255, 0, 200), -5))
        self.bullets.add(Beam((270, 250), (0, 200, 255), -10))

class StarEmitter(Emitter):

    def __init__(self, bullet_group, initial_position):
        """
        Sets up star emitter
        Pattern: Emits a circular pattern of stars
        """
        self.num_bullets = 20
        delay = 10
        max_emissions = 3
        start_delay = 0

        self.blue_image = pygame.image.load(os.path.join('images', 'bullets', 'butterfly_blue.png')).convert_alpha()
        self.magenta_image = pygame.image.load(os.path.join('images', 'bullets', 'butterfly_magenta.png')).convert_alpha()
        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

    def emit(self):
        # Shoots bullets in a series of rings
        for counter in xrange(0, self.num_bullets):

            if counter%2:
                assign_image = self.blue_image
            else:
                assign_image = self.magenta_image
            self.bullets.add(Bullet(self.position, assign_image, 4.5, counter*360.0/self.num_bullets+7.5*(self.emissions%2)))

class Script(BulletScript):

    def __init__(self, target_surface, background):
        self.max_frames = 220
        BulletScript.__init__(self, target_surface, background)
        self.emitters = [SparkEmitter(self.bullet_group, (250, 100)),
                         StarEmitter(self.bullet_group, (250, 250)),

                         ]
        self.sfx_timings = [(0, 'beam2')]

