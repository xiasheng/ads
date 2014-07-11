
"""
Apple Push Notification Service
Documentation is available on the iOS Developer Library:
https://developer.apple.com/library/ios/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/Chapters/ApplePushService.html
"""

import json
import ssl
import struct
from binascii import unhexlify
from socket import socket


APNS_MAX_NOTIFICATION_SIZE = 256

APNS_CERTIFICATE = '/var/www/ads/ads/mm_apns.pem'
APNS_HOST = 'gateway.sandbox.push.apple.com'
#APNS_HOST = 'gateway.push.apple.com'
APNS_PORT = 2195

class APNSError():
    def __init__(self, info):
        self.info = info

def _apns_create_socket():
    sock = socket()

    sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv3, certfile=APNS_CERTIFICATE)
    sock.connect((APNS_HOST, APNS_PORT))

    return sock


def _apns_pack_message(token, data):
    format = "!cH32sH%ds" % (len(data))
    return struct.pack(format, b"\0", 32, unhexlify(token), len(data), data)


def _apns_send(token, alert, badge=0, sound="chime", content_available=False, action_loc_key=None, loc_key=None, loc_args=[], extra={}, socket=None):
    data = {}

    if action_loc_key or loc_key or loc_args:
        alert = {"body": alert}
        if action_loc_key:
            alert["action-loc-key"] = action_loc_key
        if loc_key:
            alert["loc-key"] = loc_key
        if loc_args:
            alert["loc-args"] = loc_args

    data["alert"] = alert

    if badge:
        data["badge"] = badge

    if sound:
        data["sound"] = sound

    if content_available:
        data["content-available"] = 1

    data.update(extra)

    # convert to json, avoiding unnecessary whitespace with separators
    data = json.dumps({"aps": data}, separators=(",", ":"))

    if len(data) > APNS_MAX_NOTIFICATION_SIZE:
        raise APNSError("Notification body cannot exceed %i bytes" % (APNS_MAX_NOTIFICATION_SIZE))

    data = _apns_pack_message(token, data)

    if socket:
        socket.write(data)
    else:
        socket = _apns_create_socket()
        socket.write(data)
        socket.close()


def apns_send_message(registration_id, data, **kwargs):
    """
    Sends an APNS notification to a single registration_id.
    This will send the notification as form data.
    If sending multiple notifications, it is more efficient to use
    apns_send_bulk_message()
    Note that \a data should always be a string.
    """

    return _apns_send(registration_id, data, **kwargs)


def apns_send_bulk_message(registration_ids, data, **kwargs):
    """
    Sends an APNS notification to one or more registration_ids.
    The registration_ids argument needs to be a list.
    """
    socket = _apns_create_socket()
    for registration_id in registration_ids:
        _apns_send(registration_id, data, socket=socket, **kwargs)

    socket.close()

class notifythread(threading.Thread):
    def __init__(self, token, data):
        threading.Thread.__init__(self)
        self.token = token
        self.data = data
    def run(self):
        apns_send_message(self.token, self.data)
        
def apns_notify(token, data):
    notifythread(token, data).start()


if __name__ == '__main__':
    apns_notify('11111', 'hello apns')

