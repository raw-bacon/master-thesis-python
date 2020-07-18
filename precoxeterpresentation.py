from presentation import Presentation
from copy import deepcopy
import itertools
import numpy
from precoxeterword import PreCoxeterWord


class PreCoxeterPresentation(Presentation):
    """
    A Pre-Coxeter group is a group, given as a presentation, with generators all of order two. Removes all squares
    from the relations not of the form x^2
    """

    def __init__(self, gens, rels):
        super(PreCoxeterPresentation, self).__init__(gens, rels)
        for i in range(len(self.rels)):
            word = PreCoxeterWord(self.rels[i], self)
            self.rels[i] = word.remove_squares().string
        for gen in self.gens:
            self.rels.append(gen + gen)

        # remove duplicates
        self.rels = list(set(self.rels))
        self.rels.sort(key=len)

        # remove empty relations
        self.rels = [x for x in self.rels if x]

    def has_coxeter_quotient_with_matrix(self, matrix):
        """
        :param matrix: a (square) coxeter matrix
        :return:
        """
        from coxetergroup import CoxeterGroup
        from coxeterword import CoxeterWord

        assert CoxeterGroup.is_valid(matrix)

        coxeter_group = CoxeterGroup(matrix, gens=self.gens[:])
        for rel in self.rels:
            if not CoxeterWord(rel, coxeter_group).is_identity():
                return False
        return True

    def all_obvious_visible_coxeter_quotients(self):
        from coxetergroup import CoxeterGroup

        quotients = []
        maximal_rank = len(self.gens)
        for rank in range(2, maximal_rank + 1):
            current_rank_quotients = []
            for quotient in self.all_obvious_visible_prime_coxeter_quotients_of_rank(rank):
                if quotient not in current_rank_quotients:
                    current_rank_quotients.append(quotient)
            if not current_rank_quotients:
                continue
            # compute the non-prime ones
            if rank == len(self.gens):
                super_quotient = CoxeterGroup.join(current_rank_quotients).matrix
                for i in range(rank):
                    for j in range(i + 1, rank):
                        copy = deepcopy(super_quotient)
                        copy[i][j] = copy[j][i] = 0
                        if self.has_coxeter_quotient_with_matrix(copy):
                            super_quotient[i][j] = super_quotient[j][i] = 0
                            continue

                        copy = deepcopy(super_quotient)
                        k = 1
                        while self.has_coxeter_quotient_with_matrix(copy):
                            k = k + 1
                            copy[i][j] = copy[j][i] = k * super_quotient[i][j]
                        super_quotient[i][j] = super_quotient[j][i] = (k - 1) * super_quotient[i][j]
                super_quotient = CoxeterGroup(super_quotient, gens=self.gens)
                quotients.append(super_quotient)
            else:
                quotients = quotients + current_rank_quotients
        return quotients

    def all_obvious_visible_coxeter_quotients_max_rank(self):
        from coxetergroup import CoxeterGroup

        quotients = []
        rank = len(self.gens)
        current_rank_quotients = []
        for quotient in self.all_obvious_visible_prime_coxeter_quotients_of_rank(rank):
            if quotient not in current_rank_quotients:
                current_rank_quotients.append(quotient)
        if not current_rank_quotients:
            return []
        # compute the non-prime ones
        if rank == len(self.gens):
            super_quotient = CoxeterGroup.join(current_rank_quotients).matrix
            for i in range(rank):
                for j in range(i + 1, rank):
                    copy = deepcopy(super_quotient)
                    copy[i][j] = copy[j][i] = 0
                    if self.has_coxeter_quotient_with_matrix(copy):
                        super_quotient[i][j] = super_quotient[j][i] = 0
                        continue

                    copy = deepcopy(super_quotient)
                    k = 1
                    while self.has_coxeter_quotient_with_matrix(copy):
                        k = k + 1
                        copy[i][j] = copy[j][i] = k * super_quotient[i][j]
                    super_quotient[i][j] = super_quotient[j][i] = (k - 1) * super_quotient[i][j]
            super_quotient = CoxeterGroup(super_quotient, gens=self.gens)
            quotients.append(super_quotient)
        else:
            quotients = quotients + current_rank_quotients
        return quotients

    # "private" method
    def all_obvious_visible_prime_coxeter_quotients_of_rank(self, rank):
        from coxetergroup import CoxeterGroup

        quotients = []
        if rank < len(self.gens):
            combs = itertools.combinations(self.gens, 2)
            for c in combs:
                new_presentation = self.identify_generators(c)
                for quotient in new_presentation.all_obvious_visible_coxeter_quotients():
                    if not CoxeterGroup.matrix_is_permutation_of_any(quotient, quotients):
                        quotients.append(quotient)
            return quotients

        non_trivial_relations = [rel for rel in self.rels if len(rel) > 2]
        if not non_trivial_relations:
            max_entry = 2
        else:
            max_entry = len(max(non_trivial_relations, key=len))
        matrices = PreCoxeterPresentation.prime_coxeter_matrices_of_max_entry(max_entry, rank)
        for matrix in matrices:
            if self.has_coxeter_quotient_with_matrix(matrix):
                if not CoxeterGroup.matrix_is_permutation_of_any(CoxeterGroup(matrix, gens=self.gens), quotients):
                    quotients.append(CoxeterGroup(matrix, gens=self.gens))
        return quotients

    @staticmethod
    def lcm(numbers):
        assert numbers
        lcm = numbers[0]
        for i in range(1, len(numbers)):
            lcm = numpy.lcm(lcm, numbers[i])
        return lcm

    @staticmethod
    def all_primes_less_than(maximum):
        """
        :param maximum: the maximum prime
        :return: a list of all primes less than or equal to <maximum>, including zero
        """
        primes = []
        numbers = list(range(2, maximum + 1))
        for p in numbers:
            if p != 0:
                primes.append(p)
                k = 1
                while k * p <= maximum:
                    numbers[k * p - 2] = 0
                    k = k + 1
        return primes

    @staticmethod
    def prime_coxeter_matrices_of_max_entry(maximum, rank):
        primes = PreCoxeterPresentation.all_primes_less_than(maximum)
        matrices = []

        # 1 + ... + rank - 1 = rank * (rank - 1) / 2
        count = int(rank * (rank - 1) / 2)

        combinations = itertools.product(primes, repeat=count)

        for combination in combinations:
            row = 0
            col = 1
            matrix = numpy.ones((rank, rank))
            for i in range(count):
                matrix[row, col] = combination[i]
                matrix[col, row] = combination[i]
                if col < rank - 1:
                    col = col + 1
                else:
                    row = row + 1
                    col = row + 1

            matrix_as_array_of_arrays = [[]] * rank
            for i in range(rank):
                matrix_as_array_of_arrays[i] = [0] * rank
                for j in range(rank):
                    matrix_as_array_of_arrays[i][j] = int(matrix[i, j])
            matrices.append(matrix_as_array_of_arrays)

        return matrices

    def identify_generators(self, some_generators):
        first = some_generators[0]
        new_rels = []
        for i in range(len(self.rels)):
            for gen in some_generators[1:]:
                new_rels.append(self.rels[i].replace(gen, first))

        new_gens = [first]
        for gen in self.gens:
            if gen not in some_generators:
                new_gens.append(gen)
        return PreCoxeterPresentation(new_gens, new_rels)
