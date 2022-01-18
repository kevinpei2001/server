# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import tags_pb2 as tags__pb2


class TagsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.authorizeClient = channel.unary_unary(
                '/tags.Tags/authorizeClient',
                request_serializer=tags__pb2.AuthorizeRequest.SerializeToString,
                response_deserializer=tags__pb2.AuthorizeResponse.FromString,
                )
        self.connectServer = channel.unary_unary(
                '/tags.Tags/connectServer',
                request_serializer=tags__pb2.ConnectRequest.SerializeToString,
                response_deserializer=tags__pb2.ConnectResponse.FromString,
                )
        self.disconnectServer = channel.unary_unary(
                '/tags.Tags/disconnectServer',
                request_serializer=tags__pb2.DisconnectRequest.SerializeToString,
                response_deserializer=tags__pb2.DisconnectResponse.FromString,
                )
        self.queryTags = channel.unary_unary(
                '/tags.Tags/queryTags',
                request_serializer=tags__pb2.ReadTagRequest.SerializeToString,
                response_deserializer=tags__pb2.ReadTagResponse.FromString,
                )
        self.writeTags = channel.unary_unary(
                '/tags.Tags/writeTags',
                request_serializer=tags__pb2.WriteTagRequest.SerializeToString,
                response_deserializer=tags__pb2.WriteTagResponse.FromString,
                )
        self.declareTags = channel.unary_unary(
                '/tags.Tags/declareTags',
                request_serializer=tags__pb2.DeclareRequest.SerializeToString,
                response_deserializer=tags__pb2.DeclareResponse.FromString,
                )
        self.addTags = channel.unary_unary(
                '/tags.Tags/addTags',
                request_serializer=tags__pb2.AddItemsRequest.SerializeToString,
                response_deserializer=tags__pb2.AddItemsResponse.FromString,
                )
        self.removeTags = channel.unary_unary(
                '/tags.Tags/removeTags',
                request_serializer=tags__pb2.RemoveItemsRequest.SerializeToString,
                response_deserializer=tags__pb2.RemoveItemsRequest.FromString,
                )


class TagsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def authorizeClient(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def connectServer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def disconnectServer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def queryTags(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def writeTags(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def declareTags(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def addTags(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def removeTags(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TagsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'authorizeClient': grpc.unary_unary_rpc_method_handler(
                    servicer.authorizeClient,
                    request_deserializer=tags__pb2.AuthorizeRequest.FromString,
                    response_serializer=tags__pb2.AuthorizeResponse.SerializeToString,
            ),
            'connectServer': grpc.unary_unary_rpc_method_handler(
                    servicer.connectServer,
                    request_deserializer=tags__pb2.ConnectRequest.FromString,
                    response_serializer=tags__pb2.ConnectResponse.SerializeToString,
            ),
            'disconnectServer': grpc.unary_unary_rpc_method_handler(
                    servicer.disconnectServer,
                    request_deserializer=tags__pb2.DisconnectRequest.FromString,
                    response_serializer=tags__pb2.DisconnectResponse.SerializeToString,
            ),
            'queryTags': grpc.unary_unary_rpc_method_handler(
                    servicer.queryTags,
                    request_deserializer=tags__pb2.ReadTagRequest.FromString,
                    response_serializer=tags__pb2.ReadTagResponse.SerializeToString,
            ),
            'writeTags': grpc.unary_unary_rpc_method_handler(
                    servicer.writeTags,
                    request_deserializer=tags__pb2.WriteTagRequest.FromString,
                    response_serializer=tags__pb2.WriteTagResponse.SerializeToString,
            ),
            'declareTags': grpc.unary_unary_rpc_method_handler(
                    servicer.declareTags,
                    request_deserializer=tags__pb2.DeclareRequest.FromString,
                    response_serializer=tags__pb2.DeclareResponse.SerializeToString,
            ),
            'addTags': grpc.unary_unary_rpc_method_handler(
                    servicer.addTags,
                    request_deserializer=tags__pb2.AddItemsRequest.FromString,
                    response_serializer=tags__pb2.AddItemsResponse.SerializeToString,
            ),
            'removeTags': grpc.unary_unary_rpc_method_handler(
                    servicer.removeTags,
                    request_deserializer=tags__pb2.RemoveItemsRequest.FromString,
                    response_serializer=tags__pb2.RemoveItemsRequest.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tags.Tags', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Tags(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def authorizeClient(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tags.Tags/authorizeClient',
            tags__pb2.AuthorizeRequest.SerializeToString,
            tags__pb2.AuthorizeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def connectServer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tags.Tags/connectServer',
            tags__pb2.ConnectRequest.SerializeToString,
            tags__pb2.ConnectResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def disconnectServer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tags.Tags/disconnectServer',
            tags__pb2.DisconnectRequest.SerializeToString,
            tags__pb2.DisconnectResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def queryTags(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tags.Tags/queryTags',
            tags__pb2.ReadTagRequest.SerializeToString,
            tags__pb2.ReadTagResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def writeTags(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tags.Tags/writeTags',
            tags__pb2.WriteTagRequest.SerializeToString,
            tags__pb2.WriteTagResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def declareTags(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tags.Tags/declareTags',
            tags__pb2.DeclareRequest.SerializeToString,
            tags__pb2.DeclareResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def addTags(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tags.Tags/addTags',
            tags__pb2.AddItemsRequest.SerializeToString,
            tags__pb2.AddItemsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def removeTags(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tags.Tags/removeTags',
            tags__pb2.RemoveItemsRequest.SerializeToString,
            tags__pb2.RemoveItemsRequest.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)