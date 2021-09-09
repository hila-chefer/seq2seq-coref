# Coreference Resolution with Sequence-to-Sequence Models

This repository contains the code implementation of our project.

- [Set up](#set-up)
  * [Requirements](#requirements)
  * [Download the official evaluation script](#download-the-official-evaluation-script)
  * [Prepare the dataset](#prepare-the-dataset)
- [Pre-processing](#Pre-processing)
- [Training](#training)
- [Post-processing](#Post-processing)

## Set up

#### Requirements
Set up a virtual environment and run: 
```
pip install -r requirements.txt
```

Follow the [Quick Start](https://github.com/NVIDIA/apex) to enable mixed precision using apex.

#### Download the official evaluation script
Run (from inside the repo):
 
```
git clone https://github.com/conll/reference-coreference-scorers.git
```

#### Prepare the dataset

This repo assumes access to the [OntoNotes 5.0](https://catalog.ldc.upenn.edu/LDC2013T19) corpus.
Convert the original dataset into jsonlines format using:
```
export DATA_DIR=<data_dir>
python minimize.py $DATA_DIR
``` 
Credit: This script was taken from the [e2e-coref](https://github.com/kentonl/e2e-coref/) repo.

## Pre-processing
The folder `conversion_scripts` contains all the scripts required for pre-processing and post-processing.
- To convert the OntoNotes format to the baseline format use the `conversion_scripts/onto_to_format1.py` script.
- To convert the OntoNotes format to our format use the `conversion_scripts/onto_to_format2.py` script. ########FIX THIS!######
- To split the data to chunks (after converting to the desired format):  ########COMPLETE THIS!######

## Training
Train a coreference model using `final_train.py` and your chosen hyperparameters. example for T5 ########COMPLETE THIS!######

## Post-processing
- Use the `conversion_scripts/augment_format.py` on your test file to a format that the models can genarate output for.
- Use the `generate.py` script to generate the classifications for the test set with your trained model. For example:
```
python generate.py --model_path /path/to/your/model --max_seq_length 768 --beam_size 4 --batch_size_1 3 --predict_file /path/to/your/test/file --predict_file_cache /path/to/your/test/file/cache --output_path path/to/output/results/of/generation/to --model_type T5 --conll_path_for_eval /path/to/onto/notes/test/file
```
predict_file- this is the test file after you applied `conversion_scripts/augment_format.py`.
conll_path_for_eval - this is the test file in the original OntoNotes format. If you wish to perform a local test (i.e., the test set is split to chucks as well), use the `conversion_scripts/map_orig_to_chunks.py` to split the OntoNotes format to chunks while keeping it in the original format.

- When using our format, after getting the generation results to the path specified in `output_path`, convert our format to the baseline format using: `conversion_scripts/format2_to_format1.py`.
- When running the global test, you need to stitch all chunks after the generation. This can be done using: `conversion_scripts/postprocess_upgraded_preds.py`.
- To get the final results for your generated output, run:
```
python generate.py --model_path /path/to/your/model --max_seq_length 768 --beam_size 4 --batch_size_1 3 --predict_file /path/to/your/test/file --predict_file_cache /path/to/your/test/file/cache --output_path path/to/final/generation/results --model_type T5 --conll_path_for_eval /path/to/onto/notes/test/file --get_metrics
```
output_path- in case of stitching/ format conversion, this needs to be the path to the results *after* all manipulations.
If you wish to run a local test- add the `--chunks` flag to your command as well. 

