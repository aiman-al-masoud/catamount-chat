from dataclasses import asdict, dataclass, fields
from typing import Any, Dict, List, Optional, TypeGuard
import secrets

from flask import json


@dataclass(kw_only=True)
class Schema:

    @classmethod
    def parse(cls, json: Dict[str, Any]):
        kwargs = {}
        for f in fields(cls):
            if f.name not in json:
                raise BadRequestError(text=f'The json is missing "{f.name}"')
            if issubclass(f.type, Schema):
                kwargs[f.name] = f.type.parse(json[f.name])
            else:
                kwargs[f.name] = json[f.name]
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(asdict(self))


@dataclass(kw_only=True)
class Message(Schema):
    group_id: str
    sender_id: str
    text: str  # also base 64
    date: int


@dataclass(kw_only=True)
class UploadMessageRequest(Schema):
    message: Message
    auth_token: str


@dataclass(kw_only=True)
class DownloadMailboxRequest(Schema):
    username: str
    auth_token: str


@dataclass(kw_only=True)
class DownloadMailboxResponse(Schema):
    messages: List[Message]


@dataclass(kw_only=True)
class User(Schema):
    username: str
    password: str
    auth_token: Optional[str]
    mailbox: List[Message]
    groups: List[str]


@dataclass(kw_only=True)
class GetAuthTokenRequest(Schema):
    username: str
    password: str


@dataclass(kw_only=True)
class GetAuthTokenResponse(Schema):
    auth_token: str


@dataclass(kw_only=True)
class ResetPasswordRequest(Schema):
    username: str
    old_pass: str
    new_pass: str


@dataclass(kw_only=True)
class GetGroupsRequest(Schema):
    username: str
    auth_token: str


@dataclass(kw_only=True)
class GetGroupsResponse(Schema):
    groups: List[str]


@dataclass(kw_only=True)
class UserManager(Schema):
    users: Dict[str, User]

    def add_user(self, username: str, password: str):
        self.users[username] = User(
            username=username,
            password=password,
            auth_token=None,
            mailbox=[],
            groups=[username],
        )

    def authenticate(self, username: str, password: str):
        user = self.get_user(username)
        if user.password != password:
            raise UnauthorizedError(text=f'Wrong password for {username}')
        user.auth_token = str(secrets.token_bytes(16))
        return user.auth_token

    def check_auth(self, username: str, auth_token: str):
        user = self.get_user(username)
        if user.auth_token != auth_token:
            raise UnauthorizedError(
                text=f'Auth token not valid for {username}')

    def get_user(self, username: str):
        user = self.users.get(username, None)
        if not user:
            raise NotFoundError(text=f'user "{username}" does not exist')
        return user

    def get_mailbox(self, username: str):
        user = self.get_user(username)
        return user.mailbox

    def clear_mailbox(self, username: str):
        user = self.get_user(username)
        user.mailbox = []

    def add_user_to_group(self, username: str, group_name: str):
        user = self.get_user(username)
        user.groups.append(group_name)

    def get_subscribers(self, group_name: str):
        return [u for u in self.users.values()
                if group_name in u.groups]

    def add_message(self, message: Message):
        for user in self.get_subscribers(message.group_id):
            user.mailbox.append(message)

    def change_password(self, username: str, old_pass: str, new_pass: str):
        user = self.get_user(username)
        if user.password != old_pass:
            raise UnauthorizedError(
                text=f'Wrong old password for "{username}"')
        user.password = new_pass

    def get_groups(self, username: str):
        user = self.get_user(username)
        return user.groups


def json_exists(json: Optional[Dict]) -> Dict[str, Any]:
    if json is None:
        raise BadRequestError(text='Bad request: missing json')
    return json


@dataclass(kw_only=True)
class RestError(Exception):
    status: int
    text: str


@dataclass(kw_only=True)
class BadRequestError(RestError):
    status: int = 400
    text: str


@dataclass(kw_only=True)
class UnauthorizedError(RestError):
    status: int = 401
    text: str


@dataclass(kw_only=True)
class NotFoundError(RestError):
    status: int = 404
    text: str
