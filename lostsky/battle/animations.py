import pygame
from math import sin, cos, pi
from lostsky.core.linalg import Vector2

class CharaAnimData(pygame.sprite.Sprite):

    def __init__(self, anim_dict, rhs=False):
        """
        Function Name: __init__
        Purpose: Constructs a unit's character animation object
        Inputs: anim_dict - unit's animation data
                rhs - T/F if unit is on the RHS of the screen

        """
        pygame.sprite.Sprite.__init__(self)

        # Loads the image
        frame_image = pygame.image.load(anim_dict['filename']).convert_alpha()
        # If the unit is standing on the RHS, flip the image horizontally
        self.rhs = rhs

        # Splits the complete frame image into individual frames
        # If unit is on the RHS, flip the images horizontally
        # Images are presumed to be (200, 200) pixels
        if self.rhs:
            self.frames = [[pygame.transform.flip(frame_image.subsurface((x*200, y*200, 200, 200)), True, False) for y in xrange(0, frame_image.get_height()/200)]
                        for x in xrange(0, frame_image.get_width()/200)
                        ]
        else:
            self.frames = [[frame_image.subsurface((x*200, y*200, 200, 200)) for y in xrange(0, frame_image.get_height()/200)]
                        for x in xrange(0, frame_image.get_width()/200)
                        ]

        self.anim_dict = anim_dict

        self.image = self.frames[0][0]
        self.rect = self.image.get_rect()

        # Current Frame to draw
        self.current_frame = 0

        # Number of times the current frame has been drawn
        self.frame_counter = 0

        # Default state is idle
        self.mode = 'idle'

        # Location of RHS and LHS units
        self.LHS_FRAME_COORD = (125, 160)
        self.RHS_FRAME_COORD = (510, 160)

        # Number of times to repeatedly show a frame
        # (Fixes frame rate to 15FPS for units)
        self.FRAME_REPEAT = 6

    def set_mode(self, mode):
        """
        Function name: set_mode
        Purpose: Switches which animation is being used
        Input: mode - animation mode to set animation to
        """
        self.mode = mode
        # Resets animation counters
        self.current_frame = 0
        self.frame_counter = 0

    def update(self):
        """
        Function name: update
        Purpose: Renders the animation frame to the screen
        Input: surface - Pygame surface onto which to render the animations
        Output: T/F if animation is still going
        """

        frame_coord = self.anim_dict[self.mode]['frames'][self.current_frame]
        location_coord = self.anim_dict[self.mode]['coords'][self.current_frame]

        # Updates current sprite frame and coordinate
        self.image = (self.frames[frame_coord[0]][frame_coord[1]])
        if self.rhs:
            self.rect.topleft = (self.RHS_FRAME_COORD[0]-location_coord[0], self.RHS_FRAME_COORD[1]-location_coord[1])
        else:
            self.rect.topleft = (self.LHS_FRAME_COORD[0]+location_coord[0], self.LHS_FRAME_COORD[1]-location_coord[1])

        self.frame_counter += 1

        # If this frame has been rendered FRAME_REPEAT amount of times
        #   go to the next frame and reset the frame counter
        if self.frame_counter == self.FRAME_REPEAT:
            self.current_frame += 1
            self.frame_counter = 0

        # If all the frames have been rendered
        if self.current_frame >= len(self.anim_dict[self.mode]['frames']):

            # Case: Repeat
            # Goes back to the first frame
            if self.anim_dict[self.mode]['repeat']:
                self.current_frame = 0
            # Case: Do not repeat
            # Holds the last frame
            else:
                self.current_frame = len(self.anim_dict[self.mode]['frames']) - 1


class CharaAnimPlaceholder(pygame.sprite.Sprite):
    """
    Character sprite for units without battle animations
    """
    def __init__(self, unit, rhs = False):
        """
        # Function Name: __init__
        # Purpose: Initializes the still map sprite for drawing battle scenes with units that don't have animations
        # Inputs: unit - unit to create from
        """
        pygame.sprite.Sprite.__init__(self)
        if rhs:
            self.image = unit.image.subsurface((280, 0, 35, 35))
            self.rect = self.image.get_rect()
            self.rect.topleft = (595, 280)
        else:
            self.image = unit.image.subsurface((175, 0, 35, 35))
            self.rect = self.image.get_rect()
            self.rect.topleft = (210, 280)


