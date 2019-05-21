import time

from qr import QRGenerator
from mesh.node import Node
from mesh.links import UDPLink, VirtualLink, IRCLink
from mesh.programs import Printer, Switch
from mesh.filters import UniqueFilter
from mesh.programs import BaseProgram,Switch,RoutedProgram
from mesh.routers import MessageRouter

import scapy
try:
    from queue import Empty
except ImportError:
    from Queue import Empty
from time import sleep

##--------------------------------------------------------------------##
##                        Tabla de Nodos
## 
##--------------------------------------------------------------------##
nodesTable = [
    ('ClearnetNode','1C-C2-87-54-96-4E'),
    ('RouterNode','2C-C3-87-54-96-4E'),
    ('UserNode1','1A-B5-87-59-96-4E'),
    ('UserNode2','3D-C2-45-51-96-4A'),
    ('QRTransmisor','3D-A2-A5-51-96-4E')
]

##---------------------------------------------------------------------------##
##                                  PROGRAMS
## Cada programa se encarga de manejar los paquetes que llegan a cada nodo
##---------------------------------------------------------------------------##
class IRCProgram(BaseProgram):
    def run(self):
        """runloop that reads packets off the node's incoming packet buffer (node.inq)"""
        while self.keep_listening:
            for interface in self.node.interfaces:
                try:
                    self.recv(self.node.inq[interface].get(timeout=0), interface)
                except Empty:
                    sleep(0.01)

    def recv(self, packet, interface):
        s = packet.decode()
        print("\n\n[IRC] Received packet on interface: "+str(interface))
        print("My Name: "+self.node.name)
        print('Sending Message to Router>> {}'.format(s))
        nodes[0].send(bytes(s, 'UTF-8'),interfaces=links[1])


class RouterProgram(BaseProgram):
    def recv(self, packet, interface):
        s = packet.decode()
        print("\n\n[ROUTER] Received packet on interface: "+str(interface))
        print("My Name: "+self.node.name)
        print('Sending Message to User>> {}'.format(s))
        nodes[1].send(bytes(s, 'UTF-8'),interfaces=links[4])

class NodeProgram(BaseProgram):
    def recv(self, packet, interface):
        print("\n\n[USER] Received packet on interface: "+str(interface))
        s = packet.decode()
        if(str(interface) == '<vl4>'):
            #create QR
            QRGenerator(s)
        else:
            print('\n[USER] Received message>> {}'.format(s))


##--------------------------------------------------------------------##
##                        MAIN
## Se genera una red mesh virtual previamente negociada
##--------------------------------------------------------------------##

if __name__ == "__main__":
    links = (IRCLink('irc1'),VirtualLink('vl1'),VirtualLink('vl2'),VirtualLink('vl3'),VirtualLink('vl4'))
    nodes = (
         Node([links[0], links[1]], 'ClearnetNode',mac_addr='1C-C2-87-54-96-4E', Filters=(UniqueFilter,), Program=IRCProgram),
         Node([links[1],links[2],links[3]], 'RouterNode',mac_addr='2C-C3-87-54-96-4E', Filters=(UniqueFilter,), Program=RouterProgram),
         Node([links[2]], 'UserNode1', mac_addr='1A-B5-87-59-96-4E', Filters=(UniqueFilter,), Program=NodeProgram),
         Node([links[3]], 'UserNode2', mac_addr='3D-C2-45-51-96-4E',Filters=(UniqueFilter,), Program=NodeProgram),
         Node([links[4]], 'QRTransmisor', mac_addr='3D-A2-A5-51-96-4E',Filters=(UniqueFilter,), Program=NodeProgram)
    )
    [l.start() for l in links]
    [n.start() for n in nodes]

    try:
        while True:
            #message = input("Type a message: ")
            #nodes[0].send(bytes(message, 'UTF-8',))
            time.sleep(0.3)

    except (EOFError, KeyboardInterrupt):   # graceful CTRL-D & CTRL-C
        [node.stop() for node in nodes]
        [link.stop() for link in links]
