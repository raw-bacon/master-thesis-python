import itertools
from precoxeterpresentation import PreCoxeterPresentation
from precoxeterword import PreCoxeterWord
from presentation import Presentation
from copy import deepcopy
from coxetergroup import CoxeterGroup
import numpy


class Link(object):
    """
    Links are represented via their Gauss codes.
    """
    def __init__(self, gauss_code):
        self.gauss_code = gauss_code
        self.arcs = self.arcs()
        self.names_of_arcs(self.arcs)
        self.crossings = self.crossings()

    def arcs(self):
        """An arc of a Gauss code is a subcode of the form [-*, *, ..., *, -*], i.e., a literal arc in a
        diagram on paper."""
        number_of_components = len(self.gauss_code)
        arcs = []

        for i in range(number_of_components):
            if not self.gauss_code[i]:
                arcs.append([])
                continue
            start_of_arc = 0
            first_negative = -1
            for j in range(len(self.gauss_code[i])):
                if self.gauss_code[i][j] < 0:
                    end_of_arc = j

                    # in first loop don't do this
                    if first_negative > -1:
                        arcs.append(self.gauss_code[i][start_of_arc:end_of_arc+1])

                    if first_negative == -1:
                        first_negative = j
                    start_of_arc = j
            arcs.append(deepcopy(self.gauss_code[i][start_of_arc:] + self.gauss_code[i][:first_negative+1]))
        arcs.sort()
        return arcs

    @staticmethod
    def names_of_arcs(arcs):
        """Returns a list of letters to be assigned to the arcs"""
        return [chr(i) for i in range(97, 97 + len(arcs))]

    def index_of(self, arc):
        return self.arcs.index(arc)

    def crossings(self):
        """A crossing is a list of length three of arcs, where in the first position of the list one finds the
        over-crossing, and in the second two positions one finds the under-crossing."""

        crossings = []
        max_entry_of_gauss_code = max([max(component + [0]) for component in self.gauss_code])
        for i in range(1, max_entry_of_gauss_code + 1):
            over = []
            under1 = []
            under2 = []
            for arc in self.arcs:
                if i in arc:
                    over = arc
                if -i in arc:
                    if not under1:
                        under1 = arc
                    else:
                        under2 = arc
            if not under2:
                under2 = under1
            crossings.append([over, under1, under2])

        crossings.sort()
        return crossings

    def is_obvious_visible_generating_set(self, input_arcs):
        """Computes whether the arcs in <input_arcs> obviously generate the knot group."""
        did_something = True
        generated_arcs = deepcopy(input_arcs)
        while did_something:
            did_something = False
            for crossing in self.crossings:
                if crossing[0] in generated_arcs and (crossing[1] in generated_arcs or crossing[2] in generated_arcs) \
                        and not (crossing[1] in generated_arcs and crossing[2] in generated_arcs):
                    did_something = True
                    if crossing[1] in generated_arcs:
                        generated_arcs.append(crossing[2])
                    else:
                        generated_arcs.append(crossing[1])

        return len(self.arcs) == len(generated_arcs)

    def wirtinger_rank(self):
        """Computes the minimal number of arcs generating the knot group obviously. This is a (mostly good) upper
        bound on the meridional rank."""
        length = 0
        if not self.arcs:
            return len(self.gauss_code)
        while True:
            length = length + 1
            for combination in itertools.combinations(self.arcs, length):
                potential_generating_set = []
                for arc in combination:
                    potential_generating_set.append(arc)

                if self.is_obvious_visible_generating_set(potential_generating_set):
                    return length

    def all_obvious_visible_generating_sets(self):
        """
        :return: all sets of arcs that generate the knot group in an obvious visible way
        """
        generating_sets = []
        for combination in itertools.combinations(self.arcs, self.wirtinger_rank()):
            combination = list(combination)
            if self.is_obvious_visible_generating_set(combination):
                generating_sets.append(combination)
        return generating_sets

    def get_reflection_quotient_with_respect_to_generating_set(self, generating_set):
        """
        computes the relations of the reflection quotient
        :param generating_set: subset of <self.arcs> that generate obviously the knot group
        :return: a presentation of the reflection quotient
        """
        assert self.is_obvious_visible_generating_set(generating_set), "the input set did not generate"

        gens = self.names_of_arcs(generating_set)
        rels = []

        # mark all elements of <generating_set>
        symbols_of_arcs = [False] * len(self.arcs)
        for i in range(len(generating_set)):
            symbols_of_arcs[self.index_of(generating_set[i])] = gens[i]

        crossings = deepcopy(self.crossings)

        while crossings:
            for crossing in crossings:
                over = crossing[0]
                under1 = crossing[1]
                under2 = crossing[2]
                if symbols_of_arcs[self.index_of(over)]:
                    if symbols_of_arcs[self.index_of(under1)] and not symbols_of_arcs[self.index_of(under2)]:
                        symbols_of_arcs[self.index_of(under2)] = symbols_of_arcs[self.index_of(over)] \
                                                                    + symbols_of_arcs[self.index_of(under1)] \
                                                                    + symbols_of_arcs[self.index_of(over)]
                        crossings.remove(crossing)
                    elif symbols_of_arcs[self.index_of(under2)] and not symbols_of_arcs[self.index_of(under1)]:
                        symbols_of_arcs[self.index_of(under1)] = symbols_of_arcs[self.index_of(over)] \
                                                                    + symbols_of_arcs[self.index_of(under2)] \
                                                                    + symbols_of_arcs[self.index_of(over)]
                        crossings.remove(crossing)
                    elif symbols_of_arcs[self.index_of(under1)] and symbols_of_arcs[self.index_of(under2)]:
                        rels.append(symbols_of_arcs[self.index_of(under1)] + symbols_of_arcs[self.index_of(over)]
                                                                           + symbols_of_arcs[self.index_of(under2)]
                                                                           + symbols_of_arcs[self.index_of(over)])
                        crossings.remove(crossing)
        free = PreCoxeterPresentation(gens, [])
        rels = [PreCoxeterWord(rel, free).remove_squares().string for rel in rels]
        if rels:
            longest = max(rels, key=len)
            rels.remove(longest)
        return PreCoxeterPresentation(gens, rels)

    def determinant(self):
        length = len(self.arcs)
        if length == 0:
            return 1
        matrix = numpy.zeros((length, length))
        crossings = self.crossings
        for i in range(length):
            crossing = crossings[i]
            matrix[i][self.index_of(crossing[0])] = 2
            matrix[i][self.index_of(crossing[1])] = - 1
            matrix[i][self.index_of(crossing[2])] = - 1
        return int(numpy.abs(numpy.linalg.det(matrix[:length - 1, :length - 1])))

    def all_obvious_visible_coxeter_quotients_with_respect_to_all_generating_sets(self, mode='normal'):
        """
        a coxeter quotient is obvious if generators of the presentation map to generating reflections in the quotient
        and it is visible if the generators of the presentation are meridians visible in the given diagram.
        :param mode: if set to 'interactive', the function will update the user on the progress
        :return: all matrices that are coxeter quotients of the link
        """
        presentations = []
        generating_sets = self.all_obvious_visible_generating_sets()
        quotients = []
        for generating_set in generating_sets:
            presentations.append(self.get_reflection_quotient_with_respect_to_generating_set(generating_set))
        presentations = Presentation.remove_permutations_from_list(presentations)
        # presentations.sort(key=Presentation.max_relator_length)
        for presentation in presentations:
            if mode == 'interactive':
                print("Considering presentation " + (presentations.index(presentation) + 1).__str__() +
                      " / " + len(presentations).__str__() + " of relator length " +
                      presentation.max_relator_length().__str__())
            for quotient in presentation.all_obvious_visible_coxeter_quotients():
                if not CoxeterGroup.matrix_is_permutation_of_any(quotient, quotients):
                    if mode == 'interactive':
                        print("Found a new quotient: " + quotient.__str__())
                    quotients.append(quotient)

        return quotients

    def all_max_rank_quotients(self, mode='normal'):
        """
        a coxeter quotient is obvious if generators of the presentation map to generating reflections in the quotient
        and it is visible if the generators of the presentation are meridians visible in the given diagram.
        :param mode: if set to 'interactive', the function will update the user on the progress
        :return: all matrices that are coxeter quotients of the link
        """
        presentations = []
        generating_sets = self.all_obvious_visible_generating_sets()
        quotients = []
        for generating_set in generating_sets:
            presentations.append(self.get_reflection_quotient_with_respect_to_generating_set(generating_set))
        presentations = Presentation.remove_permutations_from_list(presentations)
        presentations.sort(key=Presentation.max_relator_length)
        for presentation in presentations:
            if mode == 'interactive':
                print("Considering presentation " + (presentations.index(presentation) + 1).__str__() +
                      " / " + len(presentations).__str__() + " of relator length " +
                      presentation.max_relator_length().__str__())
            # for quotient in presentation.all_obvious_visible_coxeter_quotients():
            for quotient in presentation.all_obvious_visible_coxeter_quotients_max_rank():
                if not CoxeterGroup.matrix_is_permutation_of_any(quotient, quotients):
                    if mode == 'interactive':
                        print("Found a new quotient: " + quotient.__str__())
                    quotients.append(quotient)

        return quotients

#    def coloring_dimension(self):
#        gens = self.all_obvious_visible_generating_sets()[0]
#        pres = self.get_reflection_quotient_with_respect_to_generating_set(gens)
#        det = self.determinant()
#        prime_factors = Link.factors(det)
#        for d in prime_factors:
#            count = 0
#            combs = itertools.combinations_with_replacement(range(d), len(gens))
#            for c in combs:

    @staticmethod
    def factors(n):
        factors = []
        for d in PreCoxeterPresentation.all_primes_less_than(n):
            if n % d == 0:
                factors.append(d)
                n = int(n / d)
        return factors
