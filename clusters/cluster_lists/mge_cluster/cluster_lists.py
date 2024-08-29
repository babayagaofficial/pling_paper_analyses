import pandas as pd


clusters_df = pd.read_csv("/home/daria/Documents/papers/plasmid-dcj/pling_paper_analyses/clusters/addenbrookes/mge_cluster.csv")

for cluster in range(25):
    with open(f"cluster_{cluster}_list.txt", "w") as f:
        for name in clusters_df[clusters_df["Standard_Cluster"]==str(cluster)]["Sample_Name"].values:
            f.write(f"../fastas/addenbrookes/{name}.fna\n")
