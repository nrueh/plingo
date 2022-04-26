#!/usr/bin/env python
# libraries and data
import os
import math
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import itertools
# import seaborn as sns
from pandas_ods_reader import read_ods
# import scipy
# from scipy import stats
# import re
# import tikzplotlib

import argparse

parser = argparse.ArgumentParser(
    description='Plot obs files from benchmark tool',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
    "--approach",
    "-a",
    type=str,
    action='append',
    help=
    "Approach to be plotted folowed by name devided by a dot. Can pass multiple",
    required=True)
parser.add_argument("--dom", "-d", type=str, default='', help="Name of domain")
parser.add_argument("--opt",
                    "-o",
                    type=str,
                    default='mpe',
                    help="mpe, sample or exact")
parser.add_argument(
    "--models",
    type=int,
    default=1,
    help="Number of models computed in the benchmark with clingo -n")
parser.add_argument("--prefix",
                    type=str,
                    default="",
                    help="Prefix for output files")
parser.add_argument(
    "--csv",
    default=False,
    action='store_true',
    help="When this flag is passed, the table is also saved in csv format")
parser.add_argument(
    "--plotmodels",
    default=False,
    action='store_true',
    help="When this flag is passed, the number of models in plotted")
parser.add_argument("--type",
                    "-t",
                    type=str,
                    default="bar",
                    help="bar, line table")
parser.add_argument("--instance",
                    type=str,
                    default=None,
                    help="The name of a single instance")
parser.add_argument("--ignore_prefix",
                    type=str,
                    action='append',
                    help="Prefix to ignore in the instances")
parser.add_argument("--ignore_any",
                    type=str,
                    action='append',
                    help="Any to ignore in the instances")
parser.add_argument("--y", type=str, default=None, help="Name for the y axis")
parser.add_argument("--x",
                    type=str,
                    default="Horizon",
                    help="Name for the x axis")
args = parser.parse_args()


class ParseInstanceNames:

    def default(self, i):
        return i

    def grid(self, i):
        return i[5:].split('.')[0]

    def nasa(self, i):
        return i[5:].split('.')[0].upper()

    def squirrel(self, i):
        return i[8:].split('.')[0]

    def blocks(self, i):
        return i.split('.')[0].replace('blockmap', '').replace('L', '')

    def alzheimer_problog(self, i):
        return i.split('n')[0]

    def smokers(self, i):
        return i.split('.')[0].split('-')[1]


name_parser = ParseInstanceNames()


# ------ Clean ods
def clean_df(df):

    all_stats = set(df.iloc[0][:])
    all_stats.remove('')
    all_stats = list(all_stats)
    n_all_stats = len(all_stats)
    #Drop min max median
    df.drop(df.columns[-3 * n_all_stats:], axis=1, inplace=True)
    #Rename columns
    all_constraints = df.columns[1:]
    all_constraints = [
        c.split("/")[-1] for i, c in enumerate(all_constraints)
        if i % n_all_stats == 0
    ]
    all_stats = df.iloc[0][1:n_all_stats + 1]
    new_cols = [
        p for c, p in list(itertools.product(all_constraints, all_stats))
    ]
    new_cols = ["instance-name"] + new_cols

    df.drop(df.index[0], inplace=True)  # Remove unused out values
    df.drop(df.tail(9).index, inplace=True)  # Remove last computed values
    df.columns = new_cols

    # Convert all to floats
    for i in range(1, len(df.columns)):
        df.iloc[:, i] = pd.to_numeric(df.iloc[:, i], downcast="float")

    ###### Handle rows (INSTANCES)

    # Choose selected instances
    all_instances = df['instance-name']
    if single_instance:
        instances_to_drop = [
            i for i, c in enumerate(all_instances) if c.find(instance) == -1
        ]
        df.drop(df.index[instances_to_drop], inplace=True)
    else:
        instances_to_drop = [
            i for i, c in enumerate(all_instances)
            if any([c.find(i) == 0 for i in ignore_prefix])
        ]
        df.drop(df.index[instances_to_drop], inplace=True)
        instances_to_drop = [
            i for i, c in enumerate(all_instances)
            if any([c.find(i) != -1 for i in ignore_any])
        ]
        df.drop(df.index[instances_to_drop], inplace=True)

    # Rename
    def rename(i):
        return getattr(name_parser, dom, name_parser.default)(i.split("/")[1])

    df['instance-name'] = df['instance-name'].apply(rename)

    if dom == 'grid' and len(df) == 35:
        # Insert missing P-log instance which timed out (by copying row from below...)
        df = pd.concat([df.iloc[:33], df.iloc[32:].replace('9_6', '9_7')],
                       ignore_index=True)
        df.index += 1
    elif dom == 'squirrel':
        # Sort by ascending order (instance names are integers)
        df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], downcast="integer")
        df.sort_values(['instance-name'], inplace=True, ignore_index=True)
        # Keep only non-timeout
        df = df[df.timeout != 1]
    elif dom == 'blocks':
        # Keep only size 20 domain
        df = df[[x.startswith('20')
                 for x in df['instance-name']]].reset_index()
    elif dom == 'alzheimer_problog' or dom == 'smokers':
        # Sort by ascending order (instance names are integers)
        df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], downcast="integer")
        df.sort_values(['instance-name'], inplace=True, ignore_index=True)
    print(df)
    return df


