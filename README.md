# BTCPyment
<!---Existing self-custody Bitcoin payment processors are bloated, difficult to install, and not easily customisable.--->
BTCPyment is a simple, easily deployable, lightweight Bitcoin payment processor that connects to your own Bitcoin node or Lightning network node.

Donation Button     ----->  |  Bitcoin Payment Gateway
:-------------------------:|:-------------------------:
[![Donate demo](https://user-images.githubusercontent.com/24557779/108210832-22e33400-7180-11eb-884a-5dbad3cd8f5f.png)](https://try.btcpyment.com/) <br />(Click for embed demo)<br /> Initiates payment -----> |  [![Store demo](https://user-images.githubusercontent.com/24557779/108210961-43ab8980-7180-11eb-88e6-cc90d313076d.png)](https://store.btcpyment.com/) <br />(Click for WordPress payments demo)

BTCPyment currently serves as
1. Donation button for your website that you can easily embed/link to anywhere.
2. A Bitcoin payment gateway, including a Woocommerce plugin that easily turns ANY Wordpress site into a Bitcoin accepting store.

BTCPyment makes donation buttons simple - easy copy paste the one line HTML iframe into your site. With a simple Python backend to talk to your own Bitcoin node, BTCPyment uses RPC to generate new addresses, and monitors the payment status with your own copy of the blockchain.

# Features
* Process payments with your own Bitcoin node via RPC and SSH. Bitcoin core, or any other node software that supports RPC calls.
* Direct peer-to-peer payments without any middleman. No KYC, and greater privacy than donation systems where Bitcoin addresses are reused multiple times.
* Lightweight and highly extendable, basic html and css stying. Modular Python backend, take a [look at the code](server.py) or [lnd.py](/pay/lnd.py)!
* Natively extendable to all bitcoind node features (e.g. segwit) through RPC.
* QR codes, customizable required payment confirmations and payment expiry time.
* No shitcoin bloat. Bitcoin only.

# Installation (short!)
You require a Raspberry Pi / server (VPS) to host an instance of BTCPyment on, and a connection to a Bitcoin node. If you don't have a Bitcoin node, you should [install one](https://bitcoincore.org/en/download/).
### Install
Clone and install dependencies
```
git clone https://github.com/nickfarrow/BTCPyment
cd BTCPyment/
pip3 install -r requirements.txt
```
### Connect to your Bitcoin Node
Edit the `config.py` configuration and point to your Bitcoin node:
```python
host = "127.0.0.1"
rpcport = "8332"
username = "bitcoinrpc"
password = "RPCPASSWORD"
```
(You can find these in `~/.bitcoin/bitcoin.conf`). If your node is remote to your server, you can specify an SSH `tunnel_host = "pi@192.168.0.252"` that will forward `rpcport`. You may also need to set `rpcallowip=YOUR_SERVER_IP` in your `~/.bitcoin/bitcoin.conf`. If you want to use lightning network payments, see [Lightning instructions](docs/lightning.md)].

### Run BTCPyment
Run BTCPyment with
```
gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8000 server:app
```
Gunicorn is a lightweight python HTTP server, alternatively you can run with just `python server.py` though this is not recommended for production.

That's it! You should now be able to view your BTCPyment server at `http://YOUR_SERVER_IP:8000/`. If running locally, this will be `127.0.0.1:8000`.

If running on a Raspberry Pi, you will want to [forward port 8000 in your router settings](https://user-images.githubusercontent.com/24557779/105681219-f0f5fd80-5f44-11eb-942d-b574367a161f.png) so that BTCPYment is also visible at your external IP address. You might have to allow gunicorn through your firewall with `sudo ufw allow 8000`.

You will want to run gunicorn with nohup so it continues serving in the background:
```
nohup gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8000 server:app > log.txt 2>&1 &
tail -f log.txt
```

## Embed a Donation Button
Now embed the donation button into your website HTML:
```html
<iframe src="http://YOUR_SERVER_IP:8000/" style="margin: 0 auto;display:block;width:420px;height:240px;border:none;overflow:hidden;" scrolling="no"></iframe>
```
Changing `YOUR_SERVER_IP` to the IP address of the machine you're running BTCPyment on. Optionally, you can redirect a domain to that IP and use that instead.

### Using HTTPS & Domains
Embedded iframes are easy if your site only uses HTTP. But if your site uses HTTPS, then you can see your donation button at `http://YOUR_SERVER_IP:8000/` but will not be able to in an embedded iframe. See [HTTPS instructions](docs/HTTPS.md).

### Security
For maximum security, we recommend hosting on a machine where your node only has access to a **watch-only** wallet.


# Payment Gateway (Woocommerce)
Currently we have a plugin for Woocommerce in Wordpress that makes Bitcoin webstores extremely easy, [please click here for installation instructions](docs/woocommerce.md). BTCPyment acts as a custom payment gateway for Woocommerce via the php plugin found in `/gateways`. We have plans to extend to other web stores in the future.

# Contributions welcomed
### You only need a little python!
The main code can be found in [server.py](server.py). The client-side logic for the donation button sits in [static/server_connection.js](static/server_connection.js), invoice structure and bitcoind interface in [invoice/](invoice/), button appearance in [template/index.html](template/index.html), and Woocommerce plugin in [gateways/woo_btcpyment.php](gateways/woo_btcpyment.php). Please have ago at implementing some of the things below!

![docs/diagram.png](docs/diagram.png)

# Coming soon:
* **Better UI** with more variety of size and theme.
    * Add a currency toggle between BTC/USD on donation html.
* Handle unconfirmed payments. What is the best course of action?
* More readily customisable donation button (text/color/QR code)
* Database integration for payment invoices
* Variety or easily customisable price feeds

# Disclaimer
BTCPyment is in very early development. As such, we are not responsible for any loss of funds, vulnerabilities with software, or any other grievances which may arise. Always confirm large payments manually.

# Sponsor
Please consider [supporting me](https://btcpyment.nickfarrow.com) via my own instance of BTCPyment :). Corporate/whale support would greatly assist my ability to give 100% of my attention to BTCPyment and other Bitcoin projects, please email `baseddepartment@nickfarrow.com`.
