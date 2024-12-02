# Name: Dillon Sherling
# Student id: 11842839


class Dictionary:
    def __init__(self):
        self.dict = {}

    def add(self, key, value):
        if key in self.dict:
            self.dict[key].append(value)
        else:
            self.dict[key] = [value]

    def get(self, key):
        if key in self.dict:
            return self.dict[key]
        else:
            return []


dictionary = Dictionary()
dictionary.add("fruit", "apple")

dictionary.add("fruit", "banana")
dictionary.add("vegatable", "carrot")

print(dictionary.get("fruit"))
print(dictionary.get("vegatable"))
print(dictionary.get("meat"))
