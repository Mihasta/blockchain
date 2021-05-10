from flask import Flask, redirect, url_for, render_template, request
from web3 import Web3
import json

app = Flask(__name__)

infura_url = 'https://ropsten.infura.io/v3/8d317ca2d1664857bea20e240e716acc'
address = '0x2DBA19d3919FdE7f59C14577540987424c124E1E'
contract_address = '0x09643C595470e5527A71cA2aC8A5fCaFcCf87D88'
private_key = 'fb43d987992edea118e53df8e3a77acc25ba3c6dfbf3af6fcdccb1bd54c23e15'

w3 = Web3(Web3.HTTPProvider(infura_url))
w3.eth.defaultAccount = address

with open('rosreestr.abi') as f:
    abi = json.load(f)

contract = w3.eth.contract(address=contract_address, abi=abi)


@app.route("/")
def base():
    return render_template("base.html")

@app.route("/get_owner")
def get_owner():
    own = contract.functions.GetOwner().call()
    return render_template("base.html", own=own)

@app.route("/get_cost")
def get_cost():
    cost = contract.functions.GetCost().call()
    return render_template("base.html", cost=cost)

@app.route("/get_balance")
def get_balance():
    bln = w3.eth.getBalance(address)
    balance = w3.fromWei(bln, 'ether')
    return render_template("base.html", balance=balance)

@app.route("/add_employee")
def to_add_emp():
    return render_template("add_or_edit_employee.html", add=True)

@app.route("/get_employee")
def to_get_emp():
    return render_template("get_or_delete_employee.html", get=True)

@app.route("/edit_employee")
def to_edit_emp():
    return render_template("add_or_edit_employee.html", edit=True)

@app.route("/delete_employee")
def to_delete_emp():
    return render_template("get_or_delete_employee.html", delete=True)

@app.route("/add_employee", methods=['POST'])
def add_employee():
    nonce = w3.eth.getTransactionCount(address)
    adr = request.form.get("adr")
    name = request.form.get("name")
    pos = request.form.get("pos")
    phone = request.form.get("phone")
    empl_tr = contract.functions.AddEmployee(adr, name, pos, phone).buildTransaction({
        'gas': 3000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'from': address,
        'nonce': nonce,
    })
    signed_tr = w3.eth.account.signTransaction(empl_tr, private_key=private_key)
    w3.eth.sendRawTransaction(signed_tr.rawTransaction)
    return render_template("base.html", inf="Success: Employee added")

@app.route("/get_employee", methods=['POST'])
def get_employee():
    adr = request.form.get("adr")
    empl = contract.functions.GetEmployee(adr).call()
    return render_template("base.html", empl=empl)

@app.route("/edit_employee", methods=['POST'])
def edit_employee():
    nonce = w3.eth.getTransactionCount(address)
    adr = request.form.get("adr")
    name = request.form.get("name")
    pos = request.form.get("pos")
    phone = request.form.get("phone")
    empl_tr = contract.functions.EditEmployee(adr, name, pos, phone).buildTransaction({
        'gas': 3000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'from': address,
        'nonce': nonce,
    })
    signed_tr = w3.eth.account.signTransaction(empl_tr, private_key=private_key)
    w3.eth.sendRawTransaction(signed_tr.rawTransaction)
    return render_template("base.html", inf="Success: Employee edited")

@app.route("/delete_employee", methods=['POST'])
def delete_employee():
    nonce = w3.eth.getTransactionCount(address)
    adr = request.form.get("adr")
    empl_tr = contract.functions.DeleteEmployee(adr).buildTransaction({
        'gas': 3000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'from': address,
        'nonce': nonce,
    })
    signed_tr = w3.eth.account.signTransaction(empl_tr, private_key=private_key)
    w3.eth.sendRawTransaction(signed_tr.rawTransaction)
    return render_template("base.html", inf="Success: Employee deleted")

@app.route("/add_request")
def to_add_req():
    return render_template("add_request.html")

@app.route("/add_request", methods=['POST'])
def add_request():
    nonce = w3.eth.getTransactionCount(address)
    r_type = request.form.get("r_type")
    adr = request.form.get("adr")
    area = request.form.get("area")
    cost = request.form.get("cost")
    new_owner = request.form.get("new_owner")
    req_tr = contract.functions.AddRequest(int(r_type), str(adr), int(area), int(cost), new_owner).buildTransaction({
        'gas': 3000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'from': address,
        'nonce': nonce,
        'value': w3.toWei('100', 'wei')
    })
    signed_tr = w3.eth.account.signTransaction(req_tr, private_key=private_key)
    w3.eth.sendRawTransaction(signed_tr.rawTransaction)
    return render_template("base.html", inf="Success: Request added")

@app.route("/get_request")
def get_request():
    req = contract.functions.GetRequest().call()
    return render_template("base.html", req=req)

@app.route("/process_request")
def to_process_request():
    return render_template("process_request.html")

@app.route("/process_request", methods=['POST'])
def process_request():
    nonce = w3.eth.getTransactionCount(address)
    req_id = request.form.get("req_id")
    req_tr = contract.functions.ProcessRequest(int(req_id)).buildTransaction({
        'gas': 3000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'from': address,
        'nonce': nonce,
    })
    signed_tr = w3.eth.account.signTransaction(req_tr, private_key=private_key)
    w3.eth.sendRawTransaction(signed_tr.rawTransaction)
    return render_template("base.html", inf="Success: Request processed")

@app.route("/get_list_home")
def get_list_home():
    list_home = contract.functions.GetListHome().call()
    return render_template("base.html", list_home=list_home)


if __name__ == "__main__":
    app.run(debug=True)