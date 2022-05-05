import ipaddress

from ariadne import ScalarType
from bson import ObjectId
from graphql import GraphQLError
from utils.constants import ID_NOT_FOUND

datetime_scalar = ScalarType("Datetime")
ip_scalar = ScalarType("IP")
input_id_scalar = ScalarType("InputId")
network_id_scalar = ScalarType("NetworkId")
input_id_filtered = ScalarType("FilterById")


@datetime_scalar.serializer
def serialize_datetime(value):
    """
    :param value: datetime object
    :return: isoformat value of datetime
    """
    return value.isoformat()


@ip_scalar.value_parser
def serialize_ip(value):
    """
    :param value: String of ip
    :return: valid ip if it's correct
    """
    try:
        ipaddress.ip_address(value)
        return value
    except Exception as error:
        raise GraphQLError(f"{error}")


@input_id_scalar.value_parser
def validate_input_id(value):
    """
    :param value: core ID
    :return: ID
    Check if the core ID is a valid ObjectId
    """
    if ObjectId.is_valid(value):
        return ObjectId(value)
    raise GraphQLError(ID_NOT_FOUND)


@input_id_filtered.value_parser
def input_id(_id):
    """
    :param _id: String
    :return: Object id or String
    Transform String into ObjectId if it's possible
    """
    if ObjectId.is_valid(_id):
        return ObjectId(_id)
    return _id
