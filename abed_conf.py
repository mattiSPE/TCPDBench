import copy
import numpy as np

##############################################################################
#                                General Settings                            #
##############################################################################
PROJECT_NAME = "cpdbench"
TASK_FILE = "abed_tasks.txt"
AUTO_FILE = "abed_auto.txt"
RESULT_DIR = "./abed_results"
STAGE_DIR = "./stagedir"
PRUNE_DIR = "./pruned"
MAX_FILES = 1000
ZIP_DIR = "./zips"
LOG_DIR = "./logs"
OUTPUT_DIR = "./output"
AUTO_SLEEP = 120
HTML_PORT = 8000
COMPRESSION = "bzip2"
RESULT_EXTENSION = ".json"

##############################################################################
#                          Server parameters and settings                    #
##############################################################################
REMOTE_USER = "username"
REMOTE_HOST = "address.of.host"
REMOTE_DIR = "/home/%s/projects/%s" % (REMOTE_USER, PROJECT_NAME)
REMOTE_PORT = 22
REMOTE_SCRATCH = None
REMOTE_SCRATCH_ENV = "TMPDIR"

##############################################################################
#                      Settings for Master/Worker program                    #
##############################################################################
MW_SENDATONCE = 1  # number of tasks (hashes!) to send at once
MW_COPY_WORKER = False
MW_COPY_SLEEP = 120
MW_NUM_WORKERS = None

##############################################################################
#                               Experiment type                              #
##############################################################################
# Uncomment the desired type
# Model assessment #
TYPE = "ASSESS_LIST"

# Cross validation with train and test dataset #
# TYPE = 'CV_TT'
# CV_BASESEED = 123456
# YTRAIN_LABEL = 'y_train'

# Commands defined in a text file #
# TYPE = 'RAW'
# RAW_CMD_FILE = '/path/to/file.txt'

##############################################################################
#                                Build settings                              #
##############################################################################
NEEDS_BUILD = False  # If remote compilation is required
BUILD_DIR = "build"  # Relative directory where build takes place
BUILD_CMD = "make all"  # Build command

##############################################################################
#                      Experiment parameters and settings                    #
##############################################################################
DATADIR = "datasets"
EXECDIR = "execs"

DATASETS = [
    "apple",
    "bank",
    "bee_waggle_6",
    "bitcoin",
    "brent_spot",
    "businv",
    "centralia",
    "children_per_woman",
    "co2_canada",
    "construction",
    "debt_ireland",
    "gdp_argentina",
    "gdp_croatia",
    "gdp_iran",
    "gdp_japan",
    "global_co2",
    "homeruns",
    "iceland_tourism",
    "jfk_passengers",
    "lga_passengers",
    "measles",
    "nile",
    "occupancy",
    "ozone",
    "quality_control_1",
    "quality_control_2",
    "quality_control_3",
    "quality_control_4",
    "quality_control_5",
    "rail_lines",
    "ratner_stock",
    "robocalls",
    "run_log",
    "scanline_126007",
    "scanline_42049",
    "seatbelts",
    "shanghai_license",
    "uk_coal_employ",
    "unemployment_nl",
    "usd_isk",
    "us_population",
    "well_log",
]
DATASET_NAMES = {k: k for k in DATASETS}

METHODS = [
    "oracle_binseg", 
    "oracle_bocpd",
    "oracle_bocpdms",
    "oracle_ecp",
    "oracle_kcpa",
    "oracle_pelt",
    "oracle_wbs", 
    "oracle_changeforest",
    "oracle_zero",
    "default_binseg", 
    "default_bocpd", 
    "default_bocpdms", 
    "default_ecp", 
    "default_kcpa", 
    "default_pelt",
    "default_wbs",  
    "default_changeforest",
    "default_zero",
]

R_changepoint_params = {
    "function": ["mean", "var", "meanvar"],
    "penalty": [
        "None",
        "SIC",
        "BIC",
        "MBIC",
        "AIC",
        "Hannan-Quinn",
        "Asymptotic",
    ],
    "statistic": ["Normal", "CUSUM", "CSS", "Gamma", "Exponential", "Poisson"],
}
R_changepoint_params_seg = copy.deepcopy(R_changepoint_params)
R_changepoint_params_seg["Q"] = ["max", "default"]

bocpd_intensities = [10, 50, 100, 200]
bocpd_prior_a = [0.01, 0.1, 1.0, 10, 100]
bocpd_prior_b = [0.01, 0.1, 1.0, 10, 100]
bocpd_prior_k = [0.01, 0.1, 1.0, 10, 100]

