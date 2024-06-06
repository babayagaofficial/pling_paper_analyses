import pandas as pd


clusters_df = pd.read_csv("/home/daria/Documents/projects/addenbrookes/contain_70/dcj_thresh_4_graph/objects/typing.tsv", sep="\t")

clusters = list(set(clusters_df["type"].values))
#clusters.remove("community_0_subcommunity_21")

#cluster = "community_0_subcommunity_21"
for cluster in clusters:
    if len(clusters_df[clusters_df["type"]==cluster])>1:
        with open(f"{cluster}.txt", "w") as f:
            for name in clusters_df[clusters_df["type"]==cluster]["plasmid"].values:
                f.write(f"fastas/addenbrookes/{name}.fna\n")
