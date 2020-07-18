from link import Link
from braid import Braid
from toruslink import TorusLink
from pretzellink import PretzelLink


def main():
    while True:
        error = False
        print("In what format would you like to input your link? (<b> for braid, <g> for Gauss code, " +
              "<t> for torus link, <p> for pretzel link)")
        mode = input("Your choice: ")
        print("")
        if mode == 'g':
            print("Please enter a gauss code of a link. Separate crossings by spaces and " +
                  "components by commas. E.g., for the Hopf link enter <1 -2, -1 2> " +
                  "(without the brackets).")
            link_string = input("Your Gauss code: ")
            components_strings = link_string.split(",")
            gauss_code = []
            for component in components_strings:
                gauss_code.append([int(x) for x in component.split()])
            link = Link(gauss_code)
        elif mode == 'b':
            print("Please enter a braid. E.g., for the braid whose closure is the Figure-8 knot, " +
                  "enter <1 -2 1 -2> (without the brackets).")
            braid_string = input("Your braid: ")
            braid_representation_chars = braid_string.split()
            braid_representation = []
            for char in braid_representation_chars:
                braid_representation.append(int(char))
            link = Braid(braid_representation)
        elif mode == 't':
            print("For the (p,q)-torus knot, please enter p and q separated by spaces. E.g., for " +
                  "the trefoil, enter <2 3> (without the brackets).")
            p_q_string = input("Your parameters: ")
            p_q_chars = p_q_string.split()
            p = int(p_q_chars[0])
            q = int(p_q_chars[1])
            link = TorusLink(p, q)
        elif mode == 'p':
            print("Which Pretzel knot P(x1, ..., xn) would you like to consider? Enter the " +
                  "weights x1, ..., xn separated with spaces. E.g., for the pretzel link " +
                  "P(3, 5, -7), enter <3 5 -7> (without the brackets).")
            weights_string = input("Your weights: ")
            weights_chars = weights_string.split()
            weights = []
            for char in weights_chars:
                weights.append(int(char))
            link = PretzelLink(weights)
        else:
            error = True
            print("That was an invalid input.")
            link = Link([])

        gauss_code = link.gauss_code

        if not error:
            print("")
            print("Computing all obvious visible Coxeter quotients of the link with Gauss code " +
                  gauss_code.__str__() + "\n")
            quotients = link.all_obvious_visible_coxeter_quotients_with_respect_to_all_generating_sets('interactive')
            print("")
            print("Found the following Coxeter quotients:")
            # TODO does not work yet, just prints [<coxetergroup.CoxeterGroup object at 0x0000020BBC37F668>] or similar
            string = ''
            for quotient in quotients:
                if string:
                    string = string + ', ' + quotient.__str__()
                else:
                    string = quotient.__str__()
            print(string)


if __name__ == '__main__':
    main()
