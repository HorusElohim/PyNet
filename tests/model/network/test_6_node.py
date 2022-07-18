from pynet.model.network.node import *
from .thread_runner import WorkerRunner, Worker
from time import sleep
from pynet.model import Logger


DATA = [1, 2, 3, 4, 5, 6, 7, 8, 9]

TEST_LOG = Logger('test_6_node')


class NodePublisher(Node):
    def __init__(self):
        super().__init__('NodePublisher', logger_other=TEST_LOG)
        self.pub = self.new_publisher(Node.Url.Remote(Node.SERVER, ip='*'))
        sleep(0.3)
        self.result = self.pub.send(DATA)
        self.pub.close()


class NodeSubscriber(Node):
    def __init__(self):
        super().__init__('NodeSubscriber', logger_other=TEST_LOG)
        self.sub = self.new_subscriber(Node.Url.Remote(Node.CLIENT))
        sleep(0.3)
        self.result = self.sub.receive()
        self.sub.close()


# Actions for connection bind
# publisher, pusher, pair
class NodePublisherWorker(Worker):
    node: NodePublisher

    def run(self) -> None:
        self.node = NodePublisher()


# # Actions for connection connect
# # subscriber, puller, pair
class NodeSubscriberWorker(Worker):
    node: NodeSubscriber

    def run(self) -> None:
        self.node = NodeSubscriber()


# Test Publisher/Subscriber
# Test Pusher/Puller
# Server/Client
def test_transmission_pub_sub():
    worker = [NodePublisherWorker(), NodeSubscriberWorker()]
    WorkerRunner.run(worker)
    assert worker[0].node.result
    assert worker[1].node.result == DATA


class NodePusher(Node):
    def __init__(self):
        super().__init__('NodePusher', logger_other=TEST_LOG)
        self.pusher = self.new_publisher(Node.Url.Remote(Node.SERVER, ip='*'))
        sleep(0.3)
        self.result = self.pusher.send(DATA)
        self.pusher.close()


class NodePuller(Node):
    def __init__(self):
        super().__init__('NodePuller', logger_other=TEST_LOG)
        self.puller = self.new_subscriber(Node.Url.Remote(Node.CLIENT))
        sleep(0.3)
        self.result = self.puller.receive()
        self.puller.close()


# Actions for connection bind
# publisher, pusher, pair
class NodePusherWorker(Worker):
    node: NodePusher

    def run(self) -> None:
        self.node = NodePusher()


# # Actions for connection connect
# # subscriber, puller, pair
class NodePullerWorker(Worker):
    node: NodePuller

    def run(self) -> None:
        self.node = NodePuller()


# Test Publisher/Subscriber
# Test Pusher/Puller
# Server/Client
def test_transmission_push_pull():
    worker = [NodePusherWorker(), NodePullerWorker()]
    WorkerRunner.run(worker)
    assert worker[0].node.result
    assert worker[1].node.result == DATA
