import copy

# replace last 'x' occurrences of old to new
# source: https://stackoverflow.com/questions/2556108/rreplace-how-to-replace-the-last-occurrence-of-an-expression-in-a-string
def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

class mongo_model:

    def __init__(self, record, lookup, db_handle):
        self._mongo_record  = copy.deepcopy(record)
        self._lookup_record = copy.deepcopy(lookup)
        self._db_handle     = db_handle
    # end def

    def put(self, key, value):
        if not (key in self._lookup_record):
            raise ValueError('SETTING_NON_EXISTING_FIELD', key, value)
        # end if
        if isinstance(value, type(self)):  # if value is a mongo_model
            self._mongo_record[key] = copy.deepcopy(value.get())
        else:
            self._mongo_record[key] = copy.deepcopy(value)
    # end def

    def get(self):
        return self._mongo_record
    # end def	

    def delete(self , query):
        collection_name = self._lookup_record["__db__name__"]
        self._db_handle[collection_name].remove( query )
    # end def

    def insert(self, lock=None):
        collection_name = self._lookup_record["__db__name__"]
        # del self._mongo_record["__db__name__"]
        self._mongo_record.pop('__db__name__', None)  
        if lock == None:
            self._db_handle[collection_name].insert_one(  
                self._mongo_record
            )
        else:
            self._db_handle[collection_name].insert_one(  
                self._mongo_record,
                session=lock
            )
        # end if
    # end def

    def update(self, query):
        collection_name = self._lookup_record["__db__name__"]
        self._db_handle[collection_name].update(
            query, 
            { "$set" : self._mongo_record }
        )
    # end def
# end class

# for deep /  global updates
def _traverse_db_paths(field, table_ref_names, paths, curr_path):
    for key, value in field.items():
        value_type = type(value)
        if key in table_ref_names:              # found a referenced record!!
            if value_type == dict and "pkey" in value:
                paths.append({
                    # curr_path + key + "." : list(value.keys())
                    curr_path + key + "." : value
                })
            elif value_type == list and "pkey" in value[0]:
                paths.append({
                    # curr_path + key + ".$[elem]." : list(value[0].keys())
                    curr_path + key + ".$[elem]." : value[0]
                })
            else: 
                continue
        
        if value_type == dict:
            _traverse_db_paths(value, table_ref_names, paths, curr_path + key + ".")
        elif value_type == list and len(value) != 0 and type(value[0]) == dict:
            _traverse_db_paths(value[0], table_ref_names, paths, curr_path + key + ".$[].")

def get_db_table_paths(db):
    update_paths = {}
    table_fks = {}
    for table in db:
        update_paths[table] = []
        if "__db__referenced__names__" not in db[table]:
            continue
        for ref_table in db:
            paths = []
            _traverse_db_paths(db[ref_table], db[table]["__db__referenced__names__"], paths, "")
            if ref_table not in table_fks:
                table_fks[ref_table] = []
            for p in paths:
                temp_keys = []
                for k in p:
                    if "$[]" in k and "$[elem]" not in k:
                        temp_keys.append(k)
                for k in temp_keys:
                    p[rreplace(k,'$[]','$[elem]', 1)] = p.pop(k)
            table_fks[ref_table] += paths
            if len(paths) > 0:
                update_paths[table].append({
                    ref_table : paths
                })
    return update_paths, table_fks

# Define the models/collections here for the mongo db
db = {
    # SYSTEM TABLES WITH _sys_, do not modify
    "db_sys_resume_history"     : {
        "resume_token"          : {},
        "handler_name"          : "",
        "collection"            : "",
        "operation_type"        : "",
        "database"              : "",
        "document_key"          : "",
        "cluster_time"          : 0 ,
        "rec_timestamp"         : "",
    },

    # USER TABLES BELOW HERE, MODIFYABLE

    "db_application_sys_log"    : {
        "fk_app_id"             : "",
        "fk_user_id"            : "",
        "fk_app_user_id"        : "",
        "status"                : "",
        "status_timestamp"      : "",
        "updated_by"            : "", 
        "pkey"                  : "",
        "misc"                  : {},
    },
    "db_blockchain"             : {
        "block"                 : 0 ,
        "timestamp"             : 0 ,
        "proof"                 : 0 ,
        "last_proof"            : 0 ,
        "trans_count"           : 0 ,
        "current_hash"          : "",
        "previous_hash"         : "",
        "data_block"            : {}
    },
    "db_transaction"            : {
        "trans_hash"            : "",
        "block"                 : 0 ,
        "block_hash"            : "",
        "fk_block_id"           : "",
        "to"                    : "",
        "from"                  : "",
        "direction"             : "",
        "action_block"          : {},
        "data_block"            : {},
        "raw_data_block"        : ""
    },
    "db_blockchain_meta"        : {
        "label"                 : "BLOCKCHAIN_META",
        "last_block"            : 0 ,
        "timestamp"             : 0 ,
        "last_proof"            : 0 ,
        "last_hash"             : "",
        "fk_block_id"           : "",
    }
} 
