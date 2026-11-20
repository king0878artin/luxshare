[app]
title = LuxShare
package.name = luxshare
package.domain = com.artin
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,json,ttf,otf,txt
version = 1.0.0
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,CHANGE_WIFI_MULTICAST_STATE,NEARBY_WIFI_DEVICES
android.minapi = 26
android.api = 35
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True
android.private_storage = True
android.allow_backup = False
android.wakelock = True

[buildozer]
log_level = 2
warn_on_root = 1
