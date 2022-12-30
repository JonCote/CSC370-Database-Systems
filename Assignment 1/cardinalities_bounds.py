# Jonathan Cote A1 oct 7th

from erd import *
import networkx as nx
import sys

# This function calculates a range for combinations of two sets of attributes
# in an entity-relationship diagram (ERD).
# 
# Considering the cardinality constraints imposed by the ERD, this
# function determines how many different values from the set source_attributes
# can combine with values from destination_attributes.
# For example, if entity set A and entity set B are connected
# via a one-to-many relationship, R, with non-optional participation, then
# this function would return:
#   * (1,n) if source contained all attributes of B & dest, all of A
#   * (1,1) if source contained all attributes of A & dest, all of B
#
# @TODO: Implement me!
def calculate_bounds( erd, source_attributes, destination_attributes ):
    bounds = (0,0)
    #potential_paths = list()
    #all_paths = list()
    #paths = None
    path_bounds = list()


    # Get all potential simple paths (NOTE unsure if path givin will violate generlization ie child->gen->child)
    for source_att in source_attributes:
        all_paths, potential_paths = get_simple_paths(erd.graph, source_att, destination_attributes[0])

        #print(potential_paths)
        #print(all_paths)

        if potential_paths:
            # paths are empty if composite identifier
            # break paths into commonalities and divergences
            paths = seperate_comm_path(potential_paths)
            #print(paths)

        
            # build edge and weight list for each path
            card_dict, neighbor_dict = get_card_neighbor_dict(erd.graph, paths)
            #print(card_dict)
            #print(neighbor_dict)

            # alter card for identifiers
            card_dict = alter_card_for_attributes(erd, card_dict, neighbor_dict)

            # clean up cards for generlizations (remove child to parent card)
            card_dict = clean_cards(erd.graph, card_dict)

           # print(f'Cardinalities: {card_dict}')
           # print(f'Paths: {paths}')
            
            # get cardinalities for paths
            path_cards, exclusive_path, variable_path = get_path_cards(paths, destination_attributes[0], card_dict, source_att, erd)
            #print(f'Path cards: {path_cards}')
            
            #print(f'Excl_path: {exclusive_path}')
            # calculate total card for each path
            path_bounds.append(calc_tot_card(path_cards, exclusive_path, paths, variable_path))


            # the destination is a composite identifier thus can not be reached directly
        else:
            # if destination is a composite attribute find card to each component
            #   total card to the composite attribute = (lowest of source=>dest(intersect), highest of source=>dest(intersect))

            # get the set of attributes that are linked to the composite attribute
          #  print(erd.identifiers)'
            dest_atts = list()
            for ent in erd.identifiers:
                if len(erd.identifiers[ent]) > 1:
                    for att in erd.identifiers[ent]:
                        if att != destination_attributes[0]:
                            #print(att) # set of attributes linked to compound identity
                            dest_atts.append(att)
            
           # print(dest_atts)
            att_path_bounds = list()
            for dest_att in dest_atts:
               # print(f'{source_att}: {dest_att}')
                
                if dest_att != source_att:
                    all_paths, potential_paths = get_simple_paths(erd.graph, source_att, dest_att)

                   # print(potential_paths)
                    if potential_paths:

                        paths = seperate_comm_path(potential_paths)
                        #print(paths)

                    
                        # build edge and weight list for each path
                        card_dict, neighbor_dict = get_card_neighbor_dict(erd.graph, paths)
                        #print(card_dict)
                        #print(neighbor_dict)

                        # alter card for identifiers
                        card_dict = alter_card_for_attributes(erd, card_dict, neighbor_dict)

                        # clean up cards for generlizations (remove child to parent card)
                        card_dict = clean_cards(erd.graph, card_dict)

                    # print(f'Cardinalities: {card_dict}')
                    # print(f'Paths: {paths}')
                        
                        # get cardinalities for paths
                        path_cards, exclusive_path, variable_path = get_path_cards(paths, destination_attributes[0], card_dict, source_att, erd)
                        #print(f'Path cards: {path_cards}')
                        
                        #print(f'Excl_path: {exclusive_path}')
                        # calculate total card for each path
                        att_path_bounds.append(calc_tot_card(path_cards, exclusive_path, paths, variable_path))
                else:
                    return (1,1)

                    #print(f'path_bounds: {path_bounds}')
            
            # get path_bounds (min(low), max(high)) for att_path_bounds
           # print(att_path_bounds)
            p_bound = [math.inf, 0]
            for bound in att_path_bounds:
                if p_bound[0] > bound[0]:
                    p_bound[0] = bound[0]
                if p_bound[1] < bound[1]:
                    p_bound[1] = bound[1]
            path_bounds.append((p_bound[0], p_bound[1]))



                    
    
    #print(path_bounds)

    # this is taking the card over diff paths (max(low), min(high))
    comp_bound = [path_bounds[0][0], path_bounds[0][1]]
    #comp_bound = [math.inf, 0]
    for bound in path_bounds:
        #if not math.isinf(comp_bound[0]) and not math.isinf(bound[0]):
        if comp_bound[0] < bound[0]:
            comp_bound[0] = bound[0]
        #  if not math.isinf(comp_bound[1]) and not math.isinf(bound[1]):
        if comp_bound[1] > bound[1]:
            comp_bound[1] = bound[1]

    bounds = (comp_bound[0], comp_bound[1])
        
            

    #print(bounds)
    return bounds


