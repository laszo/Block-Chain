import hashlib
import json
import threading
from datetime import datetime

from trans import make_trans


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
        self.nonce = 0

    def get_pow_header(self):
        return '%d%d%s' % (self.index, self.timestamp, self.pre_hash)

    def refresh_hash(self):
        self.hash = calculate_hash(self.index, self.pre_hash, self.timestamp, self.data)

    def write_to_disk(self):
        pass

    def read_from_disk(self, disk_data):
        self.data = disk_data

    def __str__(self):
        return 'index: %d, time: %s, nonce: %d' % (
            self.index, datetime.fromtimestamp(self.timestamp), self.nonce)


def create_genesis_block():
    data = make_trans('myaddress', 'from miner', 50)
    gene_blk = Block(0, '00000000000000', data)
    gene_blk.nonce = 2083236893  # 2083236893
    gene_blk.refresh_hash()
    print(gene_blk)
    return gene_blk


def verify_block(blk):
    if isinstance(blk, Block):
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
        self._chain = []
        self._load_data()
        pass

    def _load_data(self):
        # self._chain.append(Block(0, '', ''))
        if len(self._chain) == 0:
            self._chain.append(create_genesis_block())

    def add_block(self, blk):
        if verify_block(blk):
            blk.index = len(self._chain)
            blk.pre_hash = self._chain[-1].hash
            blk.refresh_hash()
            self._chain.append(blk)

            return True
        return False

    def query_all(self):
        return self._chain

    def get_block_by_index(self, index):
        if len(self._chain) > index:
            return self._chain[index]

    def get_last_block(self):
        return self._chain[-1]


BlockChain = _BlockChain.process_instance()
