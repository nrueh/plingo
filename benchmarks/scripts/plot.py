#!/usr/bin/env python
# libraries and data
# from cProfile import label
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
parser.add_argument("--x", type=str, default="", help="Name for the x axis")
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

    if dom == 'grid' and len(df) == 35 and args.type == 'bar':
        # Insert missing P-log instance which timed out (by copying row from below...)
        df = pd.concat([df.iloc[:33], df.iloc[32:].replace('9_6', '9_7')],
                       ignore_index=True)
        df.index += 1
    # elif dom == 'grid' and args.type == 'prob':
    #     df.loc[df.status == 0, "query"] = 0
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
    # print(df)
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
        elif approach == 'azreasoners':
            return 'LPMLN'
        if args.type == 'cactus' and approach == 'plingo' and '_b' in n[1]:
            k = n[1].split('_')[1][1:]
            # return f'k={k}'
            return f'z{k}'  # 'z' added for sorting
        return approach

    # -------- Reorder dfs
    time_df = pd.concat([instances] + [dfs[df]['time'] for df in dfs],
                        axis=1,
                        keys=['instance-name'] +
                        [parse_name(df) for df in dfs])

    if args.type == 'prob':
        query_df = pd.concat([instances] + [dfs[df]['query'] for df in dfs],
                             axis=1,
                             keys=['instance-name'] + [df for df in dfs])

    # ------- Fix wrong timeout times for plingo and LPMLN
    if dom == 'grid':
        lpmln_fixes = ['5_5', '6_5', '6_6', '7_4', '7_5', '8_7', '9_3', '9_9']
        plingo_fixes = ['8_6', '9_6', '9_8']
        time_df.loc[time_df['instance-name'].isin(lpmln_fixes),
                    'LPMLN'] = 1200.0
        time_df.loc[time_df['instance-name'].isin(plingo_fixes),
                    'plingo'] = 1200.0

    approaches_colors = {
        "plingo": "#C8F69B",
        "plingo-unsat": "#7a965e",
        "plingo-problog": "#7a965e",
        "problog": "#FFB1AF",
        "plog": "#D6D4FF",
        "plog-dco": "#83819e",
        "LPMLN": "#B3EEFF"
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

        if dom == 'grid' and 'all' not in args.prefix:
            splits = ['5_5', '7_7', '8_8', '9_9']
            until_idx = [
                time_df.index[time_df['instance-name'] == ins].tolist()[0]
                for ins in splits
            ]
            idxs = list(zip([0] + until_idx[:-1], until_idx))
            partial_dfs = [time_df[idx[0]:idx[1]] for idx in idxs]
            partial_dfs = zip(splits, partial_dfs)
        elif dom == 'grid' and 'all' in args.prefix:
            instances = time_df[~time_df['instance-name'].str.
                                contains("_2")].reset_index(drop=True)[3:15]
            partial_dfs = [('all', instances)]
            prefix = 'runtime'
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

        if dom == 'grid':
            instances = time_df[~time_df['instance-name'].str.
                                contains("_2")].reset_index(drop=True)[3:15]
            partial_dfs = [('all', instances)]

        file_name_img = f'plots/img/{dom}/{prefix}-line.png'
        dir_name = os.path.dirname(file_name_img)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        colors = [approaches_colors[n] for n in time_df.columns[1:]]

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
            plt.ylim(bottom=0.8)
        plt.savefig(file_name_img, dpi=300, bbox_inches='tight')
        print("Saved {}".format(file_name_img))
        plt.clf()

    elif args.type == 'prob':
        app_names = query_df.columns[1:-1]
        true_prob = list(query_df[query_df.columns[-1]].to_numpy())

        file_name_img = f'plots/img/{dom}/{prefix}-all.png'
        dir_name = os.path.dirname(file_name_img)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # for labels in [app_names[:3], app_names[3:]]:
        for name in app_names:
            # min = str(labels[0][1]).split('_')[1][1:]
            # max = str(labels[-1][1]).split('_')[1][1:]
            # file_name_img = f'plots/img/{dom}/{prefix}-{min}-{max}.png'

            # k = str(name[1]).split("_")[1][1:]
            label = f'k = 10^{len(name[1][5:])}'

            abs_error = np.abs(true_prob - query_df[name].to_numpy()) * 100
            rel_error = (abs_error / true_prob) * 100

            print(label)
            print(
                f'Avg. error: {abs_error.mean():.1f} +- {abs_error.std():.1f}')
            print(f'Max error: {abs_error.max():.1f}')
            # print(
            #     f'Avg. relative error: {rel_error.mean():.2f} +- {rel_error.std():.2f}'
            # )
            print("")

            plt.scatter(x=true_prob,
                        y=query_df[name].to_numpy(),
                        marker='x',
                        label=label,
                        s=15,
                        lw=0.5)

        plt.title(f"{dom} {opt}", fontsize=12, fontweight=0)
        plt.axline([0, 0], [1, 1], color='grey', ls='dashed', lw=0.5)
        plt.xlim(left=0.5, right=1)
        plt.ylim(bottom=0.5, top=1)
        plt.xticks([i * 0.1 for i in range(5, 11)])
        plt.legend(loc='lower right')

        plt.xlabel(args.x)
        # plt.xticks(rotation='horizontal')
        plt.ylabel(args.y)

        plt.savefig(file_name_img, dpi=300, bbox_inches='tight')
        print("Saved {}".format(file_name_img))
        plt.clf()

    elif args.type == 'cactus':
        time_df.replace(1200, 1e5, inplace=True)

        app_names = time_df.columns[1:].sort_values()
        file_name_img = f'plots/img/{dom}/{prefix}-cactus.png'
        dir_name = os.path.dirname(file_name_img)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        for name in app_names:
            runtimes = time_df[name].sort_values().to_numpy()

            ls = 'solid'
            if name.startswith('z'):
                name = f'k = 10^{len(name[2:])}'
                ls = 'dashed'

            x = np.arange(len(runtimes))
            # color = approaches_colors[name]
            plt.plot(
                x,
                runtimes,
                ls=ls,
                #  color=color,
                lw=1,
                # marker='x',
                # ms=5,
                label=name)

        plt.ylim(bottom=0, top=800)
        plt.xlim(left=0)
        plt.grid()
        plt.legend()

        plt.title(f"{dom} {opt}", fontsize=12, fontweight=0)
        plt.xlabel(args.x)
        plt.xticks(list(range(10, 40, 10)))
        plt.ylabel(args.y)

        plt.savefig(file_name_img, dpi=300, bbox_inches='tight')
        print("Saved {}".format(file_name_img))
        plt.clf()
