import base64

from dharitri_py_sdk.core.address import Address
from dharitri_py_sdk.core.transaction_on_network import (
    SmartContractResult,
    TransactionEvent,
    TransactionLogs,
)
from dharitri_py_sdk.delegation import DelegationTransactionsOutcomeParser
from dharitri_py_sdk.testutils.mock_transaction_on_network import (
    get_empty_transaction_on_network,
)
from dharitri_py_sdk.testutils.utils import base64_topics_to_bytes


class TestDelegationTransactionsOutcomeParser:
    parser = DelegationTransactionsOutcomeParser()

    def test_parse_create_new_delegation_contract(self):
        contract_address = Address.new_from_bech32("drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqy8llllssrzx6z")

        encodedTopics = [
            "Q8M8GTdWSAAA",
            "Q8M8GTdWSAAA",
            "AQ==",
            "Q8M8GTdWSAAA",
            "IzMAAAAAAAAAAAAAAAAAAAACMzAAAAAAAAAAAAP///8=",
        ]

        delegate_event = TransactionEvent(
            raw={},
            address=Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"),
            identifier="delegate",
            topics=base64_topics_to_bytes(encodedTopics),
            data=b"",
            additional_data=[],
        )

        encodedTopics = [
            "IzMAAAAAAAAAAAAAAAAAAAACMzAAAAAAAAAAAAP///8=",
            "PDXX6ssamaSgzKpTfvDMCuEJ9B9sK0AiA+Yzv7sHH1w=",
        ]

        sc_deploy_event = TransactionEvent(
            raw={},
            address=Address.new_from_bech32("drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqy8llllssrzx6z"),
            identifier="SCDeploy",
            topics=base64_topics_to_bytes(encodedTopics),
            data=b"",
            additional_data=[],
        )

        logs = TransactionLogs(address=Address.empty(), events=[delegate_event, sc_deploy_event])

        encoded_topics = ["b2g6sUl6beG17FCUIkFwCOTGJjoJJi5SjkP2077e6xA="]
        sc_result_event = TransactionEvent(
            raw={},
            address=Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"),
            identifier="completedTxEvent",
            topics=base64_topics_to_bytes(encoded_topics),
            data=b"",
            additional_data=[],
        )

        sc_result_log = TransactionLogs(
            address=Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"),
            events=[sc_result_event],
        )

        sc_result = SmartContractResult(
            raw={},
            sender=Address.new_from_bech32("drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqyllls4jxmwv"),
            receiver=Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"),
            data=base64.b64decode(
                "QDZmNmJAMjMzMzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAyMzMzMDAwMDAwMDAwMDAwMDAwMDAxMGZmZmZmZg=="
            ),
            logs=sc_result_log,
        )

        tx = get_empty_transaction_on_network()
        tx.smart_contract_results = [sc_result]
        tx.logs = logs

        outcome = self.parser.parse_create_new_delegation_contract(tx)

        assert len(outcome) == 1
        assert outcome[0].contract_address == contract_address
