import os
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from web3 import Web3


class PolygonService:
    """Minimal Polygon (MATIC) integration using Web3.py"""

    def __init__(self) -> None:
        load_dotenv(override=True)

        rpc_url = os.getenv("POLYGON_RPC_URL", "")
        if not rpc_url:
            raise ValueError("POLYGON_RPC_URL is not configured in environment")

        self.web3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={"timeout": 20}))
        if not self.web3.is_connected():
            raise ConnectionError("Failed to connect to Polygon RPC")

        self.chain_id = int(os.getenv("POLYGON_CHAIN_ID", "137"))  # 137 = mainnet, 80001 = Mumbai

        # Optional server wallet for server-initiated transfers
        self.server_private_key = os.getenv("POLYGON_PRIVATE_KEY")
        self.server_address = None
        if self.server_private_key:
            acct = self.web3.eth.account.from_key(self.server_private_key)
            self.server_address = acct.address

    def get_network_info(self) -> Dict[str, Any]:
        return {
            "chain_id": self.chain_id,
            "client_version": self.web3.client_version,
            "is_connected": self.web3.is_connected(),
            "block_number": self.web3.eth.block_number,
        }

    def get_balance(self, address: str) -> Dict[str, Any]:
        checksum = self.web3.to_checksum_address(address)
        wei = self.web3.eth.get_balance(checksum)
        return {
            "address": checksum,
            "balance_wei": str(wei),
            "balance_matic": self.web3.from_wei(wei, "ether"),
        }

    def transfer_native(self, to_address: str, amount_matic: float, from_private_key: Optional[str] = None) -> Dict[str, Any]:
        """Send native MATIC. Uses provided key, else server key if configured."""
        private_key = from_private_key or self.server_private_key
        if not private_key:
            raise ValueError("No private key provided and POLYGON_PRIVATE_KEY not set")

        account = self.web3.eth.account.from_key(private_key)
        to_checksum = self.web3.to_checksum_address(to_address)

        nonce = self.web3.eth.get_transaction_count(account.address)
        tx = {
            "nonce": nonce,
            "to": to_checksum,
            "value": self.web3.to_wei(amount_matic, "ether"),
            "gas": 21000,
            "maxFeePerGas": self.web3.to_wei("60", "gwei"),
            "maxPriorityFeePerGas": self.web3.to_wei("30", "gwei"),
            "chainId": self.chain_id,
            "type": 2,
        }

        signed = self.web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed.raw_transaction)
        return {"tx_hash": tx_hash.hex(), "from": account.address, "to": to_checksum, "amount_matic": amount_matic}