def calc_tot_card(path_cards, exclusive_path, paths, variable_path):
    path_tot_card = {}
    com_path_card = (0,0)
    path_with_excluder = {}
    for path in path_cards:
        for excl in exclusive_path:
            if excl in paths[path]:
                if excl in path_with_excluder:
                    path_with_excluder[excl].append(path)
                else:
                    path_with_excluder[excl] = [path]

        if path != 'com':
            if 'com' in path_cards:
                tot_card = [com_path_card[0], com_path_card[1]]
            else:
                tot_card = [math.inf, 0]

            for card in path_cards[path]:
                tot_card[0] = tot_card[0] * card[0]
                tot_card[1] = tot_card[1] * card[1]
                #if card[0] < tot_card[0]:
                #    tot_card[0] = card[0]
                #if card[1] > tot_card[1]:
                #    tot_card[1] = card[1]
            tot_card = (tot_card[0], tot_card[1])
            path_tot_card[path] = tot_card
           # print(f'{path}:{tot_card}')
        else:
            tot_card = [path_cards['com'][0][0], path_cards['com'][0][1]]
            for card in path_cards[path]:
                tot_card[0] = tot_card[0] * card[0]
                tot_card[1] = tot_card[1] * card[1]
                #if card[0] < tot_card[0]:
                #    tot_card[0] = card[0]
                #if card[1] > tot_card[1]:
                #    tot_card[1] = card[1]
            com_path_card = (tot_card[0], tot_card[1])
    
      
   # print(f'p_exc: {path_with_excluder}')

    # make paths to not be totalled
    # validate excluder working with card * imp (need a new test case)
    path_tot_exc = {}
    comm_excluder = False
    for excluder in path_with_excluder:
        if 'com' in path_with_excluder[excluder]:
            comm_excluder = True
        elif comm_excluder == False:
            # take 1 card from paths in this excluder
            path_excl_card = (None,None)
            exc_paths = ''
            for path in path_with_excluder[excluder]:
                tot_excl_min = math.inf
                tot_excl_max = 0
                if tot_excl_min > path_tot_card[path][0]:
                    tot_excl_min = path_tot_card[path][0]
                    #print(f'min {path_tot_card[path][0]}')
                if tot_excl_max < path_tot_card[path][1]:
                    tot_excl_max = path_tot_card[path][1]
                    #print(f'max {path_tot_card[path][1]}')
                if path_excl_card[0] is None and path_excl_card[1] is None:
                    path_excl_card = (tot_excl_min, tot_excl_max)
                else:
                    if path_excl_card[0] > tot_excl_min:
                        path_excl_card = (tot_excl_min, tot_excl_max)
                    elif path_excl_card[0] >= tot_excl_min and path_excl_card[1] < tot_excl_max:
                        path_excl_card = (tot_excl_min, tot_excl_max)
                exc_paths += f' {path}'
            #print(exc_paths)
            path_tot_exc[exc_paths] = path_excl_card
    
    #print(path_tot_exc)

    if comm_excluder == True:
        path_excl_card = (None,None)
        for path in path_tot_card:
            tot_excl_min = math.inf
            tot_excl_max = 0
            if tot_excl_min > path_tot_card[path][0]:
                tot_excl_min = path_tot_card[path][0]
                #print(f'min {path_tot_card[path][0]}')
            if tot_excl_max < path_tot_card[path][1]:
                tot_excl_max = path_tot_card[path][1]
                #print(f'max {path_tot_card[path][1]}')
            if path_excl_card[0] is None and path_excl_card[1] is None:
                path_excl_card = (tot_excl_min, tot_excl_max)
            else:
                if path_excl_card[0] > tot_excl_min:
                    path_excl_card = (tot_excl_min, tot_excl_max)
                elif path_excl_card[0] >= tot_excl_min and path_excl_card[1] < tot_excl_max:
                    path_excl_card = (tot_excl_min, tot_excl_max)
        tot_card = path_excl_card
    
    #print(f'tot: {tot_card}')

    if comm_excluder == False:
        for exc_p in path_tot_exc:
            del_path = list()
            for p in path_tot_card:
                if str(p) in exc_p:
                    del_path.append(p)
            for p in del_path:
                del path_tot_card[p]
            
            path_tot_card[exc_p] = path_tot_exc[exc_p]

       # print(path_tot_card)

        if variable_path:
            tot_min = math.inf
            tot_max = 0
            for path in path_tot_card:
                if tot_min > path_tot_card[path][0]:
                    tot_min = path_tot_card[path][0]
                tot_max += path_tot_card[path][1]

            tot_card = (tot_min, tot_max)

        else:
            # calculate overall card (min(lows), total(highs))
            tot_min = 0
            tot_max = 0
            for path in path_tot_card:
                if tot_min < path_tot_card[path][0]:
                    tot_min = path_tot_card[path][0]
                tot_max += path_tot_card[path][1]

        tot_card = (tot_min, tot_max)

   # print(f'tot: {tot_card}')
    return tot_card


