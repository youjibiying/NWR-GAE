# -*- coding: utf-8 -*-
"""
@author: cdonnat
"""
### Random tools useful for saveing stuff and manipulating pickle/numpy objects
import numpy as np
import pickle
import gzip
import re
import networkx as nx
import dgl
import torch


def save_obj(obj, name, path, compress=False):
    # print path+name+ ".pkl"
    if compress is False:
        with open(path + name + ".pkl", 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    else:
        with gzip.open(path + name + '.pklz','wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name,compressed=False):
    if compressed is False:
        with open(name, 'rb') as f:
            return pickle.load(f)
    else:
        with gzip.open(name,'rb') as f:
            return pickle.load(f)



def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval


def natural_keys(l):
    '''
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        float regex comes from https://stackoverflow.com/a/12643073/190597
        '''
    t = np.array([ int(re.split(r"([a-zA-Z]*)([0-9]*)", c)[2]) for c in l  ])
    order = np.argsort(t)
    return [l[o] for o in order]


def saveNet2txt(G, colors=[], name="net", path="plots/"):
    '''saves graph to txt file (for Gephi plotting)
    INPUT:
    ========================================================================
    G:      nx graph
    colors: colors of the nodes
    name:   name of the file
    path:   path of the storing folder
    OUTPUT:
    ========================================================================
    2 files containing the edges and the nodes of the corresponding graph
    '''
    if len(colors) == 0:
        colors = range(nx.number_of_nodes(G))
    graph_list_rep = [["Id","color"]] + [[i,colors[i]]
                      for i in range(nx.number_of_nodes(G))]
    np.savetxt(path + name + "_nodes.txt", graph_list_rep, fmt='%s %s')
    edges = G.edges(data=False)
    edgeList = [["Source", "Target"]] + [[v[0], v[1]] for v in edges]
    np.savetxt(path + name + "_edges.txt", edgeList, fmt='%s %s')
    print ("saved network  edges and nodes to txt file (for Gephi vis)")
    return


def read_real_datasets(datasets):
    edge_path = "../datasets/{}/out1_graph_edges.txt".format(datasets)
    node_feature_path = "../datasets/{}/out1_node_feature_label.txt".format(datasets)
    with open(edge_path) as edge_file:
        edge_file_lines = edge_file.readlines()
        G = nx.parse_edgelist(edge_file_lines[1:], nodetype=int)
        g = dgl.from_networkx(G)
    with open(node_feature_path) as node_feature_file:
        node_lines = node_feature_file.readlines()[1:]
        feature_list = []
        labels = []
        for node_line in node_lines:
            node_id, feature, label = node_line.split("\t")
            labels.append(int(label))
            features = feature.split(",")
            feature_list.append([float(feature) for feature in features])
        feature_array = np.array(feature_list)
        features = torch.from_numpy(feature_array)
        g.ndata['attr'] = features.float()
        labels = np.array(labels)
    return g, labels