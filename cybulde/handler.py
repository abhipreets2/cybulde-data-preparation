from cybulde.process_data import process_data
from cybulde.train_tokenizer import train_tokenizer

import argparse, sys

parser=argparse.ArgumentParser()

parser.add_argument("--process_data", help="Run the data processing module. Can be True/False")
parser.add_argument("--train_tokenizer", help="Run the tokenizer processing module. Can be True/False")

args=parser.parse_args()
if args.process_data == "True":
    process_data()

if args.train_tokenizer == "True":
    train_tokenizer()
