# -*- coding: utf-8 -*-
#  Copyright (c) 2022 - 2023 Ricardo Bartels. All rights reserved.
#  Modified and maintained by wolkenlosIT.
#  fritzinfluxdb.py
#
#  This work is licensed under the terms of the MIT license.
#  For a copy, see file LICENSE.txt included in this
#  repository or visit: <https://opensource.org/licenses/MIT>.

from datetime import datetime

from fritzinfluxdb.classes.fritzbox.service_definitions import lua_services


def prepare_json_response_data(response):
    return response.json()


def parse_log_timestamp(data):
    return datetime.strptime(
        f'{data["date"]} {data["time"]}',
        '%d.%m.%y %H:%M:%S'
    )


def parse_log_message(data):
    return data.get("msg")


LOG_CATEGORIES = [
    ("System logs", "sys", "System", 60),
    ("Internet connection logs", "net", "Internet connection", 61),
    ("Telephony logs", "fon", "Telephony", 62),
    ("WLAN logs", "wlan", "WLAN", 63),
    ("USB Devices logs", "usb", "USB Devices", 64),
]

for name, filter_name, log_type, interval in LOG_CATEGORIES:
    lua_services.append({
        "name": name,
        "os_min_versions": "7.39",
        "method": "POST",
        "params": {
            "filter": filter_name,
            "page": "log",
            "lang": "de"
        },
        "response_parser": prepare_json_response_data,
        "track": True,
        "interval": interval,
        "value_instances": {
            "log_entry": {
                "data_path": "data.log",
                "type": list,
                "next": {
                    "type": str,
                    "tags": {
                        "log_type": log_type
                    },
                    "timestamp_function": parse_log_timestamp,
                    "value_function": parse_log_message,
                    "tags_function": None
                }
            }
        }
    })
