import os
import sys
from pymei import XmlImport

def load(file):
    return XmlImport.documentFromFile(file)

if __name__ == "__main__":
    file = raw_input("Filename please? ")
    MEI_file = load(file)
    root = MEI_file.getRootElement()
    if not root.hasParent():
    	print("success!")
    if root.hasChildren():
    	print("Well at least a little")
