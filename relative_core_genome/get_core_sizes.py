import pandas as pd
from Bio import SeqIO
import glob
import os
from math import floor
from statistics import mode, mean, median
import seaborn as sns
import seaborn.objects as so
import matplotlib.pyplot as plt

tools = ["mge_cluster", "MOB-suite", "pling"]

cores = {"tool":[], "core_size_%":[], "cluster_size":[]}

for tool in tools:
    if tool=="MOB-suite":
        cluster_path = f"../clusters/cluster_lists/MOB_secondary/addenbrookes"
        ggcaller = f"ggcaller/MOB_secondary"
    else:
        cluster_path = f"../clusters/cluster_lists/{tool}/addenbrookes"
        ggcaller = f"ggcaller/{tool}"
    clusters = [os.path.basename(el).replace('.txt','').replace("_list", '') for el in glob.glob(f"{cluster_path}/*.txt")]
    if tool == "mge_cluster":
        clusters.remove("cluster_22") #seg fault on cluster 22 from ggcaller
    modal_core_sizes = []
    for cluster in clusters:
        cores["tool"].append(tool)
        rel_core_size = []
        if tool == "pling":
            dir = f"{ggcaller}/{cluster}"
            genes = pd.read_csv(f"{dir}/gene_presence_absence_roary.csv")
            fastas = [el[0] for el in pd.read_csv(f"{cluster_path}/{cluster}.txt", header=None).values]
        else:
            dir = f"{ggcaller}/{cluster}"
            genes = pd.read_csv(f"{dir}/gene_presence_absence_roary.csv")
            fastas = [el[0] for el in pd.read_csv(f"{cluster_path}/{cluster}_list.txt", header=None).values]
        num_isolates = len(fastas)
        cores["cluster_size"].append(num_isolates)
        avg_core_length = genes[genes["No. isolates"]==num_isolates]["Avg group size nuc"].sum() #core genes are those present in 100% of the samples; take the average length over all the samples for core gene size
        for fasta in fastas:
            seq = SeqIO.read(fasta, "fasta")
            length = len(seq.seq)
            name = seq.name.split("/")[-1].replace(".fasta",'')
            ids = genes[genes["No. isolates"]==num_isolates][name].to_list()
            rel_core_size.append(floor((avg_core_length/length)*100))
        print(tool, cluster, median(rel_core_size))
        cores["core_size_%"].append(median(rel_core_size))

cores_df = pd.DataFrame.from_dict(cores)
fig, (ax, ax2) = plt.subplots(1,2)
fig.tight_layout(pad=5.0)
fig.set_figwidth(15)
sns.scatterplot(data=cores_df, x="core_size_%", y="cluster_size", hue="tool", ax=ax2)
ax2.set_xlim(-2.5,100)
ax.set_title("Distribution of median relative core genome size")
sns.swarmplot(data=cores_df, y="core_size_%", x="tool", hue="tool", zorder=0, ax=ax)
sns.boxplot(data=cores_df, y="core_size_%", x="tool", hue="tool", fill=False, ax=ax)
ax.set_ylim(-2.5,100)
ax2.set_title("Median relative core genome size vs cluster size")
plt.savefig("both_plots.png")
