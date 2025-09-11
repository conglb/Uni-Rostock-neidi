import networkx as nx

# Đọc file GraphML
G = nx.read_graphml("results/high-level-petrinet/Retrieval.graphml")

# In thông tin tổng quan
#print(nx.info(G))
print(G)

# In danh sách nodes với thuộc tính
print("\n--- Nodes ---")
for node, data in G.nodes(data=True):
    print(f"{node}: {data}")

# In danh sách edges với thuộc tính
print("\n--- Edges ---")
for src, tgt, data in G.edges(data=True):
    print(f"{src} -> {tgt} {data}")