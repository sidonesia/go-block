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

class view_index:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def html( self, params ):
        response = helper.response_msg(
            "VIEW_HTML_SUCCESS",
            "VIEW HTML SUCCESS", {},
            "0000"
        )
        try:
            template_html   = render_template(
                'index.html'
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
