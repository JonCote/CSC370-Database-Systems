# Counts the number of steps required to decompose a relation into BCNF.

from relation import *
from functional_dependency import *

# You should implement the static function declared
# in the ImplementMe class and submit this (and only this!) file.
# You are welcome to add supporting classes and methods in this file.
class ImplementMe:

    # Returns the number of recursive steps required for BCNF decomposition
    #
    # The input is a set of relations and a set of functional dependencies.
    # The relations have *already* been decomposed.
    # This function determines how many recursive steps were required for that
    # decomposition or -1 if the relations are not a correct decomposition.


    # remake relations are what is gotten after decomposition
    # take relations and union them
    # do decomposition
    # if result is same as the set of relations return decomposition steps
    # else return -1

    @staticmethod
    def DecompositionSteps( relations, fds ):
      #  print(f'relations: {relations}\nfds: {fds}\n')

        # reconstruct relations with union
        complete_relation = build_relation(relations)
        
    #    print(complete_relation)
        
       # print('@@@@@@@@@@@@@@@@@ START @@@@@@@@@@@@@@@@@')
        fd_set = fds.functional_dependencies.copy()
        fd_set = minimal_basis_plus_trivial(fd_set)
        decomp_steps, bcnf_relations = decomposition(complete_relation, fd_set, 0)
    #    print(bcnf_relations)
        
        if not bcnf_relations:
            #print(len(relations.relations))
            #print(len(complete_relation))
            if len(relations.relations) == 1:  # this seems sketch should prob compare elements not lengths
                return 0
        elif compare_bcnf_results(relations, bcnf_relations):
            return decomp_steps

        return -1



def compare_bcnf_results(relations, bcnf_relations):
    for relation in relations.relations:
        found = False
    #    print(relation.attributes)
        for bcnf_rel in bcnf_relations:
            if bcnf_rel == relation.attributes:
                found = True
                break
        if not found:
            break
    return found    



def build_relation(relations):
    comp_rel = set()
    for relation in relations.relations:
        comp_rel.update(relation.attributes)


    return comp_rel


# ****add a breakdown of the fds into x->y where y is 1 element****
# do i even need to go to a basis?
def minimal_basis_plus_trivial(fd_set):
    # use splitting rule to clean right hand side
    fd_min_set = set()
    for fd in fd_set:
        #print(fd)
        for att_right in fd.right_hand_side:
         #   print(att_right)
            newfd = FunctionalDependency(fd.left_hand_side, {att_right})
            fd_min_set.add(newfd)
    #print(f'fd_set_min: {fd_min_set}')

    #print(f'fd_set_min: {fd_min_set}')
    # remove redundant fds
    #fd_full_reach = list()
    #fd_remove_list = list()
    for fd_base in fd_min_set:
        #print(f'fd_base: {fd_base}')
        complete_att_set = fd_base.left_hand_side.copy()
        complete_att_set.update(fd_base.right_hand_side)
        fd_set_left = fd_min_set.copy()
        change = True

        while change:
            change = False
            used_fd = list()
            for fd in fd_set_left:
                if fd != fd_base:            
                    if fd.left_hand_side.issubset(complete_att_set):
                        complete_att_set.update(fd.right_hand_side)
                        used_fd.append(fd)
                        change = True
            if used_fd:
                for ufd in used_fd:
                    fd_set_left.discard(ufd)
            
        
        #if complete_att_set in fd_full_reach:
         #   fd_remove_list.append(fd_base)
       # else:
         #   fd_full_reach.append(complete_att_set)

    #print(f'fd_full_reach: {fd_full_reach}')
    #print(f'fd_remove_list: {fd_remove_list}')

    #for rm in fd_remove_list:
    #    fd_min_set.discard(rm)

    # add trivial cases
    fd_min_set_ptriv = set()
    for fd in fd_min_set:
        for att_left in fd.left_hand_side:
            newfd = FunctionalDependency({att_left}, {att_left})
            fd_min_set_ptriv.add(newfd)
            for att_right in fd.right_hand_side:
                newfd = FunctionalDependency({att_right}, {att_right})
                fd_min_set_ptriv.add(newfd)
    fd_min_set.update(fd_min_set_ptriv)
    #print(f'fd_min_set_ptriv: {fd_min_set_ptriv}')

    # remove redundant left-hand side attributes (TODO)


   # print(f'fd_set_min: {fd_min_set}')

    return fd_min_set

