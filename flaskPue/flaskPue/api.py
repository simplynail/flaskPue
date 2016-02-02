from extendedmodels import *

def connect_db(filepath, debug=False):
    if debug == True: sql_debug(True)
    db.bind("sqlite", filepath, create_db=True)
    db.generate_mapping(create_tables=True)
    return