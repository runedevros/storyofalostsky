# Items / Synthesis module

# Treasure item class
# Purpose: Static items used for synthesis / trading
class Treasure(object):

    def __init__(self, name, id_string, desc, icon, type):

        """
        # Function Name: Init
        # Purpose: Creates a treasure item
        # Inputs:
        #           name - treasure's displayed name
        #           id_string - treasure id value
        #           desc - description of treasure
        #           icon - icon name
        """

        self.name = name
        self.desc = desc
        self.id_string = id_string
        self.icon = icon
        self.type = type

    def __str__(self):
        """
        # Function Name: str
        # Purpose: Returns treasure's name
        """

        return self.name