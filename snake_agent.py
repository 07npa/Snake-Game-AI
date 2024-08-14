import numpy as np
from une_ai.models import Agent


class SnakeAgent(Agent):

    # DO NOT CHANGE THE PARAMETERS OF THIS METHOD
    def __init__(self, agent_program):
        # DO NOT CHANGE THE FOLLOWING LINES OF CODE
        super().__init__("Snake Agent", agent_program)

    HEAD_DIRECTIONS = ['up', 'down', 'left', 'right']
    MOUTH_ACTIONS = ['open', 'close']
    # Define the dictionary mapping each direction to its opposite
    OPPOSITE_DIRECTIONS = {
        'up': 'down',
        'down': 'up',
        'left': 'right',
        'right': 'left'
    }

    def add_all_sensors(self):
        self.add_sensor('body-sensor',
                        [(0, 0)],
                        lambda v: isinstance(v, list)
                        and len(v[0]) == 2
                        and isinstance(v[0], tuple)
                        and isinstance(v[0][0], int)
                        and isinstance(v[0][1], int)
                        )

        self.add_sensor('food-sensor',
                        [(0, 0, 0)],
                        lambda v: isinstance(v, list)
                        and len(v[0]) == 3
                        and isinstance(v[0], tuple)
                        and isinstance(v[0][0], int)
                        and isinstance(v[0][1], int)
                        and isinstance(v[0][2], (int, np.int32, np.int64))
                        )

        self.add_sensor('obstacles-sensor',
                        [(0, 0)],
                        lambda v: isinstance(v, list)
                        and len(v[0]) == 2
                        and isinstance(v[0], tuple)
                        and isinstance(v[0][0], int)
                        )

        self.add_sensor('clock',
                        0,
                        lambda v: isinstance(v, int)
                        and v >= 0)

    def add_all_actuators(self):
        self.add_actuator('head', 'up',
                          lambda v: v in SnakeAgent.HEAD_DIRECTIONS)
        self.add_actuator('mouth', 'close',
                          lambda v: v in SnakeAgent.MOUTH_ACTIONS)

    def add_all_actions(self):
        # Move actions
        for direction in SnakeAgent.HEAD_DIRECTIONS.copy():
            self.add_action('move-{0}'.format(direction),
                            lambda d=direction: {'head': d}
                            if d != self.get_opposite_direction() else {}
                            )
        # Mouth open-close actions
        for mouth in SnakeAgent.MOUTH_ACTIONS.copy():
            self.add_action('{0}-mouth'.format(mouth),
                            lambda m=mouth: {'mouth': m}
                            )

    # Class method
    def get_opposite_direction(self):
        return SnakeAgent.OPPOSITE_DIRECTIONS.get(self.read_actuator_value('head'), None)
