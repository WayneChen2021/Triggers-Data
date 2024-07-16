import numpy as np
import json
from itertools import product
import ast


def minimize_variance(template, pronouns_file="pronouns.txt"):
    pronoun_set = set()
    with open(pronouns_file, "r") as f:
        for line in f:
            pronoun_set.add(line.strip())

    options = []
    for role, entities in template.items():
        if role != "incident_type" and not "Trig" in role:
            for coref_mentions in entities:
                non_pronouns = [
                    tup
                    for tup in coref_mentions
                    if not tup[0].lower().strip() in pronoun_set
                ]

                options.append(
                    [
                        tup + [role]
                        for tup in (
                            coref_mentions if len(non_pronouns) == 0 else non_pronouns
                        )
                    ]
                )

    minimal_variance = 2e10
    chosen_args = {}
    args_mean_pos = 0
    def assign_trig():
        for trig_type, trig_annotations in template.items():
            if "Trig" in trig_type:
                chosen_args[trig_type] = [
                    min(
                        trig_annotations,
                        key=lambda annotation: np.abs(annotation[0][1] - args_mean_pos),
                    )
                ]
                assert len(chosen_args[trig_type]) == 1

    if not len(options):
        assign_trig()
        return 0, chosen_args

    for comb_ in product(*options):
        comb = [i[1] for i in comb_]
        var = np.var(comb)
        if var < minimal_variance:
            chosen_args = {}
            minimal_variance = var
            args_mean_pos = 0
            for i in comb_:
                role = i[-1]
                if not role in chosen_args:
                    chosen_args[role] = []

                if not [i[:2]] in chosen_args[role]:
                    chosen_args[role].append([i[:2]])
                    args_mean_pos += i[1]
            args_mean_pos /= len(comb_)

    assign_trig()
    return minimal_variance, chosen_args


def event_spread(template):
    return minimize_variance(template)[0]


def do_grouping(data_files, metric_func, num_buckets, is_template_level=True):
    documents = []
    for file_path in data_files:
        with open(file_path, "r") as f:
            documents += list(json.loads(f.read()).values())

    all_metrics = []
    metric_map = {}
    for document in documents:
        if is_template_level:
            for template_ind, template in enumerate(document["templates"]):
                metric_val = metric_func(template)
                if not metric_val in metric_map:
                    metric_map[metric_val] = []
                metric_map[metric_val].append([document["docid"], template_ind])
                all_metrics.append(metric_val)
        else:
            metric_val = metric_func(document)
            if not metric_val in metric_map:
                metric_map[metric_val] = []
            metric_map[metric_val].append(document["docid"])
            all_metrics.append(metric_val)

    all_metrics = sorted(all_metrics)
    instances_per_bucket = len(all_metrics) // num_buckets
    buckets = []

    def remove_from_map(metric_val):
        val = metric_map[metric_val][0]
        metric_map[metric_val] = metric_map[metric_val][1:]
        return val

    for i in range(num_buckets + 1):
        metric_group = all_metrics[
            i * instances_per_bucket : (i + 1) * instances_per_bucket
        ]
        if len(metric_group):
            bucket = [remove_from_map(metric_val) for metric_val in metric_group]
            buckets.append(
                {"min": metric_group[0], "max": metric_group[-1], "selections": bucket}
            )

    return buckets
