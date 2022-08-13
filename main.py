import os
import re
from pyquery import PyQuery as pq
import matplotlib.pyplot as plt
import numpy as np

catch_times = []  # Contains sublist for each tournament. Time in seconds
max_value = 0  # Latest snitch catch across all tournaments. In seconds

'''
Extract snitch catch times from the html files and store them in catch_times
'''
for i, filename in enumerate(os.listdir("tournaments")):
    catch_times.append([])
    with open("tournaments/" + filename, "r") as f:
        raw_text = pq(f.read())
        raw_catch_times = raw_text.find("img.snitch").parents(".card-row").children(".event_time div:first").text()
        for raw_catch_time in re.findall(r"@(\d+)'(\d+)\"", raw_catch_times):
            catch_times[i].append(int(raw_catch_time[0]) * 60 + int(raw_catch_time[1]))
        if max(catch_times[i]) > max_value:
            max_value = max(catch_times[i])

'''
Plots layout
'''
fig, axes = plt.subplots(2)
fig.suptitle("When are snitches most often caught?")
plt.subplots_adjust(
    left=0.12,
    bottom=0.15,
    right=0.95,
    top=0.9,
    wspace=0.4,
    hspace=0.4
)
major_ticks = np.arange(18, max_value, 5)
minor_ticks = np.arange(17, max_value, 1)
for ax in axes:
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.grid(which="minor", alpha=0.2)
    ax.grid(which="major", alpha=1)
axes[0].set(
    xlabel="game time (min)",
    ylabel="number of catches"
)
axes[1].set(
    xlabel="game time (min)",
    ylabel="probability of catch"
)

bin_size = 30  # In seconds
max_value = max_value + bin_size
bins = np.array(range(17 * 60, max_value, bin_size))

# First subplot
for i in range(len(catch_times)):
    values = np.append(np.histogram(catch_times[i], bins=bins)[0], [0])
    axes[0].plot([b / 60 for b in bins], values, label=os.listdir("tournaments")[i].strip(".html"))
# Too messy with label for each tournament # axes[0].legend()

# Second subplot
all_catch_times = np.concatenate(catch_times, axis=None)
data = np.histogram(all_catch_times, bins=bins)
values = np.append(data[0], [0])
axes[1].plot([b / 60 for b in bins], [value / sum(values) for value in values], label="sum over total")
axes[1].legend()

fig.savefig("plot.png")
plt.show()
