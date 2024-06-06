import pandas as pd


clusters_df = pd.read_csv("/home/daria/Documents/projects/addenbrookes/MOB-suite/clusters/clusters.txt", sep="\t")
clusters = list(set(clusters_df["secondary_cluster_id"].values))

for cluster in clusters:
    if len(clusters_df[clusters_df["secondary_cluster_id"]==cluster]["sample_id"].values)>1:
        with open(f"cluster_{cluster}_list.txt", "w") as f:
            for name in clusters_df[clusters_df["secondary_cluster_id"]==cluster]["sample_id"].values:
                f.write(f"fastas/addenbrookes/{name}.fna\n")

'''
count=0
for cluster in clusters:
    if len(clusters_df[clusters_df["secondary_cluster_id"]==cluster]["sample_id"].values)==1:
        count= count+1

print(count)
'''