cpt_manual_penalty = list(np.logspace(-3, 3, 101))
cpt_penalties = [
    "None",
    "SIC",
    "BIC",
    "MBIC",
    "AIC",
    "Hannan-Quinn",
    "Asymptotic",
]
cpt_Q = ["default", "max"]
cpt_function = ["mean", "var", "meanvar"]
cpt_statistic = {
    "mean": ["Normal", "CUSUM"],
    "var": ["Normal", "CSS"],
    "meanvar": ["Normal", "Gamma", "Exponential", "Poisson"],
}
cptnp_penalties = [p for p in cpt_penalties if not p == "Asymptotic"]
cptnp_quantiles = [10, 20, 30, 40]

pelt_params = [
    {"function": f, "penalty": p, "penvalue": "NULL", "statistic": s}
    for f in cpt_function
    for p in cpt_penalties
    for s in cpt_statistic[f]
] + [
    {"function": f, "penalty": "Manual", "penvalue": pv, "statistic": s}
    for f in cpt_function
    for pv in cpt_manual_penalty
    for s in cpt_statistic[f]
]

binseg_params = [
    {"function": f, "penalty": p, "penvalue": "NULL", "statistic": s, "Q": q}
    for f in cpt_function
    for p in cpt_penalties
    for s in cpt_statistic[f]
    for q in cpt_Q
] + [
    {
        "function": f,
        "penalty": "Manual",
        "penvalue": pv,
        "statistic": s,
        "Q": q,
    }
    for f in cpt_function
    for pv in cpt_manual_penalty
    for s in cpt_statistic[f]
    for q in cpt_Q
]


PARAMS = {
    "oracle_bocpd": [
        {
            "intensity": i,
            "prior_a": a,
            "prior_b": b,
            "prior_k": k,
        }
        for i in bocpd_intensities
        for a in bocpd_prior_a
        for b in bocpd_prior_b
        for k in bocpd_prior_k
    ],
    "oracle_bocpdms": [
        {
            "intensity": i,
            "prior_a": a,
            "prior_b": b,
        }
        for i in bocpd_intensities
        for a in bocpd_prior_a
        for b in bocpd_prior_b
    ],
    "oracle_pelt": pelt_params,
    "oracle_binseg": binseg_params,
    "oracle_ecp": [
        {"algorithm": a, "siglvl": s, "minsize": m, "alpha": v}
        for a in ["e.agglo", "e.divisive"]
        for s in [0.01, 0.05]
        for m in [2, 30]
        for v in [0.5, 1.0, 1.5]
    ],
    "oracle_kcpa": [
        {"maxcp": m, "cost": c}
        for m in ["max", "default"]
        for c in cpt_manual_penalty
    ],
    "oracle_wbs": [
        {"Kmax": K, "penalty": p, "integrated": i}
        for K in ["max", "default"]
        for p in ["SSIC", "BIC", "MBIC"]
        for i in ["true", "false"]
    ],
    "oracle_changeforest": [
        {"n_estimators": n, "max_depth": d, "mtry": m}
        for n in [20,100,500]
        for d in [2, 8, None]
        for m in [1, "sqrt"]
],
    "oracle_zero": [{"no_param": 0}],
    "default_bocpd": [{"no_param": 0}],
    "default_bocpdms": [{"no_param": 0}],
    "default_pelt": [{"no_param": 0}],
    "default_binseg": [{"no_param": 0}],
    "default_ecp": [{"no_param": 0}],
    "default_kcpa": [{"no_param": 0}],
    "default_wbs": [{"no_param": 0}],
    "default_changeforest": [{"no_param": 0}],
    "default_zero": [{"no_param": 0}],
}

