
def hasType(type, stringToCheck):
    return stringToCheck.find(type) != -1

input = open("skimmed_input", "r")

for line in input:
    print("Substring contains something", hasType("something", line))
# print(input.readline())
input.close()
