from braid import Braid


class BraidEnumerator(object):
    def __init__(self, number_of_braids, number_of_strands):
        self.number_of_braids = number_of_braids
        self.number_of_strands = number_of_strands
        self.braids = self.enumerate_braids()

    def enumerate_braids(self):
        braids = [[] * self.number_of_strands]
        crossings = 0
        while len(braids) <= self.number_of_braids:


        return braids
