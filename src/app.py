from flask import Flask, render_template, request

from utils import DownloadMailboxRequest, DownloadMailboxResponse, GetAuthTokenRequest, GetAuthTokenResponse, GetGroupsRequest, GetGroupsResponse, ResetPasswordRequest, RestError, UploadMessageRequest, User, UserManager, json_exists

app = Flask(__name__)

manager = UserManager(users={})
manager.add_user('luna', 'password')
manager.add_user('capra', 'password')
manager.add_user('cammello', 'password')
manager.add_user_to_group('luna', 'riunione')
manager.add_user_to_group('capra', 'riunione')
manager.add_user_to_group('cammello', 'riunione')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chats')
def group_list():
    return render_template('group-list.html')


@app.route('/chats/<group_name>')
def group_chat(group_name: str):
    return render_template('group-chat.html', group_name=group_name)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/reset-password')
def reset_password_page():
    return render_template('reset-password.html')


@app.errorhandler(RestError)
def error(err: RestError):
    return err.text, err.status


@app.route('/api/upload-message', methods=['GET', 'POST'])
def upload_message():
    json = json_exists(request.json)
    req = UploadMessageRequest.parse(json)
    manager.check_auth(req.message.sender_id, req.auth_token)
    manager.add_message(req.message)
    return 'ok'


@app.route('/api/download-mailbox', methods=['GET', 'POST'])
def download_mailbox():
    json = json_exists(request.json)
    req = DownloadMailboxRequest.parse(json)
    manager.check_auth(req.username, req.auth_token)
    messages = manager.get_mailbox(req.username)
    manager.clear_mailbox(req.username)
    return DownloadMailboxResponse(
        messages=messages
    ).to_json()


@app.route('/api/get-auth-token', methods=['GET', 'POST'])
def get_auth_token():
    json = json_exists(request.json)
    req = GetAuthTokenRequest.parse(json)
    auth_token = manager.authenticate(req.username, req.password)
    return GetAuthTokenResponse(auth_token=auth_token).to_json()


@app.route('/api/reset-password', methods=['GET', 'POST'])
def reset_password():
    json = json_exists(request.json)
    req = ResetPasswordRequest.parse(json)
    manager.change_password(req.username, req.old_pass, req.new_pass)
    return 'ok'


@app.route('/api/get-groups', methods=['GET', 'POST'])
def get_groups():

    json = json_exists(request.json)
    req = GetGroupsRequest.parse(json)
    manager.check_auth(req.username, req.auth_token)
    return GetGroupsResponse(
        groups=manager.get_groups(req.username)
    ).to_json()


app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run()
