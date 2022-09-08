from modbus_mapper_updated import csv_mapping_parser
from modbus_mapper_updated import modbus_context_decoder

from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore.context import ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.version import version

from pprint import pprint
import logging

FORMAT = "%(asctime)-15s %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s"
logging.basicConfig(format=FORMAT)
_logger = logging.getLogger()
_logger.setLevel(logging.DEBUG)

template = ["address", "value", "function", "name", "description"]
raw_mapping = csv_mapping_parser("simple_mapping_server.csv", template)
print("raw_mapping")
pprint(raw_mapping)

slave_context = modbus_context_decoder(raw_mapping)
print("slave_context.store")
pprint(slave_context.store)
context = ModbusServerContext(slaves=slave_context, single=True)

identity = ModbusDeviceIdentification(
    info_name={
        "VendorName": "Pymodbus",
        "ProductCode": "PM",
        "VendorUrl": "https://github.com/riptideio/pymodbus/",
        "ProductName": "Pymodbus Server",
        "ModelName": "Pymodbus Server",
        "MajorMinorRevision": version.short(),
    }
)
StartTcpServer(context=context, identity=identity, address=("localhost", 5020))
