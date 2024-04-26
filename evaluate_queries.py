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
    testcase = sys.argv[1]
    updates = []
    input_stream_file = "datasets/" + testcase + "_stream_binary"
    with open(input_stream_file, 'rb') as input_stream:
        print("Reading in entire stream")
        vertexcount = int.from_bytes(input_stream.read(4), "little")
        updatecount = int.from_bytes(input_stream.read(8), "little")
        print(vertexcount, "vertices", updatecount, "updates", "in stream.")
        updatecount = min(updatecount, 100000000)
        print("Doing", updatecount, "updates.")
        for i in range(updatecount):
            update_type = int.from_bytes(input_stream.read(1), "little")
            src = int.from_bytes(input_stream.read(4), "little")
            dst = int.from_bytes(input_stream.read(4), "little")
            updates.append((update_type, src, dst))

    graph = defaultdict(set)
    spanningtree, tree_edges, non_tree_edges = constructST_adjacency_list(graph, 0)
    _, Dtree = Dtree_utils.construct_BFS_tree(graph, 0, non_tree_edges)
    v_set = set()

    total_time = 0
    total_queries = 0

    for batch in range(10):
        print("Update batch", batch)
        for i in range((updatecount//10)*batch + (updatecount//10)):
            (update_type,a,b) = updates[i]
            if (update_type == 0): # EDGE INSERTION
                if a not in Dtree:
                    Dtree[a] = DTNode(a)
                    v_set.add(a)
                if b not in Dtree:
                    Dtree[b] = DTNode(b)
                    v_set.add(b)
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

        print("Doing queries")
        test_edges = generatePairs(v_set)
        start = timer()
        for (x, y) in test_edges:
            Dtree_utils.query(Dtree[x], Dtree[y])
        query_time = timer() - start
        print("QUERY TIME:", query_time)
        print("NUM QUERIES:", str(len(test_edges)))
        total_time += query_time
        total_queries += len(test_edges)

    print("TOTAL TIME:", total_time)
    print("TOTAL QUERIES:", total_queries)
    print("QUERIES/SECOND:", str(total_queries/total_time))

    file1 = open("results/query_results.txt", 'a')
    file1.write(input_stream_file)
    file1.write(" UPDATES/SEC: ")
    file1.write(str(total_queries/total_time))
    file1.write("\n")
    file1.close()
