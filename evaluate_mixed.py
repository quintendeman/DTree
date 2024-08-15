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
    updates = []
    input_stream_file = "datasets/" + stream_file
    with open(input_stream_file, 'rb') as input_stream:
        print("Reading in entire stream")
        vertexcount = int.from_bytes(input_stream.read(4), "little")
        updatecount = int.from_bytes(input_stream.read(8), "little")
        print(vertexcount, "vertices", updatecount, "updates", "in stream.")
        # updatecount = min(updatecount, 100000000)
        print("Doing", updatecount, "operations.")
        for i in range(updatecount):
            update_type = int.from_bytes(input_stream.read(1), "little")
            src = int.from_bytes(input_stream.read(4), "little")
            dst = int.from_bytes(input_stream.read(4), "little")
            updates.append((update_type, src, dst))

    graph = defaultdict(set)
    spanningtree, tree_edges, non_tree_edges = constructST_adjacency_list(graph, 0)
    _, Dtree = Dtree_utils.construct_BFS_tree(graph, 0, non_tree_edges)

    i = 0
    doing_updates = True
    total_update_time = 0
    total_query_time = 0
    update_timer_start = timer()
    query_timer_start = update_timer_start

    for update in updates:
        i += 1
        (update_type,a,b) = update

        if (update_type == 2): # QUERIES IN STREAM
            if (doing_updates):
                total_update_time += timer() - update_timer_start
                doing_updates = False
                query_timer_start = timer()

            if a in Dtree and b in Dtree:
                Dtree_utils.query(Dtree[a], Dtree[b])

        else:   # UPDATE OPERATIONS
            if (not doing_updates):
                total_query_time += timer() - query_timer_start
                doing_updates = True
                update_timer_start = timer()

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


    filename = "results/" + stream_file + "_mixed_results.txt"
    file1 = open(filename, 'a')
    file1.write(" UPDATES/SEC: ")
    file1.write(str((0.9*len(updates))/total_update_time))
    file1.write("\n")
    file1.write(" QUERIES/SEC: ")
    file1.write(str((0.1*len(updates))/total_query_time))
    file1.write("\n")
    file1.close()
