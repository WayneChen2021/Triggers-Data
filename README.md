# Triggers-Data
Data for paper "Are Triggers Needed for Document-Level Event Extraction"

## Data format

MUC data is all contained in [`all_splits.json`](data/MUC/all_splits.json). IDs `TST4-*` and `TST3-*` were used for evaluation; IDs `TST2-*` and `TST1-*` were used for evaluation; everything else was for training.

WikiEvents data is split up [here](data/WikiEvents)

The translated CMNEE data is split up [here](data/CMNEE)

The data is a dictionary, where each entry is
```
<document id>: {
    "source": <annotation source>, # one of "human", "llm", "keyword"
    "docid": <document id>,
    "doctext": <article text>,
    "templates": [
        {
            "incident_type": <incident type>, # (i.e. "attack", "kidnapping" for MUC or "Life.Die" for WikiEvents),
            "Role1": [
                [
                    [
                        <entity 1 mention 1>,
                        <entity 1 mention 1 offset in text>
                    ],
                    [
                        <entity 1 mention 2>,
                        <entity 1 mention 2 offset in text>
                    ],
                    ...
                ],
                [
                    [
                        <entity 2 mention 1>,
                        <entity 2 mention 1 offset in text>
                    ],
                    [
                        <entity 2 mention 2>,
                        <entity 2 mention 2 offset in text>
                    ],
                    ...
                ],
                ...
            ],
            "Role2": [],
            ...,
            "Human_Trig": [
                [
                    [
                        <trigger span 1>,
                        <trigger span 1 offset in text>
                    ]
                ],
                [
                    [
                        <trigger span 2>,
                        <trigger span 2 offset in text>
                    ]
                ]
            ],
            "Keyword_Trig": [
                ...
            ],
            "LLM_Trig": [
                ...
            ],
            "Random_Trig": [
                ...
            ]
        }
    ]
}
```