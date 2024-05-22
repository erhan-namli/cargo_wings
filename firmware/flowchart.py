

import networkx as nx
import pygraphviz as pgv
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt

# Flowchart için bir Graph (grafik) oluşturun
G = nx.DiGraph()

# Nodeları (düğümleri) ekleyin
G.add_node("Start")
G.add_node("Import Libraries")
G.add_node("Initialize Ground Control Interface")
G.add_node("Listen for Drone Messages")
G.add_node("Main Window Initialization")
G.add_node("Button Click Handlers")
G.add_node("Start Scanning for Drones")
G.add_node("Handle Drone Messages")
G.add_node("Start Mission")
G.add_node("Adhoc Mission")
G.add_node("Send JSON Packet")
G.add_node("Start Adhoc Mode")
G.add_node("Take Picture and Scan QR Code")
G.add_node("Connect Tello AP")
G.add_node("Connect to Home Network")

# Kapsamındaki kenarları (edges) ekleyin
edges = [
    ("Start", "Import Libraries"),
    ("Import Libraries", "Initialize Ground Control Interface"),
    ("Initialize Ground Control Interface", "Listen for Drone Messages"),
    ("Listen for Drone Messages", "Main Window Initialization"),
    ("Main Window Initialization", "Button Click Handlers"),
    ("Button Click Handlers", "Start Scanning for Drones"),
    ("Start Scanning for Drones", "Handle Drone Messages"),
    ("Handle Drone Messages", "Start Mission"),
    ("Start Mission", "Adhoc Mission"),
    ("Adhoc Mission", "Send JSON Packet"),
    ("Send JSON Packet", "Start Adhoc Mode"),
    ("Start Adhoc Mode", "Take Picture and Scan QR Code"),
    ("Take Picture and Scan QR Code", "Connect Tello AP"),
    ("Connect Tello AP", "Connect to Home Network")
]

G.add_edges_from(edges)

# Grafiği çizdirin
pos = graphviz_layout(G, prog='dot')
nx.draw(G, pos, with_labels=True, arrows=True)
plt.show()
