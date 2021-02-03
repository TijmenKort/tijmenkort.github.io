import pickle


def select_r_scores(r_scores, clusters):

    selected = []
    for c in r_scores:
        if c['Cluster'] in clusters or c['Cluster'] == 'sum':
            selected.append(c)

    return selected


def run_analyses_scores(clusters):
    selected = None
    if clusters:
        with open('new_graphs/pearson_r.pickle', 'rb') as f:
            r_scores = pickle.load(f)

        selected = select_r_scores(r_scores, clusters)

    return selected
