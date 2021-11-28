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

import mine_block

class hash_transaction:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def process(self, params):
        response = helper.response_msg(
            "HASH_TRANSACTION_SUCCESS",
            "HASH TRANSACTION SUCCESS", {},
            "0000"
        )
        try:
            block         = params["block"]
            to_data       = params["to"]
            from_data     = params["from"]
            payload       = params["payload"]
            block         = int( block )

            block_rec     = self.mgdDB.db_blockchain.find_one({
                "block" : block
            })
            block         = block_rec["block"]
            timestamp     = block_rec["timestamp"]
            proof         = block_rec["proof"]
            current_hash  = block_rec["current_hash"]

            trx_hash      = str( block ) + str( timestamp ) + str( proof ) +\
                    str( current_hash ) + str( to_data )   + str( from_data ) +\
                    str( payload ) 
            trx_hash_value = hashlib.sha256( trx_hash.encode("utf-8") ).hexdigest()
            response.put( "data" , {
                "trx_hash_value" : trx_hash_value
            })
        except:
            self.webapp.logger.debug(traceback.format_exc())
            response.put( "status"      ,  "HASH_TRANSACTION_FAILED" )
            response.put( "desc"        ,  "GENERAL ERROR" )
            response.put( "status_code" ,  "9999" )
        # end try
        return response
    # end def
# end class
