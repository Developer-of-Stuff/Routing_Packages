class HashTable:
    def __init__(self, capacity):
        self.table = []
        for i in range(capacity):
            self.table.append('')

    def insert(self, package):
        bucket = hash(package.package_id) % len(self.table)
        while self.table[bucket] != '':
            if bucket == len(self.table) - 1:
                bucket = -1
            bucket += 1
        self.table[bucket] = package

    def search(self, key):
        bucket = hash(str(key)) % len(self.table)
        while self.table[bucket] != '' and self.table[bucket].package_id != str(key):
            if bucket == len(self.table) - 1:
                bucket = -1
            bucket += 1
        if self.table[bucket] == '':
            return None
        return self.table[bucket]
