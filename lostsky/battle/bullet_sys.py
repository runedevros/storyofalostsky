import pygame
from lostsky.core.linalg import Vector2
from math import cos, sin, degrees, radians, atan2

class Emitter(object):

    def __init__(self, bullet_group, initial_position, delay, max_emissions, start_delay):
        """
        Function: __init__
        Purpose: Sets up an emitter
        Inputs:

                bullet_group - bullet sprite group to associate with
                initial_position - (x, y) pixel where emitter is located
                delay - how long to wait between each emission
                max_emissions - how many emissions this emitter puts out
                start_delay - how long to wait until the first emission

        """


        self.position = initial_position

        # Delay between emissions
        self.start_delay = start_delay
        self.frame_delay = delay
        self.max_emissions = max_emissions
        self.bullets = bullet_group

        self.first_emission = True

        self.emissions = 0
        self.framenum = 0


    def update(self, delta_t):
        """
        Function Name: update
        Purpose: Updates each emitter by one tick
                 Checks if the emitter is ready to send another bullet group out
        Input:  target_surface - screen to draw on
                background - background screen

        Output: Rectangles that need to be updated for the drawing
        """
        self.check_emit_delay()


    def check_emit_delay(self):
        """
        Function: Check emit delay
        Emits a set of bullets if:
            - On the first emission, wait till the start delay is met
            - On subsequent emissions, wait every emission delay

        """

        if (((self.first_emission and self.framenum == self.start_delay)
            or (not self.first_emission and self.framenum == self.frame_delay))
            and self.emissions < self.max_emissions):
            self.framenum = 0
            self.emit()
            self.emissions += 1
            self.first_emission = False
        self.framenum += 1

    def emit(self):
        """
        Function: emit
        Purpose: Does nothing since emitters will inherit from this class.
        """
        pass

class MovingEmitter(Emitter):

    def __init__(self, bullet_group, initial_position, delay, max_emissions, start_delay, speed, angle):
        """
        Function: __init__
        Purpose: Sets of a moving emitter

        Inputs: Same as standard emitter
                + speed - speed (in pixels per frame) to move the emitter
                + angle - angle (relative to x-axis with positive angle being downward)

        """

        Emitter.__init__(self, bullet_group, initial_position, delay, max_emissions, start_delay)

        angle_rad = radians(angle)
        self.velocity = Vector2(speed*cos(angle_rad), speed*sin(angle_rad))


    def update(self, delta_t):
        """
        Function Name: update
        Purpose: Updates each emitter by one tick
                 Checks if the emitter is ready to send another bullet group out
        Input:  target_surface - screen to draw on
                background - background screen

        Output: Rectangles that need to be updated for the drawing
        """
        self.position += (delta_t/16.7)*self.velocity
        self.check_emit_delay()


class Bullet(pygame.sprite.DirtySprite):

    def __init__(self, initial_position, image, speed, angle):
        """
        Function: __init__
        Purpose: Sets up a bullet object
        Inputs:
                initial_position - (x, y) pixel location of bullet
                image - bullet image to use
                speed - speed in (Pix/frame)
                angle - angle to move (relative to x axis, positive angle being down)

        """

        pygame.sprite.DirtySprite.__init__(self)
        self.float_position = Vector2(float(initial_position[0]), float(initial_position[1]))

        angle_rad = radians(angle)
        self.velocity = Vector2(speed*cos(angle_rad), speed*sin(angle_rad))

        # If bullet has non-zero y velocity rotate image appropriately
        self.unrotated_image = image

        if angle != 0:
            self.lhs_image = pygame.transform.rotate(image, -angle)
        else:
            self.lhs_image = image

        self.rhs_image = pygame.transform.flip(self.lhs_image, True, False)
        self.image = self.lhs_image


        self.rect = self.image.get_rect()
        self.rect.center = initial_position

    def update_velocity(self, delta_t):
        """
        function: update_velocity
        purpose: updates the velocity by one time interval delta_t
                 override this function with a custom velocity update function,
                 otherwise, normal bullets have a constant velocity
        """
        pass

    def update_rotation(self):
        """
        function: update_rotation
        purpose: updates the rotation of the image depending on the current direction
        """
        if self.velocity.get_magnitude() > 0:
            norm_velocity = self.velocity.get_normalized()
            angle_rad = atan2(norm_velocity.y, norm_velocity.x)

            if angle_rad != 0:
                self.lhs_image = pygame.transform.rotate(self.unrotated_image, -degrees(angle_rad))
            else:
                self.lhs_image = self.unrotated_image

            self.rhs_image = pygame.transform.flip(self.lhs_image, True, False)

    def update(self, delta_t, rhs_source):

        """
        Function: Update
        Purpose: Uses a basic Euler's method to update the position of the bullets
        Inputs: delta_t - time elapsed between frames
                rhs_source - (T/F) if bullet is coming from RHS unit
        """

        self.update_velocity(delta_t)
        self.update_rotation()

        # Espected 16.7 ms/frame
        self.float_position += (delta_t/16.7)*self.velocity


        # If the RHS unit is using the spell, invert across the center of the screen.
        if not rhs_source:
            self.image = self.lhs_image
            self.rect.center = (int(self.float_position.x), int(self.float_position.y))
        else:
            self.image = self.rhs_image
            self.rect.center = (int(840-self.float_position.x), int(self.float_position.y))

        # check bounds
        if (    (self.rect.topleft[0] > 840 or self.rect.topleft[0] < 0) or
                (self.rect.bottomleft[1] > 490 or self.rect.topleft[1] < 100)):
            self.kill()


