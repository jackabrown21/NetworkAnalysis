from matplotlib import pyplot as plt
import pandas as pd
import networkx as nx

# Load the CSV file
df = pd.read_csv("data/processed/SoutheastenAssetManagement/cash.csv")
df2 = pd.read_csv("data/processed/PolenCapitalManagement/cashagain.csv")

# Define the investing companies
investing_company = "Southeastern Asset Management"
new_investing_company = "Polen Capital Management"

# Create the graph
G = nx.Graph()

# Add investing companies as nodes
G.add_node(investing_company)
G.add_node(new_investing_company)

# Create a dictionary to hold the invested companies and the investing companies
investments_dict = {}

# Iterate over each row in the first dataframe
for index, row in df.iterrows():
    invested_company = row['Name of Issuer'].lower()  # normalize the company name
    if invested_company not in G.nodes:  # only add the node if it's not already in the graph
        G.add_node(invested_company)
    G.add_edge(investing_company, invested_company)
    investments_dict[invested_company] = investments_dict.get(invested_company, [])
    investments_dict[invested_company].append(investing_company)

# Iterate over each row in the second dataframe
for index, row in df2.iterrows():
    new_invested_company = row['Name of Issuer'].lower()  # normalize the company name
    if new_invested_company not in G.nodes:  # only add the node if it's not already in the graph
        G.add_node(new_invested_company)
    G.add_edge(new_investing_company, new_invested_company)
    investments_dict[new_invested_company] = investments_dict.get(new_invested_company, [])
    investments_dict[new_invested_company].append(new_investing_company)

# Connect investing companies through common investments
for invested_company, investing_companies in investments_dict.items():
    if len(investing_companies) > 1:  # if the company is a common investment
        for i in range(len(investing_companies) - 1):
            for j in range(i + 1, len(investing_companies)):
                G.add_edge(investing_companies[i], investing_companies[j])

# Create a list of node colors
colors = ["blue" if node in [investing_company, new_investing_company] 
          else "red" if G.degree(node) > 1
          else "grey" for node in G.nodes]

# Draw the graph
nx.draw(G, with_labels=True, node_color=colors, font_size=7)
plt.show()

