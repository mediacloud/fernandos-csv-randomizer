import chardet
import csv
import random


def _predict_encoding(file_path: str, n_lines: int = 20) -> str:
    """Predict a file's encoding using chardet."""

    # Open the file as binary data
    with open(file_path, 'rb') as f:
        # Join binary lines for specified number of lines
        raw_data = b''.join([f.readline() for _ in range(n_lines)])

    return chardet.detect(raw_data)['encoding']


def csv_random_rows(input_csv_path: str, output_csv_path: str, row_count: int = 100):
    if not input_csv_path:
        raise Exception("Input CSV path is not set.")

    if not output_csv_path:
        raise Exception("Output CSV path is not set.")

    if not row_count:
        raise Exception("Row count is not set.")

    if input_csv_path == output_csv_path:
        raise Exception("Can't read from and write to the same file.")

    input_encoding = _predict_encoding(file_path=input_csv_path)
    if input_encoding.lower() == 'ascii':
        input_encoding = 'utf-8'

    with open(input_csv_path, mode='r', encoding=input_encoding) as input_file:

        csv_sample = input_file.read(4096)
        input_file.seek(0)

        sniffer = csv.Sniffer()

        try:
            dialect = sniffer.sniff(csv_sample)
        except Exception as ex:
            raise Exception("Unable to determine CSV dialect: {}".format(str(ex)))

        if not dialect.escapechar:
            dialect.escapechar = '\\'

        try:
            has_header = sniffer.has_header(csv_sample)
        except Exception as ex:
            raise Exception("Unable to determine whether CSV file has header: {}".format(str(ex)))

        csv_input = csv.reader(input_file, dialect=dialect)

        if has_header:
            csv_header = next(csv_input)
        else:
            csv_header = None

        csv_rows = []
        for row in csv_input:
            csv_rows.append(row)

        if len(csv_rows) < row_count:
            raise Exception("File '{}' does not have {} rows.".format(input_csv_path, row_count))

        random.shuffle(csv_rows)
        sample_rows = csv_rows[:row_count]

        with open(output_csv_path, mode='w', encoding='utf-8') as output_file:
            csv_output = csv.writer(output_file, dialect=dialect)
            if csv_header:
                csv_output.writerow(csv_header)
            for row in sample_rows:
                csv_output.writerow(row)
