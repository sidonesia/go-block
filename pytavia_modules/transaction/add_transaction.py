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

from pytavia_stdlib     import idgen
from pytavia_stdlib     import utils
from pytavia_core       import database
from pytavia_core       import config
from pytavia_core       import helper
from pytavia_core       import bulk_db_insert
from pytavia_core       import bulk_db_update
from pytavia_core       import bulk_db_multi

import hash_transaction

class add_transaction:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def process(self, params):
        response = helper.response_msg(
            "ADD_TRANSACTION_SUCCESS",
            "ADD TRANSACTION SUCCESS", {},
            "0000"
        )
        try:
            block           = params["block"]
            to_data         = params["to"]
            from_data       = params["from"]
            payload         = params["payload"]
            block           = int(block)

            hash_resp       = hash_transaction.hash_transaction({}).process( params )
            trans_data      = hash_resp.get("data")
            trx_hash_value  = trans_data["trx_hash_value"]

            block_rec       = self.mgdDB.db_blockchain.find_one({
                "block" : block
            })
            block           = block_rec["block"]
            timestamp       = block_rec["timestamp"]
            proof           = block_rec["proof"]
            current_hash    = block_rec["current_hash"]
            fk_block_id     = block_rec["pkey"]
            data_block      = json.loads( payload )

            mdl_transaction = database.new( self.mgdDB , "db_transaction" )
            mdl_transaction.put( "trans_hash"     , trx_hash_value )
            mdl_transaction.put( "block"          , block )
            mdl_transaction.put( "block_hash"     , current_hash )
            mdl_transaction.put( "fk_block_id"    , fk_block_id )
            mdl_transaction.put( "to"             , to_data )
            mdl_transaction.put( "from"           , from_data )
            mdl_transaction.put( "action_block"   , {} )
            mdl_transaction.put( "data_block"     , data_block )
            mdl_transaction.put( "raw_data_block" , payload )
            mdl_transaction.insert()
            mdl_trans_json   = mdl_transaction.get()
            transaction_view = self.mgdDB.db_transaction.find({
                "block"       : block,
                "block_hash"  : current_hash,
                "fk_block_id" : fk_block_id
            })
            trans_count = transaction_view.count()
            self.mgdDB.db_blockchain.update(
                {
                    "pkey"        : fk_block_id,
                    "block_hash"  : current_hash,
                    "block"       : block 
                },
                {   "$set"        : { "trans_count" : trans_count }}
            )
            del mdl_trans_json["_id"]
            response.put( "data" , mdl_trans_json )
        except:
            self.webapp.logger.debug(traceback.format_exc())
            response.put( "status"      ,  "ADD_TRANSACTION_FAILED" )
            response.put( "desc"        ,  "GENERAL ERROR" )
            response.put( "status_code" ,  "9999" )
        # end try
        return response
    # end def
# end class