class BulletScript(object):

    def __init__(self, target_surface, background):
        """
        Sets up a bullet script

        Inputs:    target_surface - surface to draw to
                   background - background image to clear bullets from
        """

        self.emitters = []
        self.sfx_timings = []
        self.bullet_group = pygame.sprite.RenderUpdates()
        self.target_surface = target_surface
        self.background = background

    def clear(self):
        self.bullet_group.clear(self.target_surface, self.background)


    def update(self, t0, rhs_source):
        """
        Function: update
        Purpose: updates all bullets and emitters
                t0 - time of last frame
                rhs_source - (T/F) if RHS unit using this spell.
        """

        delta_t = pygame.time.get_ticks()-t0
        [emitter.update(delta_t) for emitter in self.emitters]
        self.bullet_group.update(delta_t, rhs_source)
        return self.bullet_group.draw(self.target_surface)

class PreRenderedSprite(pygame.sprite.DirtySprite):

    def __init__(self, frames, frame_delay, location, angle, speed):

        pygame.sprite.DirtySprite.__init__(self)

        self.float_position = Vector2(float(location[0]), float(location[1]))
        self.frames = frames
        self.frame_delay = frame_delay
        self.location = location

        if speed:

            angle_rad = radians(angle)
            self.velocity = Vector2(speed*cos(angle_rad), speed*sin(angle_rad))

        else:

            self.velocity = Vector2(0, 0)

        self.current_frame = 0
        self.frame_num = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.location


    def update(self, delta_t, rhs_source):
        if self.frame_num == self.frame_delay:
            self.image = self.frames[self.current_frame]
            self.current_frame += 1
            self.frame_num = 0
        self.frame_num += 1


        # Espected 16.7 ms/frame
        self.float_position += (delta_t/16.7)*self.velocity


        # If the RHS unit is using the spell, invert across the center of the screen.
        if not rhs_source:
            self.rect.center = (int(self.float_position.x), int(self.float_position.y))
        else:
            self.rect.center = (int(840-self.float_position.x), int(self.float_position.y))


class PreRenderedScript(object):

    def __init__(self, target_surface, background, image, frame_size, frame_delay, location, angle = 0, speed = 0):
        """
        Function: __init__
        Purpose: Creates a prerendered script object
        Inputs: target_surface - target surface to draw to
                background - background surface to clear by
                image - image containing the frames of this aniomation
                frame_size - (x, y) pixel how large each frame is
                frame_delay - how many frames to hold each frame in the animation for
                location - where to draw the frame
                angle - angle of moving spell (optional)
                speed - speed of moving animation (optional)

        """
        self.target_surface = target_surface
        self.background = background

        frames = [image.subsurface(frame_size[0]*x, frame_size[1]*y, frame_size[0], frame_size[1])
                      for y in xrange(0, image.get_height()/frame_size[1]) for x in xrange(0, image.get_width()/frame_size[0]) ]


        self.max_frames = len(frames)*frame_delay

        self.sfx_timings = []
        self.sprite_group = pygame.sprite.RenderUpdates()
        self.anim_sprite = PreRenderedSprite(frames, frame_delay, location, angle, speed)
        self.sprite_group.add(self.anim_sprite)

    def clear(self):
        self.sprite_group.clear(self.target_surface, self.background)

    def update(self, t0, rhs_source):

        delta_t = pygame.time.get_ticks()-t0
        self.sprite_group.update(delta_t, rhs_source)
        return self.sprite_group.draw(self.target_surface)


class MultiPartScript(object):

    def __init__(self, scripts):
        self.scripts = scripts
        self.max_frames = sum([script.max_frames for script in scripts])

        self.sfx_timings = []
        offset = 0

        # Assembles the multi-component sound effect scripts
        for index, script in enumerate(scripts):
            for sfx in script.sfx_timings:
                self.sfx_timings.append((sfx[0]+offset, sfx[1]))
            offset += script.max_frames

        self.current_script = scripts.pop(0)
        self.current_max = self.current_script.max_frames
        self.frame_counter = 0

    def check_script(self):
        # If the script has completed, go to the next script

        if self.frame_counter == self.current_max:
            self.current_script = self.scripts.pop(0)
            self.current_max = self.current_script.max_frames
            self.frame_counter = 0
            pygame.display.flip()
        else:
            self.frame_counter += 1

    def clear(self):
        self.check_script()
        self.current_script.clear()

    def update(self, t0, rhs_mode):
        # Updates the current script
        return self.current_script.update(t0, rhs_mode)
