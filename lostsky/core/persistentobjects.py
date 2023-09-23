# This contains all the objects that are persistent "Options / Save System etc"
import os
import cPickle as pickle
from time import strftime

try:
    from xdg import BaseDirectory
    use_xdg = True
except ImportError:
    use_xdg = False

def get_file_path(filename=None):
    if use_xdg:
        if filename == 'options.dat':
            directory = BaseDirectory.save_config_path('lostsky')
        else:
            directory = BaseDirectory.save_data_path('lostsky')
    else:
        directory = 'data'
    if filename:
        return os.path.join(directory, filename)
    return directory

##############################
# Persistent Options Class
##############################
class Options(object):

    def __init__(self):

        """
        # Function Name: __init__
        # Purpose: Initializes a new object of the options class
        """

        # Show Battle Animations?
        self.battle_anim = True
        # End turn when all units have moved
        self.turn_end = True
        # Display a grid
        self.grid = False

        # Music Volume
        self.music_volume = 5

        # Music Volume
        self.sfx_volume = 5


        # Show Enemy Moves?
        self.show_enemy_moves = True
        # Auto Save
        self.auto_save = True

    def __str__(self):
        """
        # Function Name: __str__
        # Purpose: String representation of the options class
        """

        return str((self.battle_anim, self.turn_end, self.grid, self.music_volume, self.sfx_volume, self.auto_save))

    @classmethod
    def load(self):

        """
        # Function Name: load
        # Purpose: Load saved options
        # Inputs: None
        """

        print "Loading options!"
        data_file = open(get_file_path('options.dat'), 'rb')
        options = pickle.load(data_file)

        data_file.close()
        print "Loaded saved options!"
        return options

    def apply_saved_config(self, config):


        """

        apply_saved_config

        purpose: From a loaded Options object, apply the changes to all settings.
                 If a setting is not present due to being from an older version, the defaults will be used.

        """

        try:
            self.battle_anim = config.battle_anim
        except AttributeError:
            print "Battle Animation Config not found. Using default = True"

        try:
            self.turn_end = config.turn_end
        except AttributeError:
            print "Automatic Turn End Config not found. Using default = True."

        try:
            self.grid = config.grid
        except AttributeError:
            print "Grid Enable Config not found. Using default = False."

        try:
            self.music_volume = config.music_volume
        except AttributeError:
            print "Music Volume Config not found. Using default = 5."

        try:
            self.sfx_volume = config.sfx_volume
        except AttributeError:
            print "Sound Effects Volume Config not found. Using default = 5."

        try:
            self.show_enemy_moves = config.show_enemy_moves
        except AttributeError:
            print "Show Enemy Moves Config not found. Using default = True."

        try:
            self.auto_save = config.auto_save
        except AttributeError:
            print "Auto Save Config not found. Using default = True."

    def save(self):

        """
        # Function Name: save
        # Purpose: Saves the options to a file
        # Inputs: None
        """

        print "Saving Options!"
        data_file = open(get_file_path('options.dat'), 'wb')
        pickle.dump(self, data_file)
        data_file.close
        print "Saved Options!"

##################################
# Player Data Class
##################################

class PlayerData(object):

    def __init__(self):

        """
        # Function Name: __init__
        # Purpose: Initializes a new object of the Player Data
        # Inputs: None
        """

        self.all_unit_data = {}
        # Item storage
        self.items = [
                      [],       # List 0 - Attack Sorcery
                      [],       # List 1 - Healing Sorcery
                      [],       # List 2 - Spell Cards
                      []        # List 3 - Healing Items
                      ]

        # Treasure (Loot for trading, synth items)
        self.treasures = {}

        self.party_members = []
        self.all_event_data = {}
        self.wm_data = {"wm_coords": (0, 0),
                        "in_region": False,
                        "region_coords": (0, 0)}

        self.trading_data = {'first_time': True,
                             'non_repeatable': [],
                             'found_treasures': [],
                             'next_milestone': 0}

        self.known_recipes = []
        self.comment = None             # Comment regarding the save data

    @classmethod
    def load(self, filename):

        """
        # Function Name: load
        # Purpose: Loads the player data
        # Inputs: slot - save slot to load from
        """

        print "Loading!"

        data_file = open(get_file_path(filename), 'rb')
