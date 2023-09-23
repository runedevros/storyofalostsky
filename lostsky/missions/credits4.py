from lostsky.worldmap.event import ConversationEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent

class Mission(ConversationEvent):

    def __init__(self):
        # Event Data
        name = 'Credits 4'
        location = 'Human Village'
        id_string = 'Credits4'
        prereqs = ['CH5ST2']
        show_rewards = False
        desc = ''

        ConversationEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch4st2.txt'
        mission_type = 'conversation'
        objective = None
        deploy_data = {}
        reward_list = []

        # Enemy Unit Data
        enemy_unit_data = []

        initial_spells = {}
        initial_traits = {}
        initial_ai_states = {}
        initial_locations = {'Eirin':(20,16),
                             'Reisen':(22,16),
                             'Kaguya':(21,17),

                             'Mokou':(21, 20),
                             'Marisa':(40, 19),

                             }

        reserve_units = []
        all_landmarks = [{'name':'Eientei',
                          'id_string':'eientei',
                          'location':(20, 16)}]


        required_starters = ['Mokou', 'Kaguya', 'Reisen', 'Eirin', 'Marisa']
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
        Kaguya and Mokou are getting into their usual fights again.

        While they're fighting, Marisa interrupts the battle.

        """
        self.set_cursor_state(False)
        self.set_stats_display(False)

        self.fade_from_color('black', 2.0)

        self.center_on('Kaguya')
        self.emote('Kaguya', 'annoyed')
        self.emote('Mokou', 'scribble')

        self.move_unit('Kaguya', (21, 19))
        self.startle('Kaguya')
        self.emote('Mokou', 'exclamation')
        self.startle('Mokou')

        self.move_unit('Mokou', (21, 19))
        self.fade_to_color('white', 0.2)
        self.set_unit_pos('Kaguya', (22, 19))
        self.fade_from_color('white', 0.2)
        self.emote('Kaguya', 'musicnote')
        self.emote('Mokou', 'annoyed')

        self.startle('Kaguya')
        self.emote('Mokou', 'exclamation')
        self.emote('Kaguya', 'questionmark')

        self.move_unit('Marisa', (22, 19))
        self.move_unit('Kaguya', (22, 17))

        self.emote('Eirin', 'exclamation')
        self.emote('Mokou', 'scribble')
        self.emote('Kaguya', 'scribble')

        self.emote('Marisa', 'sweatdrop')
        self.startle('Marisa')
        self.emote('Marisa', 'lightbulb')
        self.emote('Marisa', 'musicnote')
        self.startle('Marisa')

        self.emote('Kaguya', 'musicnote')
        self.emote('Mokou', 'musicnote')


        self.fade_to_color('black', 2.0)


        self.set_cursor_state(True)
        self.set_stats_display(True)
        self.done = True
