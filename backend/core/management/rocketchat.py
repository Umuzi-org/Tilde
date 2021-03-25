import requests
import json

from collections import namedtuple
from backend.settings import ROCKETCHAT

User = namedtuple("User", "user_id name username email")
Channel = namedtuple("Channel", "channel_id name type")

CHANNEL = "CHANNEL"  # public channel
GROUP = "GROUP"  # private channel
CHANNEL_TYPE_RESOURCES = {GROUP: "groups", CHANNEL: "channels"}


BASE_URL = ROCKETCHAT["BASE_URL"]
assert BASE_URL, 'Please set the ROCKETCHAT["BASE_URL"] setting'


class Rocketchat:
    def __init__(self):
        self._set_not_logged_in()
        self.existing_users = {}
        self.existing_channels = {}

    def _set_not_logged_in(self):
        self.login_response = None
        self.auth_token = None
        self.user_id = None

    @property
    def _headers(self):
        if self.auth_token:
            return {
                "X-User-Id": self.user_id,
                "X-Auth-Token": self.auth_token,
            }
        return {"Content-Type": "application/json"}

    def login(self, user, password):

        response = requests.post(
            f"{BASE_URL}/v1/login",
            json={"user": user, "password": password},
            headers=self._headers,
        )
        data = response.json()
        assert data["status"] == "success", json.dumps(data, indent=2, sort_keys=True)

        self.login_response = data["data"]
        self.auth_token = data["data"]["authToken"]
        self.user_id = data["data"]["userId"]

    def logout(self):
        response = requests.post(
            f"{BASE_URL}/v1/logout",
            headers=self._headers,
        )
        data = response.json()
        assert data["status"] == "success", json.dumps(data, indent=2, sort_keys=True)

        self._set_not_logged_in()

    def create_user(self, name, username, email, password):
        response = requests.post(
            f"{BASE_URL}/v1/users.create",
            headers=self._headers,
            json={
                "requirePasswordChange": True,
                "name": name,
                "username": username,
                "email": email,
                "password": password,
            },
        )
        data = response.json()
        pretty_json = json.dumps(data, indent=2, sort_keys=True)
        assert data["success"] == True, pretty_json

        user_id = data["user"]["_id"]
        user = User(user_id, name, username, email)
        self.existing_users[user_id] = user
        return user

    def create_user_if_not_exists(self, name, username, email, password):
        user = self.get_existing_user(email_address=email)
        if user:
            return user

        return self.create_user(name, username, email, password)

    def get_existing_user(self, email_address="", username=""):
        if self.existing_users == {}:
            self.load_all_users()

        for user in self.existing_users.values():
            if email_address and user.email == email_address:
                return user
            if username and user.username == username:
                return user

    def load_all_channels(self):
        for resource_type, CHANNEL_TYPE in [("channels", CHANNEL), ("groups", GROUP)]:

            channels = self._fetch_all_x(resource_type)
            for channel in channels:
                channel_id = channel["_id"]
                name = channel["name"]
                self.existing_channels[channel_id] = Channel(
                    channel_id, name, CHANNEL_TYPE
                )

    def load_all_users(self):
        users = self._fetch_all_x("users")
        for user in users:
            user_id = user["_id"]
            name = user["name"]
            username = user.get("username")
            email = user.get("emails", [{"address": None}])[0]["address"]
            self.existing_users[user_id] = User(user_id, name, username, email)

    def _fetch_all_x(self, resource_type):
        offset = 0
        total = 1

        while total > offset:
            response = requests.get(
                f"{BASE_URL}/v1/{resource_type}.list?count=100&offset={offset}",
                headers=self._headers,
            )
            data = response.json()
            assert data["success"] == True, json.dumps(data, indent=2, sort_keys=True)

            total = data["total"]
            offset += data["count"]

            for resource in data[resource_type]:
                yield resource

    def update_user(self, user_id, name, active=True):
        response = requests.post(
            f"{BASE_URL}/v1/users.update",
            headers=self._headers,
            json={"userId": user_id, "data": {"name": name, "active": active}},
        )
        data = response.json()
        assert data["success"] == True, json.dumps(data, indent=2, sort_keys=True)
        pass

    def get_existing_channel(self, name):
        if self.existing_channels == {}:
            self.load_all_channels()

        for channel in self.existing_channels.values():
            if channel.name.strip().lower() == name.strip().lower():
                return channel

    def create_channel_if_not_exists(self, name, channel_type):
        channel = self.get_existing_channel(name=name)
        if channel:
            return channel

        return self.create_channel(name=name, channel_type=channel_type)

    def create_channel(self, name, channel_type):
        resource = CHANNEL_TYPE_RESOURCES[channel_type]
        response = requests.post(
            f"{BASE_URL}/v1/{resource}.create",
            headers=self._headers,
            json={"name": name},
        )
        data = response.json()
        pretty_json = json.dumps(data, indent=2, sort_keys=True)
        assert data["success"] == True, pretty_json

        channel_id = data["group"]["_id"] if "group" in data else data["channel"]["_id"]
        channel = Channel(channel_id, name, channel_type)
        self.existing_channels[channel_id] = channel
        return channel

    def add_user_to_channnel(self, user_id, channel_id):
        channel_type = self.existing_channels[channel_id].type
        resource = CHANNEL_TYPE_RESOURCES[channel_type]

        response = requests.post(
            f"{BASE_URL}/v1/{resource}.invite",
            headers=self._headers,
            json={"roomId": channel_id, "userId": user_id},
        )
        data = response.json()
        pretty_json = json.dumps(data, indent=2, sort_keys=True)
        assert data["success"] == True, pretty_json

    def add_channel_owner(self, user_id, channel_id):
        channel_type = self.existing_channels[channel_id].type
        resource = CHANNEL_TYPE_RESOURCES[channel_type]

        response = requests.post(
            f"{BASE_URL}/v1/{resource}.addOwner",
            headers=self._headers,
            json={"roomId": channel_id, "userId": user_id},
        )
        data = response.json()
        pretty_json = json.dumps(data, indent=2, sort_keys=True)

        success = data["success"] == True
        success = success or data["errorType"] == "error-user-already-owner"
        assert success, pretty_json

    @property
    def me(self):
        my_id = self.login_response["userId"]
        return self.existing_users[my_id]

    def get_user_info(self, user_id):
        response = requests.get(
            f"{BASE_URL}/v1/users.info?userId={user_id}",
            headers=self._headers,
        )
        data = response.json()
        pretty_json = json.dumps(data, indent=2, sort_keys=True)
        assert data["success"] == True, pretty_json
        return data["user"]
