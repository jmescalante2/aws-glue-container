import json
from functools import partial

import boto3

ssm = boto3.client("ssm")


def get_parameter(parameter_name, convert_to_dict=False, with_decryption=True):
    parameter = ssm.get_parameter(Name=parameter_name, WithDecryption=with_decryption)[
        "Parameter"
    ]["Value"]

    if convert_to_dict:
        parameter = json.loads(parameter)

    return parameter


def put_parameter(parameter_name, value, parameter_type=None, overwrite=True):
    params = {
        "Name": parameter_name,
        "Overwrite": overwrite,
        "Value": value,
    }

    if parameter_type:
        params["Type"] = parameter_type

    ssm.put_parameter(**params)


def try_get_parameter(*args, **kwargs):
    try:
        return get_parameter(*args, **kwargs)
    except ssm.exceptions.ParameterNotFound:
        return None


put_string_parameter = partial(put_parameter, parameter_type="String")
