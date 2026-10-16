
from src.ApplicationSpecific.DSA.SkipList import SkipList
from src.ApplicationSpecific.DSA.BinaryTree import BinaryTree
from src.ApplicationSpecific.DSA.LinkedList import LinkedList


DSAs = {
    "LinkedList": LinkedList,
    "BinaryTree": BinaryTree,
    "SkipList": SkipList
}





#def ClientFactory(name: str, data_structure: str):
#    if data_structure in DSAs:
#        return Client(name, data_structure)
#    else:
#        raise ValueError(f"Invalid data structure: {data_structure}")