import argparse
import json
from datetime import datetime


def convert(file_path_from, file_path_to):
    headers = ['id', 'val', 'desc', 'date']
    transforms = [None, float, str, convert_stamp_to_date]

    file_to = open(file_path_to, 'w')
    file_to.write(";".join(headers) + "\n")

    with open(file_path_from, 'r') as file_from:
        for line in file_from.readlines():
            file_to.write(convert_line(line, transforms))

    file_to.close()


def convert_stamp_to_date(timestamp) -> str:
    try:
        date = datetime.utcfromtimestamp(int(timestamp) / 1000)
        return str(date.strftime("%Y/%m/%d"))
    except ValueError:
        return timestamp


def convert_line(line, transforms=[]) -> str:
    i = 0
    result = []
    raw = json.loads(line)

    for key, val in raw.items():
        if type(val) is dict:
            prepared = ",".join(val.values())
        else:
            prepared = val

        if len(transforms) > i and transforms[i] is not None:
            prepared = transforms[i](prepared)

        result.append(str(prepared))
        i += 1

    return ";".join(result) + "\n"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert from JSON to CSV format')
    parser.add_argument('input', help='Path of a file to parse from')
    parser.add_argument('output', help='Path of a file to save result to')
    args = parser.parse_args()

    try:
        convert(args.input, args.output)
    except FileNotFoundError as e:
        print(e)
        exit(1)
