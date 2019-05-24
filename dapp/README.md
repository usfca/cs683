# Lottery Application on My Blockchain

I build my own blockchain in golang. And on top of my blockchain, I implement a simple lottery application. 
https://github.com/QiyanYu/dapp

## My Blockchain

### Merkle Patricia Trie

Merkle Patricia tries provide a cryptographically authenticated data structure that can be used to store all (key, value) bindings. They are fully deterministic, meaning that a Patricia trie with the same (key,value) bindings is guaranteed to be exactly the same down to the last byte and therefore have the same root hash, provide the holy grail of O(log(n)) efficiency for inserts, lookups and deletes, and are much easier to understand and code than more complex comparison-based alternatives like red-black tries.

Build my own implementation of a Merkle Patricia Trie, following the specifications at the Ethereum wiki. Ethereum uses a Merkle Patricia Tree. Links to an external site. to store the transaction data in a block. By organizing the transaction data in a Merkle Patricia Tree, any block with fraudulent transactions would not match the tree's root hash. 

### Concurrency

- The latest block of blockchain will reach all the peers online.
- Does not create too much congestion.

Every user would hold a PeerList of up to 32 peer nodes. The PeerList can temporarily hold more than 32 nodes, but before sending HeartBeats, a node will first re-balance the PeerList by choosing the 32 closest peers. And the heartbeat will hop only 3 times in case of over-shotting problem.

### Simple Proof of Work

Because we don't want to everyone produce block too easy, they need to pay something to get the right of producing block. Simple Proof of Work(PoW) is the simplest way to make everyone became a miner to participate into blockchain. The puzzle is that you need to find out a string that have a particular prefix.

My blockchain requires the hash of a block to begin with a certain amount of 0s. Since you cannot influence a hash function, the system has to try multiple combinations to arrive at a hash value that begins with that number of 0s. This is the puzzle that miners need to solve which requires a lot of computing power.

## Lottery Application

This application is for buying lottery. 

### Sign up
type *signup {password}*

User just provides password, username is auto-generated. This is because the blockchain does not write the data into the chain immediately, so when user sign up, the app cannot check the existed username and there can be two or more users used same username. In this case, I can prevent duplicate username in blockchain.

I use MD5 to make the username shorter. It hash the current Unix time.

At this time, when you sign up a new account, your balance will automatically be $10, for buying lottery.

If the sign up success, it will return username, otherwise it will show error.

### Login
type *login {username} {password}*

When you login, will use username as key to retrieve transaction in blockchain, then compare this password with user's provide password, and then it will check if the last transaction is finished, if not, it means that the user did not finish last time. 

When you login successfully, the app will store this retrieved transaction.

### Lucky
type *lucky {5 nums}*

This is the for generate the lottey numbers. For now, the app will generate 5 numbers range from 1 to 10.

Random function set the seed with username's hash value plus current Unix time. 