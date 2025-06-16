from pathlib import Path

from dharitri_py_sdk.accounts.account import Account
from dharitri_py_sdk.core.address import Address
from dharitri_py_sdk.core.message import Message
from dharitri_py_sdk.core.transaction import Transaction
from dharitri_py_sdk.wallet.keypair import KeyPair
from dharitri_py_sdk.wallet.user_keys import UserSecretKey

testwallets = Path(__file__).parent.parent / "testutils" / "testwallets"
DUMMY_MNEMONIC = "moral volcano peasant pass circle pen over picture flat shop clap goat never lyrics gather prepare woman film husband gravity behind test tiger improve"
alice = testwallets / "alice.pem"


def test_create_account_from_pem():
    account = Account.new_from_pem(alice)

    assert account.secret_key.get_bytes().hex() == "7b4686f3c925f9f6571de5fa24fb6a7ac0a2e5439a48bad8ed90b6690aad6017"
    assert account.address.to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"


def test_create_account_from_keystore():
    account = Account.new_from_keystore(testwallets / "withDummyMnemonic.json", "password")

    assert account.secret_key.get_bytes().hex() == "413f42575f7f26fad3317a778771212fdb80245850981e48b58a4f25e344e8f9"
    assert account.address.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"


def test_create_account_from_mnemonic():
    account = Account.new_from_mnemonic(DUMMY_MNEMONIC)

    assert account.secret_key.get_bytes().hex() == "413f42575f7f26fad3317a778771212fdb80245850981e48b58a4f25e344e8f9"
    assert account.address.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"


def test_create_account_from_keypair():
    secret_key = UserSecretKey.new_from_string("413f42575f7f26fad3317a778771212fdb80245850981e48b58a4f25e344e8f9")
    keypair = KeyPair(secret_key)
    account = Account.new_from_keypair(keypair)

    assert account.secret_key == secret_key
    assert account.address.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"


def test_account_nonce_holder():
    account = Account.new_from_pem(alice)
    account.nonce = 42
    assert account.get_nonce_then_increment() == 42
    assert account.get_nonce_then_increment() == 43

    account.get_nonce_then_increment()
    account.get_nonce_then_increment()
    account.get_nonce_then_increment()
    assert account.nonce == 47


def test_sign_transaction():
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

    account = Account.new_from_pem(alice)
    tx.signature = account.sign_transaction(tx)
    assert (
        tx.signature.hex()
        == "9bd579f3aabb32551b83880a60745a5ab65af4ce8d1061b1ea7dbf00b1352bca2da0d60daba622cb8298ac24167c1530d9bf850b901dd039d6abe0ff1455980c"
    )


def test_sign_message():
    message = Message(
        "hello".encode(),
        address=Address.new_from_bech32("drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"),
    )

    account = Account.new_from_pem(alice)
    message.signature = account.sign_message(message)
    assert (
        message.signature.hex()
        == "fe1d7c955128a6a97e0a1c05e972d2dd457b3371a3ec4274ca911c7bd34ce0e3263ef8370aa36190f7545201a173c3f1ec38ece249c806de3887cbd075198806"
    )


def test_sign_tx_by_hash():
    account = Account.new_from_pem(alice)

    tx = Transaction(
        sender=Address.new_from_bech32("drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"),
        receiver=Address.new_from_bech32("drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"),
        value=0,
        gas_limit=50000,
        version=2,
        options=1,
        chain_id="integration tests chain ID",
        nonce=89,
    )

    tx.signature = account.sign_transaction(tx)

    assert (
        tx.signature.hex()
        == "1280c117b6b2ce130b4f74018883a5225d99aa63e7cc3242f5612002c670eebccc2aea51cf4aca6802fcb02269891f6926b525c6a4c30850d980917965bafa0e"
    )
