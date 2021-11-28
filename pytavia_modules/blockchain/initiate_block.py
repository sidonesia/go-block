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

class initiate_block:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def process(self, params):
        response = helper.response_msg(
            "INITIATE_BLOCK_SUCCESS",
            "INITIATE BLOCK SUCCESS", {},
            "0000"
        )
        try:
            block_tm = int( time.time() * 1000)
            block    = database.new( self.mgdDB , "db_blockchain" )
            block.put( "block"              , 0 )
            block.put( "timestamp"          , block_tm )
            block.put( "proof"              , 1 )
            block.put( "last_proof"         , 0 )
            block.put( "current_hash"       , "NONE" )
            block.put( "previous_hash"      , "NONE" )
            block.put( "data_block"         , {} )
            block.insert()

            block_pkey = block.get()["pkey"]
            block_meta = database.new( self.mgdDB , "db_blockchain_meta" )
            block_meta.put( "label"         , "BLOCKCHAIN_META" )
            block_meta.put( "last_block"    , 0 )
            block_meta.put( "timestamp"     , block_tm )
            block_meta.put( "last_proof"    , 1 )
            block_meta.put( "last_hash"     , "NONE" )
            block_meta.put( "fk_block_id"   , block_pkey )
            block_meta.insert()
        except:
            self.webapp.logger.debug(traceback.format_exc())
            response.put( "status"      ,  "INITIATE_BLOCK_FAILED" )
            response.put( "desc"        ,  "GENERAL ERROR" )
            response.put( "status_code" ,  "9999" )
        # end try
        return response
    # end def
# end class
