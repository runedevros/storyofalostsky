from lostsky.worldmap.event import ConversationEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent

class Mission(ConversationEvent):

    def __init__(self):
        # Event Data
        name = 'Credits 8'
        location = 'Western Village Path'
        id_string = 'Credits8'
        prereqs = ['CH5ST2']
        show_rewards = False
        desc = "No Description"
        ConversationEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'credits1.txt'
        mission_type = 'conversation'
        objective = None

        deploy_data = {'enable':False,
                       'max_units':None,
                       'preset_units':None,
                       'boxes':[]
                       }

        reward_list = []


        enemy_unit_data = [{'template_name': 'CreditsAlice',
                                 'unit_name': 'Alice',
                                     'level': 5 },
                           {'template_name': 'Nitori',
                                 'unit_name': 'Nitori',
                                     'level': 5 },

                           {'template_name': 'Tsubaki',
                                 'unit_name': 'Tsubaki',
                                     'level': 5 },
                           {'template_name': 'Momiji',
                                 'unit_name': 'Momiji',
                                     'level': 5 },

                           {'template_name': 'Wriggle',
                                 'unit_name': 'Wriggle',
                                     'level': 5 },
                           {'template_name': 'Haruna',
                                 'unit_name': 'Haruna',
                                     'level': 5 },
                           {'template_name': 'Kotone',
                                 'unit_name': 'Kotone',
                                     'level': 5 },
                           {'template_name': 'Miu',
                                 'unit_name': 'Miu',
                                     'level': 5 },

                           {'template_name': 'Akyu',
                                 'unit_name': 'Akyu',
                                     'level': 5 },

                           ]

        initial_spells = {}

        initial_traits = {}

        initial_ai_states = {}

        initial_locations = {'Reimu':(11, 8),
                             'Marisa':(12, 8),
                             'Alice':(-1, -1),
                             'Ran':(-1,-1),
                             'Chen':(-1,-1),
                             'Youmu':(-1,-1),
                             'Yukari':(-1,-1),
                             'Yuyuko':(-1,-1),
                             'Mokou':(-1,-1),
                             'Keine':(-1,-1),
                             'Kaguya':(-1,-1),
                             'Aya':(-1,-1),
                             'Eirin':(-1,-1),
                             'Reisen':(-1,-1),

                             }

        reserve_units = ['Nitori', 'Tsubaki', 'Momiji', 'Akyu', 'Wriggle', 'Haruna', 'Kotone', 'Miu',]#[list of unit names to deploy later in mission]

        all_landmarks = [
                         {'name':'Shrine',
                         'id_string':'shrine',
                         'location':(11, 7)},

                         {'name':'Torii',
                         'id_string':'small_torii',
                         'location':(11, 10)},

                         {'name':'RHouse',
                         'id_string':'house_1',
                         'location':(13, 4)},


                          {'name':'CB1',
                          'id_string':'cherryblossom_tree',
                          'location':(7, 7)},

                          {'name':'CB2',
                          'id_string':'cherryblossom_tree',
                          'location':(8, 4)},

                          {'name':'CB3',
                          'id_string':'cherryblossom_tree',
                          'location':(14, 5)},

                          {'name':'CB4',
                          'id_string':'cherryblossom_tree',
                          'location':(17, 8)},

                          {'name':'lp1',
                          'id_string':'lilypad',
                          'location':(10, 3)},

                         ]

        required_starters = ['Reimu', 'Marisa', 'Ran', 'Chen', 'Youmu', 'Mokou', 'Kaguya', 'Keine', 'Eirin', 'Reisen', 'Aya', 'Yuyuko', 'Yukari']
        pre_mission_MAE = PreMissionMAE()
        mid_mission_MAE_list = []
        required_survivors = []
        post_mission_MAE = None

        self.map_data = MapData(map_name, mission_type, objective,
                                deploy_data, reward_list, enemy_unit_data,
                                initial_spells, initial_traits, initial_ai_states,
                                initial_locations, reserve_units, all_landmarks,
                                required_starters, pre_mission_MAE, mid_mission_MAE_list,
                                required_survivors, post_mission_MAE)

