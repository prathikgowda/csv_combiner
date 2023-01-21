#!/usr/bin/env python3

import argparse
import csv
import os
import pandas as pd
import sys

# checks to see if two dataframes have the same number of column headers and that their contents are the same
def headers_equal(df1, df2):
    df1_header = df1.columns
    df2_header = df2.columns
    return df1_header.equals(df2_header)

# parses the command line arguments using the argparse library and returns
def handle_cli_args(args):
    parser = argparse.ArgumentParser(usage = "%(prog)s csv1 csv2 [csv3...]")
    parser.add_argument("csv1", nargs = 1)
    parser.add_argument("csv2", nargs = "+")
    return parser.parse_args(args)

def combine_csvs(args):
    df = pd.read_csv(args.csv1[0])
    
    df["filename"] = os.path.basename(args.csv1[0])

    for arg in args.csv2:
        df_temp = pd.read_csv(arg)
        df_temp["filename"] = os.path.basename(arg)
        if (not headers_equal(df, df_temp)):
            print("error: files must contain the same headers in order to be combined")
            raise SystemExit()
        df = pd.concat([df, df_temp], ignore_index = True)

    return df

def main():
    args = handle_cli_args(sys.argv[1:])
    print(combine_csvs(args).to_string())
    

if __name__ == "__main__":
    main()
