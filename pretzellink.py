from link import Link
import itertools


class PretzelLink(Link):
    def __init__(self, weights):
        super(PretzelLink, self).__init__(PretzelLink.gauss_code_from_weights(weights))

    @staticmethod
    def gauss_code_from_weights(weights):
        strand = 0

        # 0 for down; 1 for up
        height = 0

        # 0 for left, 1 for right
        direction = 0
        components = []
        component = []
        unvisited_positions = list(itertools.product(range(len(weights)), [0, 1], [0, 1]))

        while unvisited_positions:
            position = (strand, height, direction)

            if position not in unvisited_positions:
                components.append(component)
                component = []
                position = unvisited_positions[0]
                strand = position[0]
                height = position[1]
                direction = position[2]
            unvisited_positions.remove(position)

            # Position down
            if height == 0:
                crossing = sum([abs(w) for w in weights[:strand]]) + 1
                if weights[strand] < 0:
                    start_sign = (-1) ** (direction + 1)
                else:
                    start_sign = (-1) ** direction
                for i in range(crossing, crossing + abs(weights[strand])):
                    component.append(start_sign * (-1) ** ((i - crossing) % 2) * i)

            # Position up
            else:
                crossing = sum([abs(w) for w in weights[:strand + 1]])
                if weights[strand] < 0:
                    start_sign = (-1) ** direction
                else:
                    start_sign = (-1) ** (direction + 1)
                for i in reversed(range(crossing - abs(weights[strand]) + 1, crossing + 1)):
                    component.append(start_sign * (-1) ** ((i - crossing) % 2) * i)

            height = (height + 1) % 2

            # even weight
            if weights[strand] % 2 == 0:
                unvisited_positions.remove((strand, height, direction))
                if direction == 0:
                    strand = (strand - 1) % len(weights)
                else:
                    strand = (strand + 1) % len(weights)
                direction = (direction + 1) % 2

            # odd weight
            else:
                unvisited_positions.remove((strand, height, (direction + 1) % 2))
                if direction == 0:
                    strand = (strand + 1) % len(weights)
                else:
                    strand = (strand - 1) % len(weights)
        components.append(component)
        return components
