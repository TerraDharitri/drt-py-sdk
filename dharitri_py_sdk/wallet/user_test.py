import json
from pathlib import Path

import pytest

from dharitri_py_sdk.core import (
    Address,
    Message,
    MessageComputer,
    Transaction,
    TransactionComputer,
)
from dharitri_py_sdk.wallet.crypto.randomness import Randomness
from dharitri_py_sdk.wallet.user_keys import UserSecretKey
from dharitri_py_sdk.wallet.user_pem import UserPEM
from dharitri_py_sdk.wallet.user_signer import UserSigner
from dharitri_py_sdk.wallet.user_verifer import UserVerifier
from dharitri_py_sdk.wallet.user_wallet import UserWallet

testwallets = Path(__file__).parent.parent / "testutils" / "testwallets"
DUMMY_MNEMONIC = "moral volcano peasant pass circle pen over picture flat shop clap goat never lyrics gather prepare woman film husband gravity behind test tiger improve"


def test_user_secret_key_create():
    buffer_hex = "413f42575f7f26fad3317a778771212fdb80245850981e48b58a4f25e344e8f9"
    buffer = bytes.fromhex(buffer_hex)
    secret_key = UserSecretKey(buffer)
    secret_key_from_string = UserSecretKey.new_from_string(buffer_hex)

    assert secret_key.hex() == buffer_hex
    assert secret_key_from_string.hex() == buffer_hex


def test_user_secret_key_generate_public_key():
    assert (
        UserSecretKey.new_from_string("413f42575f7f26fad3317a778771212fdb80245850981e48b58a4f25e344e8f9")
        .generate_public_key()
        .hex()
        == "0139472eff6886771a982f3083da5d421f24c29181e63888228dc81ca60d69e1"
    )
    assert (
        UserSecretKey.new_from_string("b8ca6f8203fb4b545a8e83c5384da033c415db155b53fb5b8eba7ff5a039d639")
        .generate_public_key()
        .hex()
        == "8049d639e5a6980d1cd2392abcce41029cda74a1563523a202f09641cc2618f8"
    )
    assert (
        UserSecretKey.new_from_string("e253a571ca153dc2aee845819f74bcc9773b0586edead15a94cb7235a5027436")
        .generate_public_key()
        .hex()
        == "b2a11555ce521e4944e09ab17549d85b487dcd26c84b5017a39e31a3670889ba"
    )


def test_user_signer_from_pem_file():
    pubkey = UserSigner.from_pem_file(testwallets / "alice.pem", 0).get_pubkey()
    assert Address(pubkey.buffer, "drt").to_bech32() == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"

    pubkey = UserSigner.from_pem_file(testwallets / "bob.pem", 0).get_pubkey()
    assert Address(pubkey.buffer, "drt").to_bech32() == "drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"

    pubkey = UserSigner.from_pem_file(testwallets / "carol.pem", 0).get_pubkey()
    assert Address(pubkey.buffer, "drt").to_bech32() == "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"


def test_load_signers_from_pem():
    signers = UserSigner.from_pem_file_all(testwallets / "multipleUserKeys.pem")

    assert len(signers) == 3
    assert (
        Address(signers[0].get_pubkey().buffer, "drt").to_bech32()
        == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    )
    assert (
        Address(signers[1].get_pubkey().buffer, "drt").to_bech32()
        == "drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"
    )
    assert (
        Address(signers[2].get_pubkey().buffer, "drt").to_bech32()
        == "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"
    )


