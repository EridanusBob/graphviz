from graphviz import Digraph

grap_g = Digraph("G", format="pdf")

sub_g0 = Digraph(name='cluster0', comment="process0", graph_attr={"style": 'filled', "color": 'lightgrey'},
                 node_attr={"style": "filled", "color": "white"})
sub_g0.node("a0", "a0")
sub_g0.node("a1", "a1")
sub_g0.node("a2", "a2")
sub_g0.node("a3", "a3")
sub_g0.edges([("a0", "a1"), ("a1", "a2"), ("a2", "a3")])

sub_g1 = Digraph(name='cluster1', comment="process1", graph_attr={"color": 'blue'},
                 node_attr={"style": "filled"})
sub_g1.node("b0", "b0")
sub_g1.node("b1", "b1")
sub_g1.node("b2", "b2")
sub_g1.node("b3", "b3")
sub_g1.edges([("b0", "b1"), ("b1", "b2"), ("b2", "b3")])

grap_g.node("start", label="start", shape="Mdiamond")
grap_g.node("end", label="end", shape="Msquare")

grap_g.subgraph(sub_g0)
grap_g.subgraph(sub_g1)
grap_g.edge("start", "a0")
grap_g.edge("start", "b0")

grap_g.edge("a1", "b3")
grap_g.edge("b2", "a3")

grap_g.edge("a3", "end")
grap_g.edge("b3", "end")
print(grap_g.source)
