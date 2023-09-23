

################
#  Map Data Object
# Purpose: Assembles all the information needed for a single map
###############
class MapData(object):

    def __init__(self, map_name, mission_type, objective,
                 deploy_data, reward_list, enemy_unit_data,
                 initial_spells, initial_traits, initial_ai_states,
                 initial_locations, reserve_units, all_landmarks,
                 required_starters, pre_mission_MAE, mid_mission_MAE_list,
                 required_survivors, post_mission_MAE):

        """
        # Function name: __init__
        # Purpose: Creates a data object for each mission
        # Inputs:
                    map_name - filename of map
                    mission_type - 'battle' or 'conversation'
                    objective - Specified in the following way depending on objective
                     None - Use None for conversation missions

                     {'type':'Defeat Boss',
                      'target': name,
                      'desc': description}

                     {'type':'Defeat All and Protect',
                     'target': name,
                     'desc': description}

                     {'type':'Survive',
                     'turns':#turns,
                     'desc': description}

                     {'type':'Survive',
                     'turns': turn_limit,
                     'location_name': destination_name,
                     'location_box': (x, y, dx, dy),
                     'desc': description}}

                     {'type':'Arrive and Defeat Boss',
                     'target': name,
                     'location_name': destination_name,
                     'location_box': (x, y, dx, dy),
                     'desc': description}}

                     {'type':'Capture Spirit Sources',
                      'number': number_to_capture,
                      'ssps': [list of ssp objects],
                      'desc': description}}

                     {'type':'Defend and Defeat Boss',
                     'target': name,
                     'location_name': destination_name,
                     'location_box': (x, y, dx, dy),
                     'desc': description}}


                    deploy_data - {'enable': True/False
                                   'max_units': Max number of units to deploy
                                   'preset_units': {'unit_name':(x, y)}
                                   'boxes': [List of (x, y, dx, dy) specifying where
                                    units can be deploy.]
                                    }

                    reward_list - [list of ('type', 'id_string') for mission rewards]
                    enemy_unit_data - [list of dicts of the following format]
                                {'template_name': template_name,
                                 'unit_name': unit_name,
                                 'level': level
                                }
                    initial_spells - {'unit_name':[list of spells to assign]
                                        }
                    initial_traits - {'unit_name':[list of traits to assign]
                                        }
                    initial_ai_states - {'unit_name':'ai state id_string'}
                    initial_locations - {'unit_name':(x, y)}
                    reserved_units - [list of unit names to deploy later in mission]
                    all_landmarks - [list of all landmarks (id_string, (x, y))]

                    required_starters - [list of units required for pre mission MAE]
                    pre_mission_MAE
                    mid_mission_MAE_list - [list of mid mission MAEs to use]
                    required_survivors - [list of units required for post mission MAE]
                    post_mission_MAE

        """
        # General mission data
        self.text_map = map_name

        self.mission_type = mission_type
        if self.mission_type == 'battle':
            self.objective = objective
        else:
            self.objective = None

        if self.mission_type == 'battle' and deploy_data['enable']:
            self.enable_deploy = True
            self.deploy_boxes = deploy_data['boxes']
            self.max_deployed_units = deploy_data['max_units']
            self.preset_units = deploy_data['preset_units']

            if 'default_locations' in deploy_data.keys():
                self.default_locations = deploy_data['default_locations']
            else:
                self.default_locations = {}

        else:
            self.enable_deploy = False
            self.deploy_boxes = []
            self.max_deployed_units = 0
            self.preset_units = {}
        self.rewards_list = reward_list


        # Data to set up units on the map
        self.enemy_unit_data = enemy_unit_data
        self.initial_spells = initial_spells
        self.initial_traits = initial_traits
        self.initial_locations = initial_locations
        self.reserve_units = reserve_units
        self.initial_AI = initial_ai_states

        # Landmarks
        self.all_landmarks = all_landmarks

        # MAE Data
        self.required_starters = required_starters
        self.pre_mission_MAE = pre_mission_MAE

        self.mid_mission_MAE_list = mid_mission_MAE_list

        self.required_survivors = required_survivors
        self.post_mission_MAE = post_mission_MAE
