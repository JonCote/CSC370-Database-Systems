# Entity-Relationship Diagram (ERD) Definition

import networkx as nx
import matplotlib.pyplot as plt
from functools import reduce
import math

# An Entity-Relationship Diagram as a type of networkx graph
#
# The vertex set includes all entity sets, relationships,
# attributes, and collections of entity sets
# The edge set connects entity sets to relationships, attributes,
# and/or collections of other entity sets. It also may connect
# attributes to relationships (i.e., the graph has a min colouring of 3)
#
# The class also contains a mapping from every entity set to one identifier.
# These are not drawn by the plotting library due to the complexity of support
# for weak entity sets.
import networkx as nx
import matplotlib.pyplot as plt
from functools import reduce
import math

# An Entity-Relationship Diagram as a type of networkx graph
#
# The vertex set includes all entity sets, relationships,
# attributes, and collections of entity sets
# The edge set connects entity sets to relationships, attributes,
# and/or collections of other entity sets. It also may connect
# attributes to relationships (i.e., the graph has a min colouring of 3)
#
# The class also contains a mapping from every entity set to one identifier.
# These are not drawn by the plotting library due to the complexity of support
# for weak entity sets.
class ERD:
    def __init__(self):
        self.graph = nx.Graph()
        self.identifiers = {}
    def add_entity_set(self, es):
        self.graph.add_node(es, s='s')
    def add_relationship(self, rel):
        self.graph.add_node(rel, s='d')
    def add_attribute(self, att):
        self.graph.add_node(att, s='o')
    def add_identifier(self, es, attributes):
        self.identifiers[es] = attributes
    def add_generalisation(self, generalisation, specialisations, style):
        self.add_entity_set(generalisation)
        isA = reduce(lambda x, y: x + " " + y, specialisations) + " "
        self.graph.add_node(isA, s='^')
        self.graph.add_edges_from([(generalisation, isA, {"style":style})])
        self.graph.add_edges_from([(specialisation, isA) for specialisation in specialisations])
    def connect(self, es, rel, min_card, max_card):
        self.graph.add_edges_from([(es, rel, {"min": min_card, "max" : max_card})])
    def attach(self, att, es):
        self.graph.add_edge(att, es)
    def draw(self):
        # TODO: Draw edge and vertex labels
        # From https://stackoverflow.com/a/31195070/2769271
        nodePos = nx.layout.spring_layout(self.graph)
        nodeShapes = set((aShape[1]["s"] for aShape in self.graph.nodes(data = True)))
        for aShape in nodeShapes:
             nx.draw_networkx_nodes(self.graph,nodePos,node_shape = aShape, \
                nodelist = [sNode[0] for sNode in filter(lambda x: x[1]["s"]==aShape,self.graph.nodes(data = True))])
        nx.draw_networkx_edges(self.graph,nodePos)
        plt.show()

def test(): 
    erd = ERD()
    erd.add_entity_set("A")
    erd.add_attribute("a")
    erd.add_entity_set("B")
    erd.add_attribute("b")
    erd.add_relationship("R")
    erd.connect("A", "R", 0, 1)
    erd.connect("B", "R", 1, 100)
    erd.attach('a', "A")
    erd.attach('b', "B")
    erd.add_generalisation("C", ["A","B"], "(t,e)")
    #erd.draw()
    return erd

def test6():
    erd = ERD()
    erd.add_entity_set("A")
    erd.add_entity_set("B")
    erd.add_entity_set("C")
    erd.add_attribute("a1")
    erd.add_attribute("a2")
    erd.add_attribute("b")
    erd.add_attribute("c")
    erd.add_relationship("R1")
    erd.add_relationship("R2")
    erd.connect("A", "R1", 1, 1)
    erd.connect("B", "R1", 1, math.inf)
    erd.connect("A", "R2", 0, 1)
    erd.connect("C", "R2", 0, math.inf)
    erd.attach('a1', "A")
    erd.attach('a2', "A")
    erd.attach('b', "B")
    erd.attach('c', "C")
    erd.add_identifier('A', ['a1','b'])
    erd.add_identifier('B', ['b'])
    erd.add_identifier('C', ['c'])
   # erd.draw()
    return erd

def test7():
    erd = ERD()
    erd.add_entity_set("A")
    erd.add_entity_set("C")
    erd.add_attribute("a")
    erd.add_attribute("b")
    erd.add_attribute("c")
    erd.add_generalisation("B", ["C"], "(p,e)")
    erd.attach('c', "C")
    erd.attach('b', "B")
    erd.attach('a', "A")

    erd.add_identifier("A", ["a"])
    erd.add_identifier("B", ["b"])

    erd.add_relationship("R")
    erd.connect("A", "R", 1, 1)
    erd.connect("B", "R", 1, 1)

    #erd.draw()
    return erd

