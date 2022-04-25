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
    "--stat",
    type=str,
    action='append',
    help=
    "Status: choices,conflicts,cons,csolve,ctime,error,mem,memout,models,ngadded,optimal,restarts,status,time,timeout,vars,ptime"
)
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
# parser.add_argument("--name", type=str,
# help="Name of benchmark bm")
# parser.add_argument("--horizon", type=int, action='append',
#         help="Horizon to be plotted. Can pass multiple",required=True)
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
    elif dom == 'alzheimer_problog':
        # Sort by ascending order (instance names are integers)
        df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], downcast="integer")
        df.sort_values(['instance-name'], inplace=True, ignore_index=True)
    print(df)
    return df


# ------- Aux for tex output
def csv2textable(df,
                 ins,
                 approaches,
                 spetial_words,
                 base_headers=[""],
                 caption=None,
                 limitter='stats'):
    n_base_headers = len(base_headers)
    non_mc_approaches = [x for x in approaches if x != 'nc']
    used_words = {}
    formats = {'stats': 'textbf', 'ins': 'texttt', 'cons': 'texttt'}

    def f_tex(x):
        if isinstance(x, np.floating):
            if np.isnan(x):
                return "\\color{red}{-}"
            return str(f'{int(x):,}')
        if x in spetial_words:
            to_ret = ""
            word_type = spetial_words[x]
            if word_type in used_words:
                if used_words[word_type] != x:
                    to_ret = f'\\{formats[word_type]}' + '{' + x + '}'
                    if word_type == limitter:
                        to_ret = '\\hline' + to_ret
            else:
                to_ret = f'\\{formats[word_type]}' + '{' + x + '}'
                if word_type == limitter:
                    to_ret = '\\hline' + to_ret
            used_words[word_type] = x

            return to_ret
        if type(x) is str and x[-1] == '~':
            return '\\sout{' + x[:-1] + '}'
        if type(x) is str and x[-1] == '*':
            val = str(f'{int(x[:-1]):,}')
            return "\\textbf{" + val + "}"
        if type(x) is int:
            return str(f'{x:,}')
        if x == "NaN":
            return "\\color{red}{-}"
        return str(f'{int(x):,}')

    cons_name = "\\texttt{" + cons.replace('_', ' ') + "}"
    ins_name = "\\texttt{" + ins.replace('_', ' ') + "}"
    app_names = df.columns[n_base_headers:] if use_gmean else df.columns[
        n_base_headers + 1:]
    if use_lambda:
        approaches_map = {
            "afw": "\\WFA",
            "dfa-mso": "\\WFMm",
            "dfa-stm": "\\WFMs",
            "telingo": "\\WFT",
            "nc": "\\WFNC"
        }
        headers = base_headers + ["$\\lambda$"] + [
            "$" + approaches_map[str(c)] + "$" for c in app_names
        ]
    else:
        headers = base_headers + ["", "H"] + [
            "\\textbf{" + str(c) + "}" for c in app_names
        ]

    if use_gmean:
        headers = headers[0:n_base_headers] + headers[n_base_headers + 1:]

    models_str = f"getting {'one model' if models==1 else 'all_models'}"
    column_format = f'|{"l"*n_base_headers}{"" if use_gmean else "l"}|{"r"*len(non_mc_approaches)}{"|r" if "nc" in approaches else ""}|'
    if caption is None:
        caption = f"Statistics instance {ins_name} {models_str}. Crossed out lambdas are those for which the instance was UNSAT with the constraint. Best performance excluding NC (No Constraint) is found in bold."
    tex_table = df.to_latex(index=False,
                            caption=caption,
                            formatters=[f_tex] * len(df.columns),
                            escape=False,
                            header=headers,
                            label=f"tbl:eval:{cons}:{ins}",
                            column_format=column_format,
                            na_rep="\\color{red}{-}")
    return tex_table