def get_path_cards(paths, destination_attribute, card_dict, source_att, erd):
    path_cards = {}
    exclusive_path = {}
    variable_path = False
    p_var_val = {}
   # print(paths)
    for path in paths:
        #print(paths[path])
        cards = list()
        if path == 'com':
            prev_node = None
        else:
            prev_node = paths['com'][-1]
        #print(prev_node)
       # print(path)
        for node in paths[path]:
            if node is not destination_attribute:  # NOTE this might have to change so multi destination works
                #print(f'{prev_node}->{node}: {card_dict[prev_node][node]}')
                if prev_node != None:
                    min_card = None
                    max_card = None
                    #print(f'{prev_node}->{node}: {card_dict[prev_node][node]}')
                    if 'min' in card_dict[prev_node][node]:
                        min_card = card_dict[prev_node][node]['min']
                    if 'max' in card_dict[prev_node][node]:
                        max_card = card_dict[prev_node][node]['max']
                    if 'style' in card_dict[prev_node][node]:
                        if 't' in card_dict[prev_node][node]['style']:
                            min_card = 1
                        if 'p' in card_dict[prev_node][node]['style']:
                           min_card = 0
                        if 'e' in card_dict[prev_node][node]['style']:
                            max_card = 1
                            #print(node)
                           # print(erd.identifiers)
                            for key in erd.identifiers:
                                if source_att in erd.identifiers[key]:
                                    for ex_path in card_dict[node]:
                                       # print(ex_path)
                                        if node in exclusive_path:
                                            if ex_path != prev_node and ex_path not in exclusive_path[node]:
                                                exclusive_path[node].append(ex_path)
                                        elif ex_path != prev_node:    
                                            exclusive_path[node] = [ex_path]
                                    non_entity_ele = list()
                                    for ele in exclusive_path[node]:
                                        if erd.graph.nodes[ele]['s'] != 's':
                                            non_entity_ele.append(ele)
                                    for ele in non_entity_ele:
                                        exclusive_path[node].remove(ele)
                                    if not exclusive_path[node]:
                                        del exclusive_path[node]

                        if 'o' in card_dict[prev_node][node]['style']:
                            for key in erd.identifiers:
                                if source_att in erd.identifiers[key]:
                                    max_card = None
                                    variable_path = True
                                    break
                                else:
                                    max_card = math.inf
                                
                            
                            
                    
                    card = (min_card, max_card)
                    #print(f'{prev_node}->{node}: {card}')
                    
                    if card[0] is not None and card[1] is not None:
                        cards.append(card)
                    #print(cards)
                    prev_node = node
                else:
                    prev_node = node
        #print(f'{path}: {cards}')
        path_cards[path] = cards
    return path_cards, exclusive_path, variable_path


def clean_cards(graph, card_dict):
    for key in card_dict:
        for neig_node in card_dict[key]:
            if key in card_dict[key] or graph.nodes[key]['s'] == '^':
                if 'style' in card_dict[key][neig_node]:
                    card_dict[key][neig_node] = {}
            elif graph.nodes[key]['s'] == 'd':
                card_dict[key][neig_node] = {}
        

    return card_dict  


