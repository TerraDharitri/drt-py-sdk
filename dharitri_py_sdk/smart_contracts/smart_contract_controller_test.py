from pathlib import Path

import pytest

from dharitri_py_sdk.abi.abi import Abi
from dharitri_py_sdk.abi.biguint_value import BigUIntValue
from dharitri_py_sdk.abi.small_int_values import U32Value, U64Value
from dharitri_py_sdk.abi.string_value import StringValue
from dharitri_py_sdk.accounts.account import Account
from dharitri_py_sdk.core.address import Address
from dharitri_py_sdk.core.constants import CONTRACT_DEPLOY_ADDRESS_HEX
from dharitri_py_sdk.network_providers.api_network_provider import ApiNetworkProvider
from dharitri_py_sdk.smart_contracts.smart_contract_controller import (
    SmartContractController,
)
from dharitri_py_sdk.smart_contracts.smart_contract_query import (
    SmartContractQuery,
    SmartContractQueryResponse,
)
from dharitri_py_sdk.testutils.mock_network_provider import MockNetworkProvider


class TestSmartContractQueriesController:
    testdata = Path(__file__).parent.parent / "testutils" / "testdata"
    testwallets = Path(__file__).parent.parent / "testutils" / "testwallets"
    alice = Account.new_from_pem(testwallets / "alice.pem")
    bytecode = (testdata / "adder.wasm").read_bytes()
    abi = Abi.load(testdata / "adder.abi.json")

    def test_create_transaction_for_deploy(self):
        controller = SmartContractController(chain_id="D", network_provider=MockNetworkProvider(), abi=self.abi)
        gas_limit = 6000000

        transaction = controller.create_transaction_for_deploy(
            sender=self.alice,
            nonce=self.alice.get_nonce_then_increment(),
            bytecode=self.bytecode,
            gas_limit=gas_limit,
            arguments=[BigUIntValue(1)],
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == Address.new_from_hex(CONTRACT_DEPLOY_ADDRESS_HEX).to_bech32()
        assert transaction.data == f"{self.bytecode.hex()}@0500@0504@01".encode()
        assert transaction.gas_limit == gas_limit
        assert transaction.value == 0

    def test_create_transaction_for_execute(self):
        controller = SmartContractController(chain_id="D", network_provider=MockNetworkProvider(), abi=self.abi)
        contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqpgqhy6nl6zq07rnzry8uyh6rtyq0uzgtk3e69fq4h4xut")
        function = "add"
        gas_limit = 6000000

        transaction = controller.create_transaction_for_execute(
            sender=self.alice,
            nonce=self.alice.get_nonce_then_increment(),
            contract=contract,
            function=function,
            gas_limit=gas_limit,
            arguments=[U32Value(7)],
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqpgqhy6nl6zq07rnzry8uyh6rtyq0uzgtk3e69fq4h4xut"
        assert transaction.gas_limit == gas_limit
        assert transaction.data.decode() == "add@07"
        assert transaction.value == 0

    def test_create_transaction_for_upgrade(self):
        controller = SmartContractController(chain_id="D", network_provider=MockNetworkProvider(), abi=self.abi)
        contract_address = Address.new_from_bech32("drt1qqqqqqqqqqqqqpgqhy6nl6zq07rnzry8uyh6rtyq0uzgtk3e69fq4h4xut")
        gas_limit = 6000000

        transaction = controller.create_transaction_for_upgrade(
            sender=self.alice,
            nonce=self.alice.get_nonce_then_increment(),
            contract=contract_address,
            bytecode=self.bytecode,
            gas_limit=gas_limit,
            arguments=[BigUIntValue(0)],
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqpgqhy6nl6zq07rnzry8uyh6rtyq0uzgtk3e69fq4h4xut"
        assert transaction.data == f"upgradeContract@{self.bytecode.hex()}@0504@".encode()
        assert transaction.gas_limit == gas_limit
        assert transaction.value == 0

    def test_create_query_without_arguments(self):
        controller = SmartContractController(chain_id="D", network_provider=MockNetworkProvider())
        contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqpgqsnwuj85zv7t0wnxfetyqqyjvvg444lpk7uasmss4gc")
        function = "getSum"

        query = controller.create_query(contract=contract, function=function, arguments=[])

        assert query.contract == contract
        assert query.function == function
        assert query.arguments == []
        assert query.caller is None
        assert query.value is None

    def test_create_query_with_arguments(self):
        controller = SmartContractController(chain_id="D", network_provider=MockNetworkProvider())
        contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqpgqsnwuj85zv7t0wnxfetyqqyjvvg444lpk7uasmss4gc")
        function = "getSum"

        query = controller.create_query(
            contract=contract,
            function=function,
            arguments=[U64Value(7), StringValue("abba")],
        )

        assert query.contract == contract
        assert query.function == function
        assert query.arguments == [b"\x07", b"abba"]
        assert query.caller is None
        assert query.value is None

    def test_create_query_with_arguments_with_abi(self):
        abi = Abi.load(self.testdata / "lottery-dcdt.abi.json")
        controller = SmartContractController(chain_id="D", network_provider=MockNetworkProvider(), abi=abi)
        contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqpgqsnwuj85zv7t0wnxfetyqqyjvvg444lpk7uasmss4gc")
        function = "getLotteryInfo"

        query = controller.create_query(contract=contract, function=function, arguments=["myLottery"])

        query_with_typed = controller.create_query(
            contract=contract, function=function, arguments=[StringValue("myLottery")]
        )

        assert query.contract == contract
        assert query.function == function
        assert query.arguments == [b"myLottery"]
        assert query.caller is None
        assert query.value is None

        assert query_with_typed == query

    def test_run_query_with_mock_provider(self):
        network_provider = MockNetworkProvider()
        controller = SmartContractController(chain_id="D", network_provider=network_provider)

        contract_query_response = SmartContractQueryResponse(
            function="bar",
            return_code="ok",
            return_message="",
            return_data_parts=["abba".encode()],
        )

        network_provider.mock_query_contract_on_function("bar", contract_query_response)

        query = SmartContractQuery(
            contract=Address.new_from_bech32("drt1qqqqqqqqqqqqqpgqvc7gdl0p4s97guh498wgz75k8sav6sjfjlwq2xfx36"),
            function="bar",
            arguments=[],
        )

        response = controller.run_query(query)
        assert response.return_code == "ok"
        assert response.return_data_parts == ["abba".encode()]

    def test_parse_query_response(self):
        controller = SmartContractController(chain_id="D", network_provider=MockNetworkProvider())

        response = SmartContractQueryResponse(
            function="bar",
            return_code="ok",
            return_message="ok",
            return_data_parts=["abba".encode()],
        )

        parsed = controller.parse_query_response(response)
        assert parsed == ["abba".encode()]

    def test_parse_query_response_with_abi(self):
        abi = Abi.load(self.testdata / "lottery-dcdt.abi.json")
        controller = SmartContractController(chain_id="D", network_provider=MockNetworkProvider(), abi=abi)

        response = SmartContractQueryResponse(
            function="getLotteryInfo",
            return_code="ok",
            return_message="ok",
            return_data_parts=[
                bytes.fromhex(
                    "0000000b6c75636b792d746f6b656e000000010100000000000000005fc2b9dbffffffff00000001640000000a140ec80fa7ee88000000"
                )
            ],
        )

        [lottery_info] = controller.parse_query_response(response)
        assert lottery_info.token_identifier == "lucky-token"
        assert lottery_info.ticket_price == 1
        assert lottery_info.tickets_left == 0
        assert lottery_info.deadline == 0x000000005FC2B9DB
        assert lottery_info.max_entries_per_user == 0xFFFFFFFF
        assert lottery_info.prize_distribution == bytes([0x64])
        assert lottery_info.prize_pool == 94720000000000000000000

    @pytest.mark.networkInteraction
    def test_run_query_on_network(self):
        provider = ApiNetworkProvider("https://devnet-api.dharitri.org")
        controller = SmartContractController(chain_id="D", network_provider=provider)
        contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqpgqsnwuj85zv7t0wnxfetyqqyjvvg444lpk7uasmss4gc")
        function = "getSum"

        query = controller.create_query(contract=contract, function=function, arguments=[])

        query_response = controller.run_query(query)
        assert query_response.return_code == "ok"
        assert query_response.return_message == ""
        assert query_response.return_data_parts == [b"\x05"]

    @pytest.mark.networkInteraction
    def test_query_on_network(self):
        provider = ApiNetworkProvider("https://devnet-api.dharitri.org")
        controller = SmartContractController(chain_id="D", network_provider=provider)
        contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqpgqsnwuj85zv7t0wnxfetyqqyjvvg444lpk7uasmss4gc")
        function = "getSum"

        return_data_parts = controller.query(contract=contract, function=function, arguments=[])

        assert return_data_parts == [b"\x05"]
