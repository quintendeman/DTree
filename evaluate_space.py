import sys
import random
from _collections import defaultdict
from utils import tree_utils
from utils.tree_utils import constructST_adjacency_list
from utils.graph_utils import loadGraph

from Dtree import Dtree_utils
from Dtree.DTNode import DTNode
from timeit import default_timer as timer

import HK.updates as HKupdate
import ET.updates as ETupdate

from Class.Res import Res
from utils.IO import setup, printRes, output_average_dist_by_method, update_maintanence, update_res_query_Sd, \
    update_res_vertices_edges, update_average_distance, update_average_uneven_size_beta, update_average_runtime,\
    copyRes
from utils.graph_utils import best_BFS, order
from utils.tree_utils import generatePairs


if __name__ == '__main__':
    stream_file = sys.argv[1]
    input_stream_file = "datasets/" + stream_file
    with open(input_stream_file, 'rb') as input_stream:
        print("Reading in entire stream")
        vertexcount = int.from_bytes(input_stream.read(4), "little")
        updatecount = int.from_bytes(input_stream.read(8), "little")
        print(vertexcount, "vertices", updatecount, "updates", "in stream.")
        print("Doing", updatecount, "updates.")

        graph = defaultdict(set)
        spanningtree, tree_edges, non_tree_edges = constructST_adjacency_list(graph, 0)
        _, Dtree = Dtree_utils.construct_BFS_tree(graph, 0, non_tree_edges)

        i = 0
        overall_time_start = timer()

        for i in range(updatecount):

            if(i % 1000 == 0):
                print("UPDATE", i, stream_file)

            update_type = int.from_bytes(input_stream.read(1), "little")
            a = int.from_bytes(input_stream.read(4), "little")
            b = int.from_bytes(input_stream.read(4), "little")

            if (update_type == 0): # EDGE INSERTION
                if a not in Dtree:
                    Dtree[a] = DTNode(a)
                if b not in Dtree:
                    Dtree[b] = DTNode(b)

                root_a, distance_a = Dtree_utils.find_root(Dtree[a])
                root_b, distance_b = Dtree_utils.find_root(Dtree[b])

                if root_a.val != root_b.val:                                # tree edge insertion
                    Dtree_utils.insert_te(Dtree[a], Dtree[b], root_a, root_b)
                else:                                                       # non tree edge insertion
                    if not (Dtree[a].parent == Dtree[b] or Dtree[b].parent == Dtree[a]):
                        Dtree_utils.insert_nte(root_a, Dtree[a], distance_a, Dtree[b], distance_b)
                    
            else: # EDGE DELETION
                if Dtree[a] in Dtree[b].nte or Dtree[b] in Dtree[a].nte:    # non tree edge deletion
                    Dtree_utils.delete_nte(Dtree[a], Dtree[b])
                else:                                                       # tree edge deletion
                    Dtree_utils.delete_te(Dtree[a], Dtree[b])
