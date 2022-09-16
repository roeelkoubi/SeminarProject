import pickle

"""  The function Serialized Data To Bytes 
:param self: the function get self as a parameter
:param client: client that we send the data.
:type client: client
:param obj: obj that we send 
:type obj: 
:returns: the function do not return any value.
"""


def SerializedDataToBytes(client, Obj, the_type='text'):
    client.send(pickle.dumps(Obj))


"""  The function  de Serialized Data To Bytes 
:param self: the function get self as a parameter
:param client: client that we send the data.
:type client: client
:returns: the function do not return any value.
"""


def DeSerializedBytesToData(client, data=None):
    if data is None:
        obj = pickle.loads(client.recv(1024))
        return obj
    return pickle.loads(data)
