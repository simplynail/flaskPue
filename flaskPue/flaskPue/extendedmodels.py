from models import *

class Sites(Site):
    """
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    air_ro = Required(float, default=1.2)
    air_cp = Required(float, default=1.005)
    rooms = Set("Room")
    cooling_systems = Set("CoolingSystem")
    electric_systems = Set("TxSystem")
    """

class Rooms(Room):
    """
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    room_type = Required("RoomType")
    it_load = Required(float)
    site = Required(Site)
    cracs = Set("Crac")
    ups_systems = Set("UpsSystem")
    percentage_ups_load = Optional(buffer)
    """

class RoomTypes(RoomType):
    """
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    rooms = Set(Room)
    supply_air_temp = Required(float, default=20)
    return_air_temp = Required(float, default=30)
    """

class CoolingSystems(CoolingSystem):
    """
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    cracs = Set("Crac")
    cooling_system_type = Required("CoolingSystemType")
    site = Required(Site)
    """

class Cracs(Crac):
    """
    id = PrimaryKey(int, auto=True)
    name = Optional(str, unique=True)
    room = Required(Room)
    cooling_system = Required(CoolingSystem)
    crac_model = Required("CracModel")
    cooling = Optional(float, default=0)
    power = Optional(float, default=0)
    enabled = Required(bool, default=True)
    tx_system = Required("TxSystem")
    """
    def operate(self):
        room_load = self.room.it_load
        room_cooling = sum(crac.crac_model.maxcooling for crac in room.cracs)
        unit_capacity = self.crac_model.maxcooling
        self.cooling = min(unit_capacity,room_load * unit_capacity / room_cooling)

        unit_flow = self.cooling / (self.room.airro * self.room.aircp *
                                    (self.room.returntemp - self.room.supplytemp))
        unit_flow = max(unit_flow,self.model.maxfanflow * self.model.fanturndown)
        unit_flow = min(unit_flow,self.model.maxfanflow)
        self.fanpower = (unit_flow/self.model.maxfanflow)**(3.0) * self.model.maxfanpower

class CracModels(CracModel):
    """
    id = PrimaryKey(int, auto=True)
    cracs = Set(Crac)
    cooling_system_type = Required("CoolingSystemType")
    name = Required(str, unique=True)
    maxcooling = Required(float)
    maxpower = Required(float, default=0)
    maxfanflow = Required(float, default=0)
    fanturndown = Required(float)
    """

class CoolingSystemTypes(CoolingSystemType):
    """
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    cooling_systems = Set(CoolingSystem)
    crac_models = Set(CracModel)
    """

class LiquidSystems(LiquidSystem):
    """
    liquid_cp = Required(float, default=4.187)
    liquid_ro = Required(float, default=1000)
    supply_liquid_temp = Required(float)
    return_liquid_temp = Required(unicode)
    """

class TxSystems(TxSystem):
    """
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    site = Required(Site)
    cracs = Set(Crac)
    txs = Set("Tx")
    ups_systems = Set("UpsSystem")
    """

class Txes(Tx):
    """
    id = PrimaryKey(int, auto=True)
    name = Optional(str, unique=True)
    tx_system = Required(TxSystem)
    tx_model = Required("TxModel")
    """

class PowerModels(PowerModel):
    """
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    maxpower = Required(float)
    percentage_losses = Optional(buffer)
    """

class TxModels(TxModel):
    """
    txs = Set(Tx)
    """

class UpsModels(UpsModel):
    """
    upses = Set("Ups")
    """

class Upses(Ups):
    """
    id = PrimaryKey(int, auto=True)
    name = Optional(str, unique=True)
    ups_model = Required(UpsModel)
    ups_system = Required("UpsSystem")
    """

class UpsSystems(UpsSystem):
    """
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    rooms = Set(Room)
    tx_system = Required(TxSystem)
    upses = Set(Ups)
    """
