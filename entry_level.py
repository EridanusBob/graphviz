from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Graphviz2.38\bin"

dot = Digraph(comment='The Round Table', engine='dot')

dot.edge_attr = {'comment': "Wildcard edge",
                 'fontname': "sans-serif",
                 'fontsize': '10',
                 'colorscheme': "blues3",
                 'color': '2',
                 'fontcolor': '3'}
dot.node_attr = {'fontname': "serif",
                 'colorscheme': "blues4",
                 'color': "2",
                 'style': "filled",
                 'shape': "rectangle",
                 'fontsize': '13',
                 'fillcolor': "1",
                 'fontcolor': "4"}
# Add nodes and edges:
dot.node('1', "开始", {'shape': "Mdiamond"})
dot.node('start', "开始", {'shape': "Mdiamond"})
dot.node('kb_scan1', "键盘扫描", {'shape': "rectangle"})
dot.node('key_down', "有键按下？", {'shape': "diamond"})
dot.node('delay', "延时去抖")
dot.node('kb_scan2', "按键扫描")
dot.node('find_pressed_key', "找到闭合键？", {'shape': "diamond"})
dot.node('key_release', "闭合键释放？", {'shape': "diamond"})
dot.node('find_keyCodeTable', "根据扫描码查找键码表")
dot.node('mainCtrl', "发送键码到主控器")

dot.edges([("start", "kb_scan1"),
           ("kb_scan1", "key_down"),
           ("delay", "kb_scan2"),
           ("kb_scan2", "find_pressed_key"),
           ("find_keyCodeTable", "mainCtrl"),
           ("mainCtrl", "kb_scan1")])
dot.edge('key_down', 'kb_scan1', label="N")
dot.edge('key_down', 'delay', label="Y")
dot.edge('find_pressed_key', 'kb_scan1', label="N")
dot.edge('find_pressed_key', 'key_release', label="Y")
dot.edge('key_release', 'key_release', label="N")
dot.edge('key_release', 'find_keyCodeTable', label="Y")
# Check the generated source code:
print(dot.source)

# Save and render the source code, optionally view the result:
# dot.render('round-table.gv', view=True)  # doctest: +SKIP
# dot.view('round-table.gv')
