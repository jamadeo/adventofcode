import fileinput


REQUIRED_FIELDS = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')


def split_into_records(lines):
    record = set()
    for line in lines:
        stripped = line.strip()
        if stripped == '':
            yield record
            record = set()
        else:
            record.update(entry.split(':')[0] for entry in stripped.split(' '))
    yield record


def is_valid_record(record):
    return all(key in record for key in REQUIRED_FIELDS)


print(sum(1 for rec in split_into_records(fileinput.input()) if is_valid_record(rec)))
