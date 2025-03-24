# clean_framework
This is a framework to train language model fast on different data.

## Project structure

- Data must be in a json format that looks like this:
  
```
[
  {
    "input": "E0 . T3 . T5 . T18",
    "output": "E45"
  },
  {
    "input": "E0 . T3 . T8 . T16 . T16",
    "output": "E1"
  }, ...
]
```

- Data will be tokenized like so: [BOS] E0 . T3 . T5 . T18 [SEP] E45 [EOS] [PAD] [PAD] ... up to _model.block_size_
  
    - Where **OUT** is a delimiter token up to which the model sees the input, it is added during data preprocessing in **data.py**.
    - Anything after the delimiter, including the delimiter, is masked.

- Data must be in the directory **data** saved as **train.json** and **test.json**

- Code to generate data must be in the directory **data_generation**.
    - It should output train.json and test.json into directory **./data**.

- Prior to setting _model.block_size_ in **base.yaml**, run _data_info.py_ in directory utils to obtain information about the length of examples.

- Every time you work on a new project, config needs to be changed!

    - **config/base.yaml** contains "None" for string values or None for integer/float values: this needs to be filled in (project specific)

- Everything should be run from the root directory, ex:
    
    - cd clean_framework
    - python utils/inference.py

- Data generation script should be named "generate_data.py"
