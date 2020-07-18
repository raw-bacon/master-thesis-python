from link import Link


class Braid(Link):
    def __init__(self, braid_notation):
        gauss_code = Braid.gauss_code_from_braid_notation(braid_notation)
        self.braid_word = braid_notation
        super(Braid, self).__init__(gauss_code)

    @staticmethod
    def gauss_code_from_braid_notation(braid_notation):
        gauss_code = []
        number_of_strands = max([abs(x) + 1 for x in braid_notation])
        unvisited = list(range(number_of_strands))
        current_strand = 0
        component = []
        while unvisited:
            if current_strand not in unvisited:
                current_strand = unvisited[0]
                gauss_code.append(component)
                component = []
            unvisited.remove(current_strand)
            for i in range(len(braid_notation)):
                if abs(braid_notation[i]) == current_strand + 1:
                    current_strand = current_strand + 1
                    if braid_notation[i] < 0:
                        component.append(-i - 1)
                    else:
                        component.append(i+1)
                elif abs(braid_notation[i]) == current_strand:
                    current_strand = current_strand - 1
                    if braid_notation[i] < 0:
                        component.append(i + 1)
                    else:
                        component.append(-i - 1)
        gauss_code.append(component)
        return gauss_code
