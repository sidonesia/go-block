import json
import time
import pymongo
import sys
import urllib.parse
import base64

sys.path.append("pytavia_core"    ) 
sys.path.append("pytavia_settings") 
sys.path.append("pytavia_stdlib"  ) 
sys.path.append("pytavia_storage" ) 
sys.path.append("pytavia_modules" ) 
sys.path.append("pytavia_modules/blockchain") 
sys.path.append("pytavia_modules/transaction") 
sys.path.append("pytavia_modules/view") 
sys.path.append("pytavia_modules/insurance") 

from blockchain      import create_block
from blockchain      import get_blockchain
from blockchain      import initiate_block
from transaction     import verify_transaction
from transaction     import add_transaction
from transaction     import get_transaction

from view            import view_blockchain
from view            import view_index
from view            import view_policy
from view            import view_api

# adding comments
from pytavia_stdlib  import utils
from pytavia_core    import database 
from pytavia_core    import config 
from pytavia_core    import model
from pytavia_stdlib  import idgen 

##########################################################

from flask import request
from flask import render_template
from flask import Flask
from flask import session
from flask import make_response
from flask import redirect
from flask import url_for
from flask import flash


from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import CSRFError
#
# Main app configurations
#
app             = Flask( __name__, config.G_STATIC_URL_PATH )
app.secret_key  = config.G_FLASK_SECRET
app.db_update_context, app.db_table_fks = model.get_db_table_paths(model.db)

########################## CALLBACK API ###################################

# -- DONE --
@app.route("/api/mine-block", methods=["POST"])
def mine_block():
    params = request.form.to_dict()
    response = mine_block.mine_block(app).process( params )
    return response.http_stringify()
# end def

# -- DONE --
@app.route("/api/initiate-block", methods=["POST"])
def start_initiate_block():
    params = request.form.to_dict()
    response = initiate_block.initiate_block(app).process( params )
    return response.http_stringify()
# end def

# -- DONE --
@app.route("/api/create-block", methods=["POST"])
def new_block():
    params = request.form.to_dict()
    response = create_block.create_block(app).process( params )
    return response.http_stringify()
# end def

# -- DONE --
@app.route("/api/get-blockchain", methods=["GET"])
def block_get_blockchain():
    params = request.args.to_dict()
    response = get_blockchain.get_blockchain(app).process( params )
    return response.http_stringify()
# end def

# -- DONE --
@app.route("/api/new-transaction", methods=["POST"])
def new_transaction():
    params = request.form.to_dict()
    response = add_transaction.add_transaction(app).process( params )
    return response.http_stringify()
# end def

# -- DONE --
@app.route("/api/get-transaction", methods=["GET"])
def block_get_transaction():
    params = request.args.to_dict()
    response = get_transaction.get_transaction(app).process( params )
    return response.http_stringify()
# end def

@app.route("/api/verify-transaction", methods=["POST"])
def verify_transaction():
    params = request.form.to_dict()
    response = verify_transaction.verify_transaction(app).process( params )
    return response.http_stringify()
# end def

######### VIEW ARE BELOW FOR BLOCKCHAIN#########

@app.route("/view/blockchain", methods=["GET"])
def view_blockchain_display():
    params   = request.args.to_dict()
    response = view_blockchain.view_blockchain(app).html( params )
    html     = response.get("data")["html"]
    return html
# end def

@app.route("/view/chain-api", methods=["GET"])
def view_api_display():
    params   = request.args.to_dict()
    response = view_api.view_api(app).html( params )
    html     = response.get("data")["html"]
    return html
# end def

