from precoxeterpresentation import PreCoxeterPresentation
from itertools import permutations
from copy import deepcopy
from reflectionrepresentation import ReflectionRepresentation


class CoxeterGroup(PreCoxeterPresentation):
    INFINITY = 0

    def __init__(self, matrix, gens=()):
        """
        :param matrix: a square matrix consisting of integers (and 0 substituting infinity), where ones are
        on the diagonal
        """
        assert CoxeterGroup.is_valid(matrix)
        self.matrix = matrix
        if not gens:
            gens = [chr(i) for i in range(97, 97 + len(matrix))]
        else:
            assert len(gens) == len(matrix)
        rels = []
        for i in range(len(matrix)):
            for j in range(i, len(matrix)):
                if matrix[i][j] != CoxeterGroup.INFINITY:
                    rels.append((gens[i] + gens[j]) * matrix[i][j])
        self.reflection_representation = ReflectionRepresentation(self)
        super(CoxeterGroup, self).__init__(gens, rels)

    def __str__(self):
        copy = deepcopy(self.matrix)
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if copy[i][j] == 0:
                    copy[i][j] = -1
        return str(copy).replace('-1', 'inf')

    @staticmethod
    def is_valid(matrix):
        """
        checks whether <matrix> is square, has ones on the diagonal and no negatives or ones anywhere else.
        zeros are allowed
        :param matrix: any matrix
        """
        size = len(matrix)
        for i in range(size):
            if len(matrix[i]) != size:
                return False
            if matrix[i][i] != 1:
                return False
        for i in range(size):
            for j in range(i + 1, size):
                if matrix[i][j] != matrix[j][i]:
                    return False
                if matrix[i][j] == 1 or matrix[i][j] < 0:
                    return False
        return True

    @staticmethod
    def matrices_are_permutations(matrix1, matrix2):
        """
        checks whether renaming the rows and columns of <matrix1> can yield <matrix2>
        :param matrix1:
        :param matrix2:
        :return:
        """
        if len(matrix1) != len(matrix2):
            return False
        size = len(matrix1)
        perms = permutations(range(size))
        for perm in perms:
            tmp = deepcopy(matrix1)

            # permute rows
            for row in range(size):
                tmp[row] = deepcopy(matrix1[perm[row]])

            # permute cols
            tmp2 = deepcopy(tmp)
            for col in range(size):
                for row in range(size):
                    tmp[row][col] = tmp2[row][perm[col]]

            if matrix2 == tmp:
                return True
        return False

    @staticmethod
    def matrix_is_permutation_of_any(group, groups):
        matrix = group.matrix
        matrices = [g.matrix for g in groups]
        for other in matrices:
            if CoxeterGroup.matrices_are_permutations(matrix, other):
                return True
        return False

    def rank(self):
        return len(self.matrix)

    @staticmethod
    def join(coxeter_groups):
        matrices = [deepcopy(group.matrix) for group in coxeter_groups]
        if not matrices:
            return []
        rank = len(matrices[0])
        joined = deepcopy(matrices[0])
        for i in range(rank):
            for j in range(i + 1, rank):
                numbers = []
                for matrix in matrices:
                    numbers.append(matrix[i][j])
                    joined[i][j] = joined[j][i] = PreCoxeterPresentation.lcm(numbers)
        return CoxeterGroup(joined, gens=coxeter_groups[0].gens)
