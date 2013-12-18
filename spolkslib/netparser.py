import re
import argparse

reg_dict = {
    "port": (r"^[0-9]+$", int, lambda x: int(x) in range(0, 65353)),
    "host": (r"^[0-9]{1,3}(\.[0-9]{1,3}){3}$", str,
    lambda x: not (True in map(lambda x: int(x) > 255, x.split(".")))),
    "filename": (r".", str, lambda x: True)
}


def create_parser(*p):

    parser = argparse.ArgumentParser()
    
    if '-t' in p:
        if '-u' in p:
            group = parser.add_mutually_exclusive_group(required=True)
            group.add_argument('-u', '--udp', action='store_true')
            group.add_argument('-t', '--tcp', action='store_true')
        else:
            parser.add_argument('-t', '--tcp', action='store_true')
    if '-s' in p:
        if '-c' in p:
            group = parser.add_mutually_exclusive_group(required=True)
            group.add_argument('-s', '--server',
            type=parse_type("port"), dest='port')

            group.add_argument('-c', '--client', nargs=3,
            type=''.join, dest='args')
        else:
            parser.add_argument('-s', '--server',
            type=parse_type("port"), dest='port')

    if '-v' in p:
            parser.add_argument('-v', '--verbosity', action='store_true')

    return parser


def parse_it(reg_ex, arg_type, check_function=lambda x: True):

    def parse_routine(string):
        m = re.match(reg_ex, string)
        if m and check_function(m.group()):
            return arg_type(m.group())
        else:
            raise argparse.ArgumentTypeError(("%s argument does not match"
            % string))

    return parse_routine


def parse_type(arg_type):

    return parse_it(*(reg_dict[arg_type]))


class ClientInfo:
    pass


def parse_list(values, keys=["host", "port", "filename"]):

    list_dict = ClientInfo()

    for value in values:
        for key in keys:
            reg_ex, arg_type, check_function = reg_dict[key]
            m = re.match(reg_ex, value)
            if m:
                if check_function(value):
                    setattr(list_dict, key, arg_type(value))
                    break
                else:
                    raise argparse.ArgumentTypeError(
                    ("%s argument does not match") % value)

    return list_dict