# ------- Aux for marking minimum
def mark_minimum(df):
    mins = df.min(axis=1)
    min_mx = df.eq(mins, axis=0)
    for c in min_mx.columns:
        if c == 'instance-name':
            continue
        for row in df.index:
            str_value = "NaN" if math.isnan(df.loc[row, c]) else str(
                float(df.loc[row, c]))
            # # str_value = "\\color{red}{-}" if math.isnan(df.loc[row,c]) else str(f'{int(df.loc[row,c]):,}')
            df.loc[row, c] = str_value + "*" if min_mx.loc[row,
                                                           c] else str_value
    return df


# ------- Aux for tex output
def csv2textable(df, caption=None):

    def f_names(x):
        return str(x)

    def f_values(x):
        if type(x) is str and x[-1] == '*':
            val = str(f'{float(x[:-1]):.2f}')
            return f'\\textbf{{{val}s}}'
        return str(f'{float(x):.2f}s')

    app_names = df.columns[1:]
    headers = ['\\textbf{Instance}'] + [f'\\textbf{{{n}}}' for n in app_names]
    column_format = f'|l{"|l"*len(app_names)}|'

    tex_table = df.to_latex(header=headers,
                            index=False,
                            formatters=[f_names] + [f_values] * len(app_names),
                            column_format=column_format,
                            caption=caption,
                            escape=False,
                            label="",
                            na_rep="\\color{red}{-}")
    return tex_table


