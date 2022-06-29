Quick Start
=================================

Example Publisher / Subscriber using TCP connection:

Publisher
__________________

Basic scripting example:

.. code-block:: python

    from pynet import Node
    import numpy as np

    sock_url = Node.Url.Remote(Node.SERVER, ip='*', port=5555)

    node = Node('MyNode')
    pub = node.new_publisher(sock_url)

    data = np.random.normal(0, 0.1, 10)
    print(data)
    # array([ 0.07293256,  0.13225427, -0.06779154,  0.08097599, -0.14389639,
    #        -0.09090942, -0.13478001, -0.03325298, -0.08833111, -0.02072214])

    pub.send(data)


Class example:

.. code-block:: python

    from pynet import Node
    import numpy as np

    sock_url = Node.Url.Remote(Node.SERVER, ip='*', port=5555)

    class NodePublisher(Node):
        def __init__(self):
            super().__init__('MyNode')
            self.pub = self.new_publisher(sock_url)

    my_pub = NodePublisher()
    data = np.random.normal(0, 0.1, 10)

    print(data)

    # array([ 0.07293256,  0.13225427, -0.06779154,  0.08097599, -0.14389639,
    #        -0.09090942, -0.13478001, -0.03325298, -0.08833111, -0.02072214])

    my_pub.pub.send(data)


Subscriber
__________________

Basic scripting example:

.. code-block:: python

    from pynet import Node
    import numpy as np

    sock_url = Node.Url.Remote(Node.SERVER, ip='127.0.0.1', port=5555)

    node = Node('MyNode')
    sub = self.new_publisher(sock_url)
    data = my_pub.sub.recv()

    print(data)

    # array([ 0.07293256,  0.13225427, -0.06779154,  0.08097599, -0.14389639,
    #        -0.09090942, -0.13478001, -0.03325298, -0.08833111, -0.02072214])


Class example:

.. code-block:: python

    from pynet import Node
    import numpy as np

    sock_url = Node.Url.Remote(Node.SERVER, ip='127.0.0.1', port=5555)

    class NodeSubscriber(Node):
        def __init__(self):
            super().__init__('MyNode')
            self.sub = self.new_publisher(sock_url)

    my_pub = NodePublisher()
    data = my_pub.sub.recv()

    print(data)

    # array([ 0.07293256,  0.13225427, -0.06779154,  0.08097599, -0.14389639,
    #        -0.09090942, -0.13478001, -0.03325298, -0.08833111, -0.02072214])








