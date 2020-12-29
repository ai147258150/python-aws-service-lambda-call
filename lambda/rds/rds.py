import json
import pymysql
import sys
import rds_config

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# rds settings
rds_host = rds_config.rds_host
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
# rds settings

# connect to rds
try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()
# connect to rds


def lambda_handler(event, context):

    update_data("table_name", "Modify field", "condition")
    # update_data("table_name", "`show`='1'", "`id` = '1'")

    return {
        'statusCode': 200,
        'body': json.dumps("Success")
    }

def update_data(table, update_field, update_where):
    sql = "UPDATE `" + table + "` SET " + update_field + " WHERE " + update_where

    logger.info(sql)

    with conn.cursor() as cur:
        cur.execute(sql)
        conn.commit()