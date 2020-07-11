from concurrent import futures
import grpc
from grpc_reflection.v1alpha import reflection
import wemmick_pb2
import wemmick_pb2_grpc
import api


class Wemmick(wemmick_pb2_grpc.WemmickServicer):

    def HelloWorld(self, request, context):
        return wemmick_pb2.Response(message='Hello World!')

    def ListDataSources(self, request, context):
        data_sources = api.list_datasources()
        result = []
        for data_source in data_sources:
            credentials = wemmick_pb2.DataSource.Credentials(
                connection_string=data_source['credentials']['connection_string']
            )
            data_source = wemmick_pb2.DataSource(
                name=data_source['name'],
                class_name=data_source['class_name'],
                module_name=data_source['module_name'],
                credentials=credentials
            )
            result.append(data_source)

        return wemmick_pb2.DataSourceList(data_sources=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    wemmick_pb2_grpc.add_WemmickServicer_to_server(Wemmick(), server)
    SERVICE_NAMES = (
        wemmick_pb2.DESCRIPTOR.services_by_name['Wemmick'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()