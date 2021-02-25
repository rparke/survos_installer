import numpy as np
import yaml

with open("construct.yaml") as f:
    construct = yaml.safe_load(f)

with open("construct_working.yaml") as f:
    construct_working = yaml.safe_load(f)


print(construct['specs'])
print(construct_working['specs'])


checker = (np.asarray(construct['specs']) == np.asarray(construct_working['specs']))

for i in range(checker.size):
    if checker[i] == False:
        print(i)
        print(np.asarray(construct['specs'])[i])
        print(checker[i])


for i in range(checker.size):
    if checker[i] == False:
        print(i)
        print(np.asarray(construct_working['specs'])[i])
        print(checker[i])