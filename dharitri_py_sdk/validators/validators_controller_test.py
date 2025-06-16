from pathlib import Path

from dharitri_py_sdk.accounts.account import Account
from dharitri_py_sdk.core.address import Address
from dharitri_py_sdk.validators.validators_controller import ValidatorsController
from dharitri_py_sdk.validators.validators_signers import ValidatorsSigners
from dharitri_py_sdk.wallet.validator_keys import ValidatorPublicKey


class TestValidatorsController:
    testdata = Path(__file__).parent.parent / "testutils" / "testdata"
    testwallets = Path(__file__).parent.parent / "testutils" / "testwallets"
    validators_file = testwallets / "validators.pem"

    alice = Account.new_from_pem(testwallets / "alice.pem")
    reward_address = Address.new_from_bech32("drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q")

    validator_pubkey = ValidatorPublicKey.from_string(
        "e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
    )

    controller = ValidatorsController(chain_id="localnet")

    def test_create_transaction_for_staking_using_path_to_validators_file(self):
        transaction = self.controller.create_transaction_for_staking(
            sender=self.alice,
            nonce=self.alice.nonce,
            validators_file=self.validators_file,
            amount=2500000000000000000000,
            rewards_address=self.reward_address,
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 0
        assert transaction.gas_limit == 11029500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "e9dd1159bc55bde84872f0595c9e24b0b210deb8cb02a1df7d7b0e1277436d2043437ffeaff540e11200c00417cf5ce396b3154f968ad62ab4359fb05a493b0d"
        )
        assert (
            transaction.data.decode()
            == "stake@02@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1865870f7f69162a2dfefd33fe232a9ca984c6f22d1ee3f6a5b34a8eb8c9f7319001f29d5a2eed85c1500aca19fa4189@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d@12b309791213aac8ad9f34f0d912261e30f9ab060859e4d515e020a98b91d82a7cd334e4b504bb93d6b75347cccd6318@b05fe535c27f46911f74f8b7f2051c54f792fca08c7ab23c53e77ececd2cd928"
        )

    def test_create_transaction_for_staking_using_validators_file(self):
        validators_file = ValidatorsSigners.new_from_pem(self.validators_file)

        transaction = self.controller.create_transaction_for_staking(
            sender=self.alice,
            nonce=self.alice.nonce,
            validators_file=validators_file,
            amount=2500000000000000000000,
            rewards_address=self.reward_address,
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 0
        assert transaction.gas_limit == 11029500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "e9dd1159bc55bde84872f0595c9e24b0b210deb8cb02a1df7d7b0e1277436d2043437ffeaff540e11200c00417cf5ce396b3154f968ad62ab4359fb05a493b0d"
        )
        assert (
            transaction.data.decode()
            == "stake@02@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1865870f7f69162a2dfefd33fe232a9ca984c6f22d1ee3f6a5b34a8eb8c9f7319001f29d5a2eed85c1500aca19fa4189@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d@12b309791213aac8ad9f34f0d912261e30f9ab060859e4d515e020a98b91d82a7cd334e4b504bb93d6b75347cccd6318@b05fe535c27f46911f74f8b7f2051c54f792fca08c7ab23c53e77ececd2cd928"
        )

    def test_create_transaction_for_staking_with_relayer_and_guardian(self):
        validators_file = ValidatorsSigners.new_from_pem(self.validators_file)

        transaction = self.controller.create_transaction_for_staking(
            sender=self.alice,
            nonce=self.alice.nonce,
            validators_file=validators_file,
            amount=2500000000000000000000,
            rewards_address=self.reward_address,
            guardian=Address.new_from_bech32("drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"),
            relayer=Address.new_from_bech32("drt1ssmsc9022udc8pdw7wk3hxw74jr900xg28vwpz3z60gep66fasaszky4ct"),
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 0
        assert transaction.gas_limit == 11129500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian == Address.new_from_bech32(
            "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"
        )
        assert transaction.relayer == Address.new_from_bech32(
            "drt1ssmsc9022udc8pdw7wk3hxw74jr900xg28vwpz3z60gep66fasaszky4ct"
        )
        assert (
            transaction.signature.hex()
            == "b12d607a8c52c2cdfc8f239274a45ead211fb12e79fb6c36866d9bae74c6a50b52ebf1c2eb57e2a89dc29fd8da8f6d7ff70c96a0267dd7e2f050d5b61f439100"
        )
        assert (
            transaction.data.decode()
            == "stake@02@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1865870f7f69162a2dfefd33fe232a9ca984c6f22d1ee3f6a5b34a8eb8c9f7319001f29d5a2eed85c1500aca19fa4189@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d@12b309791213aac8ad9f34f0d912261e30f9ab060859e4d515e020a98b91d82a7cd334e4b504bb93d6b75347cccd6318@b05fe535c27f46911f74f8b7f2051c54f792fca08c7ab23c53e77ececd2cd928"
        )

    def test_create_transaction_for_topping_up(self):
        transaction = self.controller.create_transaction_for_topping_up(
            sender=self.alice,
            nonce=self.alice.nonce,
            amount=2500000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5057500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert transaction.data.decode() == "stake"
        assert (
            transaction.signature.hex()
            == "6e6ba71060ae3ff9e05f9da8e74b27e956ad024861cf595fc27b6ebff2b0d02d4b7689935e4343f04c8476cd7933ed8e50f2233a8cb091093c2c36044fbe0404"
        )

    def test_create_transaction_for_unstaking(self):
        transaction = self.controller.create_transaction_for_unstaking(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5350000
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "d0090943d330dd98f802c5289e2215d6b4eef4e378eef45d8e252f01f9a1829057b6dc499126a6e5348bf188bb04282815b1118a515ed317619135da87102d07"
        )
        assert (
            transaction.data.decode()
            == "unStake@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )

    def test_create_transaction_for_unbonding(self):
        transaction = self.controller.create_transaction_for_unbonding(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5348500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "4d6c66fd8afa31dead5fa9fe02371307ea5a0375a54977547c09318740d4b75d9b992668b7721b82ed93fb680932d5b1110cd44d0501a4e9f4d3552a0710c000"
        )
        assert (
            transaction.data.decode()
            == "unBond@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )

    def test_create_transaction_for_unjailing(self):
        transaction = self.controller.create_transaction_for_unjailing(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
            amount=2500000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5348500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "863104a589b6a167631e330521eca3024d792be3eb87846bd99b265efa010763ef175ca3faba387bb01453223e948a7012baf3820648fa55ea65a9f13f0d980f"
        )
        assert (
            transaction.data.decode()
            == "unJail@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )

    def test_create_transaction_for_changing_rewards_address(self):
        transaction = self.controller.create_transaction_for_changing_rewards_address(
            sender=self.alice,
            nonce=7,
            rewards_address=self.reward_address,
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5176000
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "d005ec3dbb234ac64437b126b66c9e37a4fe1cc09315729dd775eaa20edd199f4f538486c391c25ec5eb6afe2c85db277c38e32d95eba380e78b05d51ae9220c"
        )
        assert (
            transaction.data.decode()
            == "changeRewardAddress@b05fe535c27f46911f74f8b7f2051c54f792fca08c7ab23c53e77ececd2cd928"
        )

    def test_create_transaction_for_claiming(self):
        transaction = self.controller.create_transaction_for_claiming(
            sender=self.alice,
            nonce=7,
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5057500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert transaction.data.decode() == "claim"
        assert (
            transaction.signature.hex()
            == "f9a6c55147a2eac64aa81fd7c592a7199be124cbc92c157235dcf42f9a3f9bda9a0271359b029b07ad0f30167d459b615b18d619b226b2cc67ef30e4a4d28b06"
        )

    def test_create_transaction_for_unstaking_nodes(self):
        transaction = self.controller.create_transaction_for_unstaking_nodes(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5357500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "0edb5048838791e00aaee2960310e74b17071d5d36446b8c0a803f35d3657cab0a36aba5f4695322904f618cc9580c3448afcf3bc15d9509eb1c86dd1f216f04"
        )
        assert (
            transaction.data.decode()
            == "unStakeNodes@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )

    def test_create_transaction_for_unstaking_tokens(self):
        transaction = self.controller.create_transaction_for_unstaking_tokens(
            sender=self.alice,
            nonce=7,
            amount=11000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5095000
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "dc402cecf430480bbf373a7dcdaea24caa6cb91d1c20609b4ff7445b884a6bfdd6447d6ae4e8cd6f07e64d3cef11bcd72e74cb1c62ada87cb4f652519702eb0a"
        )
        assert transaction.data.decode() == "unStakeTokens@98a7d9b8314c0000"

    def test_create_transaction_for_unbonding_nodes(self):
        transaction = self.controller.create_transaction_for_unbonding_nodes(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5356000
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "461599e42ab804133de625896b3494d5754a5f89ec3e02e421e6872ec12437d92f90997719e462adf5d25a19a7d10dc0dde66280fb4b9625ef6a24f6658c7f09"
        )
        assert (
            transaction.data.decode()
            == "unBondNodes@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )

    def test_create_transaction_for_unbonding_tokens(self):
        transaction = self.controller.create_transaction_for_unbonding_tokens(
            sender=self.alice,
            nonce=7,
            amount=20000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5096500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "158d6d230cf64ff8c996dd1c8ca5e191fab5b4233f1271622e3a66ab557ff72ecd03fbd6a3d63f5f644881af23766d470f8f1bc16d341ca91b0a56499e720a0c"
        )
        assert transaction.data.decode() == "unBondTokens@01158e460913d00000"

    def test_create_transaction_for_cleaning_registered_data(self):
        transaction = self.controller.create_transaction_for_cleaning_registered_data(
            sender=self.alice,
            nonce=7,
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5078500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "0f12db6fe5e02c06f7fd28e8d4fd91ca9b728e49da71053bb02581c946aecc9fea5c6b1a54b386a249c927ec89c61bc5210095dd6a60853b53de3246c3fa7504"
        )
        assert transaction.data.decode() == "cleanRegisteredData"

    def test_create_transaction_for_restaking_unstaked_nodes(self):
        transaction = self.controller.create_transaction_for_restaking_unstaked_nodes(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert transaction.receiver.to_bech32() == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5369500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "c40832505eae036a148543d398c4a92bda692172d7f0e6e84c505b84968506394e8d30b63ac0c84dbb2610be50c3b03a3619884d7e55c3ced9438bc0e1034407"
        )
        assert (
            transaction.data.decode()
            == "reStakeUnStakedNodes@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )
