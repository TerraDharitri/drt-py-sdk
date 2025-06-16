from pathlib import Path

from dharitri_py_sdk.core.address import Address
from dharitri_py_sdk.core.transactions_factory_config import TransactionsFactoryConfig
from dharitri_py_sdk.validators.validators_signers import ValidatorsSigners
from dharitri_py_sdk.validators.validators_transactions_factory import (
    ValidatorsTransactionsFactory,
)
from dharitri_py_sdk.wallet.validator_keys import ValidatorPublicKey


class TestValidatorsTransactionsFactory:
    testdata = Path(__file__).parent.parent / "testutils" / "testdata"
    testwallets = Path(__file__).parent.parent / "testutils" / "testwallets"
    validators_file = testwallets / "validators.pem"

    alice = Address.new_from_bech32("drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l")
    reward_address = Address.new_from_bech32("drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q")

    validator_pubkey = ValidatorPublicKey.from_string(
        "e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
    )

    factory = ValidatorsTransactionsFactory(TransactionsFactoryConfig("D"))

    def test_create_transaction_for_staking_using_path_to_validators_file(self):
        transaction = self.factory.create_transaction_for_staking(
            sender=self.alice,
            validators_file=self.validators_file,
            amount=2500000000000000000000,
            rewards_address=self.reward_address,
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 0
        assert transaction.gas_limit == 11029500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "stake@02@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1dbc595db6361a15ac59e12745c33dd0b6b9f0e2ac1634fb69e5f77f4865150a5c79055c11e84980a9228a9998fb628e@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d@7b902a5c75d527437dfd821702472adf20c88f67d4df24a3b9048d520a6d18e628a08314d963bd12b837593bbcb4020a@b05fe535c27f46911f74f8b7f2051c54f792fca08c7ab23c53e77ececd2cd928"
        )

    def test_create_transaction_for_staking_using_validators_file(self):
        validators_file = ValidatorsSigners.new_from_pem(self.validators_file)

        transaction = self.factory.create_transaction_for_staking(
            sender=self.alice,
            validators_file=validators_file,
            amount=2500000000000000000000,
            rewards_address=self.reward_address,
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 0
        assert transaction.gas_limit == 11029500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "stake@02@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1dbc595db6361a15ac59e12745c33dd0b6b9f0e2ac1634fb69e5f77f4865150a5c79055c11e84980a9228a9998fb628e@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d@7b902a5c75d527437dfd821702472adf20c88f67d4df24a3b9048d520a6d18e628a08314d963bd12b837593bbcb4020a@b05fe535c27f46911f74f8b7f2051c54f792fca08c7ab23c53e77ececd2cd928"
        )

    def test_create_transaction_for_topping_up(self):
        transaction = self.factory.create_transaction_for_topping_up(
            sender=self.alice,
            amount=2500000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5057500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.data.decode() == "stake"

    def test_create_transaction_for_unstaking(self):
        transaction = self.factory.create_transaction_for_unstaking(
            sender=self.alice,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5350000
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "unStake@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )

    def test_create_transaction_for_unbonding(self):
        transaction = self.factory.create_transaction_for_unbonding(
            sender=self.alice,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5348500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "unBond@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )

    def test_create_transaction_for_unjailing(self):
        transaction = self.factory.create_transaction_for_unjailing(
            sender=self.alice,
            public_keys=[self.validator_pubkey],
            amount=2500000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5348500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "unJail@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )

    def test_create_transaction_for_changing_rewards_address(self):
        transaction = self.factory.create_transaction_for_changing_rewards_address(
            sender=self.alice,
            rewards_address=self.reward_address,
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5176000
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "changeRewardAddress@b05fe535c27f46911f74f8b7f2051c54f792fca08c7ab23c53e77ececd2cd928"
        )

    def test_create_transaction_for_claiming(self):
        transaction = self.factory.create_transaction_for_claiming(sender=self.alice)

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5057500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.data.decode() == "claim"

    def test_create_transaction_for_unstaking_nodes(self):
        transaction = self.factory.create_transaction_for_unstaking_nodes(
            sender=self.alice,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5357500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "unStakeNodes@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )

    def test_create_transaction_for_unstaking_tokens(self):
        transaction = self.factory.create_transaction_for_unstaking_tokens(
            sender=self.alice,
            amount=11000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5095000
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.data.decode() == "unStakeTokens@98a7d9b8314c0000"

    def test_create_transaction_for_unbonding_nodes(self):
        transaction = self.factory.create_transaction_for_unbonding_nodes(
            sender=self.alice,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5356000
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "unBondNodes@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )

    def test_create_transaction_for_unbonding_tokens(self):
        transaction = self.factory.create_transaction_for_unbonding_tokens(
            sender=self.alice,
            amount=20000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5096500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.data.decode() == "unBondTokens@01158e460913d00000"

    def test_create_transaction_for_cleaning_registered_data(self):
        transaction = self.factory.create_transaction_for_cleaning_registered_data(sender=self.alice)

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5078500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.data.decode() == "cleanRegisteredData"

    def test_create_transaction_for_restaking_unstaked_nodes(self):
        transaction = self.factory.create_transaction_for_restaking_unstaked_nodes(
            sender=self.alice,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5369500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "reStakeUnStakedNodes@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )
