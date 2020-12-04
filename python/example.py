from substrateinterface import SubstrateInterface, Keypair, SubstrateRequestException
from substrateinterface.utils.ss58 import ss58_encode

# the RPC endpoint you want to use
node_rpc = "wss://rpc.pirl.network"

# Generate a new address and get the mnemonic
mnemonic = Keypair.generate_mnemonic()
# create a keypair using the generated mnemonic. Replace with your own mnemonic 
# if you have already address with funds.
keypair = Keypair.create_from_mnemonic(mnemonic)



# send PIRL
def sendPirl(mnemonic, destination, value):
    substrate = SubstrateInterface(
            url=node_rpc,
            address_type=42,
            type_registry_preset='substrate-node-template'
        )
    call = substrate.compose_call(
        call_module='Balances',
        call_function='transfer',
        call_params={
            'dest': destination, # recipient address
            'value': value * 10**12 # we send PIRLs and apply the 12 decimals
            }
        )      
    keypair = Keypair.create_from_mnemonic(mnemonic)
    extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)
    transaction = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
    print("extrinsic_hash: " + transaction['extrinsic_hash'], "block: " + transaction['block_hash'])
