from FileReader import FileReader
from Path import Path
import datetime

DISTANCE_TABLE_FILE_PATH = 'CSVFiles/WGUPSDistanceTable.csv'
PACKAGE_FILE_PATH = 'CSVFiles/WGUPSPackageFile.csv'
NUM_ADDRESSES = 27
NUM_PACKAGES = 40
NUM_DRIVERS = 2
NUM_TRUCKS = 3
TRUCK_PACKAGE_CAPACITY = 16
TRUCK_SPEED = 18
START_TIME = datetime.datetime(1, 1, 1, 8)
START_ADDRESS_ID = 0

file_reader = FileReader(NUM_ADDRESSES, NUM_PACKAGES, DISTANCE_TABLE_FILE_PATH, PACKAGE_FILE_PATH)
path = Path(NUM_TRUCKS, NUM_DRIVERS, NUM_PACKAGES, TRUCK_PACKAGE_CAPACITY, TRUCK_SPEED, START_TIME, START_ADDRESS_ID, file_reader)

path.load_truck(path.trucks[0])
path.load_truck(path.trucks[1])
path.deliver_all_packages()

# SHOW PACKAGES
# for i in range(1, 41):
#     print('Package: ' + str(i))
#     print('Destination: ' + file_reader.address_legend[file_reader.package_table.search(i).destination_id])
#     print('Deadline: ' + str(file_reader.package_table.search(i).deadline))
#     print('Package Hold Time: ' + str(file_reader.package_table.search(i).constraints.hold_time))
#     print('Required Truck: ' + str(file_reader.package_table.search(i).constraints.required_truck_id))
#     print('Partner Packages: ' + str(file_reader.package_table.search(i).constraints.partner_packages))
#     print()


