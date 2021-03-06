# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import serverAvailability_pb2 as serverAvailability__pb2


class serverAvailStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.serverAvailability = channel.unary_unary(
                '/serverAvailablility.serverAvail/serverAvailability',
                request_serializer=serverAvailability__pb2.AvailabilityRequest.SerializeToString,
                response_deserializer=serverAvailability__pb2.AvailabilityResponse.FromString,
                )


class serverAvailServicer(object):
    """Missing associated documentation comment in .proto file."""

    def serverAvailability(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_serverAvailServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'serverAvailability': grpc.unary_unary_rpc_method_handler(
                    servicer.serverAvailability,
                    request_deserializer=serverAvailability__pb2.AvailabilityRequest.FromString,
                    response_serializer=serverAvailability__pb2.AvailabilityResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'serverAvailablility.serverAvail', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class serverAvail(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def serverAvailability(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/serverAvailablility.serverAvail/serverAvailability',
            serverAvailability__pb2.AvailabilityRequest.SerializeToString,
            serverAvailability__pb2.AvailabilityResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
