import re


def hasType(type, stringToCheck):
    return stringToCheck.find(type) != -1

def filterFunction(variable):
    if (variable == True):
        return True
    else:
        return False

def determineLabel(stringToCheck):
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

input = open("skimmed_input", "r")

for line in input:
    # Toss out everything that's not TCP
    s = re.search('\{TCP\}', line)
    if (s != None):
        p = re.compile("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):?(\d{0,9})\s->\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):?(\d{0,9})")
        ip1 = p.search(line).group(1)
        port1 = p.search(line).group(2)
        ip2 = p.search(line).group(3)
        port2 = p.search(line).group(4)
        print(ip1)
        print(port1)
        print(ip2)
        print(port2)
        print("Label is.. ", determineLabel(line))
# print(input.readline())
input.close()