def test9():
    erd = ERD()
    erd.add_entity_set("A")
    erd.add_entity_set("B")
    erd.add_entity_set("D")
    erd.add_attribute("d")
    erd.add_attribute("c")
    erd.add_generalisation("C", ["A","B"], "(t,e)")
    erd.attach('c', "C")
    erd.attach('d', "D")

    erd.add_identifier("C", ["c"])
    erd.add_identifier("D", ["d"])

    erd.add_relationship("R1")
    erd.add_relationship("R2")
    erd.connect("A", "R1", 1, 1)
    erd.connect("B", "R2", 0, 1)
    erd.connect("D", "R1", 1, math.inf)
    erd.connect("D", "R2", 1, math.inf)

    #erd.draw()
    return erd

def testA():   # (1, n)
    erd = ERD()
    erd.add_entity_set("B")
    erd.add_attribute("b1")
    erd.add_attribute("b2")
    erd.attach('b1', "B")
    erd.attach('b2', "B")
    return erd

def testB():   # (1, 1)
    erd = ERD()
    erd.add_entity_set("B")
    erd.add_attribute("b1")
    erd.add_attribute("b2")
    erd.attach('b1', "B")
    erd.attach('b2', "B")
    erd.add_identifier("B", ['b1', 'b2'])
    return erd

def testC():   # (1, n)
    erd = ERD()
    erd.add_entity_set("B")
    erd.add_attribute("b1")
    erd.add_attribute("b2")
    erd.attach('b1', "B")
    erd.attach('b2', "B")
    erd.add_identifier("B", ['b2'])
    return erd

def testD():   # (1, 1)
    erd = ERD()
    erd.add_entity_set("B")
    erd.add_attribute("b1")
    erd.add_attribute("b2")
    erd.attach('b1', "B")
    erd.attach('b2', "B")
    erd.add_identifier("B", ['b1'])
    return erd

def testE():   # (1, 1)
    erd = ERD()
    erd.add_entity_set("B")
    erd.add_attribute("b1")
    erd.add_attribute("b2")
    erd.attach('b1', "B")
    erd.attach('b2', "B")
    erd.add_identifier("B", ['b1'])
    erd.draw()
    return erd

def test15():   # (1, 1)
    erd = ERD()
    erd.add_entity_set("A")
    erd.add_attribute("a")
    erd.add_attribute("b")
    erd.add_attribute("c")
    erd.attach('a', "A")
    erd.attach('b', "A")
    erd.add_identifier("A", ['a', 'b', 'c'])
    #erd.draw()
    return erd

def test15A():   # (1, 1) 
    erd = ERD()
    erd.add_entity_set("A")
    erd.add_entity_set("B")
    erd.add_attribute("a")
    erd.add_attribute("a1")
    erd.add_attribute("b")
    erd.add_attribute("c")

    erd.attach('a', "A")
    erd.attach('a1', "A")
    erd.attach('b', "B")
    erd.add_identifier("B", ['b'])
    erd.add_identifier("A", ['a', 'a1', 'c'])

    erd.add_relationship("R1")
    erd.connect("A", "R1", 1, 1)
    erd.connect("B", "R1", 1, 1)
    #erd.draw()
    return erd

def test15B():  # (0, n)
    erd = ERD()
    erd.add_entity_set("A")
    erd.add_entity_set("B")
    erd.add_entity_set("C")
    erd.add_attribute("a")
    erd.add_attribute("b")
    erd.add_attribute("c")
    erd.add_attribute("d")

    erd.attach('a', "A")
    erd.attach('b', "B")
    erd.attach('c', "C")
    erd.add_identifier("B", ['b'])
    erd.add_identifier("C", ['c'])
    erd.add_identifier("A", ['a', 'b', 'd'])

    erd.add_relationship("R1")
    erd.connect("C", "R1", 0, math.inf)
    erd.connect("A", "R1", 1, 1)
    erd.add_relationship("R2")
    erd.connect("C", "R2", 1, 1)
    erd.connect("B", "R2", 1, 1)
    #erd.draw()
    return erd

def test15C():  # (0, n)
    erd = ERD()
    erd.add_entity_set("A")
    erd.add_entity_set("B")
    erd.add_entity_set("C")
    erd.add_attribute("a")
    erd.add_attribute("b")
    erd.add_attribute("c")
    erd.add_attribute("d")

    erd.attach('a', "A")
    erd.attach('b', "B")
    erd.attach('c', "C")
    erd.add_identifier("A", ['a', 'b', 'd'])
    erd.add_identifier("B", ['b'])
    erd.add_identifier("C", ['c'])

    erd.add_relationship("R1")
    erd.connect("C", "R1", 0, math.inf)
    erd.connect("A", "R1", 1, 1)
    erd.add_relationship("R2")
    erd.connect("A", "R2", 1, 1)
    erd.connect("B", "R2", 1, 1)
    #erd.draw()
    return erd

