from flask import Flask, render_template, request
import requests
import re

app = Flask(__name__)

SECRET  = "725a4d590096f971b61a79faa5abc905"
URL = "https://eth-mainnet.gateway.pokt.network/v1/lb/618ee32ee365be00341be117"
HDR = {
	"Content-Type": "application/json",
	"user": SECRET
}

def use(method, params=[]):
    '''To call a method using the Pocket API'''
    DAT = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_"+method,
        "params": params
    }
    r = requests.post(URL, headers=HDR, json=DAT)
    print(method, ":", r.status_code, r.reason)
    try:
        ans = r.json()["result"]
    except Exception:
        ans = r.json()["error"]
    return ans

def weiToEth(hexWeiValue):
    '''To convert Wei to Eth'''
    wei = int(hexWeiValue, 0)
    strVal = str(wei)
    if(len(strVal)>18):
        return strVal[:-18]+"."+strVal[-18:]
    else:
        residue = ''.join(['0' for _ in range(18-len(strVal))])
        return '0.'+ residue + strVal

# Single page
@app.route('/', methods=['GET', 'POST'])
def main():
    '''Main method'''
    kwargs = {}
    kwargs['gas'] = weiToEth(use("gasPrice"))
    if request.method == "POST":
        add = request.form['address']
        kwargs['address'] = add
        addRegex = re.compile(r"0x[0-9a-fA-F]{40}")
        validAdd = addRegex.search(add)
        if(validAdd):
            kwargs['balance'] = weiToEth(use("getBalance", [add, "latest"]))
        else:
            kwargs['balance'] = -1
    return render_template("index.html", **kwargs)

if __name__=="__main__":
    app.debug = True
    app.run()