class BulletAnimData(object):
    """
    # Animations Class
    """

    def __init__(self, bullet_count, distribution_type, dist_parameter, animation_type, parameters = None):
        """
        # Function Name: __init__
        # Purpose: Initializes the bullet animation data for the spell
        # Inputs: Bullet Count - How many bullets to plot
        #         Distribution type - vertical, circular, forward arc
        #         Animation type - line, sin, cos, spiral
        #         Parameters - Optional settings for the animation
        """

        self.bullet_count = bullet_count
        self.bullet_coords = {'forward': [], 'backward': []}
        distributions = {
            'linear': self.linear_distribution,
            'circle': self.circular_distribution,
            'semicircle': self.semicircle_distribution
            }
        generators = {
            'linear': self.linear_generator,
            'radial': self.radial_generator,
            'sin': self.sine_generator,
            'spiral': self.spiral_generator,
            'wheel': self.wheel_generator
            }
        distributions[distribution_type](dist_parameter)
        generators[animation_type]()

    def linear_distribution(self, spacing):

        """
        # Function Name: linear dist
        # Purpose: Gets the initial position of the bullets, and generates it so that the spacing is linear and vertical
        # Inputs: Spacing - number of pixels between each
        """

        self.bullet_coords['forward'].append([])
        self.bullet_coords['backward'].append([])
        x_0 = 225
        if self.bullet_count % 2 == 1:
            self.bullet_coords['forward'][0].append((225, 275))
            self.bullet_coords['backward'][0].append((580, 275))
            count = 1
        else:
            count = 0

        while count < self.bullet_count:
            self.bullet_coords['forward'][0].append((225, 275+spacing))
            self.bullet_coords['forward'][0].append((225, 275-spacing))
            self.bullet_coords['backward'][0].append((580, 275+spacing))
            self.bullet_coords['backward'][0].append((580, 275-spacing))
            spacing += spacing
            count += 2

    def circular_distribution(self, radius):

        """
        # Function Name: circular distribution
        # Purpose: Gets the initial position of the bullets, and generates it so that the spacing is equally spaced in a circle
        # Inputs: Radius - radius to distribute the bullets
        """

        self.bullet_coords['forward'].append([])
        self.bullet_coords['backward'].append([])
        center_f = Vector2(210, 280)
        center_b = Vector2(595, 280)

        angular_spread = 2*pi/self.bullet_count
        angle = 0
        while angle < 2*pi:
            r_0_f = center_f + Vector2(int(radius*cos(angle)), int(radius*sin(angle)))
            r_0_b = center_b + Vector2(int(-radius*cos(angle)), int(radius*sin(angle)))
            self.bullet_coords['forward'][0].append(tuple(r_0_f))
            self.bullet_coords['backward'][0].append(tuple(r_0_b))
            angle += angular_spread


    def semicircle_distribution(self, radius):

        """
        # Function Name: circular distribution
        # Purpose: Gets the initial position of the bullets, and generates it so that the spacing is equally spaced in a forward facing semicircle
        # Inputs: Radius - radius to distribute the bullets
        """

        self.bullet_coords['forward'].append([])
        self.bullet_coords['backward'].append([])
        center_f = Vector2(210, 280)
        center_b = Vector2(595, 280)

        if self.bullet_count % 2 == 1:
            r_0_f = center_f + Vector2(radius, 0)
            r_0_b = center_b + Vector2(-radius, 0)
            self.bullet_coords['forward'][0].append(tuple(r_0_f))
            self.bullet_coords['backward'][0].append(tuple(r_0_b))
            angular_spread = pi/(self.bullet_count-1)
        else:
            angular_spread = pi/(self.bullet_count)

        angle = angular_spread

        while angle <= pi/2:
            r_0_f = center_f + Vector2(int(radius*cos(angle)), int(radius*sin(angle)))
            p_0_f = center_f + Vector2(int(radius*cos(angle)), int(radius*sin(-angle)))
            r_0_b = center_b + Vector2(int(-radius*cos(angle)), int(radius*sin(angle)))
            p_0_b = center_b + Vector2(int(-radius*cos(angle)), int(radius*sin(-angle)))

            self.bullet_coords['forward'][0].append(tuple(r_0_f))
            self.bullet_coords['forward'][0].append(tuple(p_0_f))
            self.bullet_coords['backward'][0].append(tuple(r_0_b))
            self.bullet_coords['backward'][0].append(tuple(p_0_b))
            angle += angular_spread


    def linear_generator(self, parameters=[30, 13]):

        """
        # Function Name: linear generator
        # Purpose: Generates the coordinates for a linear animation
        # Inputs: Parameters - List containing #frames and pixels per frame to advance
        """

        for i in xrange(1, parameters[0]):
            self.bullet_coords['forward'].append([])
            self.bullet_coords['backward'].append([])
            for j in xrange(0, len(self.bullet_coords['forward'][0])):
                x_0_f, y_0_f = self.bullet_coords['forward'][0][j]
                x_0_b, y_0_b = self.bullet_coords['backward'][0][j]
                # X(t) = Xo + V*T
                x_j_f = x_0_f + i*parameters[1]
                x_j_b = x_0_b - i*parameters[1]
                self.bullet_coords['forward'][i].append((x_j_f, y_0_f))
                self.bullet_coords['backward'][i].append((x_j_b, y_0_b))


    def sine_generator(self, parameters=[30, 13]):

        """
        # Function Name: sine generator
        # Purpose: Generates the coordinates for a sinusoidal moving wave
        # Inputs: Parameters - List containing #frames and pixels per frame to advance
        """

        for i in xrange(1, parameters[0]):
            self.bullet_coords['forward'].append([])
            self.bullet_coords['backward'].append([])

            wave = int(40*sin(i*pi/15))

            for j in xrange(0, len(self.bullet_coords['forward'][0])):
                x_0_f, y_0_f = self.bullet_coords['forward'][0][j]
                x_0_b, y_0_b = self.bullet_coords['backward'][0][j]
                # X(t) = Xo + V*T
                x_j_f = x_0_f + i*parameters[1]
                x_j_b = x_0_b - i*parameters[1]
                y_j_f = y_0_f + wave
                y_j_b = y_0_f - wave
                self.bullet_coords['forward'][i].append((x_j_f, y_j_f))
                self.bullet_coords['backward'][i].append((x_j_b, y_j_b))


    def spiral_generator(self, parameters=[60, 7, 35]):

        """
        # Function Name: spiral generator
        # Purpose: Generates the coordinates for a spiral animation
        # Inputs: Parameters - List containing #frames and pixels per frame outward to advance, as well as the radius
        # NOTE! This generator overrides the initial distribution because it requires a circular distribution
        """

        radius = parameters[2]
        for i in xrange(0, parameters[0]):
            self.bullet_coords['forward'].append([])
            self.bullet_coords['backward'].append([])
            center_f = Vector2(210, 280)
            center_b = Vector2(595, 280)

            angular_spread = 2*pi/self.bullet_count
            angle = 0
            while angle < 2*pi:
                r_0_f = center_f + Vector2(int((parameters[1]*i+radius)*cos(i*pi/5+angle)), int((parameters[1]*i+radius)*sin(i*pi/5+angle)))
                r_0_b = center_b + Vector2(int(-(parameters[1]*i+radius)*cos(i*pi/5+angle)), int((parameters[1]*i+radius)*sin(i*pi/5+angle)))
                self.bullet_coords['forward'][i].append(tuple(r_0_f))
                self.bullet_coords['backward'][i].append(tuple(r_0_b))
                angle += angular_spread


    def wheel_generator(self, parameters=[30, 13, 50]):

        """
        # Function Name: wheel generator
        # Purpose: Generates the coordinates for a wheel of danmaku rolling
        # Inputs: Parameters - List containing #frames and pixels per frame to advance, as well as the radius
        # NOTE! This generator overrides the initial distribution because it requires a circular distribution
        """

        radius = parameters[2]
        for i in xrange(0, parameters[0]):
            self.bullet_coords['forward'].append([])
            self.bullet_coords['backward'].append([])
            center_f = Vector2(210, 280)
            center_b = Vector2(595, 280)

            angular_spread = 2*pi/self.bullet_count
            angle = 0
            while angle < 2*pi:
                r_0_f = center_f + Vector2(int(parameters[1]*i+radius*cos(i*pi/10+angle)), int(radius*sin(i*pi/10+angle)))
                r_0_b = center_b + Vector2(int(-(parameters[1]*i)+radius*cos(i*pi/10+angle)), int(radius*sin(i*pi/10+angle)))
                self.bullet_coords['forward'][i].append(tuple(r_0_f))
                self.bullet_coords['backward'][i].append(tuple(r_0_b))
                angle += angular_spread



    def radial_generator(self, parameters=[60, 13]):

        """
        # Function Name: radial generator
        # Purpose: Generates the coordinates for a radial animation
        # Inputs: Parameters - List containing #frames and pixels per frame to advance
        """

        for i in xrange(1, parameters[0]):
            self.bullet_coords['forward'].append([])
            self.bullet_coords['backward'].append([])

            for j in xrange(0, len(self.bullet_coords['forward'][0])):
                # Absolute Position
                p_0_f = Vector2(self.bullet_coords['forward'][0][j])
                p_0_b = Vector2(self.bullet_coords['backward'][0][j])
                # Relative position to sprite
                r_0_f = Vector2.from_points((210, 280), self.bullet_coords['forward'][0][j])
                r_0_b = Vector2.from_points((595, 280), self.bullet_coords['backward'][0][j])

                # X(t) = Xo + V*T
                r_j_f = p_0_f + i*parameters[1]*r_0_f.normalize()
                r_j_b = p_0_b + i*parameters[1]*r_0_b.normalize()
                r_j_f.x = int(r_j_f.x)
                r_j_f.y = int(r_j_f.y)
                r_j_b.x = int(r_j_b.x)
                r_j_b.y = int(r_j_b.y)
                self.bullet_coords['forward'][i].append(tuple(r_j_f))
                self.bullet_coords['backward'][i].append(tuple(r_j_b))
