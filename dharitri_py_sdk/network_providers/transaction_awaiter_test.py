import pytest

from dharitri_py_sdk.core.address import Address
from dharitri_py_sdk.core.transaction import Transaction
from dharitri_py_sdk.core.transaction_computer import TransactionComputer
from dharitri_py_sdk.core.transaction_on_network import TransactionOnNetwork
from dharitri_py_sdk.core.transaction_status import TransactionStatus
from dharitri_py_sdk.network_providers.api_network_provider import ApiNetworkProvider
from dharitri_py_sdk.network_providers.errors import (
    ExpectedTransactionStatusNotReachedError,
)
from dharitri_py_sdk.network_providers.proxy_network_provider import ProxyNetworkProvider
from dharitri_py_sdk.network_providers.transaction_awaiter import TransactionAwaiter
from dharitri_py_sdk.testutils.mock_network_provider import (
    MockNetworkProvider,
    TimelinePointMarkCompleted,
    TimelinePointWait,
)
from dharitri_py_sdk.testutils.mock_transaction_on_network import (
    get_empty_transaction_on_network,
)
from dharitri_py_sdk.testutils.wallets import load_wallets


class TestTransactionAwaiter:
    provider = MockNetworkProvider()
    watcher = TransactionAwaiter(
        fetcher=provider,
        polling_interval_in_milliseconds=42,
        timeout_interval_in_milliseconds=42 * 42,
        patience_time_in_milliseconds=42,
    )

    def test_await_status_executed(self):
        tx_hash = "abbaabbaabbaabbaabbaabbaabbaabbaabbaabbaabbaabbaabbaabbaabbaabba"
        tx_on_network = get_empty_transaction_on_network()
        tx_on_network.status = TransactionStatus("unknown")
        self.provider.mock_put_transaction(tx_hash, tx_on_network)

        self.provider.mock_transaction_timeline_by_hash(
            tx_hash,
            [
                TimelinePointWait(40),
                TransactionStatus("pending"),
                TimelinePointWait(40),
                TransactionStatus("executed"),
                TimelinePointMarkCompleted(),
            ],
        )
        tx_from_network = self.watcher.await_completed(tx_hash)

        assert tx_from_network.status.is_completed

    @pytest.mark.networkInteraction
    def test_on_network(self):
        alice = load_wallets()["alice"]
        proxy = ProxyNetworkProvider("https://devnet-api.dharitri.org")
        watcher = TransactionAwaiter(proxy)
        tx_computer = TransactionComputer()

        transaction = Transaction(
            sender=Address.new_from_bech32(alice.label),
            receiver=Address.new_from_bech32(alice.label),
            gas_limit=50000,
            chain_id="D",
        )
        transaction.nonce = proxy.get_account(Address.new_from_bech32(alice.label)).nonce
        transaction.signature = alice.secret_key.sign(tx_computer.compute_bytes_for_signing(transaction))

        hash = proxy.send_transaction(transaction)
        tx_on_network = watcher.await_completed(hash)
        assert tx_on_network.status.is_completed

    def test_await_on_condition(self):
        tx_hash = "abbaabbaabbaabbaabbaabbaabbaabbaabbaabbaabbaabbaabbaabbaabbaabba"
        tx_on_network = get_empty_transaction_on_network()
        tx_on_network.status = TransactionStatus("unknown")
        self.provider.mock_put_transaction(tx_hash, tx_on_network)

        self.provider.mock_transaction_timeline_by_hash(
            tx_hash,
            [
                TimelinePointWait(40),
                TransactionStatus("pending"),
                TimelinePointWait(40),
                TransactionStatus("pending"),
                TimelinePointWait(40),
                TransactionStatus("failed"),
            ],
        )

        def condition(tx: TransactionOnNetwork) -> bool:
            return tx.status.status == "failed"

        tx_from_network = self.watcher.await_on_condition(tx_hash, condition)
        assert tx_from_network.status.status == "failed"

    @pytest.mark.networkInteraction
    def test_ensure_error_if_timeout(self):
        alice = load_wallets()["alice"]
        alice_address = Address.new_from_bech32(alice.label)
        bob = Address.new_from_bech32("drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2")

        api = ApiNetworkProvider("https://devnet-api.dharitri.org")
        watcher = TransactionAwaiter(
            fetcher=api,
            polling_interval_in_milliseconds=1000,
            timeout_interval_in_milliseconds=10000,
        )

        transaction = Transaction(
            sender=alice_address,
            receiver=bob,
            gas_limit=50000,
            chain_id="D",
        )
        transaction.nonce = api.get_account(alice_address).nonce

        tx_computer = TransactionComputer()
        transaction.signature = alice.secret_key.sign(tx_computer.compute_bytes_for_signing(transaction))

        def condition(transaction: TransactionOnNetwork) -> bool:
            return transaction.status.status == "failed"

        tx_hash = api.send_transaction(transaction)

        with pytest.raises(ExpectedTransactionStatusNotReachedError):
            watcher.await_on_condition(tx_hash, condition)
