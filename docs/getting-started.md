#### Table of contents

- [README.md](https://github.com/StakeSquid/graphprotocol-testnet-docker/blob/master/README.md)
- [Pre-requisites](https://github.com/StakeSquid/graphprotocol-testnet-docker/blob/master/docs/pre-requisites.md)
- [Getting Started](https://github.com/StakeSquid/graphprotocol-testnet-docker/blob/master/docs/getting-started.md) <- you are here
- [Advanced Configuration](https://github.com/StakeSquid/graphprotocol-testnet-docker/blob/master/docs/advanced-config.md)
- [Setting Up Allocations](https://github.com/StakeSquid/graphprotocol-testnet-docker/blob/master/docs/allocations.md)
- [Setting Up Cost Models](https://github.com/StakeSquid/graphprotocol-testnet-docker/blob/master/docs/costmodels.md)
- [Tips and Tricks](https://github.com/StakeSquid/graphprotocol-testnet-docker/blob/master/docs/tips.md)
- [Troubleshooting](https://github.com/StakeSquid/graphprotocol-testnet-docker/blob/master/docs/troubleshooting.md)



## Install from scratch

Run the following commands to clone the repository and set everything up:

```bash
git clone git@github.com:StakeSquid/graphprotocol-testnet-docker.git
cd graphprotocol-testnet-docker
git submodule init
git submodule update
git config --global user.email "you@example.com"
git config --global user.name "Example User"
git branch --set-upstream-to=origin


```



## Get a domain

To enable SSL on your host you should get a domain.

You can use any domain and any regsitrar that allowes you to edit DNS records to point subdomains to your IP address.

For a free option go to [myFreenom](https://my.freenom.com/) and find a free domain name. Create a account and complete the registration.

In the last step choose "use dns" and enter the IP address of your server. You can choose up to 12 months for free.

Under "Service > My Domains > Manage Domain > Manage Freenom DNS" you can add more subdomains later.

Create 3 subdomains, named as follows:
```
index.sld.tld
query.sld.tld
grafana.sld.tld
```



## Create a mnemonic

You need a wallet with a seed phrase that is registered as your operator wallet. This wallet will be the one that makes transactions on behalf of your main wallet (which holds and stakes the GRT).

The operator wallet has limited functionality, and it's recommended to be used for security reasons.

*You need a 12-word, or 15-word mnemonic phrase in order for it to work.*

To make yourself a mnemonic eth wallet you can go to this [website](https://iancoleman.io/bip39/), select ETH from the dropdown and press generate.

You get a seed phrase in the input field labeled BIP39 Mnemonic.

You can find your address, public key and private key in the first row of the table if you scroll down the page in the section with the heading "Derived Addresses".

**Make sure you save the mnemonic, private key and the wallet address somewhere safe.**

If you need, you can import the wallet using the private key into Metamask



## Configure the environment variables

Edit the file called `start` and add your values to the following envs:

```bash
EMAIL=email@domain.com \
INDEX_HOST=index.sld.tld \
QUERY_HOST=query.sld.tld \
GRAFANA_HOST=grafana.sld.tld \
ADMIN_USER=your_user \
ADMIN_PASSWORD=your_password \
DB_USER=your_db_user \
DB_PASS=your_db_password \
GRAPH_NODE_DB_NAME=your_graphnode_db_name \
AGENT_DB_NAME=your_agent_db_name \
MAINNET_RPC_0="http://ip:port" \
GOERLI_RPC="http://ip:port" \
TXN_RPC="http://ip:port" \
OPERATOR_SEED_PHRASE="12 or 15 word mnemonic" \
STAKING_WALLET_ADDRESS=0xAdDreSs \
GEO_COORDINATES="69.420 69.420" \
docker-compose up -d --remove-orphans --build $@


#The following ENV vars are optional
#they need to be added above the last line containing
#docker-compose...

#QUERY_FEE_REBATE_CLAIM_THRESHOLD=number-in-grt \
#REBATE_CLAIM_BATCH_THRESHOLD=number-in-grt \
#NETWORK_SUBGRAPH_DEPLOYMENT=QmTePWCvPedmVxAvPnDFmFVxxYNW73z6xisyKCL2xa5P6e \
#INDEXER_AGENT_OFFCHAIN_SUBGRAPHS="Qm,Qm,Qm" \
#GRAPHNODE_LOGLEVEL=warn \
#ETHEREUM_TRACE_STREAM_STEP_SIZE=100 \
#ETHEREUM_BLOCK_BATCH_SIZE=50 \
#ETHEREUM_RPC_MAX_PARALLEL_REQUESTS=128 \
#GRAPH_ETHEREUM_MAX_BLOCK_RANGE_SIZE=1000 \
#GRAPH_ETHEREUM_TARGET_TRIGGERS_PER_BLOCK_RANGE=500 \
#INDEXER_AGENT_GAS_PRICE_MAX=gas-price-in-gwei \
#GRAPH_GRAPHQL_WARN_RESULT_SIZE=bytes \
#GRAPH_GRAPHQL_ERROR_RESULT_SIZE=bytes \

```

**Required env vars:**
- `EMAIL` - only used as contact to create SSL certificates. Usually it doesn't receive any emails but is required by the certificate issuer.
- `INDEX_HOST` - your indexer public endpoint. The gateway will be sending queries to this endpoint.
- `QUERY_HOST` - your query public playground. You can use this endpoint to send test queries directly into your Graph infrastructure to see if everything works properly. This env var is not present on the Mainnet Docker build.
- `GRAFANA_HOST` - your Grafana dashboard for indexer stack monitoring.
- `ADMIN_USER` and `ADMIN_PASSWORD` - will be used by Grafana, Prometheus and AlertManager.
- `DB_USER` and `DB_PASS` - will be used for initializing the PostgreSQL Databases (both index/query DB and indexer agent/service DB).
- `GRAPH_NODE_DB_NAME` - the name of the database used by the Index/Query nodes.
- `AGENT_DB_NAME` - the name of the database used by the Indexer agent/service nodes.
- `ETHERUM_RPC_0` and `ETHEREUM_RPC_1` - your ETH RPCs used by the index nodes. They can be different URLs or the same, up to you.
- `TXN_RPC` - your ETH RPC used by Indexer agent/service nodes. This can be a fast/full/archive node, up to you! Please note that using Erigon as the TXN_RPC has proven unreliable by some indexers.
- `OPERATOR_SEED_PHRASE` - the 12/15 word mnemonic that you generated earlier. Will be used by the Agent/Service to send transactions (open/close allocations, etc)
- `STAKING_WALLET_ADDRESS` - the address (0x...) that you staked your GRT with, ideally living on an entirely different mnemonic phrase than your Operator Wallet. 
- `GEO_COORDINATES` of your server - you can search for an ip location website and check your server exact coordinates.

**Optional env vars:**
- `QUERY_FEE_REBATE_CLAIM_THRESHOLD`  - the minimum amount of GRT to claim per allocation
- `REBATE_CLAIM_BATCH_THRESHOLD` - the minimum amount of Total GRT to batch claim for all allocations combined
- `NETWORK_SUBGRAPH_DEPLOYMENT` - The Mainnet Network Subgraph IPFS hash, used if you want to rely on your own subgraph deployment rather than the gateways subgraphs 
- `INDEXER_AGENT_OFFCHAIN_SUBGRAPHS` - Gives you the possibility of syncing subgraphs locally without allocating to them onchain
- `GRAPHNODE_LOGLEVEL` - the log level of the graph-node (indexer/query) - trace/debug/info/warn/error - if you have a whackton of subgraphs, increasing the loglevel to warn/error helps lowering the indexing time
- `ETHEREUM_TRACE_STREAM_STEP_SIZE` - this helps (or not) indexing times by very small margins - use at own risk
- `ETHEREUM_TRACE_STREAM_STEP_SIZE` - this helps (or not) indexing times by very small margins - use at own risk
- `ETHEREUM_BLOCK_BATCH_SIZE` - this helps (or not) indexing times by very small margins - use at own risk
- `ETHEREUM_RPC_MAX_PARALLEL_REQUESTS` - this helps (or not) indexing times by very small margins - use at own risk
- `GRAPH_ETHEREUM_MAX_BLOCK_RANGE_SIZE` - this helps (or not) indexing times by very small margins - use at own risk
- `GRAPH_ETHEREUM_TARGET_TRIGGERS_PER_BLOCK_RANGE` - this helps (or not) indexing times by very small margins - use at own risk
- `INDEXER_AGENT_GAS_PRICE_MAX` - the maximum Gas Price (GWEI) that the indexer-agent will attempt to send transactions with
- `GRAPH_GRAPHQL_WARN_RESULT_SIZE` - these vars are disabled in docker-compose.yaml for the time being, do not uncomment and leave empty
- `GRAPH_GRAPHQL_ERROR_RESULT_SIZE` - these vars are disabled in docker-compose.yaml for the time being, do not uncomment and leave empty

**Note:** If you want to use any of the optional env vars, you need to copy the line that you want to enable above the `docker-compose up...` part, and uncomment it. Do NOT uncomment lines below it, or comment lines above it.


**Containers:**
* Graph Node (query node)
* Graph Node (index node)
* Indexer Agent
* Indexer Service
* Indexer CLI
* Postgres Database for the index/query nodes
* Postgres Database for the agent/service nodes
* Prometheus (metrics database) `http://<host-ip>:9090`
* Prometheus-Pushgateway (push acceptor for ephemeral and batch jobs) `http://<host-ip>:9091`
* AlertManager (alerts management) `http://<host-ip>:9093`
* Grafana (visualize metrics) `http://<host-ip>:3000`
* NodeExporter (host metrics collector)
* cAdvisor (containers metrics collector)
* Caddy (reverse proxy and basic auth provider for prometheus and alertmanager)



**Additional configs and details:**

- Agent/Service - [networks.md](https://github.com/graphprotocol/indexer/blob/main/docs/networks.md)
- Graph-Node - [environment-variables.md](https://github.com/graphprotocol/graph-node/blob/master/docs/environment-variables.md)


## Start

To start, all you need to do is to:

```bash
bash start


```

Be aware that initially it takes several minutes to download and run all the containers (especially the cli container, that one takes a while to build), so be patient. :)

Subsequent restarts will be much faster.

In case something goes wrong, find the problem, edit the variables, and add `--force-recreate` at the end of the command, plus the container you want to recreate:

```bash 
bash start --force-recreate <container_name>

```

Or to recreate the entire stack:

```bash 
bash start --force-recreate

```


## Verify that it runs properly

To verify that everything is up and running, you need to:

```bash
docker ps

```

And look for containers that are crash looping - you will notice `restarting` and a countdown - that means those containers are not working properly.

To further debug, try looking for the container logs and see what they say. 
More information in the [troubleshooting](https://github.com/StakeSquid/graphprotocol-testnet-docker/blob/master/docs/troubleshooting.md) section.




## Indexer Infrastructure Ports

### Ports Overview

The following ports are being used by all components by default. Also listed are
the CLI flags and environment variables that can be used to change the ports.

#### Graphical Overview

![](https://raw.githubusercontent.com/graphprotocol/mission-control-indexer/master/files/ports.png)

#### Graph Node

| Port | Purpose                                    | Routes                                             | CLI argument        | Environment variable |
| ---- | ------------------------------------------ | -------------------------------------------------- | ------------------- | -------------------- |
| 8000 | GraphQL HTTP server (for subgraph queries) | `/subgraphs/id/...` <br/> `subgraphs/name/.../...` | `--http-port`       | -                    |
| 8001 | GraphQL WS (for subgraph subscriptions)    | `/subgraphs/id/...` <br/> `subgraphs/name/.../...` | `--ws-port`         | -                    |
| 8020 | JSON-RPC (for managing deployments)        | `/`                                                | `--admin-port`      | -                    |
| 8030 | Subgraph indexing status API               | `/graphql`                                         | `--index-node-port` | -                    |
| 8040 | Prometheus metrics                         | `/metrics`                                         | `--metrics-port`    | -                    |

#### Indexer Service

| Port | Purpose                                         | Routes                                                              | CLI argument | Environment variable   |
| ---- | ----------------------------------------------- | ------------------------------------------------------------------- | ------------ | ---------------------- |
| 7600 | GraphQL HTTP server (for paid subgraph queries) | `/subgraphs/id/...` <br/> `/status` | `--port`     | `INDEXER_SERVICE_PORT` |
| 7300 | Prometheus metrics                              | `/metrics`                                                          | -            | -                      |

#### Indexer Agent

| Port | Purpose                                      | Routes | CLI argument                | Environment variable                    |
| ---- | -------------------------------------------- | ------ | --------------------------- | --------------------------------------- |
| 8000 | Indexer management API (for `graph indexer`) | `/`    | `--indexer-management-port` | `INDEXER_AGENT_INDEXER_MANAGEMENT_PORT` |



## Install or Update the Agora and Qlog modules

To update those repos to the latest version just do the following command occasionally.

```bash
git submodule update

```



To use qlog or agora execute the `runqlog` or `runagora` scripts in the root of the repository.

```bash
./runagora --help
./runqlog --help

```



This will use the compiled qlog tool and extract queries since yesterday or 5 hours ago and store them to the query-logs folder.

```bash
./extract_queries_since yesterday
./extract_queries_since "5 hours ago"

```



To make journald logs persistent across restarts you need to create a folder for the logs to store in like this:

```
mkdir -p /var/log/journal

```






## Updates and Upgrades

The general procedure is the following:

```bash
cd <project-folder>
git fetch
git pull

```

This will update the scripts from the repository.

To upgrade the containers:
```bash
bash start --force-recreate

```


To update Agora or Qlog repos to the latest version just do the following command occasionally:

```bash
git submodule update

```


To use qlog or agora execute the `runqlog` or `runagora` scripts in the root of the repository.

```bash
./runagora --help
./runqlog --help

```







#### Table of contents

- [README.md](https://github.com/StakeSquid/graphprotocol-testnet-docker/blob/master/README.md)
- [Pre-requisites](https://github.com/StakeSquid/graphprotocol-testnet-docker/blob/master/docs/pre-requisites.md)
- [Getting Started](https://github.com/StakeSquid/graphprotocol-testnet-docker/blob/master/docs/getting-started.md) <- you are here
- [Advanced Configuration](https://github.com/StakeSquid/graphprotocol-testnet-docker/blob/master/docs/advanced-config.md)
- [Setting Up Allocations](https://github.com/StakeSquid/graphprotocol-testnet-docker/blob/master/docs/allocations.md)
- [Setting Up Cost Models](https://github.com/StakeSquid/graphprotocol-testnet-docker/blob/master/docs/costmodels.md)
- [Tips and Tricks](https://github.com/StakeSquid/graphprotocol-testnet-docker/blob/master/docs/tips.md)
- [Troubleshooting](https://github.com/StakeSquid/graphprotocol-testnet-docker/blob/master/docs/troubleshooting.md)
