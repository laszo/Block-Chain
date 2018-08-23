import hashlib
import json


class Block(object):
    def __init__(self, index, timestamp, pre_hash, data):
        self.index = index
        self.timestamp = timestamp
        self.pre_hash = pre_hash
        self.data = data
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        thestring = str(self.index) + self.pre_hash + self.timestamp + json.dumps(self.data)
        return hashlib.sha256(thestring.encode()).hexdigest()

    def write_to_disk(self):
        pass

    def read_from_disk(self, disk_data):
        self.data = disk_data


def create_block():
    pass


def broadcast_block():
    pass


def verify_block():
    pass


def add_trans_to_block():
    pass


def add_block():
    pass
