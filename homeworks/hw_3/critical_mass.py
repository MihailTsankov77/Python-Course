from math import dist


class Candy:

    def __init__(self, mass, uranium):
        self.mass = mass
        self.uranium = uranium

    def get_uranium_quantity(self):
        return self.mass * self.uranium

    def get_mass(self):
        return self.mass

    def __str__(self) -> str:
        return f"({self.mass}, {self.uranium})"


class Person:

    def __init__(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def __hash__(self) -> int:
        return self.position.__hash__()


class Kid(Person):

    I_am_glowing_in_the_dark_magic_number = 20

    def __init__(self, position, initiative):
        Person.__init__(self, position)
        self.initiative = initiative
        self.candies = []
        self.visited_hosts = set()

    def get_initiative(self):
        return self.initiative

    def add_candy(self, candy):
        if candy is not None:
            self.candies.append(candy)

    def is_critical(self):
        return sum([candy.get_uranium_quantity() for candy in self.candies]) > self.I_am_glowing_in_the_dark_magic_number

    def get_closest_host(self, hosts):
        available_hosts = [
            host for host in hosts if host not in self.visited_hosts]

        if not available_hosts:
            return None

        closest_host = min(available_hosts, key=lambda host:
                           (dist(host.get_position(), self.get_position()),
                            *host.get_position())
                           )

        self.visited_hosts.add(closest_host)
        self.set_position(closest_host.get_position())
        return closest_host

    def __str__(self) -> str:
        candy_str = ""
        for candy in self.candies:
            candy_str += str(candy) + " "

        hosts_str = ""
        for host in self.visited_hosts:
            hosts_str += str(host.get_position()) + " "

        return f"Kid at {self.position} with initiative {self.initiative} and candies {candy_str}visited hosts {hosts_str}"


class Host(Person):

    def __init__(self, position, candies):
        Person.__init__(self, position)
        self.candies = [Candy(*candy) for candy in candies]

    def remove_candy(self, func):
        if len(self.candies) == 0:
            return None

        candy = func(self.candies)
        self.candies.remove(candy)
        return candy

    def give_away_happiness(self, kids, func):
        for kid in sorted(kids, key=lambda kid: kid.get_initiative(), reverse=True):
            kid.add_candy(self.remove_candy(func))


class FluxCapacitor:

    def __init__(self, participants):
        self.kids = [participant for participant in participants if isinstance(
            participant, Kid)]
        self.hosts = [participant for participant in participants if isinstance(
            participant, Host)]

    def get_victim(self):

        # RIP dead_kids_tell_no_tales() 05.11.2023 - 07.11.2023 :pepesad:
        while True:
            kids_to_hosts = {
                host: [] for host in self.hosts
            }

            for kid in self.kids:
                host = kid.get_closest_host(self.hosts)
                if host is not None:
                    kids_to_hosts[host].append(kid)

            self.are_there_candies = False

            def compare(candies):
                self.are_there_candies = True
                return max(candies, key=lambda candy: candy.get_mass())

            for host in self.hosts:
                host.give_away_happiness(kids_to_hosts[host], compare)

            if not self.are_there_candies:
                return None

            dead_kids = {kid for kid in self.kids if kid.is_critical()}

            if dead_kids:
                return dead_kids
