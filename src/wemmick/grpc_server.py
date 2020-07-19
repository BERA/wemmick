from concurrent import futures
import grpc
from grpc_reflection.v1alpha import reflection
import wemmick_pb2
import wemmick_pb2_grpc
import wemmick.api


class Wemmick(wemmick_pb2_grpc.WemmickServicer):

    def HelloWorld(self, request, context):
        return wemmick_pb2.Response(message='Hello World!')

    def ListDataSources(self, request, context):
        data_sources = wemmick.api.list_datasources()
        result = []
        for data_source_item in data_sources:
            data_source = wemmick_pb2.DataSource(
                name=data_source_item['name'],
                class_name=data_source_item['class_name'],
                module_name=data_source_item['module_name']
            )
            result.append(data_source)

        return wemmick_pb2.DataSourceList(data_sources=result)

    def ListExpectationSuites(self, request, context):
        suites = wemmick.api.list_expectation_suites()
        result = []
        for suite_item in suites:
            result.append(suite_item.expectation_suite_name)

        return wemmick_pb2.ExpectationSuitesList(expectation_suites=result)

    def CreateExpectationSuiteFromJsonSchema(self, request, context):
        create_suite = wemmick.api.CreateExpectationSuiteFromJsonSchema(
            file_path=request.file_path,
            suite_name=request.suite_name
        )
        create_suite.run()
        return wemmick_pb2.Response(message=f'Successfully created {request.suite_name} expectation suite')

    def CreateExpectationSuiteFromAvroSchema(self, request, context):
        create_suite = wemmick.api.CreateExpectationSuiteFromAvroSchema(
            file_path=request.file_path,
            suite_name=request.suite_name
        )
        create_suite.run()
        return wemmick_pb2.Response(message=f'Successfully created {request.suite_name} expectation suite')

    def RunValidation(self, request, context):
        run_validation = wemmick.api.RunValidation(
            datasource=request.datasource,
            table=request.table,
            suite_name=request.suite_name
        )
        run_validation.run()
        return wemmick_pb2.Response(message=f'Successfully ran {request.suite_name} validation')


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