def test_user_wallet_to_keyfile_object_using_known_test_wallets_with_their_randomness():
    alice_secret_key = UserSecretKey.new_from_string("413f42575f7f26fad3317a778771212fdb80245850981e48b58a4f25e344e8f9")
    alice_wallet = UserWallet.from_secret_key(
        alice_secret_key,
        "password",
        Randomness(
            salt=bytes.fromhex("4903bd0e7880baa04fc4f886518ac5c672cdc745a6bd13dcec2b6c12e9bffe8d"),
            iv=bytes.fromhex("033182afaa1ebaafcde9ccc68a5eac31"),
            id="0dc10c02-b59b-4bac-9710-6b2cfa4284ba",
        ),
    )

    bob_secret_key = UserSecretKey.new_from_string("b8ca6f8203fb4b545a8e83c5384da033c415db155b53fb5b8eba7ff5a039d639")
    bob_wallet = UserWallet.from_secret_key(
        bob_secret_key,
        "password",
        Randomness(
            salt=bytes.fromhex("18304455ac2dbe2a2018bda162bd03ef95b81622e99d8275c34a6d5e6932a68b"),
            iv=bytes.fromhex("18378411e31f6c4e99f1435d9ab82831"),
            id="85fdc8a7-7119-479d-b7fb-ab4413ed038d",
        ),
    )

    carol_secret_key = UserSecretKey.new_from_string("e253a571ca153dc2aee845819f74bcc9773b0586edead15a94cb7235a5027436")
    carol_wallet = UserWallet.from_secret_key(
        carol_secret_key,
        "password",
        Randomness(
            salt=bytes.fromhex("4f2f5530ce28dc0210962589b908f52714f75c8fb79ff18bdd0024c43c7a220b"),
            iv=bytes.fromhex("258ed2b4dc506b4dc9d274b0449b0eb0"),
            id="65894f35-d142-41d2-9335-6ad02e0ed0be",
        ),
    )

    alice_saved_path = testwallets / "alice.saved.json"
    bob_saved_path = testwallets / "bob.saved.json"
    carol_saved_path = testwallets / "carol.saved.json"

    alice_wallet.save(alice_saved_path, "drt")
    bob_wallet.save(bob_saved_path, "drt")
    carol_wallet.save(carol_saved_path, "drt")

    assert alice_saved_path.read_text().strip() == (testwallets / "alice.json").read_text().strip()
    assert bob_saved_path.read_text().strip() == (testwallets / "bob.json").read_text().strip()
    assert carol_saved_path.read_text().strip() == (testwallets / "carol.json").read_text().strip()

    alice_saved_path.unlink()
    bob_saved_path.unlink()
    carol_saved_path.unlink()


def test_user_wallet_encrypt_then_decrypt():
    alice_secret_key = UserSecretKey.new_from_string("413f42575f7f26fad3317a778771212fdb80245850981e48b58a4f25e344e8f9")
    alice_wallet = UserWallet.from_secret_key(alice_secret_key, "password")
    alice_keyfile_object = alice_wallet.to_dict("drt")
    decrypted_secret_key = UserWallet.decrypt_secret_key(alice_keyfile_object, "password")
    assert decrypted_secret_key.buffer == alice_secret_key.buffer

    bob_secret_key = UserSecretKey.new_from_string("b8ca6f8203fb4b545a8e83c5384da033c415db155b53fb5b8eba7ff5a039d639")
    bob_wallet = UserWallet.from_secret_key(bob_secret_key, "password")
    bob_keyfile_object = bob_wallet.to_dict("drt")
    decrypted_secret_key = UserWallet.decrypt_secret_key(bob_keyfile_object, "password")
    assert decrypted_secret_key.buffer == bob_secret_key.buffer

    carol_secret_key = UserSecretKey.new_from_string("e253a571ca153dc2aee845819f74bcc9773b0586edead15a94cb7235a5027436")
    carol_wallet = UserWallet.from_secret_key(carol_secret_key, "password")
    carol_keyfile_object = carol_wallet.to_dict("drt")
    decrypted_secret_key = UserWallet.decrypt_secret_key(carol_keyfile_object, "password")
    assert decrypted_secret_key.buffer == carol_secret_key.buffer


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

    signer = UserSigner.from_pem_file(testwallets / "alice.pem")
    verifier = UserVerifier.from_address(
        Address.new_from_bech32("drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l")
    )
    transaction_computer = TransactionComputer()

    tx.signature = signer.sign(transaction_computer.compute_bytes_for_signing(tx))
    assert (
        tx.signature.hex()
        == "9bd579f3aabb32551b83880a60745a5ab65af4ce8d1061b1ea7dbf00b1352bca2da0d60daba622cb8298ac24167c1530d9bf850b901dd039d6abe0ff1455980c"
    )
    assert verifier.verify(transaction_computer.compute_bytes_for_signing(tx), tx.signature)


