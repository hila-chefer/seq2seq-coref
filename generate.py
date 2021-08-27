from __future__ import absolute_import, division, print_function

import logging
import os
import shutil
import git
import torch
import ast
from transformers import BartTokenizer, T5Tokenizer, BartForConditionalGeneration, T5ForConditionalGeneration
from conversion_scripts import format1_to_clusters
from conversion_scripts import post_process
# from conversion_scripts import post_process_no_space as post_process
from data import get_dataset_generate
from cli_generate import parse_args
from utils import write_meta_data
from conll import evaluate_conll
from training import set_seed
logger = logging.getLogger(__name__)
from coref_bucket_batch_sampler import BucketBatchSampler
import json

def main():
    args = parse_args()

    transformers_logger = logging.getLogger("transformers")
    transformers_logger.setLevel(logging.ERROR)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    args.n_gpu = torch.cuda.device_count()

    # Setup logging
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        level=logging.INFO)

    for key, val in vars(args).items():
        logger.info(f"{key} - {val}")


    logger.info("device: %s:",device)

    # Set seed
    set_seed(args)

    if args.model_type == 'Bart':
        logger.info("inferring with Bart")
        model = BartForConditionalGeneration.from_pretrained(args.model_path)
        tokenizer = BartTokenizer.from_pretrained(args.model_path)
    elif args.model_type == 'T5':
        logger.info("inferring with T5")
        tokenizer = T5Tokenizer.from_pretrained(args.model_path)
        model = T5ForConditionalGeneration.from_pretrained(args.model_path)
    else:
        raise ValueError(
            "model type {0} not recognized!".format(args.model_type))

    model.to(device)

    eval_dataset = get_dataset_generate(args, tokenizer=tokenizer, evaluate=True)

    # Evaluation
    eval_dataloader = BucketBatchSampler(eval_dataset, max_total_seq_len=args.max_seq_length, batch_size_1=args.batch_size_1)

    # Eval!
    logger.info("***** Running evaluation*****")
    logger.info("  Examples number: %d", len(eval_dataset))
    model.eval()

    # results = []
    # for batch in eval_dataloader:
    #     with torch.no_grad():
    #         # "sentence_len", "input_ids", "sentences", "doc_id"
    #         _, input_ids, sentences, doc_id = batch
    #         input_ids = input_ids.to(device)
    #         summary_ids = model.generate(input_ids, num_beams=args.beam_size, max_length=args.max_seq_length, early_stopping=True)
    #         # replace <unk> special token with actual word
    #         unk_id = tokenizer("unknown", add_special_tokens=False)['input_ids'][0]
    #         final_ids = [[id.item() if id != tokenizer.unk_token_id else unk_id for id in summary_ids[0]]]
    #         decoded = tokenizer.batch_decode(final_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
    #
    #         batch_size = input_ids.shape[0]
    #         for b in range(batch_size):
    #             json_result = {}
    #             json_result['sentences'] = sentences[b]
    #             json_result['doc_id'] = doc_id[b]
    #             json_result['clusters'] = decoded[b]
    #
    #             results.append(json_result)
    #
    # with open(args.output_path, 'w') as f:
    #     for i in results:
    #         json.dump(i, f)
    #         f.write('\n')

    # post process
    post_processed = []
    with open(args.output_path, 'r') as f:
        lines = f.readlines()
        for i in lines:
            dic = ast.literal_eval(i)
            dic['clusters'] = post_process.postprocess(dic['sentences'], dic['clusters'].split())
            post_processed.append(dic)
            with open('{}_processed'.format(args.output_path), 'a+') as f:
                json.dump(dic, f)
                f.write('\n')

    cluster_format = format1_to_clusters.convert_file('{}_processed'.format(args.output_path))
    predictions = []
    for dic in cluster_format:
        prediction = {}
        prediction['doc_id'] = dic['doc_id']
        prediction['clusters'] = dic['clusters']
        predictions.append(prediction)

    conll_results = evaluate_conll(args.conll_path_for_eval, predictions)
    official_f1 = sum(results["f"] for results in conll_results.values()) / len(conll_results)
    logger.info('Official avg F1: %.4f' % official_f1)

if __name__ == "__main__":
    main()
