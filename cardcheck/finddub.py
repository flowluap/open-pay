import collections

cards=[]

with open("cards.txt","r") as f:
    #read lines in array
    for line in f.read().split("\n"):
        print(line)
        cards.append(line)

if __name__=="__main__":
    #print duplicates
    print ([item for item, count in collections.Counter(cards).items() if count > 1])