COMMANDS = {
    "oracle_binseg": (
        "Rscript --no-save --slave "
        "{execdir}/R/cpdbench_changepoint.R -i {datadir}/{dataset}.json "
        "-p {penalty} -f {function} -t {statistic} -m BinSeg -Q {Q} "
        "--pen.value {penvalue}"
    ),
    "oracle_ecp": (
        "Rscript --no-save --slave "
        "{execdir}/R/cpdbench_ecp.R -i {datadir}/{dataset}.json "
        "-a {algorithm} --siglvl {siglvl} --minsize {minsize} --alpha {alpha}"
    ),
    "oracle_kcpa": (
        "Rscript --no-save --slave "
        "{execdir}/R/cpdbench_ecp.R -i {datadir}/{dataset}.json -a kcpa "
        "--maxcp {maxcp} --cost {cost}"
    ),
    "oracle_pelt": (
        "Rscript --no-save --slave "
        "{execdir}/R/cpdbench_changepoint.R -i {datadir}/{dataset}.json "
        "-p {penalty} -f {function} -t {statistic} -m PELT "
        "--pen.value {penvalue}"
    ),
    "oracle_wbs": (
        "Rscript --no-save --slave "
        "{execdir}/R/cpdbench_wbs.R -i {datadir}/{dataset}.json -K {Kmax} "
        "--penalty {penalty} -g {integrated}"
    ),
    "oracle_bocpd": (
        "Rscript --no-save --slave "
        "{execdir}/R/cpdbench_ocp.R -i {datadir}/{dataset}.json "
        "-l {intensity} --prior-a {prior_a} --prior-b {prior_b} "
        "--prior-k {prior_k}"
    ),
    "oracle_bocpdms": (
        "source {execdir}/python/bocpdms/venv/bin/activate && "
        "python {execdir}/python/cpdbench_bocpdms.py "
        "-i {datadir}/{dataset}.json --intensity {intensity} "
        "--prior-a {prior_a} --prior-b {prior_b} --threshold 100 "
        "--use-timeout"
    ),
    "oracle_changeforest": (
        "source {execdir}/python/changeforest/venv/bin/activate && "
        "python {execdir}/python/changeforest.py "
        "-i {datadir}/{dataset}.json --n-estimators {n_estimators} "
        "--max-depth {max_depth} --mtry {mtry} --use-timeout"
    ), 
    "oracle_zero": (
        "python {execdir}/python/cpdbench_zero.py "
        "-i {datadir}/{dataset}.json"
    ),
    "default_binseg": (
        "Rscript --no-save --slave "
        "{execdir}/R/cpdbench_changepoint.R -i {datadir}/{dataset}.json "
        "-p MBIC -f mean -t Normal -m BinSeg -Q default"
    ),
    "default_pelt": (
        "Rscript --no-save --slave "
        "{execdir}/R/cpdbench_changepoint.R -i {datadir}/{dataset}.json "
        "-p MBIC -f mean -t Normal -m PELT"
    ),
    "default_wbs": (
        "Rscript --no-save --slave "
        "{execdir}/R/cpdbench_wbs.R -i {datadir}/{dataset}.json -K default "
        "-p SSIC -g true"
    ),
    "default_ecp": (
        "Rscript --no-save --slave "
        "{execdir}/R/cpdbench_ecp.R -i {datadir}/{dataset}.json -a e.divisive "
        "--alpha 1.0 --minsize 30 --runs 199 --siglvl 0.05"
    ),
    "default_kcpa": (
        "Rscript --no-save --slave "
        "{execdir}/R/cpdbench_ecp.R -i {datadir}/{dataset}.json -a kcpa "
        "-C 1.0 -L max"
    ),
    "default_bocpd": (
        "Rscript --no-save --slave "
        "{execdir}/R/cpdbench_ocp.R -i {datadir}/{dataset}.json -l 100 "
        "--prior-a 1.0 --prior-b 1.0 --prior-k 1.0"
    ),
    "default_bocpdms": (
        "source {execdir}/python/bocpdms/venv/bin/activate && "
        "python {execdir}/python/cpdbench_bocpdms.py "
        "-i {datadir}/{dataset}.json --intensity 100 --prior-a 1.0 "
        "--prior-b 1.0 --threshold 0"
    ),
    "default_changeforest": (
        "source {execdir}/python/changeforest/venv/bin/activate && "
        "python {execdir}/python/changeforest.py -i {datadir}/{dataset}.json"
    ),
    "default_zero": (
        "python {execdir}/python/cpdbench_zero.py "
        "-i {datadir}/{dataset}.json"
    ),
}

METRICS = {}

SCALARS = {"time": {"best": min}}

RESULT_PRECISION = 15

DATA_DESCRIPTION_CSV = None

REFERENCE_METHOD = None

SIGNIFICANCE_LEVEL = 0.05

###############################################################################
#                                PBS Settings                                 #
###############################################################################
PBS_NODES = 1
PBS_WALLTIME = 360  # Walltime in minutes
PBS_CPUTYPE = None
PBS_CORETYPE = None
PBS_PPN = None
PBS_MODULES = ["mpicopy", "python/2.7.9"]
PBS_EXPORTS = ["PATH=$PATH:/home/%s/.local/bin/abed" % REMOTE_USER]
PBS_MPICOPY = ["datasets", "execs", TASK_FILE]
PBS_TIME_REDUCE = 600  # Reduction of runtime in seconds
PBS_LINES_BEFORE = []
PBS_LINES_AFTER = []
