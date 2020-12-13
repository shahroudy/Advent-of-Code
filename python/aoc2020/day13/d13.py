class ShuttleSearch:
    def __init__(self, filename):
        self.read_file(filename)

    def read_file(self, filename):
        with open(filename, 'r') as file:
            self.current_time = int(file.readline().strip())
            bus_str = file.readline().strip().split(',')
            self.buses = [int(b if b != 'x' else 0) for b in bus_str]

    def find_earliest(self):
        min_wait = -1
        result = 0
        for bus in [b for b in self.buses if b > 0]:
            wait_time = self.current_time % bus
            if wait_time > 0:
                wait_time = bus - wait_time
            if wait_time < min_wait or min_wait < 0:
                min_wait = wait_time
                result = wait_time * bus
        return result

    def find_magic_time(self):
        den_rem_pairs = []
        for wait_time in range(len(self.buses)):
            busid = self.buses[wait_time]
            if busid > 0:
                actual_wait = wait_time
                if actual_wait>0:
                    actual_wait = (busid - actual_wait) % busid
                den_rem_pairs.append((busid, actual_wait))

        # sort in ascending order of denominators
        pairs_sorted = sorted(den_rem_pairs, key=lambda x:x[0])

        multiples = 1
        result = 0
        for p in pairs_sorted:
            den, rem = p
            while (result % den) != rem:
                result += multiples
            multiples *= den
        return result


if __name__ == '__main__':
    test1 = ShuttleSearch('test1.txt')
    assert test1.find_earliest() == 295
    test2 = ShuttleSearch('test2.txt')
    assert test2.find_magic_time() == 3417

    shuttle = ShuttleSearch('input.txt')
    print(shuttle.find_earliest())
    print(shuttle.find_magic_time())
