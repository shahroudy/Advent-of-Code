from myutils.file_reader import read_str_list


class Orbits:
    def __init__(self, filename):
        self.read_orbit_info(filename)

    def read_orbit_info(self, filename):
        self.orbits = dict()
        lines = read_str_list(filename)
        for line in lines:
            names = line.split(')')
            self.orbits[names[1]] = names[0]

    def get_path_to_com(self, start):
        path = []
        head = start
        while head in self.orbits.keys():
            head = self.orbits[head]
            path.append(head)
        return path

    def get_sum_all_orbits(self):
        count = 0
        for start in self.orbits.keys():
            count += len(self.get_path_to_com(start))
        return count

    def calc_transitions(self, source, destination):
        source_path = self.get_path_to_com(source)
        dest_path = self.get_path_to_com(destination)
        return len(set(source_path) ^ set(dest_path))


if __name__ == '__main__':
    test_orbits = Orbits('test1.txt')
    assert test_orbits.get_sum_all_orbits() == 42
    test_orbits = Orbits('test2.txt')
    assert test_orbits.calc_transitions('YOU', 'SAN') == 4

    orbits = Orbits('input.txt')
    print(orbits.get_sum_all_orbits(),
          orbits.calc_transitions('YOU', 'SAN'))
