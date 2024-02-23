import re


def parse_wishlist(data):
    christmas_magic = re.compile(r'\(\s*(-?[\.\d]*)\s*\)\s*(.*?(?=\s+\[)).*\[\s*(\d+)|[-\*].*?(?=[^\s])(.*?(?=\s*(?:\n|$)))')
    parsed_data = christmas_magic.findall(data)

    wishlist = []
    for row in parsed_data:
        if row[3] == '':
            wishlist.append([float(row[0]), row[1], int(row[2]), []])
        else:
            wishlist[-1][-1].append(row[3])

    return list((item[0], item[1], item[2], tuple(item[3])) for item in wishlist)
