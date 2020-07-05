import re


def hasType(type, stringToCheck):
    return stringToCheck.find(type) != -1

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
# print(input.readline())
input.close()
