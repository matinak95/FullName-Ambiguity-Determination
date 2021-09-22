import sys
import csv
import os


def CSVReader(filename):
    rows = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        for row in csvreader:
            rows.append(str(row)[2:-2])

        line_num = csvreader.line_num

        return rows


class FullNamePredictor:
    def __init__(self):
        self.names = {}
        self.surnames = {}

    def dicts(self):
        file = open("dist.male.first.txt")
        for line in file:
            words = line.split()
            self.names[words[0]] = float(words[1]) / 100
        file = open("dist.female.first.txt")
        for line in file:
            words = line.split()
            try:
                self.names[words[0]] += float(words[1]) / 100
            except KeyError:
                self.names[words[0]] = float(words[1]) / 100
        file = open("Surname.txt")
        for line in file:
            words = line.split()
            self.surnames[words[0]] = float(words[1]) / 100000

    def predictor(self, file):
        rows = CSVReader(file)
        key = {}
        filename = "full-name-output.csv"
        row_counter = 0

        with open(filename, 'w') as output_file:
            wr = csv.writer(output_file)

            for row in rows:
                result = str(row) + ','
                row = row.split(' AND ')
                part1 = row[0].split()
                part2 = row[1].split()

                if len(part1) > 3:
                    for item in part1:
                        result += str(item)
                        result += " "
                    result = result[:-1]

                elif len(part1) > 1:
                    for item in part1:
                        result += str(item)
                        result += " "
                    try:
                        p_n = self.names[part1[-1]]
                        try:
                            p_n = self.names[part2[-2]]
                            result += str(part2[-1])
                        except KeyError:
                            result = result + str(part2[-2]) + " " + str(part2[-1])

                    except KeyError:
                        result = result[:-1]

                elif len(part1) == 1:
                    for item in part1:
                        result += str(item)
                        result += " "
                    if len(part2) > 2:
                        try:
                            p_n = self.names[part2[-2]]
                            result += str(part2[-1])
                        except KeyError:
                            result = result + str(part2[-2]) + " " + str(part2[-1])

                        except KeyError:
                            result += str(part2[-1])
                    else:
                        result += str(part2[-1])

                result = result.split(',')
                wr.writerow(result)


if __name__ == "__main__":
    fn = sys.argv[1]
    if not os.path.exists(fn):
        print("No file existed")
        sys.exit()
    fnp = FullNamePredictor()
    fnp.dicts()
    fnp.predictor(fn)
