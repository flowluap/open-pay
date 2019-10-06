import collections

cards=[]

with open("cards.txt","r") as f:
    for line in f.read().split("\n"):
        print(line)
        cards.append(line)
        
print ([item for item, count in collections.Counter(cards).items() if count > 1])