#        if slot in (1, 2, 3, 4):
#            data_file = open(get_file_path('savedata%d.dat' % slot), 'rb')
#        elif slot == 5:
#            data_file = open(get_file_path('autosave01.dat'), 'rb')
#        elif slot == 6:
#            data_file = open(get_file_path('autosave02.dat'), 'rb')

        player = pickle.load(data_file)
        data_file.close()
        print "Loaded!"
        return player

    def save(self, filename):

        """
        # Function Name: save
        # Purpose: Saves the player data to a file
        # Inputs: slot - save slot to save to (slot 5 is reserved for autosave)
        """
        print "Saving Player Data!"
        if 'savedata' in filename:
            data_file = open(get_file_path(filename), 'wb')
            self.comment = "Manual Save - %s" % strftime("%I:%M%p - %b %d, %Y")
        else:
            save_directory = get_file_path()

            # Rename Autosave #1 to Autosave #2
            if 'autosave01.dat' in os.listdir(save_directory):

                # delete autosave #2 if it exits
                if 'autosave02.dat' in os.listdir(save_directory):
                    os.remove(get_file_path('autosave02.dat'))

                os.rename(get_file_path('autosave01.dat'), get_file_path('autosave02.dat'))


            # Write new data to autosave #1
            data_file = open(get_file_path('autosave01.dat'), 'wb')
            self.comment = "Auto Save - %s" % strftime("%I:%M%p - %b %d, %Y")
            filename = "autosave"
        pickle.dump(self, data_file)
        data_file.close()
        self.data_print(filename)
        print "Saved Player Data!"

    def data_print(self, filename):

        """
        # Function Name: data_print
        # Purpose: Prints out the data contained in the player data
        """

        fi = open(get_file_path('player_%s.txt' % filename[:-4]), 'wt')
        print "Starting dump of player data"
        fi.write("==Character Data Dump Begins Here== \n")
        for unit in self.all_unit_data.values():
            unit_data_string = "%s: lv - %d ; exp - %d ; TP - %d ; equipped_spell_slot - %d \n" % (unit.name,
                                                                                       unit.level,
                                                                                       unit.exp,
                                                                                       unit.trait_points,
                                                                                       unit.equipped)
            fi.write(unit_data_string)
            for spell in unit.spell_actions:
                if spell:
                    spell_string = "    %s - %d/%d \n" % (spell.name, spell.livesleft, spell.lives)
                    fi.write(spell_string)

        fi.write("==Character Data Dump Ends Here== \n\n")
        print "Starting dump of event data"
        fi.write("==Event Data Dump Begins Here== \n")
        for event_id in self.all_event_data.keys():
            string = "ID: "+str(event_id)
            string += "; Done: "+str(self.all_event_data[event_id].done)
            string += "; Available: "+str(self.all_event_data[event_id].available)
            string += "; Signed Up: "+str(self.all_event_data[event_id].sign_up)+"\n"
            fi.write(string)
        fi.write("==Event Data Dump Ends Here== \n\n")

        fi.close()

    def add_unit_data(self, unit):
        """
        # Function Name: add_unit_data
        # Purpose: Adds a unit to the player's party
        # Inputs: Unit - the Unit to be added
        """

        self.party_members.append(unit.name)
        self.all_unit_data[unit.name] = UnitData(unit)

    def add_item(self, item):

        """
        # Function Name: add_item
        # Purpose: adds an item to the appropriate inventory list
        """

        # Offensive spells
        if item.type == 'attack' and item.consumable == True:
            self.items[0].append(item)
        # Non-consumable Spell Card
        elif item.consumable == False:
            self.items[2].append(item)
        # Healing and Support Spells
        elif item.type == 'healing' or item.type == 'support':
            self.items[1].append(item)
        # Healing Items
        elif item.type == 'healingitem':
            self.items[3].append(item)

    def add_treasure(self, id_string, quantity = 1):
        """
        # Function Name: add treasure
        # Purpose: Adds a treasure to the player treasure inventory
        # Inputs:  id_string - ID String of the treasure
        #          quantity - number of items to add
        """

        # Case: there's already an entry. Add the quantity to the currently available count
        if id_string in self.treasures.keys():
            self.treasures[id_string] += quantity
        # Case: There's no entry. set the number available to the quantity desired
        else:
            self.treasures[id_string] = quantity

    def remove_treasure(self, id_string, quantity = 1):

        """
        # Function Name: remves treasure
        # Purpose: Removes a treasure from the player treasure inventory
        # Inputs:  id_string - ID String of the treasure
        #          quantity - number of items to add
        """

        self.treasures[id_string] -= quantity
        # If the number goes below 0, delete the entry
        if self.treasures[id_string] <= 0:
            del(self.treasures[id_string])


