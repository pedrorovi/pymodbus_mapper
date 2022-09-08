from modbus_mapper_updated import csv_mapping_parser
from modbus_mapper_updated import mapping_decoder
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

from pprint import pprint
import logging

FORMAT = "%(asctime)-15s %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s"
logging.basicConfig(format=FORMAT)
_logger = logging.getLogger()
_logger.setLevel(logging.DEBUG)

# template = ["address", "size", "function", "name", "description"]
template = ["address", "type", "size", "name", "function"]

raw_mapping = csv_mapping_parser("simple_mapping_client.csv", template)
pprint(raw_mapping)
# print("\r\n")

mapping = mapping_decoder(raw_mapping)
# pprint(type(mapping))
# pprint(mapping)

pprint(mapping)
# print("\r\n")
# pprint(mapping.values())
# print("\r\n")
# pprint(mapping.get('type'))
# pprint(mapping.items('type'))

index, size = 0, 2
client = ModbusTcpClient(host="localhost", port=5020)

# print("HR")
# response = client.write_register(index, 100)
# pprint(response)

print("HR")
response = client.read_holding_registers(address=index, count=size)
pprint(response)
# print("IR")
# response = client.read_input_registers(index, size)
# pprint(response)
# print("CO")
# response = client.read_coils(index, size)
# pprint(response)
# print("DI")
# response = client.read_discrete_inputs(index, size)
# pprint(response)

decoder = BinaryPayloadDecoder.fromRegisters(
    response.registers, byteorder=Endian.Big, wordorder=Endian.Big
)

# print(mapping)
# while index < size:
# #     # print("[{}]\t{}".format(index, mapping[index]))
#         print(decoder.decode_16bit_int())
# #     # print(decodermapping["type"])
# #     # index += mapping[index]["size"]
#         index += 1

# response = client.read_holding_registers(index, size)
# decoder = BinaryPayloadDecoder.fromRegisters(response.registers)

# print(mapping[1])
# while index < size:
#     print(mapping[index])
#     if "type" in mapping[index]:
#         print( "[{}]\t{}".format(index, mapping[index]["type"](decoder)))
#         index += mapping[index]["size"]
#     else:
#         index+=1

for block in mapping.items():
    for mapping in block:
        if type(mapping) == dict:
            # print(type(mapping["type"]))
            # print(mapping["type"])
            
            print( "\t{}".format(mapping["type"]()(decoder)))