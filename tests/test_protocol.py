from . import context
import unittest
from reeprotocol import protocol, base_asdu

class TestProtocol(unittest.TestCase):
    pass


class TestLinkLayer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_frame(self):
        physical_layer = MockPhysicalLayer()
        link_layer = protocol.LinkLayer()
        link_layer.initialize(physical_layer)

        fixed_asdu = bytes.fromhex("10 49 0c 87 DC 16")
        variable_asdu = bytes.fromhex("68 0d 0d 68 08 95 d1 b7 01"
                                      "07 01 00 00 01 00 00 00 2f 16")

        physical_layer.to_receive = variable_asdu

        frame = link_layer.get_frame()
        self.assertIsInstance(frame, base_asdu.VariableAsdu)
        #print(frame.data)
        self.assertEqual(frame.buffer, variable_asdu)
                                      
    def test_send_frame(self):
        physical_layer = MockPhysicalLayer()
        link_layer = protocol.LinkLayer()
        link_layer.initialize(physical_layer)

        frame = base_asdu.VariableAsdu()
        frame.generate()
        link_layer.send_frame(frame)
        self.assertEqual(physical_layer.sent, frame.buffer)
        self.assertTrue(len(physical_layer.sent)  > 1)
        
    def test_link_state_request(self):
        physical_layer = MockPhysicalLayer()
        link_layer = protocol.LinkLayer(der = 1)
        link_layer.initialize(physical_layer)

        physical_layer.to_receive =  bytes.fromhex("10 0b 95 d1 71 16")
        link_layer.link_state_request()

    def test_remote_link_reposition(self):
        physical_layer = MockPhysicalLayer()
        link_layer = protocol.LinkLayer(der = 1)
        link_layer.initialize(physical_layer)

        physical_layer.to_receive =  bytes.fromhex("10 00 95 d1 66 16")
        link_layer.remote_link_reposition()

class TestAppLayer(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_send_user_data(self):
        pass
    
        
class MockPhysicalLayer(protocol.PhysicalLayer):
    def __init__(self):
        self.sent = bytearray()
        self.to_receive = None
        self.to_receive_pos = 0
    
    def send_byte(self, byte):
        self.sent.append(byte)
    
    def get_byte(self, byte):
        bt = None
        if len(self.to_receive) > self.to_receive_pos:
            bt = self.to_receive[self.to_receive_pos]
        self.to_receive_pos += 1
        return bt
