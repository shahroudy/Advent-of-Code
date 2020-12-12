import re
from myutils.file_reader import read_str_list


def read_passport_lines(filename: str):
    lines = read_str_list(filename)
    lines.append('')  # to ensure the last valid line will also read
    data = []
    buffer = ""
    for full_line in lines:
        line = full_line.strip()
        if len(line) == 0:
            data.append(buffer.strip())
            buffer = ""
        else:
            buffer += " " + line.strip()
    return data


def read_dictionaries(filename: str):
    data = read_passport_lines(filename)
    records = []
    for line in data:
        pairs = line.split(' ')
        record = dict()
        for pair in pairs:
            key_value = pair.split(":")
            key = key_value[0].lower().strip()
            value = key_value[1].strip()
            record[key] = value
        records.append(record)
    return records


def validate_keys(passport: dict):
    return {'byr',
            'iyr',
            'eyr',
            'hgt',
            'hcl',
            'ecl',
            'pid'
            # 'cid' optional
            } <= set(passport.keys())


def validate_values(passport: dict):
    try:
        if not(1920 <= int(passport['byr']) <= 2002):
            return False
        if not(2010 <= int(passport['iyr']) <= 2020):
            return False
        if not(2020 <= int(passport['eyr']) <= 2030):
            return False
        v = passport['hgt']
        val = int(v[:-2])
        if not(
                v[-2:] == 'cm' and 150 <= val <= 193
                or
                v[-2:] == 'in' and 59 <= val <= 76):
            return False
        v = passport['hcl']
        if not(
                v[0] == '#'
                and
                re.match('^[0-9,a-f]{6}$', v[1:])):
            return False
        if not (passport['ecl'] in ['amb', 'blu', 'brn', 'gry',
                                    'grn', 'hzl', 'oth']):
            return False
        v = passport['pid']
        int(v)
        if len(v) != 9:
            return False
        # passport['cid'] is optional
    except ValueError:
        return False
    except KeyError:
        return False
    return True


if __name__ == "__main__":
    all_passports = read_dictionaries('input.txt')

    valid_keys_count = valid_values_count = 0
    for passport in all_passports:
        if validate_keys(passport):
            valid_keys_count += 1
        if validate_values(passport):
            valid_values_count += 1

    print(valid_keys_count, valid_values_count)
