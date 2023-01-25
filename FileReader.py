import csv
import datetime
from Package import Package
from Constraint import Constraint
from HashTable import HashTable


def parse_constraint(string):
    package_constraint = Constraint(None, None, [])
    if 'Can only be on truck ' in string:
        package_constraint.required_truck_id = string[len(string) - 1]
    elif 'until' in string:
        hours = string[-5:-3]
        minutes = string[-2:]
        hold_time = datetime.time(int(hours), int(minutes))
        package_constraint.hold_time = hold_time
    elif 'delivered with' in string:
        package_id = ''
        partner_packages = []
        for char in string:
            if char.isdigit():
                package_id += char
            elif char == ',' and package_id != '':
                partner_packages.append(int(package_id))
                package_id = ''
        if package_id != '':
            partner_packages.append(int(package_id))
        package_constraint.partner_packages = partner_packages
    return package_constraint


class FileReader:
    def __init__(self, num_addresses, num_packages, distance_table_file_path, package_file_path):
        self.num_addresses = num_addresses
        self.num_packages = num_packages
        self.distance_table_file_path = distance_table_file_path
        self.package_file_path = package_file_path
        self.package_table = HashTable(5 * num_packages)
        self.address_legend = {}
        self.distance_matrix = []
        self.load_distance_table()
        self.load_package_file()

    def load_distance_table(self):
        with open(self.distance_table_file_path) as distance_table:
            read_csv = csv.reader(distance_table, delimiter=',')
            iterator = 0
            for row in read_csv:
                if self.num_addresses > iterator:
                    self.address_legend[row[0]] = iterator
                    self.address_legend[iterator] = row[0]
                else:
                    self.distance_matrix.append(row)
                iterator += 1

    def get_distance(self, address_1_id, address_2_id):
        return self.distance_matrix[address_1_id][address_2_id]

    def load_package_file(self):
        with open(self.package_file_path) as package_file:
            read_csv = csv.reader(package_file, delimiter=',')
            for row in read_csv:
                if row[5] != 'EOD':
                    hours = row[5][0:2]
                    minutes = row[5][3:5]
                    deadline = datetime.time(int(hours), int(minutes))
                else:
                    deadline = row[5]
                if row[7] != '':
                    new_package = Package(row[0], self.address_legend[row[1]], deadline, row[6], parse_constraint(row[7]))
                else:
                    new_package = Package(row[0], self.address_legend[row[1]], deadline, row[6], Constraint(None, None, []))
                self.package_table.insert(new_package)
            for i in range(1, self.num_packages):
                if self.package_table.search(i).constraints.partner_packages:
                    for package_id in self.package_table.search(i).constraints.partner_packages:
                        if i not in self.package_table.search(package_id).constraints.partner_packages:
                            self.package_table.search(package_id).constraints.partner_packages.append(i)
            for i in range(1, self.num_packages):
                if self.package_table.search(i).constraints.partner_packages:
                    complementary_packages = []
                    for package_id in self.package_table.search(i).constraints.partner_packages:
                        for complementary_package_id in complementary_packages:
                            if complementary_package_id not in self.package_table.search(package_id).constraints.partner_packages:
                                self.package_table.search(package_id).constraints.partner_packages.append(complementary_package_id)
                            if package_id not in self.package_table.search(complementary_package_id).constraints.partner_packages:
                                self.package_table.search(complementary_package_id).constraints.partner_packages.append(package_id)
                        complementary_packages.append(package_id)
