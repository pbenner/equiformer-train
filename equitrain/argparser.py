import argparse


def add_common_file_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--train-file",
        help    = "Training set xyz file",
        type    = str,
        default = None)
    parser.add_argument("--valid-file",
        help    = "Validation set xyz file",
        type    = str,
        default = None)
    parser.add_argument("--test-file",
        help    = "Test set xyz file",
        type    = str,
        default = None)
    parser.add_argument("--output-dir",
        help    = "Output directory for h5 files",
        type    = str,
        default = "")
    return parser


def add_common_data_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--batch-size",
        help    = "Batch size for computation",
        type    = int,
        default = 16)
    parser.add_argument("--dtype",
        help    = "Set default dtype [float16, float32, float64]",
        type    = str,
        default = "float64")
    parser.add_argument("--workers",
        help    = "Number of data loading workers",
        type    = int,
        default = 4)
    parser.add_argument('--pin-memory',
        help    = 'Pin CPU memory in DataLoader.',
        action  = 'store_true')
    parser.set_defaults(pin_mem=True)
    parser.add_argument("--seed",
        help    = "Random seed for splits",
        type    = int,
        default = 123)
    return parser


def add_model_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--model",
        help    = "Path to a model file",
        type    = str,
        default = None)
    parser.add_argument("--model-wrapper",
        help    = "Model wrapper class [mace]",
        type    = str,
        default = None)
    parser.add_argument("--load-checkpoint",
        help    = "Load full checkpoint",
        type    = str,
        default = None)
    parser.add_argument("--load-checkpoint-model",
        help    = "Load model checkpoint only",
        type    = str,
        default = None)
    parser.add_argument("--energy-weight",
        help    = "Weight for energy loss",
        type    = float,
        default = 1.0)
    parser.add_argument("--forces-weight",
        help    = "Weight for forces loss",
        type    = float,
        default = 1.0)
    parser.add_argument("--stress-weight",
        help    = "Weight for stress loss",
        type    = float,
        default = 1.0)

    return parser


def add_optimizer_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--opt",
        help    = "Optimizer (e.g., adamw)",
        type    = str,
        default = "adamw")
    parser.add_argument("--lr",
        help    = "Learning rate",
        type    = float,
        default = 0.01)
    parser.add_argument("--weight-decay",
        help    = "Weight decay",
        type    = float,
        default = 0.0)
    parser.add_argument('--alpha',
        default = 0.99,
        type    = float,
        help    = 'Smoothing constant (default: 0.99)')
    parser.add_argument('--momentum',
        default = 0.9,
        type    = float,
        help    = 'SGD momentum (default: 0.9)')
    parser.add_argument('--min-lr',
        default = 0.0,
        type    = float,
        help    = 'A lower bound on the learning rate of all param groups or each group respectively (default: 0.0)')
    parser.add_argument('--eps',
        default = 1e-8,
        type    = float,
        help    = 'Term added to the denominator to improve numerical stability (default: 1e-8)')
    parser.add_argument('--plateau-patience',
        type    = int,
        default = 2,
        help    = 'The number of allowed epochs with no improvement after which the learning rate will be reduced (default: 2)')
    parser.add_argument('--plateau-factor',
        type    = float,
        default = 0.5,
        help    = 'Factor by which the learning rate will be reduced. new_lr = lr * factor (default: 0.5)')
    parser.add_argument('--plateau-threshold',
        type    = float,
        default = 1e-4,
        help    = 'Threshold for measuring the new optimum, to only focus on significant changes (default: 1e-4)')
    parser.add_argument('--plateau-mode',
        type    = str,
        default = 'min',
        help    = 'One of min, max. In min mode, lr will be reduced when the quantity monitored has stopped decreasing; in max mode it will be reduced when the quantity monitored has stopped increasing (default: min)')
    parser.add_argument('--decay-rate', '--dr',
        type    = float,
        default = 0.5,
        help    = 'LR decay rate (default: 0.5)')

    return parser


def get_args_parser(script_type: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(f"Equitrain {script_type} script")

    if script_type == "preprocess":
        add_common_file_args(parser)
        add_common_data_args(parser)
        parser.add_argument("--valid-fraction",
            help    = "Fraction of training set for validation",
            type    = float,
            default = 0.1)
        parser.add_argument("--compute-statistics",
            help    = "Estimate statistics from training data",
            action  = "store_true",
            default = False)
        parser.add_argument("--atomic-numbers",
            help    = "List of atomic numbers",
            type    = str,
            default = None)
        parser.add_argument("--atomic-energies",
            help    = "Dictionary of isolated atom energies",
            type    = str,
            default = "average")
        parser.add_argument("--r-max",
            help    = "Cutoff radius for graphs",
            type    = float,
            default = 4.5)
        parser.add_argument("--energy-key",
            help    = "Key of reference energies in training xyz",
            type    = str,
            default = "energy")
        parser.add_argument("--forces-key",
            help    = "Key of reference forces in training xyz",
            type    = str,
            default = "forces")
        parser.add_argument("--stress-key",
            help    = "Key of reference stress in training xyz",
            type    = str,
            default = "stress")


    elif script_type == "train":
        add_common_file_args(parser)
        add_common_data_args(parser)
        add_model_args      (parser)
        add_optimizer_args  (parser)
        parser.add_argument("--epochs",
            help    = "Number of epochs",
            type    = int,
            default = 100)
        parser.add_argument("--scheduler",
            help    = "LR scheduler type",
            type    = str,
            default = "plateau")
        parser.add_argument("--shuffle",
            help    = "Shuffle the training dataset",
            type    = bool,
            default = True)
        parser.add_argument("--print-freq",
            type    = int,
            default = 100,
            help    = "Print interval during one epoch")
        parser.add_argument("--wandb-project",
            help    = "Wandb project name",
            type    = str,
            default = None)

    elif script_type == "predict":
        add_common_file_args(parser)
        add_common_data_args(parser)
        add_model_args(parser)

    return parser


def get_args_parser_preprocess() -> argparse.ArgumentParser:
    return get_args_parser('preprocess')


def get_args_parser_train() -> argparse.ArgumentParser:
    return get_args_parser('train')


def get_args_parser_predict() -> argparse.ArgumentParser:
    return get_args_parser('predict')


class ArgumentError(ValueError):
    """Custom exception raised when invalid or missing argument is present."""
    pass


class ArgsFormatter:
    def __init__(self, args):
        """
        Initialize the ArgsFormatter with parsed arguments.
        :param args: argparse.Namespace object
        """
        self.args = vars(args)  # Convert Namespace to dictionary

    def format(self):
        """
        Format the arguments into a neatly indented string.
        :return: Formatted string of arguments
        """
        max_key_length = max(len(key) for key in self.args.keys())  # Determine alignment width
        return "".join(
            [f"  {key:<{max_key_length}} : {value}\n" if key != "model" else "" for key, value in self.args.items()]
        )

    def __str__(self):
        """
        Return the formatted string when the object is printed.
        """
        return f"Options:\n{self.format()}"


class ArgsFilterSimple:
    def __init__(self, allowed_types=None):
        # Default to basic types if no custom types are provided
        self.allowed_types = allowed_types or (int, float, str, bool, list)

    def is_simple(self, value):
        """Check if a value is of an allowed type."""
        return isinstance(value, self.allowed_types)
    
    def filter(self, args):
        """Filter the list of arguments to include only allowed types."""
        return { key: value for key, value in vars(args).items() if self.is_simple(value) }
