# coding: utf-8
import argparse
import re

import global_variables as gv
import filetools
gv._init()


def show_gv():
    gv_dict = gv.get_all_value()
    print("#------Show the global variables------#")
    for key in gv_dict.keys():
        print("{}:{}".format(key, gv_dict[key]))
    print("#-------------------------------------#")


def set_global_variables(args):
    cfg_fp = args.darknet_p + '/cfg/' + args.cfg_fn
    data_fp = args.darknet_p + '/cfg/' + args.data_fn
    weight_fp = args.weight_fp

    with open(data_fp, 'r') as f:
        options = f.readlines()
        options = [op.strip('\n').split('=') for op in options]
        options = dict(options)

    args.cfg_fn = args.cfg_fn.strip('.cfg')
    args.data_fn = args.data_fn.strip('.data')
    key_name = args.data_fn

    train_fn = options['train'].split('/')[-1]
    valid_fn = options['valid'].split('/')[-1]
    cls_fp = options['names']
    result_p = options['results']
    backup_p = options['backup']

    filetools.check_makedir(result_p)
    filetools.check_makedir(backup_p)
    filetools.check_makedir(result_p+'/cache')

    dataset_p = re.sub('/filelist/.*', '', options['train'])

    gv.set_value('key_name', key_name)
    gv.set_value('cfg_fp', cfg_fp)
    gv.set_value('data_fp', data_fp)
    gv.set_value('cls_fp', cls_fp)
    gv.set_value('result_p', result_p)
    gv.set_value('backup_p', backup_p)
    gv.set_value('dataset_p', dataset_p)
    gv.set_value('train_fn', train_fn)
    gv.set_value('valid_fn', valid_fn)
    gv.set_value('weight_fp', weight_fp)
    show_gv()


def start(args):
    set_global_variables(args)
    import operations
    if args.order == 'train':
        operations.train(args)

    elif args.order == 'valid':
        args.draw_option = 'mAP'
        operations.valid(args)
        operations.compute(args)
        operations.draw(args)
        print("#------valid process is over!------#")

    elif args.order == 'draw':
        operations.draw(args)
    elif args.order == 'compute':
        # if args.compute_step is None:
        #     print("The compute_step cannot be None!")
        #     exit()
        operations.compute(args)


def get_arguments():
    """Parse all the arguments provided from the CLI.

    Returns:
      A list of parsed arguments.
    """

    Order = 'draw'
    DarkNet_P = '/home/gzh/gzh_need/pack'
    Cfg_FN = 'anngic_half_test_5.cfg'
    Data_FN = 'imagenet_anngic5.data'
    Weight_FP = ''
    GPUs = '1'
    DrawOption = 'mAP'
    ComputeStep = None
    ValidStep = None

    parser = argparse.ArgumentParser(description="Unity Scripts Project for Model Training")
    parser.add_argument("--order", type=str, default=Order,
                        help="")
    parser.add_argument("--darknet_p", type=str, default=DarkNet_P,
                        help="")
    parser.add_argument("--cfg_fn", type=str, default=Cfg_FN,
                        help="")
    parser.add_argument("--data_fn", type=str, default=Data_FN,
                        help="")
    parser.add_argument("--weight_fp", type=str, default=Weight_FP,
                        help="")
    parser.add_argument("--gpus", type=str, default=GPUs,
                        help="")
    parser.add_argument("--draw_option", type=str, default=DrawOption,
                        help="")
    parser.add_argument("--compute_step", type=str, default=ComputeStep,
                        help="")
    parser.add_argument("--valid_step", type=str, default=ValidStep,
                        help="")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_arguments()
    start(args)
