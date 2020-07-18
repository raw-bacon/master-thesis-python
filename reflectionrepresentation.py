import numpy


class ReflectionRepresentation(object):
    def __init__(self, coxeter_group):
        self.coxeter_group = coxeter_group
        self.dimension = self.coxeter_group.rank()
        bilinear_form = numpy.zeros((self.dimension, self.dimension))
        for i in range(self.dimension):
            for j in range(self.dimension):
                entry = self.coxeter_group.matrix[i][j]
                if entry == 0:
                    bilinear_form[i, j] = -1
                else:
                    bilinear_form[i, j] = - numpy.cos(numpy.pi / self.coxeter_group.matrix[i][j])
        self.bilinear_form = numpy.array(bilinear_form)

    def linear_map_corresponding_to_generator(self, gen):
        assert gen in self.coxeter_group.gens
        # s_gen (gen_i) = gen_i - 2 * B(gen, gen_i) * gen_i
        # basis = gen[1], gen[2], ... , gen[n]
        matrix = numpy.zeros((self.dimension, self.dimension))
        index_of_gen = self.coxeter_group.gens.index(gen)
        unit_gen = numpy.zeros(self.dimension)
        unit_gen[index_of_gen] = 1
        for i in range(self.dimension):
            unit_i = numpy.zeros(self.dimension)
            unit_i[i] = 1
            matrix[:, i] = unit_i - 2 * self.bilinear_form[i, index_of_gen] * unit_gen
        return matrix

    def is_identity(self, coxeter_word):
        lst = [self.linear_map_corresponding_to_generator(gen) for gen in coxeter_word.string]

        # TODO compute tolerance
        return numpy.isclose(self.product(lst), numpy.identity(self.dimension), rtol=1.e-10).all()

    def product(self, lst):
        if not lst:
            return numpy.identity(self.dimension)
        prod = lst[0]
        for elem in lst[1:]:
            prod = prod.dot(elem)
        return prod
