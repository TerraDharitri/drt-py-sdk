from dharitri_py_sdk.core.address import Address
from dharitri_py_sdk.core.transaction import Transaction
from dharitri_py_sdk.core.transaction_computer import TransactionComputer
from dharitri_py_sdk.wallet.keypair import KeyPair
from dharitri_py_sdk.wallet.user_keys import UserSecretKey


def test_create_keypair():
    buffer_hex = "413f42575f7f26fad3317a778771212fdb80245850981e48b58a4f25e344e8f9"
    buffer = bytes.fromhex(buffer_hex)

    user_secret_key = UserSecretKey(buffer)
    keypair = KeyPair.new_from_bytes(buffer)

    secret_key = keypair.get_secret_key()
    assert secret_key.hex() == buffer_hex
    assert secret_key == user_secret_key

    keypair = KeyPair(secret_key)
    assert keypair.get_secret_key() == user_secret_key
    assert keypair.get_public_key() == user_secret_key.generate_public_key()

    keypair = KeyPair.generate()
    pubkey = keypair.get_public_key()
    secret_key = keypair.get_secret_key()
    assert len(pubkey.get_bytes()) == 32
    assert len(secret_key.get_bytes()) == 32


def test_sign_and_verify_transaction():
    """
    Also see: https://github.com/TerraDharitri/drt-chain-go/blob/master/examples/construction_test.go
    """

    tx = Transaction(
        nonce=89,
        value=0,
        receiver=Address.new_from_bech32("drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"),
        sender=Address.new_from_bech32("drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"),
        data=None,
        gas_price=1000000000,
        gas_limit=50000,
        chain_id="local-testnet",
        version=1,
        options=0,
    )

    buffer_hex = "413f42575f7f26fad3317a778771212fdb80245850981e48b58a4f25e344e8f9"
    buffer = bytes.fromhex(buffer_hex)
    keypair = KeyPair.new_from_bytes(buffer)

    transaction_computer = TransactionComputer()
    serialized_tx = transaction_computer.compute_bytes_for_signing(tx)

    tx.signature = keypair.sign(serialized_tx)
    assert (
        tx.signature.hex()
        == "a492169c5372dc178f58a6b7f6226350bdae659ae5bd21447e11c3e3dd9f8347d353921b86b02f13aa7044155d7bf0f1bd9529e0f0801abe6f872040d2571e0e"
    )
    assert keypair.verify(serialized_tx, tx.signature)