def test15D():  # (20, 200) c->b
    erd = ERD()
    erd.add_entity_set("A")
    erd.add_entity_set("B")
    erd.add_entity_set("C")
    erd.add_attribute("a")
    erd.add_attribute("b")
    erd.add_attribute("c")
    erd.add_attribute("d")

    erd.attach('a', "A")
    erd.attach('b', "B")
    erd.attach('c', "C")
    erd.add_identifier("A", ['a', 'b', 'd'])
    erd.add_identifier("B", ['b'])
    erd.add_identifier("C", ['c'])

    erd.add_relationship("R1")
    erd.connect("C", "R1", 2, 4)
    erd.connect("A", "R1", 1, 1)
    erd.add_relationship("R2")
    erd.connect("A", "R2", 10, 50)
    erd.connect("B", "R2", 1, 1)
    #erd.draw()
    return erd

def test10():
    erd = ERD()
    erd.add_entity_set("B")
    erd.add_entity_set("E")
    erd.add_entity_set("F")
    erd.add_entity_set("H")

    erd.add_attribute("a")
    erd.add_attribute("b")
    erd.add_attribute("e")
    erd.add_attribute("f")
    erd.add_attribute("g1")
    erd.add_attribute("g2")
    erd.add_attribute("h")

    erd.add_generalisation("C", ["E"], "(p,e)")
    erd.add_generalisation("D", ["F"], "(p,e)")
    erd.add_generalisation("G", ["H"], "(p,e)")
    erd.add_generalisation("A", ["B", "C", "D"], "(p,o)")

    erd.attach('a', "A")
    erd.attach('b', "B")
    erd.attach('e', "E")
    erd.attach('f', "F")
    erd.attach('g1', "G")
    erd.attach('g2', "G")
    erd.attach('h', "H")

    erd.add_identifier("G", ["g1"])
    erd.add_identifier("G", ["g2"])
    erd.add_identifier("A", ["a", "g1"])
    erd.add_identifier("F", ["f"])


    erd.add_relationship("R1")
    erd.add_relationship("R2")
    erd.connect("A", "R1", 1, 1)
    erd.connect("G", "R1", 0, math.inf)
    erd.connect("F", "R2", 1, 1)
    erd.connect("H", "R2", 0, math.inf)
    #erd.draw()
    return erd

def test11():
    erd = ERD()
    erd.add_entity_set("A")
    erd.add_entity_set("B")
    erd.add_entity_set("C")
    erd.add_entity_set("D")

    erd.add_attribute("a")
    erd.add_attribute("b")
    erd.add_attribute("c")
    erd.add_attribute("d")

    erd.add_relationship("R1")
    erd.add_relationship("R2")
    erd.add_relationship("R3")
    erd.add_relationship("R4")

    erd.connect("A", "R1", 1, 2)
    erd.connect("B", "R1", 1, math.inf)
    erd.connect("C", "R2", 0, 1)
    erd.connect("B", "R2", 3, 4)
    erd.connect("A", "R3", 1, 3)
    erd.connect("D", "R3", 1, 1)
    erd.connect("C", "R4", 1, 1)
    erd.connect("D", "R4", 2, 5)

    erd.attach('a', "A")
    erd.attach('b', "B")
    erd.attach('c', "C")
    erd.attach('d', "D")

    erd.add_identifier('A', ['a'])
    erd.add_identifier('B', ['b'])
    erd.add_identifier('C', ['c'])
    erd.add_identifier('D', ['d'])

    erd.draw()
    return erd

def test19():
    erd = ERD()
    erd.add_entity_set("B")
    erd.add_entity_set("C")
    erd.add_entity_set("E")
    erd.add_entity_set("F")
    erd.add_entity_set("G")

    erd.add_attribute("b")
    erd.add_attribute("a")
    erd.add_attribute("g")

    erd.add_generalisation("D", ["E","F"], "(t,e)")
    erd.add_generalisation("A", ["C","D"], "(t,o)")

    erd.attach('a', "A")
    erd.attach('b', "B")
    erd.attach('g', "G")

    erd.add_identifier("A", ["a"])
    erd.add_identifier("B", ["b"])
    erd.add_identifier("G", ["g"])

    erd.add_relationship("R1")
    erd.add_relationship("R2")
    erd.add_relationship("R3")

    erd.connect("A", "R1", 0, math.inf)
    erd.connect("B", "R1", 1, 2)
    erd.connect("E", "R2", 1, 1)
    erd.connect("G", "R2", 0, math.inf)
    erd.connect("F", "R3", 1, 2)
    erd.connect("G", "R3", 1, 1)
    #erd.draw()
    return erd
# test()