class PreMissionMAE(MapActionEvent):

    def __init__(self):
        triggers = []
        MapActionEvent.__init__(self, triggers)

    def execute(self):
        """
        Reimu and Marisa at the shrine. Marisa arrives to try and organize a party. She runs off to get people.
        """

        self.set_bg_overlay('Sunset')
        self.set_cursor_state(False)
        self.set_stats_display(False)

        # Use the sunset color overlay

        if self.map.engine.check_event_completion(['CH2SQ2']):
            self.set_unit_pos('Alice', (13, 8))

        self.fade_from_color('black', 2.0)

        self.emote('Reimu', 'questionmark')

        # First guests to arrive are Youmu and crew
        self.fade_to_color('black', 1.0)
        self.set_unit_pos('Youmu', (11, 10))
        self.set_unit_pos('Yuyuko', (11, 11))
        self.set_unit_pos('Ran', (10, 12))
        self.set_unit_pos('Yukari', (11, 12))
        self.set_unit_pos('Chen', (12, 12))
        self.fade_from_color('black', 1.0)


        self.move_unit('Youmu', (11, 9))
        self.move_unit('Yuyuko', (11, 10))

        self.emote('Marisa', 'musicnote')
        self.emote('Youmu', 'musicnote')
        self.emote('Yukari', 'heart')
        self.emote('Reimu', 'scribble')


        # Move Youmu's crew over to the side of the map
        # Add in Momiji and co
        self.fade_to_color('black', 1.0)
        self.set_unit_pos('Youmu', (6, 8))
        self.set_unit_pos('Yuyuko', (7, 8))
        self.set_unit_pos('Ran', (8, 9))
        self.set_unit_pos('Yukari', (8, 10))
        self.set_unit_pos('Chen', (8, 11))
        self.deploy_unit('Momiji', (10, 10))
        self.deploy_unit('Tsubaki', (11, 9))
        self.deploy_unit('Nitori', (12, 10))
        self.fade_from_color('black', 1.0)

        # Aya comes in and takes some photos
        self.emote('Tsubaki', 'musicnote')
        self.set_unit_pos('Aya', (7, 15))
        self.move_unit('Aya', (7, 10))
        self.startle('Aya')
        self.fade_to_color('white', 0.1)
        self.fade_from_color('white', 0.1)
        self.move_unit('Aya', (15, 8))
        self.startle('Aya')
        self.fade_to_color('white', 0.1)
        self.fade_from_color('white', 0.1)
        self.move_unit('Aya', (11, 11))
        self.startle('Aya')
        self.fade_to_color('white', 0.1)
        self.fade_from_color('white', 0.1)

        # Move Nitori and Aya to Reimu's crew, Tsubaki and Momiji to Youmu's group
        self.fade_to_color('black', 1.0)
        self.set_unit_pos('Nitori', (12, 7))
        self.set_unit_pos('Aya', (10, 8))
        self.set_unit_pos('Momiji', (7, 11))
        self.set_unit_pos('Tsubaki', (6, 10))
        # It's night now since some time has passed
        self.set_bg_overlay('Night')
        self.set_unit_pos('Mokou', (11, 10))
        self.deploy_unit('Akyu', (10, 10))
        self.set_unit_pos('Keine', (12, 10))
        self.fade_from_color('black', 1.0)

        # Kaguya rudely interrupts and sends Mokou flying into the pond.
        self.emote('Akyu', 'musicnote')
        self.startle('Mokou')
        self.emote('Keine', 'questionmark')
        self.set_unit_pos('Kaguya', (11, 16))
        self.move_unit('Kaguya', (11, 10))
        self.move_unit('Mokou', (11, 2))

        self.emote('Reimu','exclamation')
        self.emote('Mokou', 'scribble')

        self.startle('Aya')
        self.fade_to_color('white', 0.1)
        self.fade_from_color('white', 0.1)

        self.set_unit_pos('Eirin', (10, 14))
        self.set_unit_pos('Reisen', (12, 14))

        # Eirin drags Kaguya back
        self.move_unit('Eirin', (10, 11))
        self.move_unit('Reisen', (12, 11))
        self.emote('Eirin', 'questionmark')
        self.move_unit('Eirin', (11, 11))
        self.move_unit('Kaguya', (11, 11))
        self.move_unit('Eirin', (10, 11))


        # Eientei Crew gets a spot to the right side of the map
        self.fade_to_color('black', 1.0)
        self.set_unit_pos('Kaguya', (15, 10))
        self.set_unit_pos('Eirin', (16, 10))
        self.set_unit_pos('Mokou', (15, 12))
        self.set_unit_pos('Keine', (16, 12))
        self.set_unit_pos('Reisen', (14, 11))

        # Akyu goes with Youmu's party
        self.set_unit_pos('Akyu', (6, 9))

        self.deploy_unit('Haruna', (11, 10))
        self.deploy_unit('Kotone', (10, 11))
        self.deploy_unit('Miu', (12, 11))
        if self.map.engine.check_event_completion(['CH5SQ1']):
            self.deploy_unit('Wriggle', (11, 11))

        self.fade_from_color('black', 1.0)

        self.emote('Haruna', 'musicnote')
        self.emote('Reimu', 'exclamation')
        self.emote('Marisa', 'musicnote')
        self.emote('Reimu', 'dotdotdot')
        self.emote('Reimu', 'musicnote')

        self.fade_to_color('black', 1.0)

        self.set_unit_pos('Haruna', (6, 11))
        if self.map.engine.check_event_completion(['CH5SQ1']):
            self.set_unit_pos('Wriggle', (9, 7))
        self.set_unit_pos('Kotone', (9,8))
        self.set_unit_pos('Miu', (17, 11))

        self.fade_from_color('black', 1.0)

        self.emote('Youmu', 'heart')
        self.emote('Yuyuko', 'musicnote')
        self.emote('Tsubaki', 'musicnote')
        self.startle('Mokou')
        self.emote('Kaguya', 'scribble')
        self.emote('Mokou', 'musicnote')
        self.emote('Miu', 'heart')

        self.emote('Reimu', 'musicnote')


        self.move_unit('Aya', (11, 4))
        self.emote('Aya', 'musicnote')

        self.pause(0.5)
        self.play_sfx('camera')
        self.fade_to_color('white', 0.1)
        self.fade_from_color('white', 0.1)

        self.pause(1.0)

        self.fade_to_color('black', 5.0)



        self.done = True