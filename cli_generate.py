import argparse

MODEL_TYPES = ['longformer']


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--model_path",
        type=str,
        required=True,
        help="Path to pretrained model",
    )

    parser.add_argument("--beam_size", default=-1, required=True, type=int)

    parser.add_argument("--seed", type=int, default=42, help="random seed for initialization")

    parser.add_argument("--experiment_name", type=str, default=None)
    parser.add_argument("--batch_size_1", type=int, default=1)
    parser.add_argument("--conll_path_for_eval", type=str, default=None)
    parser.add_argument("--get_metrics", default=False, action='store_true')
    parser.add_argument("--chunks", default=False, action='store_true')
    parser.add_argument(
        "--predict_file",
        required=True,
        default=None,
        type=str,
        help="The input evaluation file. If a data dir is specified, will look for the file there"
             + "If no data dir or train/predict files are specified, will run with tensorflow_datasets.",
    )
    parser.add_argument("--max_seq_length", default=-1, type=int)
    parser.add_argument(
        "--predict_file_cache",
        default=None,
        type=str,
        required=True,
        help="The output directory where the datasets will be written and read from.",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        required=True,
        help="Path to results file",
    )

    parser.add_argument(
        "--model_type",
        type=str,
        required=True,
        help="Path to results file"
    )

    args = parser.parse_args()
    return args
