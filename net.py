from enum import Enum


class EnumMsgType(Enum):
    NEW_BLK = 1


class Node(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def notify(self, mtype, blk):
        # 调用异步IO与远程节点连接并通知
        pass


ALL_NODES = []


def broadcast_block(blk):
    for node in ALL_NODES:
        node.notify(EnumMsgType.NEW_BLK, blk)


def update_nodes():
    pass


def query_nodes():
    pass


def msg_handler():
    pass


def send_msg():
    pass


def listern():
    pass
