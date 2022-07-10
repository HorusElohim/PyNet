# PyNet

![Ubuntu-Latest/py3.8,py3.9,py3.10](https://github.com/HorusElohim/PyNet/actions/workflows/ubuntu.yml/badge.svg)
![Windows-Latest/py3.8,py3.9,py3.10](https://github.com/HorusElohim/PyNet/actions/workflows/windows.yml/badge.svg)

Lightweight wrapper/abstraction of ZMQ to facilitate writing remote/local application in Python.

| Features                      |
|-------------------------------|
| Zmq as socket backend         |
| Logging as logger backend     |
| Blosc2 as compression backend |
| Low memory footprint          |



## Installation
Install PyNet with pip from GitHub
```bash
pip install git+https://github.com/HorusElohim/PyNet.git@master
```
## Quick Start
### Example Publisher/Subscriber

**Publisher**
```python
from pynet import Node
import numpy as np

class NodePublisher(Node):
    def __init__(self):
        super().__init__('MyNode')
        self.pub = self.new_publisher(self.Url.Remote(Node.SERVER, ip='*', port=5555))

my_pub = NodePublisher()

data = np.random.normal(0, 0.1, 10)
print(data)
# array([ 0.07293256,  0.13225427, -0.06779154,  0.08097599, -0.14389639,
#        -0.09090942, -0.13478001, -0.03325298, -0.08833111, -0.02072214])

my_pub.pub.send(data)
```

**Subscriber**
```python
from pynet import Node
import numpy as np

class NodeSubscriber(Node):
    def __init__(self):
        super().__init__('MyNode')
        self.sub = self.new_publisher(self.Url.Remote(Node.SERVER, ip='127.0.0.1', port=5555))

my_pub = NodePublisher()

data = my_pub.sub.recv()
print(data)
# array([ 0.07293256,  0.13225427, -0.06779154,  0.08097599, -0.14389639,
#        -0.09090942, -0.13478001, -0.03325298, -0.08833111, -0.02072214])
```

### Available Patterns
* Publisher / Subscriber
* Pusher / Puller
* Requester / Replier
* Pair / Pair


[Documentation](https://horuselohim.github.io/PyNet/html/index.html)