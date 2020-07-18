from link import Link


def main():
    gauss_code = [[1, 2, 3, 4, 5, 6, -12, -17, -4, -9, -14, -1, 7, 8, 9, 10, 11, 12, -18, -5, -10, -15, -2, -7, 13,
                   14, 15, 16, 17, 18, -6, -11, -16, -3, -8, -13]]
    link = Link(gauss_code)
    generating_sets = link.all_obvious_visible_generating_sets()
    for generating_set in generating_sets:
        reflection_quotient = link.get_reflection_quotient_with_respect_to_generating_set(generating_set)
        rels = reflection_quotient.rels
        print(rels)


if __name__ == '__main__':
    main()
