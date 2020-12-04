import fileinput
import re


def int_in_range(min_, max_):
    def f(s):
        try:
            return min_ <= int(s) <= max_
        except ValueError:
            return False
    return f


def regex_match(regex):
    expr = re.compile(regex)

    def f(s):
        return bool(expr.match(s))

    return f


def validate_height(s):
    value, suffix = s[:-2], s[-2:]
    if suffix == 'cm':
        range_ = (150, 193)
    elif suffix == 'in':
        range_ = (59, 76)
    else:
        return False
    return int_in_range(*range_)(value)


VALIDATIONS = {
    'byr': int_in_range(1920, 2002),
    'iyr': int_in_range(2010, 2020),
    'eyr': int_in_range(2020, 2030),
    'hgt': validate_height,
    'hcl': regex_match(r'#[0-9a-f]{6}$'),
    'ecl': regex_match(r'(amb|blu|brn|gry|grn|hzl|oth)$'),
    'pid': regex_match(r'[0-9]{9}$'),
}


def split_into_records(lines):
    record = {}
    for line in lines:
        stripped = line.strip()
        if stripped == '':
            yield record
            record = {}
        else:
            record.update(entry.split(':') for entry in stripped.split(' '))
    yield record


def validate_field(key, val):
    valid = VALIDATIONS[key](val)
    return valid


def is_valid_record(record):
    fields = {*record.keys()}
    fields.discard('cid')
    if len(fields) != len(VALIDATIONS):
        return False
    for key in fields:
        if key not in VALIDATIONS:
            return False
        if not validate_field(key, record[key]):
            return False
    return True


print(sum(1 for rec in split_into_records(fileinput.input()) if is_valid_record(rec)))
