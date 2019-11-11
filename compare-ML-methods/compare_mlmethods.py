import pandas as pd

from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
import random
import time
from optparse import OptionParser

data_sets = {
    "s": {
        "link": "https://s3-us-west-2.amazonaws.com/iqoqo.temp/demo/all_train_10000.csv",
        "size": 10000,
    },
    "m": {
        "link": "https://s3-us-west-2.amazonaws.com/iqoqo.temp/demo/all_train_30000.csv",
        "size": 30000,
    },
    "l": {
        "link": "https://s3-us-west-2.amazonaws.com/iqoqo.temp/demo/all_train_50000.csv",
        "size": 50000,
    },
    "all": {
        "link": "https://s3-us-west-2.amazonaws.com/iqoqo.temp/demo/all_train.csv",
        "size": "5GB",
    },
}


model_dicts = {
    "LogReg": {"model": LogisticRegression, "params": {}},
    "SVM": {"model": SVC, "params": {}},
    "DecTree": {"model": DecisionTreeClassifier, "params": {}},
    "KNN": {"model": KNeighborsClassifier, "params": {}},
    "LinDisc": {"model": LinearDiscriminantAnalysis, "params": {}},
    "GaussianNB": {"model": GaussianNB, "params": {}},
    "MLP": {"model": MLPClassifier, "params": {}},
    "GaussianPC": {"model": GaussianProcessClassifier, "params": {}},
    "RandomForest": {"model": RandomForestClassifier, "params": {}},
    "AdaBoost": {"model": AdaBoostClassifier, "params": {}},
    "QuadraticDisc": {"model": QuadraticDiscriminantAnalysis, "params": {}},
    "SVClinear": {"model": SVC, "params": {"kernel": "linear", "C": 0.025}},
    "SVCgamma": {"model": SVC, "params": {"gamma": 2, "C": 1}},
    "KNN3": {"model": KNeighborsClassifier, "params": {"n_neighbors": 3}},
    "GaussianRBF": {
        "model": GaussianProcessClassifier,
        "params": {"kernel": 1.0 * RBF(1.0)},
    },
    "DecTreeDepth": {"model": DecisionTreeClassifier, "params": {"max_depth": 5}},
    "RandomForestDepth": {
        "model": RandomForestClassifier,
        "params": {"max_depth": 100, "n_estimators": 10, "max_features": 1},
    },
    "MLPalpha": {"model": MLPClassifier, "params": {"alpha": 1}},
}


def model_str(model_name):
    cls = model_dicts[model_name]["model"]
    params = model_dicts[model_name]["params"]
    return f"{cls.__name__}({params})"


def get_model(model_name):
    if model_name in model_dicts.keys():
        cls = model_dicts[model_name]["model"]
        params = model_dicts[model_name]["params"]
        print(model_str(model_name))
        model = cls(**params)
    else:
        print("Model name not found: " + model_name)
        model = None

    return model


def print_results(model_name, results, elapsed):
    if len(results) == 0:
        print(f"{model_name}| Skipped")
    else:
        print(
            f"{model_name} [{elapsed} sec]| Mean={results.mean()} STD={results.std()}"
        )


def analyse(model_name, dset="s"):
    t = time.time()
    try:
        random_seed = random.randint
        # read in the data (HEP)

        print(f"{model_name} {dset}")
        print(f"--- read data set {data_sets[dset]} ---")

        data = pd.read_csv(data_sets[dset]["link"])
        data.dropna(inplace=True)
        elapsed = time.time() - t

        print(f"--- done reading data set elapsed time {elapsed} ---")

        values = data.values
        Y = values[:, 0]
        X = values[:, 1:28]

        model = get_model(model_name)
        if model is None:
            return

        t = time.time()

        print(f"--- starting {model_name} analysis ---")

        k_fold_validation = model_selection.KFold(n_splits=10, random_state=random_seed)
        results = model_selection.cross_val_score(
            model, X, Y, cv=k_fold_validation, scoring="accuracy"
        )

        elapsed = time.time() - t
        print(f"--- done {model_name} analysis elapsed time {elapsed} ---")

        return model_name, results, elapsed
    except Exception as e:
        print(e)
        elapsed = time.time() - t
        return model_name, [], elapsed


def gen_pool_params(model_names, dset):
    return [[m, dset] for m in model_names]


def linear_main(options):
    collected_output = []
    for m in options.model_names:
        collected_output.append(analyse(m, options.data_set_size))
    return collected_output


def mp_main(options):
    from multiprocessing import Pool

    p = Pool(processes=4)
    collected_output = p.starmap(
        analyse, gen_pool_params(options.model_names, options.data_set_size)
    )
    return collected_output


def discomp_main(options):
    import os
    from discomp import Pool

    p = Pool()
    collected_output = p.starmap(
        analyse, gen_pool_params(options.model_names, options.data_set_size)
    )
    return collected_output


execs = {
    "disco": {"ex": discomp_main, "desc": "disco cloud",},
    "linear": {"ex": linear_main, "desc": "sequentially local",},
    "multi_process": {"ex": mp_main, "desc": "multi-process local",},
}


def opts():

    parser = OptionParser()
    models_help = (
        """Specify model(s) to train. May specify more than one: """
        + ", ".join(f"{model_name}" for model_name in model_dicts.keys())
    )

    parser.add_option(
        "-m",
        "--model",
        action="append",
        dest="model_names",
        default=[],
        help=models_help,
    )

    parser.add_option(
        "-a",
        "--all_models",
        action="store_true",
        dest="all_models",
        default=False,
        help="evaluate all models. overrides '-m' option",
    )

    exec_help = "choose execution mode: " + ", ".join(
        f"'{k}' ({v['desc']})" for k, v in execs.items()
    )

    parser.add_option(
        "-e", "--exec_mode", dest="exec_mode", default="linear", help=exec_help
    )

    help_data_set = "choose data set: " + ", ".join(
        f"'{k}' ({v['size']})" for k, v in data_sets.items()
    )
    parser.add_option(
        "-d", "--data_set_size", dest="data_set_size", default="s", help=help_data_set
    )

    options, _ = parser.parse_args()

    if options.all_models:
        options.model_names = model_dicts.keys()
    options.model_names = set(options.model_names)

    return options


def main():
    options = opts()
    print(
        f"Welcome to model comparison demo\n"
        f"Going to run in execution mode {options.exec_mode}\n"
        f"Using data set {options.data_set_size} "
        f"with {data_sets[options.data_set_size]['size']} entries"
    )
    print(f"Evaluating {len(options.model_names)} models: ")
    for model_name in options.model_names:
        print(f"\t{model_name}: {model_str(model_name)}")

    ex = execs[options.exec_mode]["ex"]
    collected_output = ex(options)
    for model, result, elapsed in collected_output:
        print_results(model, result, elapsed)


if __name__ == "__main__":
    main()
