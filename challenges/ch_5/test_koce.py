from Ho_Ho_Ho import parse_wishlist

import unittest

class WishlistTest(unittest.TestCase):
    def test_one_wish(self):
        wishlist = """
        (   80  )    John Doe  [ 22 години ]  


        - по-хубаво име 😅
         -
         *
    - !!!lukanka
        """
        self.assertEqual(parse_wishlist(wishlist), [(80, 'John Doe', 22, ('по-хубаво име 😅', '!!!lukanka'))])

    def test_two_wishes(self):
        wishlist = """
        (3.1415926536)  Pitagor "Хипотенузов" :(  [ 2592 години малее]
            - триъгълник, за да си мери ... хипотенузата
            *   въже :)

        * чук и наковалня
                - 
                - 
                *
            (112)  Мечо Пух/ [8]

                    - burkanche med (x11)
            *  :лъжица:
        """

        self.assertEqual(parse_wishlist(wishlist), [
            (3.1415926536, 'Pitagor "Хипотенузов" :(', 2592,
             ('триъгълник, за да си мери ... хипотенузата', 'въже :)', 'чук и наковалня')),
            (112, 'Мечо Пух/', 8, ('burkanche med (x11)', ':лъжица:'))
        ])

    def test_dqdo_koleda(self):
        wishlist = """
        (-1)   Santa Claus  [18+]

                * snejanka

            -  snejanka
                -SNEJANKA

        (156.19) Snejanka [20 g.]

            -da e dalech ot dqdo koleda 💀              
                * 
                 *
                - pileshko s orizzz

        """
        self.assertEqual(parse_wishlist(wishlist), [
            (-1, 'Santa Claus', 18, ('snejanka', 'snejanka', 'SNEJANKA')),
            (156.19, 'Snejanka', 20, ('da e dalech ot dqdo koleda 💀', 'pileshko s orizzz'))
        ])