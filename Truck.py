import datetime


class Truck:
    def __init__(self, truck_id, capacity, current_location_id, speed, file_reader, package_list):
        self.truck_id = truck_id
        self.capacity = capacity
        self.current_location_id = current_location_id
        self.speed = speed
        self.file_reader = file_reader
        self.package_list = package_list

    def is_loaded(self):
        return len(self.package_list) == self.capacity

    def load_package(self, package, load_time):
        if self.is_loaded():
            print('Truck is full, package cannot be loaded.')
        elif package.constraints.hold_time is not None:
            if load_time < package.constraints.hold_time:
                print('Package cannot be loaded yet.')
        else:
            self.package_list.append(package.package_id)
            package.load_time = load_time
            package.truck_id = self.truck_id

    def deliver_packages(self):
        total_distance = 0.0
        total_time = datetime.timedelta(0)
        for package_id in self.package_list:
            package = self.file_reader.package_table.search(package_id)
            distance = float(self.file_reader.get_distance(self.current_location_id, package.destination_id))
            total_distance += distance
            elapsed_time = datetime.timedelta(hours=(distance / self.speed))
            total_time += elapsed_time
            load_time = datetime.datetime(1, 1, 1, package.load_time.hour, package.load_time.minute)
            package.delivery_time = load_time + total_time
            package.delivery_time = package.delivery_time.time()
            package.delivered = 1
        return total_distance