# have some variance in output is happening unsure why
def decomposition(rel, fd_set, decomp_steps):
#    print(f'**********DECOMPOSITION START*************')
#    print(f'relation (decomposition): {rel}')
#    print(f'Using FD set: {fd_set}')

    # check for Violations and get R set
    r_set = bcnf_decomposition(rel, fd_set)

    treeHead = TreeNode(rel)
    tree = Tree(treeHead, r_set)

    #print(f'r_set: {r_set}')

    # build decomposition tree
    
    decomposition_helper(tree, fd_set)
    #tree_output = tree.print_tree()
   # print(tree_output)

    # extract leaves of tree for R after decomp
    bcnf_relations = get_bcnf_relations(tree)
    #print(f" bcnf_relations: { bcnf_relations}")
    
    # extract high of tree for decomp_steps
    decomp_steps = get_decomp_steps(tree)
    #print(f'decomp_steps: {decomp_steps}')

    return decomp_steps, bcnf_relations


def get_decomp_steps(tree):
    decomp_steps = tree.get_height()
    return decomp_steps


def get_bcnf_relations(tree):
    bcnf_rels = tree.get_leaves()
    bcnf_rels = list(set(frozenset(item) for item in bcnf_rels))
    bcnf_rels = list(set(item) for item in frozenset(item for item in bcnf_rels))
    return bcnf_rels


# how do i get the relations back also?
# could just use this to build the decomposition tree then take leaves for R's after decomp and high of tree for decomp steps
def decomposition_helper(tree, fd_set):
    r_set = tree.children
#    print(f'##### Helper start #####')
   # print(f'Helper r_set: {r_set}')
    
    if r_set:
        for rel in r_set:
            projected_fd_set = get_projection_fds(rel.node.value, fd_set)
      #      print(f'rel: {rel.node.value} -> Projection: {projected_fd_set}')
   #         print('&&&&& End Projection &&&&&')
            if projected_fd_set:  
                rel_set = bcnf_decomposition(rel.node.value, projected_fd_set)
                if rel_set:
                    rel.children = rel_set
                    decomposition_helper(rel, projected_fd_set)            
        return
    return



def get_projection_fds(rel, fd_set):

  #  print('&&&&& Start Projection &&&&&')
    # find what fds are needed for the closure of rel
   # print(f'relation: {rel}')
    fds = set()
    for fd in fd_set:
        complete_att_set, fds_used = build_att_set(fd_set, fd, rel)
     #   print(f'FD: {fd}')
     #   print(f'complete_att_set: {complete_att_set}')
        
    
        if complete_att_set.issubset(rel):
  #          print(f'fds_used: {fds_used}')
  #          print("----------")
            for i in fds_used:
                fds.add(i)
  #      print("----------")
    return fds

# return r_set is a list of TreeNodes
def bcnf_decomposition(relation, fd_set):
    # get fd
  #  print(f'**********BCNF START*************')
    r_set = list()
    for fd_base in fd_set:
    #    print(f'fd_base: {fd_base}')
        complete_att_set, fds_used = build_att_set(fd_set, fd_base, relation)
        
     #   print(f'complete_att_set: {complete_att_set}')
        
        # if complete_att_set is not equal to relation then BCNF violation
        if complete_att_set != relation and fd_base.left_hand_side != fd_base.right_hand_side:
      #      print("&& BCNF VIOLATION &&")

            # do decomposition

            # calculate R1 and R2
            #r1 = fd_base.left_hand_side.copy()
            #r1.update(fd_base.right_hand_side)
            r1 = complete_att_set.copy()
            r2 = relation.copy()
            r2.difference_update(r1)
            r2.update(fd_base.left_hand_side)

            r1Node = TreeNode(r1)
            r1Tree = Tree(r1Node, None)
            r2Node = TreeNode(r2)
            r2Tree = Tree(r2Node, None)
            r_set.append(r1Tree)
            r_set.append(r2Tree)

    #        print(f"r1 : {r1}")
    #        print(f"r2 : {r2}")
   # print(f'**********BCNF END*************')
    return r_set
    


