class Word:
    """Is just a list whose elements are interpreted to be elements of <self.presentation.generators>."""
    def __init__(self, string, presentation):
        # TODO assert that string only contains letters in <presentation.generators>
        self.string = string
        self.presentation = presentation

    def __eq__(self, other):
        return self.string == other.string and self.presentation == other.presentation

    def __ne__(self, other):
        return not self.__eq__(other)

    def length(self):
        return len(self.string)

    def __str__(self):
        return self.string + " in " + self.presentation.__str__()
