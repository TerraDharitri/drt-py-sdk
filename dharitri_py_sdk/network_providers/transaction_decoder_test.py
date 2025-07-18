import base64

from dharitri_py_sdk.core.address import Address
from dharitri_py_sdk.network_providers.transaction_decoder import TransactionDecoder
from dharitri_py_sdk.testutils.mock_transaction_on_network import (
    get_empty_transaction_on_network,
)


class TestTransactionDecoder:
    transaction_decoder = TransactionDecoder()

    def test_nft_smart_contract_call(self) -> None:
        tx_to_decode = get_empty_transaction_on_network()
        tx_to_decode.sender = Address.new_from_bech32("drt18w6yj09l9jwlpj5cjqq9eccfgulkympv7d4rj6vq4u49j8fpwzws36f6y2")
        tx_to_decode.receiver = Address.new_from_bech32(
            "drt18w6yj09l9jwlpj5cjqq9eccfgulkympv7d4rj6vq4u49j8fpwzws36f6y2"
        )
        tx_to_decode.value = 0
        tx_to_decode.data = base64.b64decode(
            "RENEVE5GVFRyYW5zZmVyQDRjNGI0ZDRmNDEyZDYxNjE2MjM5MzEzMEAyZmI0ZTlAZTQwZjE2OTk3MTY1NWU2YmIwNGNAMDAwMDAwMDAwMDAwMDAwMDA1MDBkZjNiZWJlMWFmYTEwYzQwOTI1ZTgzM2MxNGE0NjBlMTBhODQ5ZjUwYTQ2OEA3Mzc3NjE3MDVmNmM2YjZkNmY2MTVmNzQ2ZjVmNzI2NTc3NjFAMGIzNzdmMjYxYzNjNzE5MUA="
        )

        metadata = self.transaction_decoder.get_transaction_metadata(tx_to_decode)

        assert metadata.sender == "drt18w6yj09l9jwlpj5cjqq9eccfgulkympv7d4rj6vq4u49j8fpwzws36f6y2"
        assert metadata.receiver == "drt1qqqqqqqqqqqqqpgqmua7hcd05yxypyj7sv7pffrquy9gf86s535qmyujkw"
        assert metadata.value == 1076977887712805212893260
        assert metadata.function_name == "swap_lkmoa_to_rewa"
        assert metadata.function_args == ["0b377f261c3c7191", ""]
        if metadata.transfers:
            assert metadata.transfers[0].amount == 1076977887712805212893260
            assert metadata.transfers[0].token.identifier == "LKMOA-aab910"
            assert metadata.transfers[0].token.nonce == 3126505

    def test_sc_call(self):
        tx_to_decode = get_empty_transaction_on_network()

        tx_to_decode.sender = Address.new_from_bech32("drt1wcn58spj6rnsexugjq3p2fxxq4t3l3kt7np078zwkrxu70ul69fq3c9sr5")
        tx_to_decode.receiver = Address.new_from_bech32(
            "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        )
        tx_to_decode.value = 0
        tx_to_decode.data = base64.b64decode("d2l0aGRyYXdHbG9iYWxPZmZlckAwMTczZDA=")

        metadata = self.transaction_decoder.get_transaction_metadata(tx_to_decode)

        assert metadata.sender == "drt1wcn58spj6rnsexugjq3p2fxxq4t3l3kt7np078zwkrxu70ul69fq3c9sr5"
        assert metadata.receiver == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert metadata.function_name == "withdrawGlobalOffer"
        assert metadata.function_args == ["0173d0"]

    def test_multi_dcdt_nft_transfer(self):
        tx_to_decode = get_empty_transaction_on_network()
        tx_to_decode.sender = Address.new_from_bech32("drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm")
        tx_to_decode.receiver = Address.new_from_bech32(
            "drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm"
        )
        tx_to_decode.value = 0
        tx_to_decode.data = base64.b64decode(
            "TXVsdGlFU0RUTkZUVHJhbnNmZXJAMDAwMDAwMDAwMDAwMDAwMDA1MDBkZjNiZWJlMWFmYTEwYzQwOTI1ZTgzM2MxNGE0NjBlMTBhODQ5ZjUwYTQ2OEAwMkA0YzRiNGQ0NTU4MmQ2MTYxNjIzOTMxMzBAMmZlM2IwQDA5Yjk5YTZkYjMwMDI3ZTRmM2VjQDRjNGI0ZDQ1NTgyZDYxNjE2MjM5MzEzMEAzMTAyY2FAMDEyNjMwZTlhMjlmMmY5MzgxNDQ5MUA3Mzc3NjE3MDVmNmM2YjZkNjU3ODVmNzQ2ZjVmNjU2NzZjNjRAMGVkZTY0MzExYjhkMDFiNUA="
        )

        metadata = self.transaction_decoder.get_transaction_metadata(tx_to_decode)

        assert metadata.sender == "drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm"
        assert metadata.receiver == "drt1qqqqqqqqqqqqqpgqmua7hcd05yxypyj7sv7pffrquy9gf86s535qmyujkw"
        assert metadata.value == 0
        assert metadata.function_name == "swap_lkmoa_to_rewa"
        assert metadata.function_args == [
            "0ede64311b8d01b5",
            "",
        ]
        if metadata.transfers:
            assert len(metadata.transfers) == 2
            assert metadata.transfers[0].amount == 45925073746530627023852
            assert metadata.transfers[0].token.identifier == "LKMOA-aab910"
            assert metadata.transfers[0].token.nonce == 3138480
            assert metadata.transfers[1].amount == 1389278024872597502641297
            assert metadata.transfers[1].token.identifier == "LKMOA-aab910"
            assert metadata.transfers[1].token.nonce == 3211978

    def test_dcdt_transfer(self):
        tx_to_decode = get_empty_transaction_on_network()

        tx_to_decode.sender = Address.new_from_bech32("drt1wcn58spj6rnsexugjq3p2fxxq4t3l3kt7np078zwkrxu70ul69fq3c9sr5")
        tx_to_decode.receiver = Address.new_from_bech32(
            "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        )
        tx_to_decode.value = 0
        tx_to_decode.data = base64.b64decode("RENEVFRyYW5zZmVyQDU0NDU1MzU0MmQzMjY1MzQzMDY0MzdAMDI1NDBiZTQwMA==")

        metadata = self.transaction_decoder.get_transaction_metadata(tx_to_decode)

        assert metadata.sender == "drt1wcn58spj6rnsexugjq3p2fxxq4t3l3kt7np078zwkrxu70ul69fq3c9sr5"
        assert metadata.receiver == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        assert metadata.value == 10000000000
        assert metadata.function_args is None
        if metadata.transfers:
            assert metadata.transfers[0].amount == 10000000000
            assert metadata.transfers[0].token.identifier == "TEST-2e40d7"
            assert metadata.transfers[0].token.nonce == 0

    def test_multi_transfer_fungible_and_meta_dcdt(self):
        tx_to_decode = get_empty_transaction_on_network()

        tx_to_decode.sender = Address.new_from_bech32("drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm")
        tx_to_decode.receiver = Address.new_from_bech32(
            "drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm"
        )
        tx_to_decode.value = 0
        tx_to_decode.data = base64.b64decode(
            "TXVsdGlFU0RUTkZUVHJhbnNmZXJAMDAwMDAwMDAwMDAwMDAwMDA1MDBkZjNiZWJlMWFmYTEwYzQwOTI1ZTgzM2MxNGE0NjBlMTBhODQ5ZjUwYTQ2OEAwMkA0YzRiNGQ0NTU4MmQ2MTYxNjIzOTMxMzBAMmZlM2IwQDA5Yjk5YTZkYjMwMDI3ZTRmM2VjQDU1NTM0NDQzMmQzMzM1MzA2MzM0NjVAMDBAMDEyNjMwZTlhMjlmMmY5MzgxNDQ5MUA3MDYxNzk1ZjZkNjU3NDYxNWY2MTZlNjQ1ZjY2NzU2ZTY3Njk2MjZjNjVAMGVkZTY0MzExYjhkMDFiNUA="
        )

        decoder = TransactionDecoder()
        metadata = decoder.get_transaction_metadata(tx_to_decode)

        assert metadata.sender == "drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm"
        assert metadata.receiver == "drt1qqqqqqqqqqqqqpgqmua7hcd05yxypyj7sv7pffrquy9gf86s535qmyujkw"

        assert metadata.value == 0
        assert metadata.function_name == "pay_meta_and_fungible"
        assert metadata.function_args == ["0ede64311b8d01b5", ""]

        if metadata.transfers:
            assert metadata.transfers[0].amount == 45925073746530627023852
            assert metadata.transfers[0].token.identifier == "LKMOA-aab910"
            assert metadata.transfers[0].token.nonce == 3138480
            assert metadata.transfers[1].amount == 1389278024872597502641297
            assert metadata.transfers[1].token.identifier == "USDC-350c4e"
            assert metadata.transfers[1].token.nonce == 0

    def test_multi_transfer_fungible_dcdt(self):
        tx_to_decode = get_empty_transaction_on_network()

        tx_to_decode.sender = Address.new_from_bech32("drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm")
        tx_to_decode.receiver = Address.new_from_bech32(
            "drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm"
        )
        tx_to_decode.value = 0
        tx_to_decode.data = base64.b64decode(
            "TXVsdGlFU0RUTkZUVHJhbnNmZXJAMDAwMDAwMDAwMDAwMDAwMDA1MDBkZjNiZWJlMWFmYTEwYzQwOTI1ZTgzM2MxNGE0NjBlMTBhODQ5ZjUwYTQ2OEAwMkA1MjQ5NDQ0NTJkMzAzNTYyMzE2MjYyQDAwQDA5Yjk5YTZkYjMwMDI3ZTRmM2VjQDU1NTM0NDQzMmQzMzM1MzA2MzM0NjVAQDAxMjYzMGU5YTI5ZjJmOTM4MTQ0OTE="
        )

        metadata = self.transaction_decoder.get_transaction_metadata(tx_to_decode)

        assert metadata.sender == "drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm"
        assert metadata.receiver == "drt1qqqqqqqqqqqqqpgqmua7hcd05yxypyj7sv7pffrquy9gf86s535qmyujkw"
        assert metadata.value == 0

        if metadata.transfers:
            assert metadata.transfers[0].amount == 45925073746530627023852
            assert metadata.transfers[0].token.identifier == "RIDE-05b1bb"

            assert metadata.transfers[1].amount == 1389278024872597502641297
            assert metadata.transfers[1].token.identifier == "USDC-350c4e"

    def test_smart_contract_call_without_args(self):
        tx_to_decode = get_empty_transaction_on_network()

        tx_to_decode.sender = Address.new_from_bech32("drt18w6yj09l9jwlpj5cjqq9eccfgulkympv7d4rj6vq4u49j8fpwzws36f6y2")
        tx_to_decode.receiver = Address.new_from_bech32(
            "drt1qqqqqqqqqqqqqpgqmua7hcd05yxypyj7sv7pffrquy9gf86s535qmyujkw"
        )
        tx_to_decode.value = 0
        tx_to_decode.data = base64.b64decode("bXlFbmRwb2ludA==")

        metadata = self.transaction_decoder.get_transaction_metadata(tx_to_decode)

        assert metadata.sender == "drt18w6yj09l9jwlpj5cjqq9eccfgulkympv7d4rj6vq4u49j8fpwzws36f6y2"
        assert metadata.receiver == "drt1qqqqqqqqqqqqqpgqmua7hcd05yxypyj7sv7pffrquy9gf86s535qmyujkw"
        assert metadata.value == 0
        assert metadata.function_name == "myEndpoint"
        assert metadata.function_args == []

    def test_dcdt_transfer_with_receiver_in_data_field(self):
        tx_to_decode = get_empty_transaction_on_network()

        tx_to_decode.sender = Address.new_from_bech32("drt1pv3020g75r033shtfzkf9yaf8xx7d76qan94wkraxm4vvqankrtsq8a5pq")
        tx_to_decode.receiver = Address.new_from_bech32(
            "drt1athw37lnw4t4d7ax9t5x9l4hvfay3qfp0k4ldxgq2wv94ln6vuesa3rc3k"
        )
        tx_to_decode.data = base64.b64decode(
            "RENEVFRyYW5zZmVyQDRjNDE0ZTQ0MmQzNDMwNjYzMjM2NjZAMDI2NWYwYTQ3ZGQ0NGMwMDAwQGVhZWVlOGZiZjM3NTU3NTZmYmE2MmFlODYyZmViNzYyN2E0ODgxMjE3ZGFiZjY5OTAwNTM5ODVhZmU3YTY3MzM="
        )

        transaction_decoder = TransactionDecoder()
        metadata = transaction_decoder.get_transaction_metadata(tx_to_decode)
        assert metadata.function_name is None
        assert metadata.function_args is None
        assert metadata.transfers
        assert metadata.transfers[0].amount == 44239040000000000000
        assert metadata.transfers[0].token.identifier == "LAND-40f26f"
        assert metadata.transfer_messages == [
            bytes.fromhex("eaeee8fbf3755756fba62ae862feb7627a4881217dabf6990053985afe7a6733")
        ]

    def test_native_transfer(self):
        tx_to_decode = get_empty_transaction_on_network()

        tx_to_decode.sender = Address.new_from_bech32("drt18w6yj09l9jwlpj5cjqq9eccfgulkympv7d4rj6vq4u49j8fpwzws36f6y2")
        tx_to_decode.receiver = Address.new_from_bech32(
            "drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm"
        )
        tx_to_decode.value = 100000000
        tx_to_decode.data = "abba".encode()

        transaction_decoder = TransactionDecoder()
        metadata = transaction_decoder.get_transaction_metadata(tx_to_decode)

        assert metadata.sender == "drt18w6yj09l9jwlpj5cjqq9eccfgulkympv7d4rj6vq4u49j8fpwzws36f6y2"
        assert metadata.receiver == "drt1lkrrrn3ws9sp854kdpzer9f77eglqpeet3e3k3uxvqxw9p3eq6xqmwzjqm"
        assert metadata.value == 100000000
        assert metadata.function_name == "transfer"
        assert metadata.function_args == []
        assert metadata.transfer_messages == [bytes.fromhex("abba")]

    def test_dcdt_transfer_separated_messages(self):
        tx_to_decode = get_empty_transaction_on_network()

        tx_to_decode.sender = Address.new_from_bech32("drt1pv3020g75r033shtfzkf9yaf8xx7d76qan94wkraxm4vvqankrtsq8a5pq")
        tx_to_decode.receiver = Address.new_from_bech32(
            "drt1athw37lnw4t4d7ax9t5x9l4hvfay3qfp0k4ldxgq2wv94ln6vuesa3rc3k"
        )
        tx_to_decode.data = "DCDTTransfer@4c414e442d343066323666@0265f0a47dd44c0000@aaaaaa@bb".encode()

        transaction_decoder = TransactionDecoder()
        metadata = transaction_decoder.get_transaction_metadata(tx_to_decode)
        assert metadata.function_name is None
        assert metadata.function_args is None
        assert metadata.transfers
        assert metadata.transfers[0].amount == 44239040000000000000
        assert metadata.transfers[0].token.identifier == "LAND-40f26f"
        assert metadata.transfer_messages == [bytes.fromhex("aaaaaa"), bytes.fromhex("bb")]

    def test_dcdtnft_transfer_separated_messages(self):
        tx_to_decode = get_empty_transaction_on_network()

        tx_to_decode.sender = Address.new_from_bech32("drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l")
        tx_to_decode.receiver = Address.new_from_bech32(
            "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        )
        tx_to_decode.data = "DCDTNFTTransfer@4d4e592d336131636566@01@01@3ddf173c9e02c0e58fb1e552f473d98da6a4c3f23c7e034c912ee98a8dddce17@aaaaaaaaaaaaaaaaaaaaaa@aa".encode()

        transaction_decoder = TransactionDecoder()
        metadata = transaction_decoder.get_transaction_metadata(tx_to_decode)
        assert metadata.function_name is None
        assert metadata.function_args is None
        assert metadata.transfers
        assert metadata.transfers[0].amount == 1
        assert metadata.transfers[0].token.identifier == "MNY-3a1cef"
        assert metadata.transfers[0].token.nonce == 1
        assert metadata.transfer_messages == [bytes.fromhex("aaaaaaaaaaaaaaaaaaaaaa"), bytes.fromhex("aa")]

    def test_multi_dcdtnft_transfer_separated_messages(self):
        tx_to_decode = get_empty_transaction_on_network()

        tx_to_decode.sender = Address.new_from_bech32("drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l")
        tx_to_decode.receiver = Address.new_from_bech32(
            "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
        )
        tx_to_decode.data = "MultiDCDTNFTTransfer@3ddf173c9e02c0e58fb1e552f473d98da6a4c3f23c7e034c912ee98a8dddce17@01@4d4e592d336131636566@02@01@aaaaaaaa@aa".encode()

        transaction_decoder = TransactionDecoder()
        metadata = transaction_decoder.get_transaction_metadata(tx_to_decode)
        assert metadata.function_name is None
        assert metadata.function_args is None
        assert metadata.transfers
        assert metadata.transfers[0].amount == 1
        assert metadata.transfers[0].token.identifier == "MNY-3a1cef"
        assert metadata.transfers[0].token.nonce == 2
        assert metadata.transfer_messages == [bytes.fromhex("aaaaaaaa"), bytes.fromhex("aa")]
