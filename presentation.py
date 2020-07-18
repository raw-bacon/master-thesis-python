from itertools import permutations


class Presentation(object):
    def __init__(self, gens, rels):
        """
        does not add the empty relations
        :param gens:
        :param rels:
        """
        # TODO assert that gens are in fact lower-case literal characters
        self.gens = gens
        self.gens.sort()
        self.rels = []
        for rel in rels:
            if rel:
                self.rels.append(rel)
        self.rels = list(set(self.rels))

    def __eq__(self, other):
        return self.gens == other.gens and self.rels == other.rels

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return tuple([tuple(self.gens), tuple(self.rels)]).__hash__()

    def is_permutation_of(self, other):
        if self.gens != other.gens:
            return False
        perms = permutations(self.gens)
        for perm in perms:
            tmp_rels = []
            for rel in self.rels:
                tmp_rels.append("")
                for i in range(len(rel)):
                    for j in range(len(perm)):
                        if rel[i] == self.gens[j]:
                            tmp_rels[len(tmp_rels) - 1] = tmp_rels[len(tmp_rels) - 1] + perm[j]
            tmp_rels.sort()
            other.rels.sort()
            if tmp_rels == other.rels:
                return True
        return False

    @staticmethod
    def remove_permutations_from_list(presentations):
        new_list = []
        for presentation in presentations:
            contains = False
            for considered in new_list:
                if considered.is_permutation_of(presentation):
                    contains = True
            if not contains:
                new_list.append(presentation)
        return new_list

    # TODO implement inverses. Represent them as the corresponding upper-case character for the generators.
    def rewrite(self, word):
        """
        rewrites the word by removing sequences of the form aA or Aa
        :type word: Word
        """
        # TODO after implementing inverses, implement this method
        assert word.presentation == self
        return word

    def max_relator_length(self):
        return max([len(rel) for rel in self.rels])

    def __str__(self):
        string = "<"
        for gen in self.gens:
            string = string + gen + ", "
        string = string[:len(string) - 2]
        string = string + " | "
        for rel in self.rels:
            string = string + rel + ", "
        string = string[:len(string) - 2]
        string = string + ">"
        return string
