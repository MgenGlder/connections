import re

logMode = False
countDict = {"cnc": 0, "infection": 0, "other": 0}
countConnectionTypes = {"cnc": 0, "infection": 0, "other": 0, "unknown": 0}
def logPrint(stringToPrint, optionalParameter = None):
    if(logMode == True):
        if(optionalParameter == None):
            print(stringToPrint)
        else:
            print(stringToPrint, optionalParameter)

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
        logPrint("There was an error,Too many labels applied to packet", filtered)
        # raise Error("Too many labels applied to packet")
    elif (len(filtered) < 1):
        logPrint("There was an error, too few labels applied to packet", filtered)
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
            p = re.compile("((?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])):([0-9]+)\s->\s((?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])):([0-9]+)")
            ip1 = p.search(line).group(1)
            port1 = p.search(line).group(2)
            ip2 = p.search(line).group(3)
            port2 = p.search(line).group(4)
            connectionType = determineConnectionType(line)
            countConnectionTypes[connectionType] += 1
            logPrint(ip1)
            logPrint(port1)
            logPrint(ip2)
            logPrint(port2)
            logPrint("Label is.. ", determineConnectionType(line))
            addressTupleVariation1 = (ip1+port1, ip2+port2)
            addressTupleVariation2 = (ip2+port2, ip1+port1)
            if (addressTupleVariation1 in items):
                logPrint("found it")
                types = items[addressTupleVariation1].connection_types
                if (connectionType not in types):
                    logPrint("Didn't have this connection type, so added it: ", connectionType)
                    types.append(connectionType)
            elif (addressTupleVariation2 in items):
                types = items[addressTupleVariation2].connection_types
                logPrint("found it")
                if (connectionType not in types):
                    logPrint("Didn't have this connection type, so added it: ", connectionType)
                    types.append(connectionType)
            else:
                logPrint("didn't find it, so adding")
                items[addressTupleVariation1] = ConnectionInfo([connectionType], None, [ip1, ip2], [port1, port2])
    return items

def determineLabel(connectionInfo):
    if("cnc" in connectionInfo.connection_types):
        if ("infection" not in connectionInfo.connection_types):
            connectionInfo.connection_label = "cnc"
        else:
            logPrint(connectionInfo.connection_types)
            raise Error("Cnc and infection types on one packet")
    elif("infection" in connectionInfo.connection_types):
        if("cnc" not in connectionInfo.connection_types):
            connectionInfo.connection_label = "infection"
        else:
            logPrint(connectionInfo)
            raise Error("Infection and cnc types on one packet")
    elif("other" in connectionInfo.connection_types):
        connectionInfo.connection_label = "other"
    else:
        logPrint(connectionInfo.connection_types)
        raise Error("Found a packet without a valid connection type")


def processConnectionsDictionary(dict):
    f = open("connections.txt", "w")

    for key, value in dict.items():
        determineLabel(value)
        countDict[value.connection_label] += 1
        # print("Item: ", value)
        # f.write()
        f.writelines(value.addresses[0] + "|" + value.ports[0] + "|" + value.addresses[1] + "|" + value.ports[1] + "|" + value.connection_label + "\n")

def main():
    if (logMode):
        print("Log mode is enabled")
    else:
        print("Log mode is disabled")
    input = open("result_after_all_rules", "r")
    dict = generateConnectionsDictionary(input)
    processConnectionsDictionary(dict)
    print(countDict)
    print(countConnectionTypes)
    input.close()

if __name__ == "__main__":
    main()

