from braid import Braid
import numpy
import itertools


class TorusLink(Braid):
    def __init__(self, p, q):
        braid_code = numpy.sign(p*q)*(list(range(1, abs(q))) * abs(p))
        super(TorusLink, self).__init__(braid_code)

    def all_obvious_visible_generating_sets(self):
        """
        Note that due to the symmetry of torus links, one can fix the first arc.
        :return: all sets of arcs that generate the knot group in an obvious visible way
        """
        generating_sets = []
        for combination in itertools.combinations(self.arcs[1:], self.wirtinger_rank() - 1):
            combination = [self.arcs[0]] + list(combination)
            if self.is_obvious_visible_generating_set(combination):
                generating_sets.append(combination)
        return generating_sets
