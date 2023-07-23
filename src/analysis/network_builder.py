from matplotlib import pyplot as plt
import pandas as pd
import networkx as nx

# Load the CSV file
df = pd.read_csv("data/processed/cash.csv")

# Define the investing company
investing_company = "Southeastern Asset Management"  # Replace with your company's name

nodes = [investing_company]
edges = []

for index, row in df.iterrows():
    invested_company = row['Name of Issuer']
    nodes.append(invested_company)

    edges.append((investing_company, invested_company))

nodes = list(set(nodes))

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
colors = ["blue" if node == "Southeastern Asset Management" or node == "Polen Capital" 
          else "grey" for node in G.nodes]

nx.draw(G, with_labels=True, node_color=colors)
plt.show()