if __name__ == "__main__":
    dom = args.dom

    # Approaches
    approaches = [(a.split(".")[0], a.split(".")[1]) for a in args.approach]
    n_approaches = len(args.approach)
    approaches.sort()

    opt = args.opt
    prefix = args.prefix

    # Instances
    single_instance = False
    if args.instance:
        single_instance = True
        instance = args.instance
    else:
        ignore_prefix = [] if args.ignore_prefix is None else args.ignore_prefix
        ignore_any = [] if args.ignore_any is None else args.ignore_any

    summary = f"""
    PLOT
        DOM: {dom}
        APPROACHES: {approaches}
        OPT: {opt}
    """

    if single_instance:
        summary += f"    ONLY INSTANCE: {instance}\n"
    else:
        summary += f"    IGNORE INSTANCE: {ignore_any} {ignore_prefix}\n"

    print(summary)

    # -------- Read DFS
    dfs = {}
    for a, n in approaches:
        path = f"results/{a}/{dom}/{opt}/{n}/{n}.ods"
        try:
            print(f"Reading path {path}")
            df = read_ods(path, 1)
            df = clean_df(df)
            dfs[(a, n)] = df
            instances = df['instance-name']
        except Exception as e:
            print(e)
            print("Error reading file {}".format(path))
            sys.exit(1)

    def parse_name(n):
        approach = n[0]
        if approach == 'plog' and n[1] == 'bm_dco':
            return 'plog-dco'
        elif approach == 'plingo' and n[1] == 'bm_unsat':
            return 'plingo-unsat'
        elif n[1] == 'bm_problog':
            return 'plingo-problog'
        return approach

    # -------- Reorder dfs
    time_df = pd.concat([instances] + [dfs[df]['time'] for df in dfs],
                        axis=1,
                        keys=['instance-name'] +
                        [parse_name(df) for df in dfs])

    if 'query' in args.prefix:
        query_df = pd.concat([instances] + [dfs[df]['query'] for df in dfs],
                             axis=1,
                             keys=['instance-name'] + [df for df in dfs])

    approaches_colors = {
        "plingo": "#C8F69B",
        "plingo-unsat": "#7a965e",
        "plingo-problog": "#7a965e",
        "problog": "#FFB1AF",
        "plog": "#D6D4FF",
        "plog-dco": "#83819e",
        "azreasoners": "#B3EEFF"
    }

    if args.type == "table":
        # -------- Save CVS
        file_name_csv = f'./plots/tables/{dom}/{prefix}-all.csv'
        file_name_tex_csv = file_name_csv.replace('.csv', '.tex')
        dir_name = os.path.dirname(file_name_csv)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        if 'runtime' in prefix:
            df = time_df
        elif 'query' in prefix:
            df = query_df

        # Add mark to minimum value
        df = mark_minimum(df)
        if args.csv:
            df.to_csv(file_name_csv, float_format='%.0f', index=False)

        tex_table = csv2textable(df)

        with open(file_name_tex_csv, "w") as f:
            f.write(tex_table)
        if args.csv:
            print("Saved {}".format(file_name_csv))
        print("Saved {}".format(file_name_tex_csv))

    elif args.type == "bar":

        # -------- Bar Plot

        if dom == 'grid':
            splits = ['5_5', '7_7', '8_8', '9_9']
            until_idx = [
                time_df.index[time_df['instance-name'] == ins].tolist()[0]
                for ins in splits
            ]
            idxs = list(zip([0] + until_idx[:-1], until_idx))
            partial_dfs = [time_df[idx[0]:idx[1]] for idx in idxs]
            partial_dfs = zip(splits, partial_dfs)
        else:
            partial_dfs = [('all', time_df)]

        for p in partial_dfs:
            ins = p[0]
            current_df = p[1]
            file_name_img = f'plots/img/{dom}/{prefix}-{ins}.png'
            dir_name = os.path.dirname(file_name_img)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

            colors = [approaches_colors[n] for n in current_df.columns[1:]]

            current_df.plot(x='instance-name',
                            y=current_df.columns[1:],
                            kind="bar",
                            color=colors)

            plt.title(f"{dom} {opt}", fontsize=12, fontweight=0)
            plt.xlabel(args.x)
            plt.xticks(rotation='horizontal')
            plt.ylabel(args.y)

            if dom == 'grid':
                plt.yscale('log')
                plt.ylim(bottom=0.8, top=2000)
                plt.axhline(1200, color='gray', ls='dashdot')

            plt.savefig(file_name_img, dpi=300, bbox_inches='tight')
            print("Saved {}".format(file_name_img))
            plt.clf()

    elif args.type == "line":

        # -------- Line Plot

        file_name_img = f'plots/img/{dom}/{prefix}-line.png'
        dir_name = os.path.dirname(file_name_img)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        colors = [approaches_colors[n] for n in time_df.columns[1:]]

        print(time_df)
        time_df.plot(x='instance-name',
                     y=time_df.columns[1:],
                     color=colors,
                     ls='dashed',
                     marker='x')

        plt.title(f"{dom} {opt}", fontsize=12, fontweight=0)
        plt.xlabel(args.x)
        plt.xticks(rotation='horizontal')
        plt.ylabel(args.y)

        if 'log' in prefix:
            plt.yscale('log')
        plt.savefig(file_name_img, dpi=300, bbox_inches='tight')
        print("Saved {}".format(file_name_img))
        plt.clf()
