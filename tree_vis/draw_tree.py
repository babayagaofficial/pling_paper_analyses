from ete3 import Tree, TreeStyle, NodeStyle, TextFace, faces, AttrFace, CircleFace
import numpy as np
import argparse
import pandas as pd

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("species", choices=["ecoli", "kleb"], help="Select whether to generate E. coli or Klebsiella pneumoniae tree visualisation.")
args = parser.parse_args()

chr_to_community = {}
subcommunities = "../clusters/addenbrookes/pling.tsv"

subcommunities_df = pd.read_csv(subcommunities, sep='\t')
subcommunities_list = list(subcommunities_df['type'])
count = [subcommunity for subcommunity in set(subcommunities_list) if subcommunities_list.count(subcommunity)>0]

plasmids = list(subcommunities_df["plasmid"])
chrs = set([plasmid.split("_")[0] for plasmid in plasmids])

with open(subcommunities) as f:
    next(f)
    for line in f:
        blub = line.strip().split("\t")
        chr = blub[0].split("_")[0]
        subcommunity = blub[1]
        if subcommunity in count:
            if chr in chr_to_community.keys():
                chr_to_community[chr].append(subcommunity)
            else:
                chr_to_community[chr] = [subcommunity]

species=args.species
filepath = f"{species}_cpe.tree"

t = Tree(filepath, format=0, quoted_node_names=True)

present_communities=[]
for n in t.traverse():
    if n.is_leaf():
        try:
            communities=chr_to_community[n.name]
        except:
            communities=[]
        for community in communities:
            present_communities.append(community)

present_communities=list(set(present_communities))

cross_communities = ["community_4_subcommunity_2", "community_1_subcommunity_17", "community_5_subcommunity_0", "community_12_subcommunity_0", "community_5_subcommunity_2", "community_1_subcommunity_21", "community_13_subcommunity_0"]

colour_codes=[[230,159,0], [0,0,0], [0,158,115], [240,228,66], [0,114,178], [213,94,0], [204,121,167]]

colours={}
for i in range(len(colour_codes)):
    hexcode = [hex(colour_codes[i][j]).replace('0x','') for j in range(3)]
    for k in range(len(hexcode)):
        if len(hexcode[k]) == 1:
            hexcode[k] = hexcode[k]+'0'
    colours[cross_communities[i]] = '#'+hexcode[0]+hexcode[1]+hexcode[2]

def layout(n):
    present_communities=set()
    if n.is_leaf():
        try:
            communities=chr_to_community[n.name]
        except:
            communities=[]
        for community in communities:
            try:
                plasmid = CircleFace(radius=20, color=colours[community], style="circle")
                faces.add_face_to_node(plasmid, n, 1)
            except:
                pass
        name_face = AttrFace("name", fsize=20)
        faces.add_face_to_node(name_face, n, column=0, position="branch-right")
        nstyle = NodeStyle()
        nstyle['shape'] = 'circle'
        nstyle['size'] = 0
        nstyle['fgcolor'] = 'black'
        nstyle['hz_line_width'] = 7
        nstyle['vt_line_width'] = 7
        n.set_style(nstyle)

    else:
        nstyle=NodeStyle()
        nstyle['size']=0
        nstyle['hz_line_width'] = 7
        nstyle['vt_line_width'] = 7
        n.set_style(nstyle)

ts = TreeStyle()
ts.layout_fn = layout

ts.show_leaf_name = False
ts.scale = 2500
ts.branch_vertical_margin = 10


for host in sorted(colours.keys()):
	ts.legend.add_face(CircleFace(10, colours[host]), column=0)
	ts.legend.add_face(TextFace(f" {host}", fsize=22), column=1)

t.render(f'{species}.jpeg', tree_style=ts)
