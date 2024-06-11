The scorer uses the Hungarian Algorithm to consider all possible template and
argument matches and computes the matching that yields the most matches. Event
type is treated as just a regular role, and the scorer can be configured to consider
triggers as well.

## Usage
- `config`: configuration file (some examples [here](scorer_configs))
- `in_file`: input JSON file; format is
```
{
     "<docid>": {
        "docid": "<docid>",
        "doctext": "abcdefg...",
        "gold_templates": [
            {
                "incident_type": "incident type 1", # one of event_type_names in the config file
                "role 1": [ # one of the role_names in the config file; all role_names types must appear in each template (scorer assumes all event types have same set of roles)
                    [
                        [
                            "entity 1 mention 1"
                        ],
                        [
                            "entity 1 mention 2"
                        ]
                    ],
                    [
                        [
                            "entity 2 mention 1"
                        ],
                        [
                            "entity 2 mention 2"
                        ]
                    ]
                    
                ],
                "role 2": [], # role with no entities
                "role 3": [],
                ...
                "Triggers": [
                    [
                        [
                            "trigger 1"
                        ],
                        [
                            "trigger 2" # multiple triggers are treated as coreferring mentions
                        ]
                    ]
                ]
            }
        ],
        "pred_templates": [
            {
                "incident_type": "incident type 1",
                "role 1": [
                    [
                        [
                            "entity 1 mention 1" # assumes only 1 mention per entity
                        ]
                    ],
                    [
                        [
                            "entity 2 mention 1"
                        ]
                    ]
                    
                ],
                "role 2": [],
                "role 3": [],
                ...,
                "Triggers": [] # if no triggers just leave it as empty list
            }
        ]
    }
}
```
- `out_file`: output JSON path
- `relax_match`: optional settable flag that allows a match as long as there's an overlap in spans (otherwise requires exact matches)
- `filter_lst`: optional settable path that specifies which documents or documents and templates to compute metrics over (otherwise computes over all documents and templates)

To have the scorer consider triggers, add `"Triggers"` to `role_names` in the config file for triggers. The gold templates do not all have to have triggers. The results will be in
the `argument_type_metrics_per_class` section of the output file.

To filter out select documents or templates provide either a document list
```
[
    "TST1-MUC3-0098",
    "TST2-MUC4-0075",
    "TST1-MUC3-0094",
    ...
]
```
or documents and the template index (index in the 'gold_templates')
```
[
    ["TST1-MUC3-0098", 1],
    ["TST2-MUC4-0075", 0],
    ["TST1-MUC3-0094", 2],
    ...
]
```