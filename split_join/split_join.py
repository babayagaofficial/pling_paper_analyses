import pandas as pd
import numpy as np

def read_in_clusters(mob, mge, pling, truth): #read in typing files for each tool and truth, and output clusters as dictionary where each entry's key is an integer label and the entry's value is a list of plasmids in a given cluster
    truth_clusters = pd.read_csv(truth, sep="\t")
    truth_clusters.rename(columns={"sample": "type", "plasmid": "plasmid"}, inplace=True)
    pling_df = pd.read_csv(pling, sep='\t')
    mob_df = pd.read_csv(mob, sep='\t', usecols=["secondary_cluster_id","sample_id"])
    mob_df.rename(columns={"secondary_cluster_id": "type", "sample_id": "plasmid"}, inplace=True)
    mge_df = pd.read_csv(mge, usecols=["Standard_Cluster","Sample_Name"])
    mge_df.rename(columns={"Standard_Cluster": "type", "Sample_Name": "plasmid"}, inplace=True)

    plasmids = list(pling_df["plasmid"].values)

    #singletons not uniquely labelled in cluster files for the truth and for mge-cluster
    singletons_mge = list(mge_df[mge_df["type"]=='-1']["plasmid"].values) + list(mge_df[mge_df["type"]=='-']["plasmid"].values)
    singletons_truth = list(set(plasmids)-set(truth_clusters["plasmid"]))
    #create dictionaries in above described format
    clusters_pling = {i:set(pling_df[pling_df["type"]==el]["plasmid"].values) for i,el in enumerate(list(set(pling_df["type"])))}
    clusters_mob = {i:set(mob_df[mob_df["type"]==el]["plasmid"].values) for i,el in enumerate(list(set(mob_df["type"])))}
    clusters_mge = {i:set(mge_df[mge_df["type"]==el]["plasmid"].values) for i,el in enumerate(list(set(mge_df["type"]))) if el!='-1' or '-'}
    max_mge = max(clusters_mge.keys())+1
    cluster_truth = {i:set(truth_clusters[truth_clusters["type"]==el]["plasmid"].values) for i,el in enumerate(list(set(truth_clusters["type"])))}
    max_truth = max(cluster_truth.keys())+1
    #add singletons as one element clusters to truth and mge-cluster cluster dictionaries
    clusters_mge.update({max_mge+i:{el} for i,el in enumerate(list(set(singletons_mge)))})
    cluster_truth.update({max_truth+i:{el} for i,el in enumerate(list(set(singletons_truth)))})

    return cluster_truth, clusters_pling, clusters_mge, clusters_mob, plasmids

def make_contingency_matrix(clusters_1, clusters_2, k_1, k_2): #clusters_1 and clusters_2 are dictionaries of clusters, k_1 and k_2 the lengths of the respective dictionaries
    contingency = np.zeros((k_1,k_2))
    for i in range(k_1):
        for j in range(k_2):
            contingency[i][j] = len(clusters_1[i].intersection(clusters_2[j]))
    return contingency

def split_join(clusters_1,clusters_2,n): #clusters_1 and clusters_2 are dictionaries of clusters, n is the total number of data points (plasmids)
    k_1 = len(clusters_1.keys())
    k_2 = len(clusters_2.keys())
    contingency = make_contingency_matrix(clusters_1,clusters_2, k_1, k_2)
    dist = 2*n - sum([max(contingency[i]) for i in range(k_1)]) - sum([max(contingency[:,j]) for j in range(k_2)])
    return int(dist)

pling = "../clusters/addenbrookes/pling.tsv"
mob = "../clusters/addenbrookes/MOB-suite.txt"
mge = "../clusters/addenbrookes/mge_cluster.csv"
truth = "../clusters/addenbrookes/truth_clusters.txt"

cluster_truth, clusters_pling, clusters_mge, clusters_mob, plasmids = read_in_clusters(mob, mge, pling, truth)

n = len(plasmids)
dist_pling = split_join(cluster_truth, clusters_pling, n)
dist_mge = split_join(cluster_truth, clusters_mge, n)
dist_mob = split_join(cluster_truth, clusters_mob, n)
print("pling:", dist_pling, f"{round(dist_pling/n*100)}%")
print("mge:", dist_mge, f"{round(dist_mge/n*100)}%")
print("MOB:", dist_mob, f"{round(dist_mob/n*100)}%")
