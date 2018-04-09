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

# with open("GenderDict.csv", 'w') as csvfile:
#     writer = csv.DictWriter(csvfile, "")
#     writer.writeheader()
#     for key, value in dict.items():
#         writer.writerow({key, value})

# input_file = csv.DictReader(open("GenderDict.csv"))
