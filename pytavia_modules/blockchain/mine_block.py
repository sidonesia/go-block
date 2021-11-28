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


class mine_block:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def process(self, params):
        response = helper.response_msg(
            "MINE_BLOCK_SUCCESS",
            "MINE BLOCK SUCCESS", {},
            "0000"
        )
        try:
            blockchain_meta_rec = self.mgdDB.db_blockchain_meta.find_one({
                "label" : "BLOCKCHAIN_META"
            })
            last_block  = blockchain_meta_rec["last_block" ]
            timestamp   = blockchain_meta_rec["timestamp"  ]
            last_proof  = blockchain_meta_rec["last_proof" ]
            last_hash   = blockchain_meta_rec["last_hash"  ]
            running     = True
            proof       = 0
            hash_value  = ""
            while running:
                guess = str(last_block) + str(proof) + str( timestamp ) + str( last_proof ) + str( last_hash )
                hash_value = hashlib.sha256( guess.encode("utf-8") ).hexdigest()
                prefix = hash_value[:4]
                if prefix == "0000":
                    running = False
                    break
                # end if
                proof = proof + 1
            # end while
            response.put( "data" , {
                "hash_value" : hash_value,
                "proof"      : proof  
            })
        except:
            self.webapp.logger.debug(traceback.format_exc())
            response.put( "status"      ,  "MINE_BLOCK_FAILED" )
            response.put( "desc"        ,  "GENERAL ERROR" )
            response.put( "status_code" ,  "9999" )
        # end try
        return response
    # end def
# end class
