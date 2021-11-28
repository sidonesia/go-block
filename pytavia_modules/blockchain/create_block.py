import json
import time
import pymongo
import sys
import urllib.parse
import base64
import traceback
import random
import urllib.request
import io
import requests
import json
import hashlib
import random
import re
import time
import datetime

sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")
sys.path.append("pytavia_modules/transaction")

from pytavia_stdlib     import idgen
from pytavia_stdlib     import utils
from pytavia_core       import database
from pytavia_core       import config
from pytavia_core       import helper
from pytavia_core       import bulk_db_insert
from pytavia_core       import bulk_db_update
from pytavia_core       import bulk_db_multi

from transaction        import add_transaction

import mine_block

class create_block:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def process(self, params):
        response = helper.response_msg(
            "CREATE_BLOCK_SUCCESS",
            "CREATE BLOCK SUCCESS", {},
            "0000"
        )
        try:
            miner       = params["miner"]
            block_tm    = int(time.time() * 1000)
            blockchain_meta_rec = self.mgdDB.db_blockchain_meta.find_one({
                "label" : "BLOCKCHAIN_META"
            })
            last_block  = blockchain_meta_rec["last_block" ]
            last_proof  = blockchain_meta_rec["last_proof" ]
            last_hash   = blockchain_meta_rec["last_hash"  ]
            fk_block_id = blockchain_meta_rec["fk_block_id"]
            mine_resp   = mine_block.mine_block(self.webapp).process({
                "last_block"    : last_block,
                "timestamp"     : block_tm,
                "last_proof"    : last_proof,
                "last_hash"     : last_hash
            })
            mine_data       = mine_resp.get("data")
            new_hash_value  = mine_data["hash_value"]
            new_proof       = mine_data["proof"]

            block = int( last_block ) + 1
            mdl_blockchain  = database.new( self.mgdDB , "db_blockchain" )
            mdl_blockchain.put( "block"         , block )
            mdl_blockchain.put( "timestamp"     , block_tm )
            mdl_blockchain.put( "proof"         , new_proof )
            mdl_blockchain.put( "last_proof"    , last_proof )
            mdl_blockchain.put( "current_hash"  , new_hash_value )
            mdl_blockchain.put( "previous_hash" , last_hash )
            mdl_blockchain.put( "data_block"    , {} )
            mdl_blockchain.insert()
            block_pkey = mdl_blockchain.get()["pkey"]

            self.mgdDB.db_blockchain_meta.update(
                { "label"   : "BLOCKCHAIN_META" },
                { "$set"    : {
                    "last_block"    : block,
                    "timestamp"     : block_tm,
                    "last_proof"    : new_proof,
                    "last_hash"     : new_hash_value,
                    "fk_block_id"   : block_pkey
                }}
            )
            payload    = {
                "amount"    : 1000,
                "type"      : "MINING"
            }
            payload = json.dumps( payload )
            trans_resp = add_transaction.add_transaction({}).process({
                "block"     : block,
                "to"        : miner,
                "from"      : "BLOCKCHAIN",
                "payload"   : payload
            })
            blockchain_json = mdl_blockchain.get()
            del blockchain_json["_id"]
            response.put( "data" , blockchain_json )
        except:
            self.webapp.logger.debug(traceback.format_exc())
            response.put( "status"      ,  "CREATE_BLOCK_FAILED" )
            response.put( "desc"        ,  "GENERAL ERROR" )
            response.put( "status_code" ,  "9999" )
        # end try
        return response
    # end def
# end class
