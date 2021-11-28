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

from flask              import render_template

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

class view_blockchain:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def get_ledger(self, params):
        response = helper.response_msg(
            "GET_BLOCKCHAIN_SUCCESS",
            "GET_BLOCKCHAIN_SUCCESS", {},
            "0000"
        )
        try:
            blockchain_view = self.mgdDB.db_blockchain.find(
                {} , {"_id" : 0}
            ).sort("rec_timestamp",-1)
            blockchain_list = []
            for blockchain_rec in blockchain_view:
                block            = blockchain_rec["block"]
                timestamp        = blockchain_rec["timestamp"]
                proof            = blockchain_rec["proof"]
                last_proof       = blockchain_rec["last_proof"]
                trans_count      = blockchain_rec["trans_count"]
                current_hash     = blockchain_rec["current_hash"]
                previous_hash    = blockchain_rec["previous_hash"]
                data_block       = blockchain_rec["data_block"]
                fk_block_id      = blockchain_rec["pkey"]
                transaction_view = self.mgdDB.db_transaction.find(
                    {
                        "fk_block_id" : fk_block_id,
                        "block_hash"  : current_hash
                    },
                    {   "_id" : 0}
                ).sort("rec_timestamp" , -1)
                transaction_list = list( transaction_view )
                blockchain_rec["transaction"] = transaction_list
                blockchain_list.append( blockchain_rec )
            # end for
            response.put( "data"  , {
                "blockchain_list" : blockchain_list
            })
        except:
            self.webapp.logger.debug(traceback.format_exc())
            response.put( "status"      ,  "GET_BLOCKCHAIN_FAILED" )
            response.put( "desc"        ,  "GENERAL ERROR" )
            response.put( "status_code" ,  "9999" )
        # end try
        return response
    # end def

    def html( self, params ):
        response = helper.response_msg(
            "VIEW_HTML_SUCCESS",
            "VIEW HTML SUCCESS", {},
            "0000"
        )
        try:
            ledger_resp     = self.get_ledger({})
            ledger_data     = ledger_resp.get("data")
            blockchain_list = ledger_data["blockchain_list"]
            template_html   = render_template(
                'ledger.html' ,
                blockchain_list = blockchain_list,
            )
            response.put( "data" , {
                "html" : template_html
            })
        except:
            print(traceback.format_exc())
            response.put( "status"      ,  "VIEW_HTML_FAILED" )
            response.put( "desc"        ,  "GENERAL ERROR" )
            response.put( "status_code" ,  "9999" )
        # end try
        return response
    # end def
# end class
