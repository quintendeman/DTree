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

def write_results(stream_file, update_times, query_times, timeout):
    f = open("results/update_speed_results.txt", "a")
    f.write(stream_file)
    if timeout >= 0:
        f.write(" Timed Out At Batch ")
        f.write(str(timeout))
        f.write("\n")
        f.write(stream_file)
    f.write(" Update Batch Times: ")
    for time in update_times:
        f.write(str(time))
        f.write(" ")
    f.write("\n")
    f.write(stream_file)
    f.write(" Query Batch Times: ")
    for time in query_times:
        f.write(str(time))
        f.write(" ")
    f.write("\n")
    f.close()



if __name__ == '__main__':
    stream_file = sys.argv[1]
    updates = []
    for batch_type in ["ins","del"]:
        update_type = 0 if (batch_type == "ins") else 1
        for batch_num in range(10):
            updates.append([])
            input_stream_file = "datasets/" + stream_file + "/" + stream_file + "_batch_" + batch_type + "_" + str(batch_num) + ".txt"
            with open(input_stream_file, 'r') as input_stream:
                print("Reading in file", input_stream_file)
                for line in input_stream.readlines():
                    src, dst = line.split(' ')
                    updates[update_type*10 + batch_num].append((update_type, src, dst))
    queries = []
    for batch_type in ["ins","del"]:
        update_type = 0 if (batch_type == "ins") else 1
        for batch_num in range(10):
            queries.append([])
            input_stream_file = "datasets/" + stream_file + "/" + stream_file + "_query_" + batch_type + "_" + str(batch_num) + ".txt"
            with open(input_stream_file, 'r') as input_stream:
                print("Reading in file", input_stream_file)
                for line in input_stream.readlines():
                    src, dst = line.split(' ')
                    queries[update_type*10 + batch_num].append((src, dst))

    graph = defaultdict(set)
    spanningtree, tree_edges, non_tree_edges = constructST_adjacency_list(graph, 0)
    _, Dtree = Dtree_utils.construct_BFS_tree(graph, 0, non_tree_edges)

    TIMEOUT = 7200

    update_times = []
    query_times = []
    print("")

    for batch_num in range(20):
        batch = updates[batch_num]
        batch_time_start = timer()
        for update in batch:
            if (timer() - batch_time_start > TIMEOUT):
                print("BATCH", batch_num, "TIMED OUT AFTER", TIMEOUT/60, "MINUTES.")
                write_results(stream_file, update_times, query_times, batch_num)
                exit()
            (update_type,a,b) = update
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
        batch_time = timer() - batch_time_start
        update_times.append(batch_time)

        start = timer()
        for (x, y) in queries[batch_num]:
            if x in Dtree and y in Dtree:
                Dtree_utils.query(Dtree[x], Dtree[y])
        query_time = timer() - start
        query_times.append(query_time)

    f = open("results/update_speed_results.txt", "a")
    f.write(stream_file)
    f.write(" Update Batch Times: ")
    for time in update_times:
        f.write(str(time))
        f.write(" ")
    f.write("\n")
    f.write(stream_file)
    f.write(" Query Batch Times: ")
    for time in query_times:
        f.write(str(time))
        f.write(" ")
    f.write("\n")
    f.close()
    write_results(stream_file, update_times, query_times, -1)
