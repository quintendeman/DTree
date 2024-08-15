import sys
import random
from _collections import defaultdict
from ET import ET_utils
from HK import HK_utils
from utils import tree_utils
from utils.tree_utils import constructST_adjacency_list
from utils.graph_utils import loadGraph

from Dtree import Dtree_utils
from ET.ETNode import ETNode
from Dtree.DTNode import DTNode
from HK.HKNode import HKNode
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
    sys.setrecursionlimit(50000000)
    folder = 'dataset/'
    testcase = sys.argv[1]
    records = loadGraph(testcase)

    # setup starting point and ending point
    start_timestamp = records[0][2]
    end_timestamp = records[-1][2]

    # As described in the paper, we slightly change the start_timestamp
    # (and end_timestamp), which includes almost all edges
    if testcase == 'dblp':
        start_timestamp = 1980
    elif testcase == 'dnc':
        start_timestamp = 1423298633
    elif testcase == 'enron':
        start_timestamp = 915445260
        end_timestamp = 1040459085

    #  setups
    survival_time, test_points = setup(testcase, start_timestamp, end_timestamp)
    sanity_check = True  # True: switch on the sanity check; False: swith off the sanity check.

    if testcase in ['fb', 'wiki', 'dnc', 'messages', 'call']:  # small graphs
        isSmallGraph = True
        n = 200000  # n is setup for opt
    else:  # large graphs
        isSmallGraph = False  # True: not test opt; False: test opt
        n = 200000

    print(survival_time, "%d tests, first test: %d, last test: %d" %(len(test_points), test_points[0], test_points[-1]))
    print(start_timestamp, end_timestamp)
    print(test_points)

    # start from an empty graph
    idx = 0
    max_priority = sys.maxsize
    graph = defaultdict(set)
    spanningtree, tree_edges, non_tree_edges = constructST_adjacency_list(graph, 0)

    _, Dtree = Dtree_utils.construct_BFS_tree(graph, 0, non_tree_edges)

    expiredDict = defaultdict(set)
    inserted_edge = defaultdict()

    insertions = 0
    deletions = 0

    # distribution of distance between root and nodes
    Dtree_accumulated_dist = defaultdict(int)

    edges_num = 0
    current_time = start_timestamp
    count_snapshot = 0

    static = True # SET THIS VARIABLE TO TRUE TO GENERATE THE STATIC GRAPH BINARY

    stream_file_name = "datasets/" + testcase + "_stream_binary"
    if static:
        stream_file_name = "datasets/" + testcase + "_static_binary"

    # MANUALLY SET THESE TO THE CORRECT VALUE
    num_vertices = 86803
    num_updates = 296831

    vertex_map = defaultdict()
    vertex_id = 0

    with open(stream_file_name, 'wb') as output_stream :
        print("Writing stream into", stream_file_name)
        print()
        print("!!!MAKE SURE THIS IS CORRECT!!!")
        print("num_vertices:", num_vertices, "num_updates", num_updates)
        print()
        output_stream.write(num_vertices.to_bytes(4, "little"))
        output_stream.write(num_updates.to_bytes(8, "little"))

        # while current_time <= end_timestamp + survival_time:
        while current_time <= test_points[-1]:
            # loop records and start with the record with current_time

            while idx < len(records) and records[idx][2] < current_time:
                idx += 1
            while idx < len(records) and records[idx][2] == current_time:
                # filter out (v, v) edges
                if records[idx][0] == records[idx][1]:
                    idx += 1
                    continue

                a, b = order(records[idx][0], records[idx][1])
                if a not in vertex_map:
                    vertex_map[a] = vertex_id
                    vertex_id += 1
                if b not in vertex_map:
                    vertex_map[b] = vertex_id
                    vertex_id += 1

                idx += 1
                if (a, b) not in inserted_edge:  # a new edge
                    # INSERT (A,B)
                    output_stream.write((0).to_bytes(1, "little"))
                    output_stream.write((vertex_map[a]).to_bytes(4, "little"))
                    output_stream.write((vertex_map[b]).to_bytes(4, "little"))
                    insertions += 1

                    inserted_edge[(a, b)] = current_time + survival_time  # we keep the expired time for the inserted edge.
                    expiredDict[current_time + survival_time].add((a, b))
                else:  # re-insert this edge, refresh the expired timestamp
                    if not static:
                        expired_ts = inserted_edge[(a, b)]
                        expiredDict[expired_ts].remove((a, b))
                        inserted_edge[
                            (a, b)] = current_time + survival_time  # we refresh the expired time for the inserted edge.
                        expiredDict[current_time + survival_time].add((a, b))

                # Dtree
                if a not in Dtree:
                    Dtree[a] = DTNode(a)
                if b not in Dtree:
                    Dtree[b] = DTNode(b)

        
            if current_time in expiredDict:
                for (a, b) in expiredDict[current_time]:
                    if not static:
                        del inserted_edge[(a, b)]
                        edges_num -= 1
                        # Dtree
                        # DELETE (A,B)
                        output_stream.write((1).to_bytes(1, "little"))
                        output_stream.write((vertex_map[a]).to_bytes(4, "little"))
                        output_stream.write((vertex_map[b]).to_bytes(4, "little"))
                        deletions += 1

                del expiredDict[current_time]

            current_time += 1

        print("# vertices %d." %(vertex_id))
        print("# of total updates: %d." %(insertions + deletions))
        print("# of insertions: %d." %(insertions))
        print("# of deletions: %d." %(deletions))