def build_att_set(fd_set, fd_base, relation):
    fds_used = {fd_base}
    complete_att_set = fd_base.left_hand_side.copy()
    complete_att_set.update(fd_base.right_hand_side)

    fd_set_left = fd_set.copy()
    change = True

    while change:   # added changes here need to make sure it works still
        change = False
        used_fd = list()

        for fd in fd_set_left:
            if fd != fd_base:
                # check if we can reach the left hand side
                #print(f'fd.left_hand_side: {fd.left_hand_side}')
               # print(f'fd: {fd}')
                
                if fd.left_hand_side.issubset(complete_att_set):
                    # add right hand side to complete_att_set
                    if fd.right_hand_side.issubset(relation):
                        #print('here')
                        complete_att_set.update(fd.right_hand_side)
                        fds_used.add(fd)
                        used_fd.append(fd)
                        change = True
        if used_fd:
            for ufd in used_fd:
                fd_set_left.discard(ufd)

    return complete_att_set, fds_used


class TreeNode:
    def __init__(self, value):
        self.value = value

class Tree:
    def __init__(self, node, children):
        self.node = node
        self.children = children
    
    def print_tree(self):
        #print(f'node: {self.node.value}')
        child_value_list = list()
        child_value_list.append(self.node.value)
        if self.children:
            for child in self.children:
                if child.children:
                    child_value_list.append(child.print_tree())
                else:
                    child_value_list.append(child.node.value)
        return child_value_list
    
    def get_leaves(self):
        leaves = list()
        if self.children:
            for child in self.children:
                if child.children:
                    child_leaves = child.get_leaves()
                    for l in child_leaves:
                        leaves.append(l)
                else:
                    leaves.append(child.node.value)
        return leaves
    
    def get_height(self):
        height = 0
        if self.children:
            for child in self.children:
                if child.children:
                    height = max(height, child.get_height())
        return height + 1
                    




    






# expected_output 0
def testcase1():
    relations = RelationSet({Relation({'a','b','c'})})
    fds = FDSet({FunctionalDependency({'a'}, {'b','c'})})
    return ImplementMe.DecompositionSteps( relations, fds )

# expected_output -1
def testcase2():
    relations = RelationSet({Relation({'a','b','c'})})
    fds = FDSet({FunctionalDependency({'a'}, {'b'})})
    return ImplementMe.DecompositionSteps( relations, fds )

# expected_output 0
def testcase3():
    relations = RelationSet({Relation({'a','b','c'})})
    fds = FDSet({FunctionalDependency({'a'}, {'b'}), \
            FunctionalDependency({'a'}, {'c'})})
    return ImplementMe.DecompositionSteps( relations, fds )

# expected_output -1  (why is it -1 not 1? tests.py says it misses the violation on second FD but mine does not miss it)
def testcase4():
    relations = RelationSet({Relation({'a','b','c'})})
    fds = FDSet({FunctionalDependency({'a'}, {'b'}), \
            FunctionalDependency({'b'}, {'c'})})
    return ImplementMe.DecompositionSteps( relations, fds )

# expected_output -1
def testcase5():
    relations = RelationSet({Relation({'a','b','c','d','e'})})
    fds = FDSet({FunctionalDependency({'a'}, {'b'}), \
            FunctionalDependency({'b'}, {'c'}), \
            FunctionalDependency({'c'}, {'d'}), \
            FunctionalDependency({'d'}, {'a'}) })
    return ImplementMe.DecompositionSteps( relations, fds )

