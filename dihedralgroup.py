from coxetergroup import CoxeterGroup


class DihedralGroup(CoxeterGroup):
    def __init__(self, n):
        super(DihedralGroup, self).__init__([[1, n], [n, 1]])
