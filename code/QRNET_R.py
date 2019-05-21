import time

from qr import DispositivoLuzAdaptador
from scanner import DispositivoLector
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

class RouterProgram(BaseProgram):
    def recv(self, packet, interface):
        s = packet.decode()
        print("\n\n[ROUTER] Received packet on interface: "+str(interface))
        print("My Name: "+self.node.name)
        print('Sending Message to User>> {}'.format(s))
        nodes[0].send(bytes(s, 'UTF-8'),interfaces=links[0])

class NodeProgram(BaseProgram):
    def recv(self, packet, interface):
        print("\n\n[USER] Received packet on interface: "+str(interface))
        s = packet.decode()
        print('\n[USER] Received message>> {}'.format(s))


##--------------------------------------------------------------------##
##                        MAIN
## Se genera una red mesh virtual previamente negociada
##--------------------------------------------------------------------##

if __name__ == "__main__":
    links = (VirtualLink('vl1'),VirtualLink('vl2'))
    nodes = (
         Node([links[0]], 'QRReceptor', mac_addr='5D-A2-A5-51-96-4E',Filters=(UniqueFilter,), Program=NodeProgram),
         Node([links[0]], 'UserNode3', mac_addr='2A-B5-87-59-96-4E', Filters=(UniqueFilter,), Program=NodeProgram)
    )
    [l.start() for l in links]
    [n.start() for n in nodes]

    try:
        #Open QR reader
        DL = DispositivoLector()
        while True:
            if(len(DL.lista) > 0):
                print("HAY DATOS")
            #message = input("Type a message: ")
            #nodes[0].send(bytes(message, 'UTF-8',))
            time.sleep(0.3)

    except (EOFError, KeyboardInterrupt):   # graceful CTRL-D & CTRL-C
        [node.stop() for node in nodes]
        [link.stop() for link in links]
