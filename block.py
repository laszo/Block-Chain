import hashlib
import json
import threading

from datetime import datetime

from net import broadcast_block


def calculate_hash(index, pre_hash, timestamp, data):
    thestring = str(index) + pre_hash + str(timestamp) + json.dumps(data)
    return hashlib.sha256(thestring.encode()).hexdigest()


class Block(object):
    def __init__(self, index, pre_hash, data):
        self.index = index
        self.timestamp = int(datetime.now().timestamp())
        self.pre_hash = pre_hash
        self.data = data
        self.hash = calculate_hash(index, pre_hash, self.timestamp, data)  # 在这里就计算hash意味着区块一经创建就不能更改

    def refresh_hash(self):
        self.hash = calculate_hash(self.index, self.pre_hash, self.timestamp, self.data)

    def write_to_disk(self):
        pass

    def read_from_disk(self, disk_data):
        self.data = disk_data


def verify_block(blk):
    if blk is isinstance(Block):
        return blk.hash == calculate_hash(blk.index, blk.pre_hash, blk.timestamp, blk.data)
    return False


class _BlockChain(object):
    _thread_lock = threading.Lock()

    @staticmethod
    def process_instance():
        """
        进程内单例
        """
        if not hasattr(_BlockChain, '_instance'):
            with _BlockChain._thread_lock:
                if not hasattr(_BlockChain, '_instance'):
                    _BlockChain._instance = _BlockChain()
        return _BlockChain._instance

    def __init__(self):
        """
        1. 从配置文件配置的数据目录中，加载现有的区块链数据，校验并加载到内存里面
        """
        self.chain = []
        pass

    def add_block(self, blk):
        if verify_block(blk):
            if blk.index == len(self.chain):
                blk.pre_hash = self.chain[-1].hash
                blk.refresh_hash()
                self.chain.append(blk)
                broadcast_block(blk)
                return True
        return False


BlockChain = _BlockChain.process_instance()



