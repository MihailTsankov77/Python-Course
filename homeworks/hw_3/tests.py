from critical_mass import *
import unittest


class FluxCapacitorTest(unittest.TestCase):
    def test_one_host_no_victims(self):
        participants = {
            Kid((1, 2), 10),
            Kid((-1, 3), 8),
            Kid((11, -3), 6),
            Kid((4, 4), 1),
            Host((10, 6), [(10, 0.6), (1, 1), (4, 0.4), (7, 0.2)])
        }
        flux_capacitor = FluxCapacitor(participants)

        victims = flux_capacitor.get_victim()

        self.assertIsNone(victims)

    def test_one_host_all_victims(self):
        kids = {
            Kid((1, 2), 10),
            Kid((-1, 3), 8),
            Kid((11, -3), 6),
            Kid((4, 4), 1),
        }
        hosts = {
            Host((10, 6), [(42, 0.5), (22, 1), (102, 0.2), (211, 0.1)])
        }
        flux_capacitor = FluxCapacitor(kids | hosts)

        victims = flux_capacitor.get_victim()

        self.assertEqual(victims, kids)

    def test_one_host_many_candies_no_victims(self):
        hosts = {
            Host((1, 1), [(1, 0.1), (2, 0.8), (10, 0.5),
                 (11, 0.2), (23, 0.1), (17, 0.5)])
        }
        kids = {
            Kid((1, 2), 1),
            Kid((3, 4), 2),
            Kid((-1, -2), 3),
            Kid((11, 23), 4),
            Kid((4, 55), 5),
        }

        victims = FluxCapacitor(kids | hosts).get_victim()

        self.assertIsNone(victims)

    def test_one_host_many_candy_one_victim(self):
        hosts = {
            Host((1, 1), [(1, 0.1), (2, 0.8), (10, 0.5),
                 (11, 0.2), (23, 1), (25, 0.5)])
        }
        kids = {
            (kid := Kid((1, 2), 9)),
            Kid((6, 5), 10),
            Kid((2, 1), 1)
        }

        victims = FluxCapacitor(kids | hosts).get_victim()

        self.assertSetEqual(victims, {kid})

    def test_one_host_few_candy_one_victim(self):
        hosts = {
            Host((1, 1), [(23, 1)])
        }
        kids = {
            (kid := Kid((1, 2), 11)),
            Kid((6, 5), 10),
            Kid((2, 1), 1)
        }

        victims = FluxCapacitor(kids | hosts).get_victim()

        self.assertSetEqual(victims, {kid})

    def test_many_hosts_no_victims(self):
        hosts = {
            Host((1, 1), [(1, 1)]),
            Host((2, 2), [(3, 0.1), (2, 0.8), (10, 0.5), (11, 0.2)]),
            Host((1, 4), [(11, 0.7), (50, 0.1), (72, 0.15)]),
            Host((5, 5), [(90, 0.01), (80, 0.01),
                 (23, 0.2), (17, 0.3), (9, 0.4)]),
        }
        kids = {
            Kid((1, 1), 1),
            Kid((4, 5), 2)
        }

        victims = FluxCapacitor(kids | hosts).get_victim()

        self.assertIsNone(victims)

    def test_many_hosts_one_victim(self):
        hosts = {
            Host((1, 1), [(1, 1)]),
            Host((2, 2), [(3, 0.1), (2, 0.8), (10, 0.5), (11, 0.2)]),
            Host((1, 4), [(11, 0.7), (50, 0.1), (72, 0.15)]),
            Host((5, 5), [(90, 0.1), (80, 0.01),
                 (23, 0.2), (17, 0.3), (9, 0.4)]),
        }
        kids = {
            Kid((1, 1), 1),
            (kid := Kid((4, 5), 2))
        }

        victims = FluxCapacitor(kids | hosts).get_victim()
        self.assertSetEqual(victims, {kid})

    def test_many_hosts_many_kids_no_victims(self):
        hosts = {
            Host((1, 1), [(1, 1)]),
            Host((2, 2), [(3, 0.1), (2, 0.8), (10, 0.5), (11, 0.2)]),
            Host((1, 4), [(11, 0.7), (50, 0.1), (72, 0.15)]),
            Host((5, 5), [(90, 0.1), (80, 0.01),
                 (23, 0.2), (17, 0.3), (9, 0.4)]),
        }
        kids = {
            Kid((1, 2), 10), Kid((-1, 3), 8),
            Kid((11, -3), 6), Kid((4, 4), 11),
            Kid((-1, -3), 12), Kid((9, 1), 3),
            Kid((8, 7), 7), Kid((-10, 14), 4),
            Kid((1, 4), 1), Kid((2, 4), 13),
            Kid((3, 4), 21), Kid((2, 5), 30)
        }
        victims = FluxCapacitor(kids | hosts).get_victim()
        self.assertIsNone(victims)

    def test_many_hosts_many_kids_many_victims(self):
        hosts = {
            Host((1, 1), [(1, 1), (100, 0.4), (28, 0.7), (17, 0.5)]),
            Host((2, 2), [(3, 0.1), (2, 0.8), (10, 0.5),
                 (11, 0.2), (40, 0.3), (69, 0.69)]),
            Host((1, 4), [(11, 0.7), (50, 0.1),
                 (72, 0.15), (81, 0.4), (75, 0.46)]),
            Host((5, 5), [(90, 0.1), (80, 0.1), (23, 0.2),
                 (17, 0.3), (9, 0.4), (96, 0.42)]),
        }
        kids = {
            Kid((1, 2), 10), Kid((-1, 3), 8),
            Kid((11, -3), 6), (k11 := Kid((4, 4), 11)),
            (k12 := Kid((-1, -3), 12)), Kid((9, 1), 3),
            Kid((8, 7), 7), Kid((-10, 14), 4),
            Kid((1, 4), 1), Kid((2, 4), 13),
            (k21 := Kid((3, 4), 21)), (k30 := Kid((2, 5), 30))
        }
        victims = FluxCapacitor(kids | hosts).get_victim()
        self.assertSetEqual(victims, {k11, k12, k21, k30})

    def test_host_without_candies(self):
        participants = {
            Kid((-2, 4), 1),
            Host((2, 4), []),
        }
        flux_capacitor = FluxCapacitor(participants)

        victims = flux_capacitor.get_victim()

        self.assertIsNone(victims)
