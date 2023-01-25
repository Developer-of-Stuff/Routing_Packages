from Truck import Truck
import datetime


def time_to_int(time):
    left = time.hour
    right = time.minute / 60.0
    return left + right


class Path:
    def __init__(self, num_trucks, num_drivers, num_packages, truck_package_capacity, truck_speed, start_time, start_address_id, file_reader):
        self.num_trucks = num_trucks
        self.num_drivers = num_drivers
        self.num_packages = num_packages
        self.truck_package_capacity = truck_package_capacity
        self.truck_speed = truck_speed
        self.start_time = start_time
        self.start_address_id = start_address_id
        self.file_reader = file_reader
        self.value_matrix = {start_address_id: float('inf')}
        self.current_address_id = start_address_id
        self.min_value_id = start_address_id
        self.unvisited = []
        self.not_loaded = []
        self.deadlines = {}
        self.trucks = []
        for i in range(1, num_trucks):
            self.trucks.append(Truck(i, truck_package_capacity, self.start_address_id, self.truck_speed, self.file_reader, []))
        for i in range(1, self.num_packages + 1):
            package = self.file_reader.package_table.search(i)
            self.not_loaded.append(package)
            deadline = package.deadline
            if deadline == 'EOD':
                deadline = datetime.time(17)
            self.deadlines[package.package_id] = deadline
            if self.file_reader.package_table.search(i).destination_id not in self.unvisited:
                self.unvisited.append(self.file_reader.package_table.search(i).destination_id)

    def fill_value_matrix(self, package_list):
        distances = {}
        for destination_id in self.unvisited:
            distances[destination_id] = self.file_reader.get_distance(self.current_address_id, destination_id)
        for package in package_list:

            """
            
            TAKE DEADLINES INTO ACCOUNT YOU IDIOT LOSER BOY
            
            """

            matrix_value = float(distances[package.destination_id]) / time_to_int(self.deadlines[package.package_id])
            self.value_matrix[package.package_id] = matrix_value
            if matrix_value < self.value_matrix[self.min_value_id]:
                self.min_value_id = package.package_id

    def load_truck(self, truck):
        held_packages = []
        while not truck.is_loaded():
            self.fill_value_matrix(self.not_loaded)
            package = self.file_reader.package_table.search(self.min_value_id)
            if self.value_matrix[package.package_id] == float('inf'):
                break
            if package.constraints.hold_time is not None and package.constraints.hold_time != self.start_time.time():
                self.start_time = datetime.datetime(1, 1, 1, package.constraints.hold_time.hour, package.constraints.hold_time.minute)
            if (package.constraints.required_truck_id is None or int(package.constraints.required_truck_id) == truck.truck_id) and \
               (package.constraints.hold_time is None or package.constraints.hold_time < self.start_time.time()):
                truck.load_package(package, self.start_time.time())
                self.current_address_id = package.destination_id
                self.value_matrix[package.package_id] = float('inf')
                if package.constraints.partner_packages:
                    for partner_id in package.constraints.partner_packages:
                        partner = self.file_reader.package_table.search(partner_id)
                        truck.load_package(partner, self.start_time.time())
                        self.current_address_id = partner.destination_id
                        self.value_matrix[str(partner_id)] = float('inf')
                        self.not_loaded.remove(partner)
            else:
                held_packages.append(package)
                self.value_matrix[package.package_id] = float('inf')
            self.not_loaded.remove(package)
        for package in held_packages:
            self.not_loaded.append(package)

        self.current_address_id = self.start_address_id
        temp_list = []
        for package_id in truck.package_list:
            temp_list.append(self.file_reader.package_table.search(package_id))
        ordered_package_list = []
        for i in range(len(truck.package_list)):
            self.fill_value_matrix(temp_list)
            ordered_package = self.file_reader.package_table.search(self.min_value_id)
            ordered_package_list.append(ordered_package.package_id)
            temp_list.remove(ordered_package)
            self.value_matrix[ordered_package.package_id] = float('inf')

        truck.package_list = ordered_package_list

    def deliver_all_packages(self):
        total_mileage = 0.0
        for truck in self.trucks:
            total_mileage += truck.deliver_packages()
        print('Total mileage: ' + str(total_mileage))