if __name__ == "__main__":
    dom = args.dom

    # Approaches
    approaches = [(a.split(".")[0], a.split(".")[1]) for a in args.approach]
    n_approaches = len(args.approach)
    approaches.sort()

    opt = args.opt

    # Statistics
    stats = args.stat
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
        STATS: {stats}
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
            last_df = df
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
        return approach

    # -------- Reorder dfs
    instances = last_df['instance-name']
    time_df = pd.concat([instances] + [dfs[df]['time'] for df in dfs],
                        axis=1,
                        keys=['instance-name'] +
                        [parse_name(df) for df in dfs])
    if 'query' in last_df.columns:
        query_df = pd.concat([instances] + [dfs[df]['query'] for df in dfs],
                             axis=1,
                             keys=['instance-name'] + [df for df in dfs])

    approaches_colors = {
        "plingo": "#C8F69B",
        "plingo-unsat": "#7a965e",
        "problog": "#FFB1AF",
        "plog": "#D6D4FF",
        "plog-dco": "#83819e",
        "azreasoners": "#B3EEFF"
    }

    if args.type == "table":
        # -------- Save CVS
        for ins, df in dfs_per_instance.items():
            file_name_csv = f'./plots/tables/{dom}/{prefix}-{ins}.csv'
            file_name_tex_csv = file_name_csv[:-3] + "tex"
            dir_name = os.path.dirname(file_name_csv)
            if not os.path.exists(dir_name): os.makedirs(dir_name)

            # Compute gmean
            # if use_gmean:
            #     mx_gmeans = []
            #     for s in [y for y in stats if y!='status']:
            #         df_s = df[df['Stat']==s]
            #         gmeans = []
            #         for app in approaches:
            #             arr_app = df_s[app].to_numpy()
            #             arr_app = [arr_app[~np.isnan(arr_app)]]
            #             gmean = list(scipy.stats.gmean(arr_app,axis=1))
            #             if len(gmean)==0:
            #                 gmean= [np.NaN]
            #             gmeans.append(gmean[0])
            #         row_list=[s]+gmeans
            #         mx_gmeans.append(row_list)
            #     df = pd.DataFrame(mx_gmeans, columns=["Stat"]+approaches)

            # Add mark to minimum value
            non_mc_approaches = [x for x in approaches if x != 'nc']
            mins = df[non_mc_approaches].min(axis=1)
            min_mx = df[non_mc_approaches].astype(float).eq(mins, axis=0)
            for c in min_mx.columns:
                for row in df.index:
                    str_value = "NaN" if math.isnan(df.loc[row, c]) else str(
                        int(df.loc[row, c]))
                    # str_value = "\\color{red}{-}" if math.isnan(df.loc[row,c]) else str(f'{int(df.loc[row,c]):,}')
                    df.loc[row,
                           c] = str_value + "*" if min_mx.loc[row,
                                                              c] else str_value
            if args.csv:
                df.to_csv(file_name_csv, float_format='%.0f', index=False)

            tex_table = csv2textable(df,
                                     ins,
                                     approaches,
                                     spetial_words={s: 'stats'
                                                    for s in stats})

            f = open(file_name_tex_csv, "w")
            f.write(tex_table)
            f.close()
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
                plt.ylim(bottom=0.1, top=2000)
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
        time_df.plot(x='instance-name', y=time_df.columns[1:], color=colors)

        plt.title(f"{dom} {opt}", fontsize=12, fontweight=0)
        plt.xlabel(args.x)
        plt.xticks(rotation='horizontal')
        plt.ylabel(args.y)

        if dom == 'squirrel':
            plt.yscale('log')
            plt.ylim(bottom=0.1, top=1400)
            plt.axhline(1200, color='gray', ls='dashdot')
        plt.yscale('log')
        plt.savefig(file_name_img, dpi=300, bbox_inches='tight')
        print("Saved {}".format(file_name_img))
        plt.clf()