######################
# Unit Data class - This contains pared down data that is saved
######################
class UnitData(object):

    def __init__(self, unit):
        """
        # Function Name: __init__
        # Purpose: Initializes a unit data object
        # Inputs: Unit
        """

        self.name = unit.name
        self.moves = unit.moves
        self.spell_actions = unit.spell_actions
        self.traits = unit.traits
        self.reserve_traits = unit.reserve_traits
        self.level = unit.level
        self.exp = unit.exp
        self.trait_points = unit.trait_points
        self.equipped = unit.equipped

    def update_from_unit(self, unit):

        """
        # Function Name: update_from_unit
        # Purpose: Given a unit, copies the data necessary to player data from the unit
        # Inputs: Unit
        """

        self.spell_actions = unit.spell_actions
        self.traits = unit.traits
        self.reserve_traits = unit.reserve_traits
        self.level = unit.level
        self.exp = unit.exp
        self.trait_points = unit.trait_points
        self.equipped = unit.equipped


    def update_to_unit(self, unit):

        """
        # Function Name: update_to_unit
        # Purpose: Given a unit, copies the data necessary to the unit from the player data
        # Inputs: Unit
        """

        unit.spell_actions = self.spell_actions
        unit.traits = self.traits
        unit.reserve_traits = self.reserve_traits
        unit.level = self.level
        unit.exp = self.exp
        unit.equipped = self.equipped
        # Does a stats update
        unit.update_stats()
        unit.update_trait_learning_data()
        unit.refresh_traits()
        unit.refresh_spells()
        unit.trait_points = self.trait_points

######################
# Event Data class - This contains pared down data that is saved
######################
class EventData(object):

    def __init__(self, event):
        """
        # Function Name: __init__
        # Purpose: Initializes a unit data object
        # Inputs: Event - event to assiate with this unit
        """

        self.event_id = event.event_id
        self.name = event.name
        self.sign_up = event.sign_up
        self.done = event.done
        self.manual_cancel = event.manual_cancel
        self.available = event.available
        self.location_name = event.location_name

    def update_from_event(self, event):

        """
        # Function Name: update_from_event
        # Purpose: Given an event, copies the data necessary to player data from the event
        # Inputs: Event - The event to update from
        """
        self.sign_up = event.sign_up
        self.done = event.done
        self.manual_cancel = event.manual_cancel
        self.available = event.available

    def update_to_event(self, event):
        """
        # Function Name: update_to_event
        # Purpose: Given a event, copies the data necessary to the event from the player data
        # Inputs: Event - The event to be updated
        """

        event.sign_up = self.sign_up
        event.done = self.done
        event.manual_cancel = self.manual_cancel
        event.available = self.available



