# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import smuTags_path_pb2 as smuTags__path__pb2


class smuTags_path_ServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.smuTags_path_rpc = channel.unary_unary(
                '/smuTags_path.smuTags_path_Service/smuTags_path_rpc',
                request_serializer=smuTags__path__pb2.smuTagsRequest.SerializeToString,
                response_deserializer=smuTags__path__pb2.smuTagsResponse.FromString,
                )


class smuTags_path_ServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def smuTags_path_rpc(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_smuTags_path_ServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'smuTags_path_rpc': grpc.unary_unary_rpc_method_handler(
                    servicer.smuTags_path_rpc,
                    request_deserializer=smuTags__path__pb2.smuTagsRequest.FromString,
                    response_serializer=smuTags__path__pb2.smuTagsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'smuTags_path.smuTags_path_Service', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class smuTags_path_Service(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def smuTags_path_rpc(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/smuTags_path.smuTags_path_Service/smuTags_path_rpc',
            smuTags__path__pb2.smuTagsRequest.SerializeToString,
            smuTags__path__pb2.smuTagsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
