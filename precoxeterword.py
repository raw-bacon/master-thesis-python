from word import Word


class PreCoxeterWord(Word):
    """
    is an element of a PreCoxeterPresentation
    """
    def remove_squares(self):
        """Removes all occurrences of squares"""
        if self.length() <= 1:
            return self
        string = self.string[:]
        i = 1
        while i < len(string):
            if i > 0:
                previous = string[i - 1]
                current = string[i]
                if previous == current:
                    string = string[:i - 1] + string[i + 1:]
                    i = i - 2
            i = i + 1
        return PreCoxeterWord(string, self.presentation)

    def contains_square(self):
        for i in range(1, self.length()):
            previous = self.string[i - 1]
            current = self.string[i]
            if previous == current:
                return True
        return False
