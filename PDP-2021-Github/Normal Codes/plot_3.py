import os
import numpy as np
import matplotlib.pyplot as plt

#programs = ["Sequential.cpp", "Barriers.cpp", "No_Sync.cpp", "Barrier_KK.cpp", "No_Sync_KK.cpp"]
#program_names = ["Sequential", "Barriers", "Lock_free", "Barrier_KK", "Lock_free_KK"]

#programs = ["Sequential.cpp", "Barriers.cpp", "No_Sync.cpp", "Barrier_helper.cpp", "Barrier_KK.cpp", "No_Sync_KK.cpp"]
#program_names = ["Sequential", "Barriers", "Lock_free", "Wait_free", "Barrier_KK", "Lock_free_KK"]
programs = ["Sequential.cpp", "Barriers.cpp","Barrier_identical.cpp", "No_Sync.cpp","No_Sync_identical.cpp", "Barrier_helper.cpp"]
program_names = ["Sequential", "Barriers", "Barrier_identical", "No_Sync", "No_Sync_identical", "Barrier_helper"]
#programs = ["Sequential.cpp", "Barriers.cpp", "No_Sync.cpp", "Barrier_helper.cpp", "Barrier_KK.cpp", "No_Sync_KK.cpp", "Barrier_helper_KK.cpp"]
#program_names = ["Sequential", "Barriers", "Lock_free", "Wait_free", "Barrier_KK", "Lock_free_KK", "Wait_free_KK"]

#programs = ["Sequential.cpp", "Barriers.cpp", "No_Sync.cpp", "Barrier_helper.cpp", "Barrier_KK.cpp", "No_Sync_KK.cpp", "Barrier_helper_KK.cpp", "Barriers_sleep.cpp", "Barrier_helper_sleep.cpp", "Barrier_helper_td_fail.cpp"]
#programs = ["Sequential.cpp", "Barriers.cpp", "No_Sync.cpp", "Barrier_helper.cpp", "Barrier_KK.cpp", "No_Sync_KK.cpp", "Barrier_helper_KK.cpp", "Barriers_sleep.cpp", "Barrier_helper_sleep.cpp", "Barrier_helper_td_fail.cpp"]
# input_files = ["10.txt", "20.txt", "30.txt", "40.txt", "50.txt", "60.txt", "70.txt"]
#input_files = ["road-italy-osm.txt","great-britain_osm.txt","asia_osm.txt","germany_osm.txt"]
input_files = ["co-AuthorsCiteseer.txt","ca-coauthors-dblp.txt"]
#input_files = ["web-BerkStan.txt","web-Stanford.txt","web-Notre.txt","web-Google.txt","10.txt", "20.txt", "30.txt", "40.txt", "50.txt", "60.txt", "70.txt"]
#input_files = ["web-Stanford.txt", "web-Notre.txt", "web-BerkStan.txt","web-Google.txt","10.txt", "20.txt", "30.txt", "40.txt", "50.txt", "60.txt", "70.txt", "RMAT_21.txt", "RMAT_22.txt", "RMAT_23.txt"]
#input_files = ["soc-Epinions1.txt", "Slashdot0811.txt", "Slashdot0902.txt","soc-LiveJournal1.txt", "web-Stanford.txt", "web-Notre.txt", "web-Google.txt"]
files = os.listdir(".")

plot_data = []
for inpt in input_files :
	program_error = []
	seq_data = []
	for program in programs :
		if program == "Sequential.cpp" :
			seq_data = [float(x.strip()) for x in open(program[:-4] + "_" + inpt[:-4] + "_pg_" + str(0) + ".txt").readlines()]
			seq_data = seq_data[2:]
			print (program[:-4] + "_" + inpt[:-4] + "_pg_" + str(0) + ".txt")
		else :
			print (program[:-4])
			manhattan_value = 0.0
			for count in range(0, 3) :
                                file = program[:-4] + "_" + inpt[:-4] + "_thd_32_" + str(count) + ".txt"
                                #if file in files :
                                data = [float(x.strip()) for x in open(program[:-4] + "_" + inpt[:-4] + "_thd_32_" + str(count) + ".txt").readlines()]
                                data = data[2:]
                                sum_ = 0.0
                                for i in range(len(seq_data)) :
                                    sum_ += abs(seq_data[i] - data[i])
                                manhattan_value += sum_
                                print(file)
                                print(manhattan_value)
                                    #break;
			print(float(manhattan_value)/3)
			program_error.append(float(manhattan_value)/3)
	plot_data.append(program_error)

dic_data = {}
_data = list(map(list, zip(*plot_data)))
for d in range(len(_data)) :
    dic_data[program_names[d+1]] = _data[d]
# print (dic_data)

def bar_plot(ax, data, colors=None, total_width=0.8, single_width=1, legend=True):
    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Iterate over all data
    for i, (name, values) in enumerate(data.items()):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    ax.set_title('PageRank Error Graph(Collaborative Network)', fontsize=20)
    #ax.set_title('PageRank Error Graph(without RMAT)', fontsize=20)
    ax.set_xlabel('Benchmarks', fontsize=18)
    ax.set_ylabel('Error (L1 norm)', fontsize=18)
    ax.set_xticks(np.arange(len(input_files)))
    ax.set_xticklabels([x[:-4] for x in input_files],rotation=25)
    ax.tick_params(axis="x", labelsize=14)
    ax.tick_params(axis="y", labelsize=14)
    # Draw legend if we need
    if legend:
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
        ax.legend(bars, data.keys(), loc="upper center", bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=6)

fig, ax = plt.subplots(figsize=(15,10))
bar_plot(ax, dic_data, total_width=.8, single_width=.9)
#plt.savefig("plot_3_WF.png")
#plt.savefig("plot_3.png")
plt.savefig("plot_3_SNAP.png")

