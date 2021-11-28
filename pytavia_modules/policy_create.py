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

class policy_create:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def process(self, params):
        response = helper.response_msg(
            "POLICY_CREATE_SUCCESS",
            "POLICY_CREATE_SUCCESS", {},
            "0000"
        )
        try:
            broker_name      = params["broker_name"]
            quote_number     = params["quote_number"]
            policy_number    = params["policy_number"]
            contract_details = params["contract_details"]

            mdl_policy = database.new ( self.mgdDB , "db_policy" )
            mdl_policy.put( "broker_name" , broker_name )
            mdl_policy.put( "quote_num" , quote_number )
            mdl_policy.put( "policy_num" , policy_number )
            mdl_policy.put( "contract" , contract_details )
            mdl_policy.put( "status" , "CREATED" )
            mdl_policy.put( "block_chain_hash" , "" )
            mdl_policy.insert()

            policy_json = mdl_policy.get()
            del policy_json["_id"]

            response.put( "data"  , {
                "blockchain_list" : blockchain_list
            })
        except:
            self.webapp.logger.debug(traceback.format_exc())
            response.put( "status"      ,  "POLICY_CREATE_FAILED" )
            response.put( "desc"        ,  "GENERAL ERROR" )
            response.put( "status_code" ,  "9999" )
        # end try
        return response
    # end def
# end class
