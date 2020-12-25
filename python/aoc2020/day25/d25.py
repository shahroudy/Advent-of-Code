from myutils.file_reader import read_int_list


class RFID:
    def __init__(self, subject_no):
        self.subject_no = subject_no
        self.reset()

    def reset(self):
        self.value = 1

    def transform_once(self):
        self.value = self.value * self.subject_no % 20201227

    def calc_loop_size(self, public_key):
        self.reset()
        loop = 0
        while self.value != public_key:
            loop += 1
            self.transform_once()
        self.subject_no = public_key
        return loop

    def encrypt(self, loop_size):
        self.reset()
        for _ in range(loop_size):
            self.transform_once()
        return self.value


class ComboBreaker:
    def __init__(self, filename):
        input = read_int_list(filename)
        self.card_public_key, self.door_public_key = input[0], input[1]

    def calc_handshake_encryption_key(self):
        card, door = RFID(7), RFID(7)
        card_loop_size = card.calc_loop_size(self.card_public_key)
        door_loop_size = door.calc_loop_size(self.door_public_key)
        return card.encrypt(door_loop_size)


if __name__ == '__main__':
    test1 = ComboBreaker('test1.txt')
    assert test1.calc_handshake_encryption_key() == 14897079

    handshake = ComboBreaker('input.txt')
    print(handshake.calc_handshake_encryption_key())
