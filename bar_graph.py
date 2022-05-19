import matplotlib.pyplot as plt
import numpy as np


filepath = "50_1_1"
column_to_use = "Success rate"

def load_data(path, dict={}):
    with open(path, "r") as f:
        lines = f.readlines()
        index = lines[0].split(",").index(column_to_use)

        for l in lines[1:]:
            if len(l) < 30:
                continue
            pom = l.split(",")
            print(pom)
            strategy = "".join(filter(lambda x: x != " ", pom[0]))
            dist = "".join(filter(lambda x: x != " ", pom[1]))
            rate = float("".join(filter(lambda x: x != " ", pom[index]))[:-1])
            if dist not in dict:
                dict[dist] = {}
            dict[dist][strategy] = rate
    return dict


dict = load_data("routing_" + filepath + ".csv")
dict = load_data("dynamic_" + filepath + ".csv", dict)

dist = ['ProbabilisticDisturbancePlayer0.2', 'ProbabilisticDisturbancePlayer0.5',
        'PeriodicDisturbancePlayer', 'MaliciousDisturbancePlayer0.2']
strategies = []

for key in dict.keys():
    for key2 in dict[key].keys():
        strategies.append(key2)
strategies = list(set(strategies))

labels = []
data = []

for s in strategies:
    data.append([])

for i in range(len(strategies)):
    for d in dist:
        data[i].append(dict[d][strategies[i]])

new_dict = {}

for i in range(len(strategies)):
    new_dict[strategies[i]] = data[i]

order = {
    'VectorSafePath'    : 4,
    'sinus'             : 7,
    '7-x'               : 8,
    'VectorSafePathCut7': 5,
    'SafestPathV2'      : 3,
    'ShortestPath'      : 1,
    'SafestPathV1'      : 2,
    '1/x'               : 6,
    }
sorted_keys = sorted(new_dict, key=lambda x: order[x], reverse=False)

# set width of bar
barWidth = 0.08
fig, ax = plt.subplots(figsize=(12, 8))

ax.set_ylim([0, 140])
br_prev = np.arange(len(new_dict["ShortestPath"]))
colors = {
    'VectorSafePath'    : 'green',
    'sinus'             : 'grey',
    '7-x'               : 'black',
    'VectorSafePathCut7': 'cyan',
    'SafestPathV2'      : 'yellow',
    'ShortestPath'      : 'red',
    'SafestPathV1'      : 'orange',
    '1/x'               : 'white',
    }
i = 0
for s in sorted_keys:
    if i != 0:
        br = [x + barWidth for x in br_prev]
    else:
        br = br_prev
    print(s + " - " + str(new_dict[s]))
    plt.bar(br, new_dict[s], color=colors[s], width=barWidth,
            edgecolor='grey', label=s)
    br_prev = br
    i += 1

print(new_dict)

# Adding Xticks
plt.xlabel('Disturbance agents', fontweight='bold', fontsize=15)
plt.ylabel(column_to_use, fontweight='bold', fontsize=15)
plt.xticks([r + 3.5 * barWidth for r in range(len(data[0]))],
           ['0.2', '0.5', 'exp', 'malicious'])

pom = filepath.split("_")
plt.title(pom[0] + "x" + pom[0] + " with disturbance force " + pom[1] + "-" + pom[2])

plt.legend()
plt.show()