# expected_output -1
def testcase6():
    relations = RelationSet({Relation({'a','b'}), \
                Relation({'c','d'}) })
    fds = FDSet({FunctionalDependency({'a'}, {'b'}) })
    return ImplementMe.DecompositionSteps( relations, fds )

# expected_output 0
def testcase7():
    relations = RelationSet({Relation({'a','b','c'}) })
    fds = FDSet({FunctionalDependency({'a'}, {'b','c'}), \
            FunctionalDependency({'b'}, {'a'}) })
    return ImplementMe.DecompositionSteps( relations, fds )

# expected_output -1
def testcase8():
    relations = RelationSet({Relation({'a','b'}), \
            Relation({'c','d'}) })
    fds = FDSet({FunctionalDependency({'a'}, {'b'}) })
    return ImplementMe.DecompositionSteps( relations, fds )

# expected_output -1
def testcase9():
    relations = RelationSet({Relation({'a','b'}), \
            Relation({'b','d'}), \
            Relation({'c','d'}) })
    fds = FDSet({FunctionalDependency({'b'}, {'a'}), \
            FunctionalDependency({'c'}, {'d'}) })
    return ImplementMe.DecompositionSteps( relations, fds )

# expected_output 1  (Cant get the 'e' so end up with -1 since BCNF WTF??? ERROR in testcase???)
def testcase10():
    relations = RelationSet({Relation({'a','b','c','d'}), \
                Relation({'a','b','e'}) })
    fds = FDSet({FunctionalDependency({'b', 'a'}, {'c'}), \
            FunctionalDependency({'a','b'}, {'d'}) })
    return ImplementMe.DecompositionSteps( relations, fds )

# expected_output 2
def testcase11():
    relations = RelationSet({Relation({'b','c'}), \
            Relation({'c','a'}) , \
            Relation({'a','d'}) })
    fds = FDSet({FunctionalDependency({'b'}, {'a','c'}), \
            FunctionalDependency({'a'}, {'d'}), \
            FunctionalDependency({'c'}, {'a'}) })
    return ImplementMe.DecompositionSteps( relations, fds )

# expected_output -1
def testcase12():
    relations = RelationSet({Relation({'a','b','c','e'}), \
                Relation({'b','a','d'}) })
    fds = FDSet({FunctionalDependency({'b', 'a'}, {'e','c'}), \
            FunctionalDependency({'a','b'}, {'d'}) })
    return ImplementMe.DecompositionSteps( relations, fds )

# expected_output 2
def testcase13():
    relations = RelationSet({Relation({'a','b'}), \
                Relation({'a','c'}), \
                Relation({'b','d'}) })
    fds = FDSet({FunctionalDependency({'b'}, {'d'}), \
            FunctionalDependency({'a'}, {'c'}) })
    return ImplementMe.DecompositionSteps( relations, fds )

# expected_output 2
def testcase17():
    relations = RelationSet({Relation({'a','b','c'}), \
                Relation({'b','d'}), \
                Relation({'e','d'}) })
    fds = FDSet({FunctionalDependency({'a'}, {'b'}), \
            FunctionalDependency({'b'}, {'c'}), \
            FunctionalDependency({'c'}, {'a'}), \
            FunctionalDependency({'d'}, {'e'}) })
    return ImplementMe.DecompositionSteps( relations, fds )


# expected output 2
# R1(e, f), R2(c, d, e), R3(a, b, c, d)
# {a b} -> {e}
# {c d} -> {e}
# {e} -> {f}
def testcase21():
    relations = RelationSet({Relation({'e','f'}), \
                    Relation({'d','c','e'}), \
                    Relation({'a','b','c','d'}) })
    fds = FDSet({FunctionalDependency({'a','b'}, {'e'}), \
                    FunctionalDependency({'c','d'}, {'e'}), \
                    FunctionalDependency({'e'}, {'f'}) })
    return ImplementMe.DecompositionSteps( relations, fds )


#steps = testcase13()
#print(steps)