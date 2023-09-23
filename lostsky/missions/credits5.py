from lostsky.worldmap.event import ConversationEvent
from lostsky.battle.mapdata import MapData
from lostsky.battle.mapaction import MapActionEvent

class Mission(ConversationEvent):

    def __init__(self):
        # Event Data
        name = 'Credits 5'
        location = 'Human Village'
        id_string = 'Credits5'
        prereqs = ['CH5ST2']
        show_rewards = False
        desc = ''

        ConversationEvent.__init__(self, name, location,
                             id_string, prereqs,
                             show_rewards, desc)

        # Map Data
        map_name = 'ch5st2.txt'
        mission_type = 'conversation'
        objective = None
        deploy_data = {}
        reward_list = []

        # Enemy Unit Data
        enemy_unit_data = [
                              {'template_name': 'Fuyuhana',
                                 'unit_name': 'Fuyuhana',
                                     'level': 5 },
                              {'template_name': 'Ayaka',
                                 'unit_name': 'Ayaka',
                                     'level': 5 },



        ]

        initial_spells = {}
        initial_traits = {}
        initial_ai_states = {}
        initial_locations = {'Ayaka':(14, 20),
                             'Fuyuhana':(-1,-1)

                             }

        reserve_units = []
        all_landmarks = []


        required_starters = []
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
        Ayaka visits the place where the final battle took place, reflecting on her failures.

        Fuyuhana's image appears and Ayaka is at first angry that conflict ended the way it did, but
        Fuyuhana thanks her for her service and departs peacefully.

        Knowing her time is up too, Ayaka leaves the forest to the other Kodama.

        """
        self.set_cursor_state(False)
        self.set_stats_display(False)

        self.fade_from_color('black', 2.0)

        self.center_on('Ayaka')
        self.emote('Ayaka', 'dotdotdot')
        self.move_unit('Ayaka', (14, 19))
        self.pause(0.3)
        self.move_unit('Ayaka', (14, 18))
        self.pause(0.3)
        self.move_unit('Ayaka', (14, 17))
        self.pause(0.3)
        self.move_unit('Ayaka', (14, 16))
        self.pause(0.3)
        self.move_unit('Ayaka', (14, 15))
        self.center_on('Ayaka')
        self.emote('Ayaka', 'dotdotdot')
        self.emote('Ayaka', 'dotdotdot')
        self.emote('Ayaka', 'dotdotdot')
        self.emote('Ayaka', 'dotdotdot')
        self.pause(0.5)
        self.move_unit('Ayaka', (14, 16))
        self.pause(0.3)
        self.move_unit('Ayaka', (14, 17))
        self.pause(0.3)
        self.move_unit('Ayaka', (14, 18))


        self.fade_to_color('white', 0.5)
        self.map.all_units_by_name['Fuyuhana'].sprite.transparent_flag = True
        self.map.all_units_by_name['Fuyuhana'].sprite.update()

        self.set_unit_pos('Fuyuhana', (14, 14))
        self.fade_from_color('white', 0.5)

        self.move_unit('Ayaka', (14, 16))

        self.emote('Ayaka', 'exclamation')
        self.startle('Ayaka')
        self.emote('Ayaka', 'annoyed')
        self.emote('Ayaka', 'dotdotdot')

        self.startle('Fuyuhana')
        self.emote('Fuyuhana', 'dotdotdot')
        self.emote('Fuyuhana', 'heart')
        self.emote('Fuyuhana', 'musicnote')


        self.fade_to_color('white', 0.5)
        self.set_unit_pos('Fuyuhana', (-1, -1))
        self.fade_from_color('white', 0.5)

        self.emote('Ayaka', 'dotdotdot')

        self.move_unit('Ayaka', (14, 16))

        self.fade_to_color('white', 0.5)
        self.map.all_units_by_name['Ayaka'].sprite.transparent_flag = True
        self.map.all_units_by_name['Ayaka'].sprite.update()
        self.fade_from_color('white', 0.5)


        self.pause(0.3)

        self.move_unit('Ayaka', (14, 18))

        self.emote('Ayaka', 'dotdotdot')

        self.move_unit('Ayaka', (14, 19))

        self.emote('Ayaka', 'musicnote')

        self.pause(1.0)

        self.fade_to_color('white', 3.0)
        self.kill_unit('Ayaka')
        self.fade_from_color('white', 1.5)

        self.pause(1.0)

        self.fade_to_color('black', 2.0)


        self.set_cursor_state(True)
        self.set_stats_display(True)
        self.done = True
