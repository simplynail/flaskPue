from pony.orm import *

db = Database()

class Site(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    air_ro = Required(float, default=1.2)
    air_cp = Required(float, default=1.005)
    rooms = Set("Room")
    cooling_systems = Set("CoolingSystem")
    electric_systems = Set("TxSystem")


class Room(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    room_type = Required("RoomType")
    it_load = Required(float)
    site = Required(Site)
    cracs = Set("Crac")
    ups_systems = Set("UpsSystem")
    percentage_ups_load = Optional(buffer)


class RoomType(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    rooms = Set(Room)
    supply_air_temp = Required(float, default=20)
    return_air_temp = Required(float, default=30)


class CoolingSystem(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    cracs = Set("Crac")
    cooling_system_type = Required("CoolingSystemType")
    site = Required(Site)


class Crac(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str, unique=True)
    room = Required(Room)
    cooling_system = Required(CoolingSystem)
    crac_model = Required("CracModel")
    cooling = Optional(float, default=0)
    power = Optional(float, default=0)
    enabled = Required(bool, default=True)
    tx_system = Required("TxSystem")


class CracModel(db.Entity):
    id = PrimaryKey(int, auto=True)
    cracs = Set(Crac)
    cooling_system_type = Required("CoolingSystemType")
    name = Required(str, unique=True)
    maxcooling = Required(float)
    maxpower = Required(float, default=0)
    maxfanflow = Required(float, default=0)
    fanturndown = Required(float)


class CoolingSystemType(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    cooling_systems = Set(CoolingSystem)
    crac_models = Set(CracModel)


class LiquidSystem(db.CoolingSystemType):
    liquid_cp = Required(float, default=4.187)
    liquid_ro = Required(float, default=1000)
    supply_liquid_temp = Required(float)
    return_liquid_temp = Required(unicode)


class TxSystem(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    site = Required(Site)
    cracs = Set(Crac)
    txs = Set("Tx")
    ups_systems = Set("UpsSystem")


class Tx(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str, unique=True)
    tx_system = Required(TxSystem)
    tx_model = Required("TxModel")


class PowerModel(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    maxpower = Required(float)
    percentage_losses = Optional(buffer)


class TxModel(db.PowerModel):
    txs = Set(Tx)


class UpsModel(db.PowerModel):
    upses = Set("Ups")


class Ups(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str, unique=True)
    ups_model = Required(UpsModel)
    ups_system = Required("UpsSystem")


class UpsSystem(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    rooms = Set(Room)
    tx_system = Required(TxSystem)
    upses = Set(Ups)


