"""
Player object
"""

from pyraknet.bitstream import c_uint8, c_uint32, c_int32, c_int64, c_float, c_bit
from pyraknet.replicamanager import Replica

from replica.controllable_physics import ControllablePhysics
from replica.destructible import Destructible
from replica.stats import Stats
from replica.character import Character
from replica.inventory import Inventory
from replica.script import Script
from replica.skill import Skill
from replica.render import Render
from replica.component107 import Component107


class Player(Replica):
    """
    Player replica object
    """
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.control = ControllablePhysics(player=True)
        self.destructible = Destructible()
        self.stats = Stats()
        self.char = Character()
        self.inventory = Inventory()
        self.script = Script()
        self.skill = Skill()
        self.render = Render()
        self.component107 = Component107()

    def serialize(self, stream):
        stream.write(c_bit(True))
        stream.write(c_bit(False))
        stream.write(c_bit(False))

        self.control.serialize(stream)
        self.destructible.serialize(stream)
        self.stats.serialize(stream)
        self.char.serialize(stream)
        self.inventory.serialize(stream)
        self.script.serialize(stream)
        self.skill.serialize(stream)
        self.render.serialize(stream)
        self.component107.serialize(stream)

    def write_construction(self, stream):
        stream.write(c_int64(self.id))
        stream.write(c_int32(1))

        stream.write(c_uint8(0))

        # stream.write(c_uint8(len(self.name)))
        # stream.write(self.name, allocated_length=len(self.name) * 2)

        stream.write(c_uint32(25))

        stream.write(c_bit(False))
        stream.write(c_bit(False))
        stream.write(c_bit(False))
        stream.write(c_bit(False))
        stream.write(c_bit(False))
        stream.write(c_bit(False))
        stream.write(c_bit(False))

        stream.write(c_bit(True))
        stream.write(c_bit(False))
        stream.write(c_bit(False))

        self.control.write_construction(stream)
        self.destructible.write_construction(stream)
        self.stats.write_construction(stream)
        self.char.write_construction(stream)
        self.inventory.write_construction(stream)
        self.script.write_construction(stream)
        self.skill.write_construction(stream)
        self.render.write_construction(stream)
        self.component107.write_construction(stream)
