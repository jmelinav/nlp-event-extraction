import csv
def getGenderNouns():
    dict = {}
    with open("./data/GenderNouns.csv") as f:
        reader = csv.reader(f, delimiter="\t")
        count =0

        for i in reader:
            if(count != 0):
                dict[i[0].split(",")[0]] = "masculine"
                dict[i[0].split(",")[1]] = "feminine"
                dict[i[0].split(",")[2]] = "common"
                count+=1
            else:
                count+=1
    return dict

def getAbstractNouns():
    with open("./data/AbstractNouns.csv", mode='r', encoding='utf-8-sig') as f:
        setWords = set()
        reader = csv.reader(f, delimiter="\n")
        for i in reader:
            if(i):
                i[0] = i[0].replace(u'\xa0', u' ')
                setWords.add(i[0].lower())

    return setWords

# with open("GenderDict.csv", 'w') as csvfile:
#     writer = csv.DictWriter(csvfile, "")
#     writer.writeheader()
#     for key, value in dict.items():
#         writer.writerow({key, value})

# input_file = csv.DictReader(open("GenderDict.csv"))

import csv

def getCollectiveNouns():

    dict = {}
    with open("./data/CollectiveNouns.csv", mode='r', encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter="\t")
        for i in reader:
            splitWords = i[0].split(" ")
            if(len(splitWords)==3):
                if( splitWords[0] in dict):
                    setOfWords = dict[splitWords[0]]
                    setOfWords.add(splitWords[1].lower() + "_" + splitWords[2].lower())
                    dict[splitWords[0]] = setOfWords
                else:
                    setOfWords = set()
                    setOfWords.add(splitWords[1].lower() + "_" + splitWords[2].lower())
                    dict[splitWords[0]] = setOfWords

    with open("./data/CollectiveWords.csv", mode='r', encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter="\t")
        for i in reader:
            splitWords = i[0].split(" ")
            removeWords = ["A", "An", "a", "an"]
            for word in splitWords:
                if word in removeWords:
                    splitWords.remove(word)
                if( splitWords[0] in dict):
                    setOfWords = dict[splitWords[0]]
                    setOfWords.add(splitWords[1].lower() + "_" + splitWords[2].lower())
                    dict[splitWords[0].lower()] = setOfWords
                else:
                    setOfWords = set()
                    setOfWords.add(splitWords[1].lower() + "_" + splitWords[2].lower())
                    dict[splitWords[0].lower()] = setOfWords

    # for key in dict:
    #     print(key)
    #     print(dict[key])
    #
    # print(len(dict))
    return dict;

import re

def get_emotion_words():
    emotion_word_list = set()
    with open("./data/word_list.txt", mode='r', encoding='utf-8-sig') as f:
        content = f.readlines()
        for line in content:
            line = re.sub(r"[\n\t\s]*", "", line)
            l = line.split('~')
            l = [x.lower() for x in l]
            emotion_word_list |= set(l)
    return emotion_word_list


#get_emotion_words()
