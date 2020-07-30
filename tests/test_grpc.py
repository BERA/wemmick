import pytest
import grpc
import grpc_testing
from wemmick import wemmick_pb2
from wemmick.grpc_server import Wemmick


@pytest.fixture(scope="module")
def test_server():
    servicers = {wemmick_pb2.DESCRIPTOR.services_by_name["Wemmick"]: Wemmick()}
    return grpc_testing.server_from_dictionary(
        servicers, grpc_testing.strict_real_time()
    )


def test_HealthCheck(test_server):
    healthcheck_method = test_server.invoke_unary_unary(
        method_descriptor=(
            wemmick_pb2.DESCRIPTOR.services_by_name["Wemmick"].methods_by_name[
                "HealthCheck"
            ]
        ),
        invocation_metadata={},
        request=None,
        timeout=1,
    )

    response, metadata, code, details = healthcheck_method.termination()
    assert response.message == "OK!"
    assert code == grpc.StatusCode.OK
