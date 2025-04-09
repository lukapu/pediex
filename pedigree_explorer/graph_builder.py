import networkx as nx

def build_graph(people):
    G = nx.DiGraph()
    for pid, data in people.items():
        G.add_node(pid)
        if data["father"]:
            G.add_edge(pid, data["father"])
        if data["mother"]:
            G.add_edge(pid, data["mother"])
    return G
