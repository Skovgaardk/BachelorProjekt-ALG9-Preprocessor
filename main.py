import xml.etree.ElementTree as ET

if __name__ == '__main__':
    tree = ET.parse('Data/malta-latest.osm')
    root = tree.getroot()



