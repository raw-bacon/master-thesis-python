from precoxeterword import PreCoxeterWord


class CoxeterWord(PreCoxeterWord):
    """
    should be chosen if self.presentation is actually an instance of CoxeterGroup
    """
    def remove_squares(self):
        """Removes all occurrences of squares"""
        if self.length() <= 1:
            return self

        for i in range(1, self.length()):
            previous = self.string[i - 1]
            current = self.string[i]
            if previous == current:
                return CoxeterWord(self.string[:i - 1] + self.string[i + 1:], self.presentation).remove_squares()
        return self

    def all_applications_of_rule(self, i, j):
        n = self.presentation.matrix[i][j]
        rewrites = set()
        a = self.presentation.gens[i]
        b = self.presentation.gens[j]
        if n % 2 == 0:
            word1 = (a + b) * int(n / 2)
            word2 = (b + a) * int(n / 2)
        else:
            word1 = ((a + b) * int((n - 1) / 2)) + a
            word2 = ((b + a) * int((n - 1) / 2)) + b

        for i in range(self.length() - n):
            if self.string[i:i+n] == word1:
                rewrites.add(CoxeterWord(self.string[:i] + word2 + self.string[i + n:], self.presentation))
            if self.string[i:i+n] == word2:
                rewrites.add(CoxeterWord(self.string[:i] + word1 + self.string[i + n:], self.presentation))

        return rewrites

    def __str__(self):
        return self.string + " in " + str(self.presentation)

    def __hash__(self):
        return self.string.__hash__()

    def is_identity(self):
        rep = self.presentation.reflection_representation
        return rep.is_identity(self)

    def is_identity_tits(self):
        """
        solves the word problem for Coxeter groups algebraically, but most likely not efficient. asymptotically
        behaves superfactorially or something
        :return: whether <word> equals the identity (bool)
        """
        string = self.string[:]
        found_simplification = True
        while found_simplification:
            found_simplification = False
            if not string:
                return True

            word = CoxeterWord(string, self.presentation)
            if word.contains_square():
                found_simplification = True
                string = word.remove_squares().string
                continue

            equals = {CoxeterWord(string, self.presentation)}
            new_equals = set()
            number_of_found_equals = 0
            while number_of_found_equals < len(equals):
                number_of_found_equals = len(equals)
                for equal in equals:
                    for i in range(len(self.presentation.gens)):
                        for j in range(i + 1, len(self.presentation.gens)):
                            current_equals = equal.all_applications_of_rule(i, j)
                            for equal2 in current_equals:
                                if equal2.contains_square():
                                    string = equal2.remove_squares().string
                                    found_simplification = True
                                    break
                            if found_simplification:
                                break
                            new_equals = new_equals.union(current_equals)
                        if found_simplification:
                            break
                    if found_simplification:
                        break
                if found_simplification:
                    break

                equals = equals.union(new_equals)
                new_equals = set()

        return False