def alter_card_for_attributes(erd, card_dict, neighbor_dict):
    # change non identifier attributes
    for node in card_dict:
        if erd.graph.nodes[node]['s'] == 'o':
            for neig in neighbor_dict[node]:
               # print(f'neig = {neig}: {erd.graph.nodes[neig]}')
                if erd.graph.nodes[neig]['s'] == 's' or erd.graph.nodes[neig]['s'] == '^':
                    card_dict[node][neig] = {'min': 1, 'max': math.inf}

    #print(card_dict)
    path_identifiers = {}
   # print(neighbor_dict)
    # change identifier attributes
    for node in neighbor_dict:
        for neig in neighbor_dict[node]:
            #print(neig)
            if neig in erd.identifiers:
                #print(f'identifiers: {erd.identifiers}')
                for ele in erd.identifiers[neig]:
                    if node == ele:
                       # print(f'{node}:{ele}')
                        path_identifiers[node] = neig

    #print(path_identifiers)

    for ident in path_identifiers:
        #print(card_dict[ident][0][path_identifiers[ident]])
        card_dict[ident][path_identifiers[ident]] = {'min': 1, 'max': 1}

    return card_dict


def get_card_neighbor_dict(graph, paths):
    card_dict = {}
    neighbors_dict = {}
    for path in paths:
        for node in paths[path]:
            neighbors_dict[node] = list(graph[node])
            for key in graph[node]:
                if node in card_dict:
                    if key not in card_dict[node]:
                        card_dict[node][key] = graph[node][key]
                else:
                    card_dict[node] = {key: graph[node][key]}
    return card_dict, neighbors_dict


def get_simple_paths(graph, source, destination):
    paths = list()
    valid_paths = list()
    for path in nx.all_simple_paths(graph, source, destination):
        valid = True
        for indx, curr in enumerate(path):
            if indx > 1:
                if path[indx-2] in path[indx-1] and curr in path[indx-1]:
                    valid = False
                    break
        if valid:
            valid_paths.append(path)
        paths.append(path)

    return paths, valid_paths

def seperate_comm_path(paths):
    common_nodes = list(set.intersection(*map(set, paths)))
    #print(common_nodes)

    common_node_loc = {}
    for path in paths:
        for comm in common_nodes:
            if comm in path:
                if comm in common_node_loc.keys():
                    common_node_loc[comm].append(path.index(comm))
                else:
                    common_node_loc[comm] = [path.index(comm)]
    
    #print(common_node_loc)
    comm_path = list()
    comm_nodes_dict = {}
    ind_list = list()
    for comm_nodes in common_node_loc:
        if len(common_node_loc[comm_nodes]) > 0:
            res = all(elem == common_node_loc[comm_nodes][0] for elem in common_node_loc[comm_nodes])
            if res:
                comm_nodes_dict[common_node_loc[comm_nodes][0]] = comm_nodes
                ind_list.append(common_node_loc[comm_nodes][0])
    
   # print(comm_nodes_dict)
    
    # sort into order
    ind_list.sort()
    prev_ind = None
    for ind in ind_list:
        if not prev_ind:
            comm_path.append(comm_nodes_dict[ind])
            prev_ind = ind
        else:
            if prev_ind+1 == ind:
                comm_path.append(comm_nodes_dict[ind])
                prev_ind = ind
        

   # print(comm_path)
    
    sep_paths = {}
    sep_paths['com'] = comm_path
    for indx, path in enumerate(paths):
        for comm_node in comm_path:
            path.remove(comm_node)
        sep_paths[indx] = path
    
    return sep_paths



#erd = test19()
#calculate_bounds(erd, ["b"], ["g"])
#print("---")
#erd = test7()
#calculate_bounds(erd, ["c"], ["a"])
#erd = test10()
#calculate_bounds(erd, ["f"], ["h"])
#erd = test11()
#calculate_bounds(erd, ["a"], ["c"])
#erd = test4()
#calculate_bounds(erd, ["a"], ["b"])
#print("----")
#erd = test15()
#calculate_bounds(erd, ["a", "b"], ["c"])
#erd = test15A()
#calculate_bounds(erd, ["b"], ["c"])
#erd = test15B()
#calculate_bounds(erd, ["c"], ["d"])
#erd = test15C()
#calculate_bounds(erd, ["c"], ["d"])
#erd = test15D()
#calculate_bounds(erd, ["c"], ["b"])
#print("------")
#print("------")
#erd = testC()
#calculate_bounds(erd, ["b1"], ["b2"])
#print("------")
#erd = testD()
#calculate_bounds(erd, ["b1"], ["b2"])
#calculate_bounds(erd, ["f"], ["h"])