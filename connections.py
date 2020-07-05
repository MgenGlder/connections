import re


def hasType(type, stringToCheck):
    return stringToCheck.find(type) != -1

def filterFunction(variable):
    if (variable == True):
        return True
    else:
        return False

def determineConnectionType(stringToCheck):
    c = stringToCheck.find("cnc") != -1
    o = stringToCheck.find("other") != -1
    i = stringToCheck.find("infection") != -1
    labels = [c, o, i]
    filtered = list(filter(filterFunction, labels))
    if (len(filtered) > 1):
        print("There was an error,Too many labels applied to packet", filtered)
        # raise Error("Too many labels applied to packet")
    elif (len(filtered) < 1):
        print("There was an error, too few labels applied to packet", filtered)
        # raise Error("Too few labels applied to packet")
    else:
        if (c == True):
            return "cnc"
        elif (o == True):
            return "other"
        elif (i == True):
            return "infection"
        else:
            return "unknown"

class ConnectionInfo(object):
    connection_types: []
    connection_label: ""
    addresses: []
    ports: []
    def __init__(self, connection_types, connection_label, addresses, ports):
        self.connection_label = connection_label
        self.connection_types = connection_types
        self.addresses = addresses
        self.ports = ports



def generateConnectionsDictionary(input):
    items = dict()
    for line in input:
        # Toss out everything that's not TCP
        # Also should check for empty lines
        s = re.search('\{TCP\}', line)
        if (s != None):
            p = re.compile("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):?(\d{0,9})\s->\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):?(\d{0,9})")
            ip1 = p.search(line).group(1)
            port1 = p.search(line).group(2)
            ip2 = p.search(line).group(3)
            port2 = p.search(line).group(4)
            connectionType = determineConnectionType(line)
            print(ip1)
            print(port1)
            print(ip2)
            print(port2)
            print("Label is.. ", determineConnectionType(line))
            addressTupleVariation1 = (ip1, ip2)
            addressTupleVariation2 = (ip2, ip1)
            if (addressTupleVariation1 in items):
                print("found it")
                types = items[addressTupleVariation1].connection_types
                if (connectionType not in types):
                    print("Didn't have this connection type, so added it: ", connectionType)
                    types.append(connectionType)
            elif (addressTupleVariation2 in items):
                types = items[addressTupleVariation2].connection_types
                print("found it")
                if (connectionType not in types):
                    print("Didn't have this connection type, so added it: ", connectionType)
                    types.append(connectionType)
            else:
                print("didn't find it, so adding")
                items[addressTupleVariation1] = ConnectionInfo([connectionType], None, [ip1, ip2], [port1, port2])
    return items

def processConnectionsDictionary(dict):
    f = open("connections.txt", "w")
    for key, value in dict.items():
        print("Item: ", value)
        # f.write()
        print(value.addresses[0] + "|" + value.ports[0] + "|" + value.addresses[1] + "|" + value.ports[1] + "|")

def main():
    input = open("skimmed_input", "r")
    dict = generateConnectionsDictionary(input)
    processConnectionsDictionary(dict)
    input.close()

if __name__ == "__main__":
    main()