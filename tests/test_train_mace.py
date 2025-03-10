from equitrain import get_args_parser_train, train
from equitrain.utility_test import MaceWrapper


def test_train_mace():
    args = get_args_parser_train().parse_args()

    args.train_file = 'data/train.h5'
    args.valid_file = 'data/valid.h5'
    args.test_file = 'data/train.h5'
    args.output_dir = 'test_train_mace'
    args.model = MaceWrapper(args)

    args.epochs = 10
    args.batch_size = 2
    args.lr = 0.001
    args.verbose = 1
    args.tqdm = True

    train(args)


if __name__ == '__main__':
    test_train_mace()
