from graphviz import Digraph

grap_g = Digraph("G", format="pdf")

sub_g0 = Digraph(name='cluster0', comment="process0", graph_attr={"style": 'filled', "color": 'lightgrey'},
                 node_attr={"style": "filled", "color": "white"})

nodes = [("a0", "a0"), ("a1", "a1"), ("a2", "a2"), ("a3", "a3")]
for node in nodes:
    sub_g0.node(node[0], label=node[1])
sub_g0.edges([("a0", "a1"), ("a1", "a2"), ("a2", "a3"), ("a3", "a0")])

sub_g1 = Digraph(name='cluster1', comment="process1", graph_attr={"color": 'blue'},
                 node_attr={"style": "filled"})
nodes = [("b0", "b0"), ("b1", "b1"), ("b2", "b2"), ("b3", "b3")]
for node in nodes:
    sub_g1.node(node[0], label=node[1])
sub_g1.edges([("b0", "b1"), ("b1", "b2"), ("b2", "b3")])

grap_g.subgraph(sub_g0)
grap_g.subgraph(sub_g1)

grap_g.node("start", label="start", shape="Mdiamond")
grap_g.node("end", label="end", shape="Msquare")
grap_g.edges([("start", "a0"), ("start", "b0"), ("a1", "b3"),
              ("b2", "a3"), ("a3", "end"), ("b3", "end")])

print(grap_g.source)
