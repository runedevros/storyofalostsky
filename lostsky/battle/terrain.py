# Terrain class of objects
# NOTE: See this website for full movement doccumentation
# http://dmf.shrinemaiden.org/Story_of_a_Lost_Sky:_Terrain
#
class Terrain(object):

    def __init__(self, name, ident, icon, color, symbol, damage_mod, evade_mod, cost, walk, fly, layer2):
        """
        # Function name: __init__
        # Purpose: Creates a terrain object
        # Inputs:   name - Name of terrain
        #           ident - Identification number (in terrain image data)
        #           icon - icon to use
        #           bg_img - background image to display in battle
        #           color - pixel color for use on minimap (Editor only)
        #           defense_bonus - Damage taken in this tile is multiplied by this value
        #           evade_bonus - change of hitting a target on this terrain is decreased by this amount
        #           cost - Movement cost
        #           walk - T/F if terrain can be walked on
        #           fly - T/F if terrain can be flown on
        """

        # The name of the terrain, as well as it's identification
        self.name = name
        self.ident = ident
        self.icon = icon
        self.color = color
        self.symbol = symbol

        # stat mods
        self.damage_mod = damage_mod
        self.evade_mod = evade_mod
        self.cost = cost
        self.walk = walk
        self.fly = fly

        # Is this a layer 2 tile?
        self.layer2 = layer2