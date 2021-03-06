from  .. import pytelemetry
import queue
import pytest
import unittest.mock as mock

class transportMock:
    def __init__(self):
        self.queue = queue.Queue()
    def read(self, maxbytes=1):
        data = []
        amount = 0
        while amount < maxbytes and not self.queue.empty():
            c = self.queue.get()
            data.append(c)
            amount += 1
        return data

    def readable(self):
        return self.queue.qsize()

    def write(self, data):
        for i in range(len(data)):
            self.queue.put(data[i])
        return 0

    def writeable(self):
        return not self.queue.full()

def test_wrong_type():
    # Setup
    t = transportMock()
    c = pytelemetry.pytelemetry(t)

    with pytest.raises(Exception) as excinfo:
        c.publish('sometopic',12,'string')
    # TODO : Assert exception
    assert t.queue.qsize() == 0

def test_unexisting_type():
    # Setup
    t = transportMock()
    c = pytelemetry.pytelemetry(t)

    c.publish('sometopic',12,'int323')
    assert t.queue.qsize() == 0

def test_hardcoded():
    t = transportMock()
    c = pytelemetry.pytelemetry(t)
    cb = mock.Mock(spec=["topic","data"])
    c.subscribe('sometopic ',cb)

    t.write([247, 6, 0, 115, 111, 109, 101, 116, 111, 112, 105, 99, 32, 0, 169, 48, 0, 0, 111, 249, 127])
    c.update()
    assert t.queue.qsize() == 0
    cb.assert_called_once_with('sometopic ',12457)

# TODO : Check what happens is string is non null terminated

# TODO : Check what happens if there are spaces in name

# TODO Check wrong crc
