import time

from mesh.node import Node
from mesh.links import UDPLink, VirtualLink, IRCLink
from mesh.programs import Printer, Switch
from mesh.filters import UniqueFilter
from mesh.programs import BaseProgram,Switch


class IRCProgram(BaseProgram):
    def recv(self, packet, interface):
        s = packet.decode()
        print("Received IRC packet on interface: "+str(interface))
        print("My MAC Address: "+self.node.mac_addr)
        print("My Name: "+self.node.name)
        print('\nCreating QR for message>> {}'.format(s))
        


if __name__ == "__main__":
    links = (IRCLink('irc1'),VirtualLink('vl2'))
    nodes = (
        Node([links[0]], 'Alejandro', Filters=(UniqueFilter,), Program=IRCProgram),
        Node([links[0],links[1]], 'Alejandro', Filters=(UniqueFilter,), Program=IRCProgram),
        Node([links[1]], 'Alejandro', Filters=(UniqueFilter,), Program=IRCProgram)
    )
    [l.start() for l in links]
    [n.start() for n in nodes]

    print("Run lan-chat.py on another laptop to talk between the two of you on en0.")
    try:
        while True:
            message = input("Type a message: ")
            nodes[0].send(bytes(message, 'UTF-8',))
            time.sleep(0.3)

    except (EOFError, KeyboardInterrupt):   # graceful CTRL-D & CTRL-C
        [n.stop() for n in nodes]
        [link.stop() for link in links]
