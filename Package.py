from Constraint import Constraint


class Package:
    def __init__(self, package_id, destination_id, deadline, weight, constraints=Constraint(None, None, []), truck_id=-1, delivered=0, load_time=None, delivery_time=None):
        self.package_id = package_id
        self.destination_id = destination_id
        self.deadline = deadline
        self.weight = weight
        self.truck_id = truck_id
        self.delivered = delivered
        self.load_time = load_time
        self.delivery_time = delivery_time
        self.constraints = constraints

    # def get_status(self):
