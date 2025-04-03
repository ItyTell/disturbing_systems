import hashlib
import secrets
import time

class SimpleBlockchain:
    def __init__(self, name):
        self.name = name
        self.contracts = {}
        self.block_height = 0
    
    def increase_blocks(self, count=1):
        self.block_height += count
        print(f"{self.name} blockchain advanced to block {self.block_height}")
    
    def create_swap_contract(self, sender, receiver, amount, secret_hash, timelock):
        contract_id = f"{self.name}-{len(self.contracts) + 1}"
        contract = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "secret_hash": secret_hash,
            "timelock": self.block_height + timelock,
            "claimed": False,
            "refunded": False,
            "secret_revealed": None
        }
        self.contracts[contract_id] = contract
        #log
        print(f"Created contract on {self.name}:")
        print(f"  ID: {contract_id}")
        print(f"  Amount: {amount} {self.name}")
        print(f"  Sender: {sender}")
        print(f"  Receiver: {receiver}")
        print(f"  Timelock: expires at block {contract.get('timelock')}")
        
        return contract_id
    
    def claim_with_secret(self, contract_id, secret):

        if contract_id not in self.contracts:
            print(f"Contract {contract_id} not found!")
            return False
        
        contract = self.contracts[contract_id]
        
        if contract["claimed"] or contract["refunded"]:
            print(f"Contract {contract_id} already settled!")
            return False
        
        computed_hash = hashlib.sha256(secret.encode()).hexdigest()
        if computed_hash != contract["secret_hash"]:
            print(f"Invalid secret for contract {contract_id}!")
            return False
        
        contract["claimed"] = True
        contract["secret_revealed"] = secret
        
        print(f"✓ Successfully claimed {contract['amount']} {self.name} from contract {contract_id}")
        print(f"  Secret revealed: {secret}")
        
        return True
    
    def refund(self, contract_id):
        if contract_id not in self.contracts:
            print(f"Contract {contract_id} not found!")
            return False
        
        contract = self.contracts[contract_id]
        
        if contract["claimed"] or contract["refunded"]:
            print(f"Contract {contract_id} already settled!")
            return False
        
        if self.block_height < contract["timelock"]:
            blocks_remaining = contract["timelock"] - self.block_height
            print(f"Cannot refund yet! Timelock expires in {blocks_remaining} blocks.")
            return False
        
        contract["refunded"] = True
        
        print(f"✓ Refunded {contract['amount']} {self.name} to {contract['sender']}")
        
        return True
    
    def get_revealed_secret(self, contract_id):
        if contract_id not in self.contracts:
            print(f"Contract {contract_id} not found!")
            return None
        
        contract = self.contracts[contract_id]
        return contract.get("secret_revealed")


def perform_atomic_swap():
    bitcoin = SimpleBlockchain("Bitcoin")
    ethereum = SimpleBlockchain("Ethereum")
    
    Carolina = "Carolina"
    bob = "Bob"
    
    print("=" * 50)
    print("ATOMIC SWAP: Carolina's BTC for Bob's ETH")
    print("=" * 50)
    
    secret = secrets.token_hex(16)
    secret_hash = hashlib.sha256(secret.encode()).hexdigest()
    
    print(f"Carolina generates secret: {secret}")
    print(f"Corresponding hash: {secret_hash}")
    print("-" * 50)
    
    print("STEP 1: Carolina creates Bitcoin contract")
    btc_contract = bitcoin.create_swap_contract(
        sender=Carolina,
        receiver=bob,
        amount=1.0,
        secret_hash=secret_hash,
        timelock=24  # 24 blocks, longer timelock
    )
    print("-" * 50)
    
    print("STEP 2: Bob creates Ethereum contract")
    eth_contract = ethereum.create_swap_contract(
        sender=bob,
        receiver=Carolina,
        amount=15.0,
        secret_hash=secret_hash,
        timelock=12  # 12 blocks, shorter timelock
    )
    print("-" * 50)
    
    print("STEP 3: Carolina claims ETH with secret")
    ethereum.claim_with_secret(eth_contract, secret)
    print("-" * 50)
    
    print("STEP 4: Bob extracts secret and claims BTC")
    revealed_secret = ethereum.get_revealed_secret(eth_contract)
    if revealed_secret:
        print(f"Bob sees the revealed secret: {revealed_secret}")
        bitcoin.claim_with_secret(btc_contract, revealed_secret)
    print("-" * 50)
    
    print("✓ Atomic swap completed successfully!")
    print("  Carolina received: 15.0 ETH")
    print("  Bob received: 1.0 BTC")


def simulate_refund_scenario():
    bitcoin = SimpleBlockchain("Bitcoin")
    ethereum = SimpleBlockchain("Ethereum")
    
    Carolina = "Carolina"
    bob = "Bob"
    
    print("\n" + "=" * 50)
    print("FAILED SWAP SCENARIO (REFUND)")
    print("=" * 50)
    
    secret = secrets.token_hex(16)
    secret_hash = hashlib.sha256(secret.encode()).hexdigest()
    
    print(f"Carolina generates secret: {secret}")
    print("-" * 50)
    
    print("STEP 1: Carolina creates Bitcoin contract")
    btc_contract = bitcoin.create_swap_contract(
        sender=Carolina,
        receiver=bob,
        amount=1.0,
        secret_hash=secret_hash,
        timelock=24
    )
    print("-" * 50)
    
    print("STEP 2: Bob creates Ethereum contract")
    eth_contract = ethereum.create_swap_contract(
        sender=bob,
        receiver=Carolina,
        amount=15.0,
        secret_hash=secret_hash,
        timelock=12
    )
    print("-" * 50)
    
    print("STEP 3: Carolina never claims the ETH...")
    print("Time passes...")
    
    ethereum.increase_blocks(15)
    bitcoin.increase_blocks(15)
    print("-" * 50)
    
    print("STEP 4: Bob refunds his ETH")
    ethereum.refund(eth_contract)
    print("-" * 50)
    
    print("STEP 5: Carolina tries to refund BTC but timelock hasn't expired")
    bitcoin.refund(btc_contract)
    
    print("More time passes...")
    bitcoin.increase_blocks(10) 
    print("-" * 50)
    
    print("STEP 6: Carolina refunds her BTC")
    bitcoin.refund(btc_contract)
    print("-" * 50)
    
    print("✓ Swap cancelled and all funds returned")


if __name__ == "__main__":
    perform_atomic_swap()
    
    simulate_refund_scenario()