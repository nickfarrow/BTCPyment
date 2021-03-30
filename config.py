import sys
import toml

if len(sys.argv) > 1:
    if sys.argv[1] == "--conf":
        if len(sys.argv) == 3:
            conf_path = sys.argv[2]
        else:
            print("Invalid number of arguments, only --conf FILE is supported now", file=sys.stderr)
            sys.exit(1)
    else:
        print("Unknown argument, only --conf FILE is supported now", file=sys.stderr)
        sys.exit(1)
else:
    conf_path = "config.toml"

with open(conf_path, "r") as config_file:
    config = toml.load(config_file)

def get_opt(name, default):
    if name in config:
        return config[name]
    else:
        return default

host = get_opt("host", "127.0.0.1")
rpcport = get_opt("rpcport", "8332")
username = get_opt("username", "bitcoinrpc")
password = get_opt("password", "RPAPASSWORD")
api_key_path = get_opt("api_key_path", "BTCPyment_API_key")
tunnel_host = get_opt("tunnel_host", None)
pollrate = get_opt("pollrate", 15)
payment_timeout = get_opt("payment_timeout", 60*60)
required_confirmations = get_opt("required_confirmations", 2)
connection_attempts = get_opt("connection_attempts", 3)
redirect = get_opt("redirect", "https://github.com/nickfarrow/btcpyment")
pay_method = get_opt("pay_method", "bitcoind")
lnd_dir = get_opt("lnd_dir", "~/.lnd/")
lnd_rpcport = get_opt("lnd_rpcport", "10009")
lnd_macaroon = get_opt("lnd_macaroon", "invoice.macaroon")
lnd_cert = get_opt("lnd_cert", "tls.cert")
free_mode = get_opt("free_mode", False)
