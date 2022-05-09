from pynet.model.network.node import *
from .thread_runner import WorkerRunner, Worker
from time import sleep
import pytest

DATA = [1, 2, 3, 4, 5, 6, 7, 8, 9]


class NodePublisher(Node):
    def __init__(self):
        super().__init__('NodePublisher')
        self.pub = self.Publisher(Url.Remote(ip='*'))
        sleep(0.3)
        self.result = self.pub.send(DATA)
        self.pub.close()


class NodeSubscriber(Node):
    def __init__(self):
        super().__init__('NodeSubscriber')
        self.sub = self.Subscriber(Url.Remote())
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
        super().__init__('NodePusher')
        self.pusher = self.Publisher(Url.Remote(ip='*'))
        sleep(0.3)
        self.result = self.pusher.send(DATA)
        self.pusher.close()


class NodePuller(Node):
    def __init__(self):
        super().__init__('NodePuller')
        self.puller = self.Subscriber(Url.Remote())
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
