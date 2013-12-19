import os

VERSION = 'Snapchat FS 0.1'
CONFIG_FILE_PATH = os.getenv("HOME") + '/.snapchat_fs'

ROOT_URL = "https://feelinsonice-hrd.appspot.com"
# appened to the ROOT_URL to get the login resource
LOGIN_RESOURCE = "/bq/login"
SEND_RESOURCE = "/bq/send"
UPLOAD_RESOURCE = "/bq/upload"
BLOB_RESOURCE = "/bq/blob"

# we pass this token to the service to "authenticate" that we're supposed
# to be able to log in
LOGIN_TOKEN = "m198sOkJEn37DjqZ32lpRu76xmw288xSQ9"

# secret key hardcoded into app; is used for things like encrypting the images
SECRET_KEY = "M02cnQ51Ji97vwT4"
# the secret salt they use for the hashes they use to generate req tokens
SALT = "iEk21fuwZApXlz93750dmW22pw389dPwOk"
# used to generate all request tokens
PATTERN = "0001110111101110001111010101111011010001001110011000110001000110"
