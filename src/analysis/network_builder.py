from matplotlib import pyplot as plt
import pandas as pd
import networkx as nx

# Load the CSV file
df = pd.read_csv("data/processed/SoutheastenAssetManagement/cash.csv")
df2 = pd.read_csv("data/processed/PolenCapitalManagement/cashagainhardcoded.csv")
df3 = pd.read_csv("data/processed/FiduciaryManagementInc/cashagainagainhardcoded.csv")

# Define the investing companies
investing_company = "Southeastern Asset Management"
new_investing_company = "Polen Capital Management"
newer_investing_company = "Fiduciary Management Incorporated"

# Create the graph
G = nx.Graph()

# Add investing companies as nodes
G.add_node(investing_company)
G.add_node(new_investing_company)
G.add_node(newer_investing_company)

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

# Iterate over each row in the third dataframe
for index, row in df3.iterrows():
    newer_invested_company = row['Name of Issuer'].lower()  # normalize the company name
    if newer_invested_company not in G.nodes:  # only add the node if it's not already in the graph
        G.add_node(newer_invested_company)
    G.add_edge(newer_investing_company, newer_invested_company)
    investments_dict[newer_invested_company] = investments_dict.get(newer_invested_company, [])
    investments_dict[newer_invested_company].append(newer_investing_company)

# Create a list of node colors
colors = []
for node in G.nodes:
    if node in [investing_company, new_investing_company, newer_investing_company]: 
        colors.append("blue")
    else:
        # count the number of investing companies connected to the node
        investing_companies_connected = sum(neighbor in [investing_company, new_investing_company, newer_investing_company] 
                                            for neighbor in G.neighbors(node))
        if investing_companies_connected == 1:
            colors.append("grey")
        elif investing_companies_connected == 2:
            colors.append("pink")
        else:  # investing_companies_connected > 2
            colors.append("red")

# Draw the graph
nx.draw(G, with_labels=True, node_color=colors, font_size=7)
plt.show()