def test_sign_message():
    message = Message(
        "hello".encode(),
        address=Address.new_from_bech32("drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"),
    )
    message_computer = MessageComputer()

    signer = UserSigner.from_pem_file(testwallets / "alice.pem")
    verifier = UserVerifier.from_address(
        Address.new_from_bech32("drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l")
    )

    message.signature = signer.sign(message_computer.compute_bytes_for_signing(message))
    assert (
        message.signature.hex()
        == "fe1d7c955128a6a97e0a1c05e972d2dd457b3371a3ec4274ca911c7bd34ce0e3263ef8370aa36190f7545201a173c3f1ec38ece249c806de3887cbd075198806"
    )
    assert verifier.verify(message_computer.compute_bytes_for_signing(message), message.signature)


def test_user_pem_save():
    path = testwallets / "alice.pem"
    path_saved = path.with_suffix(".saved")
    content_expected = path.read_text().strip()

    pem = UserPEM.from_file(path)
    pem.save(path_saved)
    content_actual = path_saved.read_text().strip()

    assert content_actual == content_expected
    path_saved.unlink()


def test_load_secret_key_but_without_kind_field():
    keystore_path = testwallets / "withoutKind.json"
    secret_key = UserWallet.load_secret_key(keystore_path, "password")
    actual_address = (secret_key.generate_public_key().to_address("drt")).to_bech32()
    assert actual_address == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"


def test_load_secret_key_with_unecessary_address_index():
    keystore_path = testwallets / "alice.json"

    with pytest.raises(Exception, match="address_index must not be provided when kind == 'secretKey'"):
        UserWallet.load_secret_key(keystore_path, "password", 42)


def test_create_keystore_file_with_mnemonic():
    wallet = UserWallet.from_mnemonic(DUMMY_MNEMONIC, "password")
    keyfile_object = wallet.to_dict()

    assert keyfile_object["version"] == 4
    assert keyfile_object["kind"] == "mnemonic"
    assert "bech32" not in keyfile_object


def test_create_keystore_with_mnemonic_with_randomness():
    expected_dummy_wallet_json = (testwallets / "withDummyMnemonic.json").read_text()
    expected_dummy_wallet_dict = json.loads(expected_dummy_wallet_json)

    randomness = Randomness(
        id="5b448dbc-5c72-4d83-8038-938b1f8dff19",
        iv=bytes.fromhex("2da5620906634972d9a623bc249d63d4"),
        salt=bytes.fromhex("aa9e0ba6b188703071a582c10e5331f2756279feb0e2768f1ba0fd38ec77f035"),
    )

    wallet = UserWallet.from_mnemonic(DUMMY_MNEMONIC, "password", randomness)
    wallet_dict = wallet.to_dict()

    assert wallet_dict == expected_dummy_wallet_dict


def test_load_secret_key_with_mnemonic():
    keystore_path = testwallets / "withDummyMnemonic.json"

    assert (
        UserWallet.load_secret_key(keystore_path, "password", 1).generate_public_key().to_address("drt").to_bech32()
        == "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c"
    )
    assert (
        UserWallet.load_secret_key(keystore_path, "password", 2).generate_public_key().to_address("drt").to_bech32()
        == "drt1k2s324ww2g0yj38qn2ch2jwctdy8mnfxep94q9arncc6xecg3xaq889n6e"
    )
    assert (
        UserWallet.load_secret_key(keystore_path, "password", 0).generate_public_key().to_address("drt").to_bech32()
        == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    )


def test_decrypt_secret_key_with_keystore_mnemonic():
    user_wallet = UserWallet.from_mnemonic(DUMMY_MNEMONIC, "")
    mnemonic_json = user_wallet.to_dict()

    with pytest.raises(Exception, match="Expected kind to be secretKey, but it was mnemonic"):
        UserWallet.decrypt_secret_key(mnemonic_json, "")
