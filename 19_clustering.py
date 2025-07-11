import pm4py
import os
import importlib.util


def execute_script():
    dataframe = pm4py.read_xes(os.path.join(".", "data_preprocessed", "merged", "Retrieval.xes"), return_legacy_log_object=True)
    print(dataframe)
    # define a K-Means with 3 clusters
    from pm4py.util import ml_utils
    clusterer = ml_utils.KMeans(n_clusters=3, random_state=0, n_init=10)

    for clust_log in pm4py.cluster_log(dataframe, sklearn_clusterer=clusterer):
        print(clust_log)
        process_tree = pm4py.discover_process_tree_inductive(clust_log)

        if importlib.util.find_spec("graphviz"):
            pm4py.view_process_tree(process_tree, format="png")


if __name__ == "__main__":
    execute_script()
