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

class get_transaction:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def process(self, params):
        response = helper.response_msg(
            "GET_TRANSACTION_SUCCESS",
            "GET TRANSACTION SUCCESS", {},
            "0000"
        )
        try:
            block = params["block"]
            block = int( block ) 

            transaction_view = self.mgdDB.db_transaction.find(
                { "block" : block }, 
                { "_id"   : 0     }
            )
            transaction_list = list( transaction_view )
            response.put( "data" , {
                "transaction_list" : transaction_list
            })
        except:
            self.webapp.logger.debug(traceback.format_exc())
            response.put( "status"      ,  "GET_TRANSACTION_FAILED" )
            response.put( "desc"        ,  "GENERAL ERROR" )
            response.put( "status_code" ,  "9999" )
        # end try
        return response
    # end def
# end class
