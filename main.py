import xml.etree.ElementTree as ET

import geopandas as gpd


def noteTest():
    tree = ET.parse('Data/malta-latest.osm')
    root = tree.getroot()
    nodeDict = {
    }


    ##Find nodes with tag = highway
    for child in root:
        if child.tag == 'node':
            for tag in child:
                if tag.attrib['k'] == 'highway':
                    nodeDict[child.attrib['id']] = child.attrib['lat'] + ',' + child.attrib['lon']
                    break

    df_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    print(f"{type(df_world)}, {df_world.geometry.name}")

def plotTest():
    df_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

    print(df_world.geometry.geom_type.value_counts())
    #df_world.plot(figsize=(10, 6))
    df_world.head()
    df_world.plot()



if __name__ == '__main__':

    plotTest()









