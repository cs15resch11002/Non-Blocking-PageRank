import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

programs = ["Sequential.cpp", "Barriers.cpp", "Barrier_KK.cpp", "No_Sync.cpp", "No_Sync_KK.cpp"]
program_names = ["Sequential", "Barriers", "Barrier_STIDC_CN", "No_Sync", "No_Sync_STIDC_CN", "Ligra"]
input_files = ["soc-Epinions1.txt", "Slashdot0811.txt", "Slashdot0902.txt","soc-LiveJournal1.txt","road-italy-osm.txt","great-britain_osm.txt","asia_osm.txt","germany_osm.txt"]
ligra_res = [0.126, 0.187, 0.189,53.4,4.8,3.36,3.04,6.88]


#programs = ["Sequential.cpp", "Barriers.cpp","Barrier_identical.cpp", "No_Sync.cpp","No_Sync_identical.cpp", "Barrier_helper.cpp"]
#program_names = ["Sequential", "Barriers", "Barrier_identical", "No_Sync", "No_Sync_identical", "Barrier_helper"]
#programs = ["Sequential.cpp", "Barriers.cpp", "No_Sync.cpp", "Barrier_helper.cpp", "Barrier_KK.cpp", "No_Sync_KK.cpp","Barrier_identical.cpp","No_Sync_identical.cpp"]
#program_names = ["Sequential", "Barriers", "No_Sync", "Wait_free", "Barrier_KK", "No_Sync_KK", "Wait_free_KK"]
#program_names = ["Sequential", "Barriers", "Lock_free", "Wait_free", "Barrier_KK", "Lock_free_KK"]
# programs = ["Barriers.cpp", "Lock_variant_2b.cpp", "No_Sync_b.cpp", "Barrier_helper.cpp", "Barrier_KK.cpp"]
#programs = ["Sequential.cpp", "Barriers.cpp", "No_Sync.cpp", "Barrier_helper.cpp", "Barrier_KK.cpp", "No_Sync_KK.cpp", "Barrier_helper_KK.cpp", "Barriers_sleep.cpp", "Barrier_helper_sleep.cpp", "Barrier_helper_td_fail.cpp"]
# input_files = ["10.txt", "20.txt", "30.txt", "40.txt", "50.txt", "60.txt", "70.txt"]
#input_files = ["road-italy-osm.txt","great-britain_osm.txt","asia_osm.txt","germany_osm.txt"]

#input_files = ["10.txt", "20.txt", "30.txt", "40.txt", "RMAT_21.txt", "RMAT_22.txt"]
#ligra_res = [0.92,2.52,4.26,6.35,30.8,80.3]
#input_files = ["co-AuthorsCiteseer.txt","ca-coauthors-dblp.txt"]

#programs = ["Sequential.cpp","Barriers.cpp","Barrier_identical.cpp","No_Sync.cpp","No_Sync_identical.cpp"]
#program_names = ["Sequential", "Barriers", "Barrier_STIDC","No_Sync", "No_Sync_STIDC"]
#input_files = ["web-Stanford.txt","web-BerkStan.txt","soc-Epinions1.txt","soc-LiveJournal1.txt","co-AuthorsCiteseer.txt","ca-coauthors-dblp.txt"]
#ligra_res = [0.756,1.36,0.126,53.4,0.083,1.45]
files = os.listdir(".")

plot_data = []
counta = 0
for inpt in input_files :
    times = []
    seq_time = 0.0
    for program in programs :
        if program == "Sequential.cpp" :
            time_val = 0.0
            for count in range(0, 1) :
                first_line=open(program[:-4] + "_" + inpt[:-4] + "_pg_" + str(count) + ".txt").readline().rstrip()
                time_val += float(first_line)
            seq_time = time_val
        else :
            time_val = 0.0
            for count in range(0, 3) :
                file = program[:-4] + "_" + inpt[:-4] + "_thd_32_" + str(count) + ".txt"
                print (program, inpt)
                print ("Here")
                print (file)
                if file in files :
                    print(program[:-4] + "_" + inpt[:-4] + "_thd_32_" + str(count) + ".txt")
                    first_line=open(program[:-4] + "_" + inpt[:-4] + "_thd_32_" + str(count) + ".txt").readline().rstrip()
                    time_val += float(first_line)
                    #break;
            print("Seq time : ", seq_time)
            print("Parallel time : ", time_val)
            #times.append(seq_time / float(time_val))
            times.append(seq_time / float(time_val) / 3)
    times.append(seq_time/ligra_res[counta])
    counta += 1
    plot_data.append(times)

dic_data = {}
_data = list(map(list, zip(*plot_data)))
for d in range(len(_data)) :
    dic_data[program_names[d+1]] = _data[d]

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

    ax.set_title('PageRank Speedup Graph(Synthetic Datasets)', fontsize=22)
    #ax.set_title('PageRank Speedup Graph', fontsize=20)
    #ax.set_xlabel('Benchmarks', fontsize=18)
    ax.set_ylabel('Speedup (w.r.t Seq)', fontsize=20)
    ax.set_xticks(np.arange(len(input_files)))
    labels = ax.set_xticklabels([x[:-4] for x in input_files], rotation=20)
    ax.tick_params(axis="x", labelsize=20)
    ax.tick_params(axis="y", labelsize=20)
    #for i, label in enumerate(labels) :
    #    label.set_y(label.get_position()[1] - (i % 2) * 0.05)
    # Draw legend if we need
    if legend:
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
        ax.legend(bars, data.keys(), loc="upper center", bbox_to_anchor=(0.5, -0.18), fancybox=True, shadow=True, ncol=6, prop={"size":20})
        

fig, ax = plt.subplots(figsize=(15,10))
bar_plot(ax, dic_data, total_width=.8, single_width=.9)
plt.savefig("plot_1_ChainNode_SN.png")
#plt.savefig("plot_1_RWG.png")
#plt.savefig("plot_1.png")
