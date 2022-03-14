import logging
import json
from flask import Flask
from flask_cors import CORS
from flask import session, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('jmapserver')


app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()

users = {
    "aa": generate_password_hash("bb"),
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}

@auth.verify_password
def verify_password(username, password):
    logging.warning("username: %s", username );
    logging.warning("password: %s", password );
    
    if username in users and \
            check_password_hash(users.get(username), password):
        logging.warning("auth worked")
        return users.get(username)
    else :
        logging.warning("no Auth")



BASEURL="http://127.0.0.1:5000"

@app.route('/')
def index():
    return 'Hello, World!'

@app.before_request
def log_request_info():
    logger.warning('User: %s', auth.current_user())
    logger.warning('Body: %s', request.get_data())
    logger.warning('Headers: %s', request.headers)


@app.route('/event/')
@auth.login_required
def event():
    res = {

    }
    return res
    
@app.route('/.well-known/jmap')
@auth.login_required
def well_known():
    # logger.warning(json.dumps(request, indent=4, sort_keys=True))
    # logger.warning(auth.current_user())
    res = {
        "capabilities": {},#{name: module.capability
                        # for name, module in CAPABILITIES.items()},
        "username": "hamish",#request.user.username,
        "accounts": {
            "1":{
                "name": "hamish",
                "isPersonal": True,
                "isArchiveUser": False,
                "accountCapabilities": {},
                "isReadOnly": False
            }
            # account.id: {
            #     "name": account.name,
            #     "isPersonal": account.is_personal,
            #     "isArchiveUser": False,
            #     "accountCapabilities": account.capabilities,
            #     "isReadOnly": False
            # } for account in request.user.accounts.values()
        },
        "primaryAccounts": {
            "urn:ietf:params:jmap:mail": "hamish", #request.user.username,
            "urn:ietf:params:jmap:submission": "hcurrie", #request.user.username,
            "urn:ietf:params:jmap:vacationresponse": "hamishvacation", #request.user.username,
        },
        "state": "0",
        "apiUrl": BASEURL + "/api/",
        "downloadUrl": BASEURL + "/download/{accountId}/{blobId}/{name}?type={type}",
        "uploadUrl": BASEURL + "/upload/{accountId}/",
        "eventSourceUrl": BASEURL + "/event/"#?types={types}&closeafter={closeafter}&ping={ping}",
    }
    return res

@app.route('/<path:path>')
def catch_all(path):
    return 'You want path: %s' % path