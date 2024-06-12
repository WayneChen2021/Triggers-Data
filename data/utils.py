import numpy as np
import json
from itertools import product

def minimize_variance(template):
    options = []
    for role, entities in template.items():
        if not role in ['incident_type', 'Triggers']:
            for coref_mentions in entities:
                options.append([tup[1] for tup in coref_mentions])
    
    if not len(options):
        return -1, []
    
    minimal_variance = 1e10
    best_comb = None
    for comb in product(*options):
        var = np.var(comb)
        if var < minimal_variance:
            best_comb = list(comb)
            minimal_variance = var

    return minimal_variance, best_comb

def event_spread(template):
    return minimize_variance(template)[0]

def do_grouping(data_files, metric_func, num_buckets, is_template_level=True):
    documents = []
    for file_path in data_files:
        with open(file_path, 'r') as f:
            documents += list(json.loads(f.read()).values())

    all_metrics = []
    metric_map = {}
    for document in documents:
        if is_template_level:
            for template_ind, template in enumerate(document['templates']):
                metric_val = metric_func(template)
                if not metric_val in metric_map:
                    metric_map[metric_val] = []
                metric_map[metric_val].append([document['docid'], template_ind])
                all_metrics.append(metric_val)
        else:
            metric_val = metric_func(document)
            if not metric_val in metric_map:
                metric_map[metric_val] = []
            metric_map[metric_val].append(document['docid'])
            all_metrics.append(metric_val)
    
    all_metrics = sorted(all_metrics)
    instances_per_bucket = len(all_metrics) // num_buckets
    buckets = []

    def remove_from_map(metric_val):
        val = metric_map[metric_val][0]
        metric_map[metric_val] = metric_map[metric_val][1:]
        return val

    for i in range(num_buckets + 1):
        metric_group = all_metrics[i * instances_per_bucket : (i + 1) * instances_per_bucket]
        if len(metric_group):
            bucket = [remove_from_map(metric_val) for metric_val in metric_group]
            buckets.append({
                'min': metric_group[0],
                'max': metric_group[-1],
                'selections': bucket
            })
    
    return buckets