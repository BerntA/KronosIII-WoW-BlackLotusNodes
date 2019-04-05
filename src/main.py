"""
Generates the 'Gatherer' formatted black lotus nodes from the twin head database.
Dire Maul has been excluded.
"""

import json

def getContinentIDForTwinHeadZoneID(id):
    """
    Convert twin-head zone ID to Gatherer's continent ID.
    """
    if id == 46 or id == 139: # Burning Steppes, Eastern Plaguelands
        return 2 # Eastern Kingdom
    elif id == 618 or id == 1377 or id == 2557: # Winterspring, Silithus, Dire Maul 
        return 1 # Kalimdor

    return 0

def getGathererIDForTwinHeadZoneID(id):
    """
    Convert twin-head zone ID to Gatherer's zone ID.
    """
    if id == 46: # Burning Steppes
        return 5
    elif id == 139: # Eastern Plaguelands
        return 9
    elif id == 618: # Winterspring
        return 21
    elif id == 1377: # Silithus
        return 13
    elif id == 2557: # Dire Maul
        pass

    return 0        

class Herb():
    """
    Represents a single herb, black lotus only for now.
    """
    def __init__(self, zone, data, num):
        self.zone = zone
        self.data = data
        self.num = num

    def __str__(self):
        if self.data is None:
            return "N/A"

        s = """				[%d] = {
					["gtype"] = 1,
					["x"] = %.3f,
					["count"] = 1,
					["icon"] = 30,
					["y"] = %.3f,
				},""" % (self.num, float(self.data[0]), float(self.data[1]))

        return s

def getNodeDatabase():
    """
    Load black lotus database from twinhead.
    """
    try:
        with open("data/black_lotus_nodes.json", "r") as f:
            return json.loads(f.read())
    except Exception as e:
        print(e)
        return dict()

def writeNodesForContinent(out, id, pair):
        out.writelines("	[%d] = {\n" % (id))
        for k, v in pair:
            out.writelines("		[%d] = {\n" % (int(k)))
            out.writelines("			[\"black lotus\"] = {\n")
            for n in v:
                out.writelines("{}\n".format(str(n)))
            out.writelines("			},\n")
            out.writelines("		},\n")
        out.writelines("	},\n")  

if __name__ == "__main__":
    data = getNodeDatabase()
    output = {
        "1": { 
            "21": list(), # WS
            "13": list() # Silit
         },
        "2": {
            "5": list(), # BS
            "9": list() # EPL
        }
    }

    for k, v in data.items():
        zone = getGathererIDForTwinHeadZoneID(int(k))
        continent = getContinentIDForTwinHeadZoneID(int(k))
        nodes = v["0"]["coords"]
        for idx, node in enumerate(nodes):
            output[str(continent)][str(zone)].append(Herb(zone, node, (idx + 1)))        

    with open("data/output.lua", "w") as out:
        writeNodesForContinent(out, 1, output["1"].items())
        writeNodesForContinent(out, 2, output["2"].items())
