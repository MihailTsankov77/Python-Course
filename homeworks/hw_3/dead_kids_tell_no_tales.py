from critical_mass import Host, Kid, FluxCapacitor


# test default case with 3 kids and 3 hosts with 3 candies each
# each kid eats 3 candies
def test_1():
    test_hosts = [
        Host((1, 1), [(3, 1), (9, 0.5), (2, 10)]),
        Host((2, 0), [(3, 1), (6, 1), (3, 3)]),
        Host((4, 1), [(3, 0.5), (2, 2), (3, 3)])
    ]

    test_kids = [
        Kid((1, 4), 1),
        Kid((2, 4), 3),
        Kid((3, 4), 2)
    ]

    flux_capacitor = FluxCapacitor(test_hosts+test_kids)

    victims = flux_capacitor.get_victim()

    # str_victims = ""
    # for kid in victims:
    #     str_victims += str(kid) + "\n"
    # print(str_victims)

    assert len(victims) == 1
    assert list(victims)[0].get_initiative() == 2


# test two kids dying
# second turn kids with initiative 2 and 3 die with 21 uranium
# all kids end up in host (2, 0)
def test_2():
    test_hosts = [
        Host((1, 1), [(11, 1), (9, 0.5), (3, 3)]),
        Host((2, 0), [(10, 1), (6, 1), (3, 3)]),
        Host((4, 1), [(30, 0.5), (2, 2), (3, 3)])
    ]

    test_kids = [
        Kid((1, 4), 1),
        Kid((2, 4), 3),
        Kid((3, 4), 2)
    ]

    flux_capacitor = FluxCapacitor(test_hosts+test_kids)

    victims = flux_capacitor.get_victim()

    # str_victims = ""
    # for kid in victims:
    #     str_victims += str(kid) + "\n"
    # print(str_victims)

    assert len(victims) == 2
    for dead_kid in list(victims):
        assert dead_kid.get_initiative() in [2, 3]


# test No one dies
def test_3():
    test_hosts = [
        Host((1, 1), [(3, 1), (9, 0.5), (3, 3)]),
        Host((2, 0), [(3, 1), (6, 1), (3, 3)]),
        Host((4, 1), [(3, 0.5), (2, 2), (3, 3)])
    ]

    test_kids = [
        Kid((1, 4), 1),
        Kid((2, 4), 3),
        Kid((3, 4), 2)
    ]

    flux_capacitor = FluxCapacitor(test_hosts+test_kids)

    victims = flux_capacitor.get_victim()

    # str_victims = ""
    # for kid in victims:
    #     str_victims += str(kid) + "\n"
    # print(str_victims)

    assert victims is None


# test sort when two host are equidistant should be the one with lower x
def test_4():
    test_hosts = [
        Host((3, 0), [(3, 1), (6, 1)]),
        Host((1, 0), [(30, 1), (9, 1)]),
    ]

    test_kids = [
        Kid((2, 0), 2),
        Kid((1, 1), 1),
    ]

    flux_capacitor = FluxCapacitor(test_hosts+test_kids)

    victims = flux_capacitor.get_victim()

    # str_victims = ""
    # for kid in victims:
    #     str_victims += str(kid) + "\n"
    # print(str_victims)

    assert len(victims) == 1
    assert list(victims)[0].get_initiative() == 2


test_1()
test_2()
test_3()
test_4()
