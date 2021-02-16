import os
import numpy as np
import matplotlib.pyplot as plt

#programs = ["Barrier_helper_td_fail.cpp", "Barrier_helper_KK.cpp"]
programs = ["Barrier_helper_td_fail.cpp"]
program_names = ["Barrier_helper"]
inpt = "70.txt"
thd_fails = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
files = os.listdir(".")

plot_data = []
for sz in thd_fails :
    times = []
    seq_time = 0.0
    for program in programs :
        time_val = 0.0
        for count in range(0, 3) :
            file = program[:-4] + "_" + inpt[:-4] + "_thd_32_" + str(count) + "_fail_" + str(sz) + ".txt"
            if file in files :
                first_line=open(file).readline().rstrip()
                time_val += float(first_line)
                break;
            if time_val == 0 :
                print("Error")
                print("File : ", file)
        times.append(float(time_val))
    plot_data.append(times)

dic_data = {}
_data = list(map(list, zip(*plot_data)))
for d in range(len(_data)) :
    dic_data[program_names[d]] = _data[d]

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

    ax.set_title('Page rank time with thread failures', fontsize=30)
    ax.set_xlabel('Failure threads', fontsize=25)
    ax.set_ylabel('Program execution time', fontsize=25)
    ax.set_xticks(np.arange(len(thd_fails)))
    ax.set_xticklabels([str(x) for x in thd_fails])
    ax.tick_params(axis="x", labelsize=25)
    ax.tick_params(axis="y", labelsize=25)
    # Draw legend if we need
    if legend:
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
        ax.legend(bars, data.keys(), loc="upper center", bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=6, prop={"size":25})

fig, ax = plt.subplots(figsize=(15,10))
bar_plot(ax, dic_data, total_width=.8, single_width=.9)
plt.savefig("plot_6.png")
