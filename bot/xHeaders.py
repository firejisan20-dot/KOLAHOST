# ═══════════════════════════════════════════════════════════════
#   ██████╗  █████╗ ███████╗██╗███╗   ██╗    ████████╗██╗  ██╗████████╗
#   ██╔══██╗██╔══██╗██╔════╝██║████╗  ██║    ╚══██╔══╝╚██╗██╔╝╚══██╔══╝
#   ██████╔╝███████║█████╗  ██║██╔██╗ ██║       ██║    ╚███╔╝    ██║
#   ██╔══██╗██╔══██║██╔══╝  ██║██║╚██╗██║       ██║    ██╔██╗    ██║
#   ██║  ██║██║  ██║██║     ██║██║ ╚████║       ██║   ██╔╝ ██╗   ██║
#   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═══╝       ╚═╝   ╚═╝  ╚═╝   ╚═╝
#
#               ★ PREMIUM API CORE — BY RAFIN TxT ★
#               ▌ Free Fire OB53 API Wrapper ▌
#               ▌ Likes / Player Info / Friend / Token ▌
# ═══════════════════════════════════════════════════════════════
#
#  ▸ মডিউল নাম     : xC4.py
#  ▸ ব্র্যান্ডিং     : RAFIN TxT
#  ▸ পাবলিশ          : @rafin_txt
#  ▸ ফিচার           : Player Info / Likes / Remove Friend / Token
# ═══════════════════════════════════════════════════════════════

import requests
import os
import psutil
import sys
import jwt
import pickle
import json
import binascii
import time
import urllib3
import base64
import datetime
import re
import socket
import threading

from protobuf_decoder.protobuf_decoder import Parser
from xC4 import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ═══════════════════════════════════════════════════════════════
#                    ★ কনস্ট্যান্ট (RAFIN TxT) ★
# ═══════════════════════════════════════════════════════════════

TOKEN_API = "https://tokens-asfufvfshnfkhvbb.francecentral-01.azurewebsites.net/ReQuesT"
LIKE_API  = "https://tokens-asfufvfshnfkhvbb.francecentral-01.azurewebsites.net/ReQuesT"
UID_API   = "https://panel-g2ccathtf6gdcmdw.polandcentral-01.azurewebsites.net/Uids"

DEFAULT_OB_HEADERS = {
    'X-Unity-Version': '2018.4.11f1',
    'ReleaseVersion':   'OB53',
    'Content-Type':     'application/x-www-form-urlencoded',
    'X-GA':             'v1 1',
    'Content-Length':   '16',
    'User-Agent':       'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
    'Host':             'clientbp.ggblueshark.com',
    'Connection':       'Keep-Alive',
    'Accept-Encoding':  'gzip',
}


# ═══════════════════════════════════════════════════════════════
#              ★ Token Auto-Refresh থ্রেড (RAFIN TxT) ★
# ═══════════════════════════════════════════════════════════════

def ToK():
    """প্রতি ৫ ঘণ্টায় টোকেন ফাইল রিফ্রেশ করে"""
    while True:
        try:
            r = requests.get(f'{TOKEN_API}?&type=ToKens')
            t = r.text
            i = t.find("ToKens : [")
            if i != -1:
                j = t.find("]", i)
                L = [x.strip(" '\"") for x in t[i+11:j].split(',') if x.strip()]
                if L:
                    with open("token.txt", "w") as f:
                        f.write(random.choice(L))
        except Exception:
            pass
        time.sleep(5 * 60 * 60)


# ব্যাকগ্রাউন্ডে টোকেন রিফ্রেশার থ্রেড চালু
Thread(target=ToK, daemon=True).start()


# ═══════════════════════════════════════════════════════════════
#              ★ হেল্পার ফাংশন (RAFIN TxT) ★
# ═══════════════════════════════════════════════════════════════

def GeTToK():
    """token.txt থেকে টোকেন পড়বে"""
    with open("token.txt") as f:
        return f.read().strip()


def equie_emote(JWT, url):
    """ইমোট সেট করার রিকোয়েস্ট"""
    url = f"{url}/ChooseEmote"

    headers = {
        "Accept-Encoding": "gzip",
        "Authorization":   f"Bearer {JWT}",
        "Connection":      "Keep-Alive",
        "Content-Type":    "application/x-www-form-urlencoded",
        "Expect":          "100-continue",
        "ReleaseVersion":  "OB53",
        "User-Agent":      "Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)",
        "X-GA":            "v1 1",
        "X-Unity-Version": "2018.4.11f1",
    }

    data = bytes.fromhex("CA F6 83 22 2A 25 C7 BE FE B5 1F 59 54 4D B3 13")

    requests.post(url, headers=headers, data=data)


# ═══════════════════════════════════════════════════════════════
#              ★ Likes তথ্য ফেচ (RAFIN TxT) ★
# ═══════════════════════════════════════════════════════════════

def Likes(id):
    """প্লেয়ারের Likes তথ্য বের করবে"""
    try:
        text = requests.get(f"{LIKE_API}?id={id}&type=likes").text
        get = lambda p: re.search(p, text)
        name, lvl, exp, lb, la, lg = (
            get(r).group(1) if get(r) else None
            for r in [
                r"PLayer NamE\s*:\s*(.+)",
                r"PLayer SerVer\s*:\s*(.+)",
                r"Exp\s*:\s*(\d+)",
                r"LiKes BeFore\s*:\s*(\d+)",
                r"LiKes After\s*:\s*(\d+)",
                r"LiKes GiVen\s*:\s*(\d+)",
            ]
        )
        return (
            name,
            f"{lvl}" if lvl else None,
            int(lb) if lb else None,
            int(la) if la else None,
            int(lg) if lg else None,
        )
    except Exception:
        return None, None, None, None, None


def Requests_SPam(id):
    """স্প্যাম রিকোয়েস্ট পাঠাবে"""
    Api = requests.get(f'{TOKEN_API}?id={id}&type=spam')
    if Api.status_code in [200, 201] and '[SuccessFuLy] -> SenDinG Spam ReQuesTs !' in Api.text:
        return True
    else:
        return False


# ═══════════════════════════════════════════════════════════════
#              ★ Player Name ফেচ (RAFIN TxT) ★
# ═══════════════════════════════════════════════════════════════

def GeT_Name(uid, Token):
    """প্লেয়ারের নাম বের করবে"""
    data = bytes.fromhex(EnC_AEs(f"08{EnC_Uid(uid, Tp='Uid')}1007"))
    url = "https://clientbp.common.ggbluefox.com/GetPlayerPersonalShow"

    headers = DEFAULT_OB_HEADERS.copy()
    headers['Authorization'] = f'Bearer {GeTToK()}'

    response = requests.post(url, headers=headers, data=data, verify=False)
    if response.status_code in (200, 201):
        packet = binascii.hexlify(response.content).decode('utf-8')
        BesTo_data = json.loads(DeCode_PackEt(packet))
        try:
            a1 = BesTo_data["1"]["data"]["3"]["data"]
            return a1
        except Exception:
            return ''
    else:
        return ''


# ═══════════════════════════════════════════════════════════════
#              ★ Player সম্পূর্ণ তথ্য (RAFIN TxT) ★
# ═══════════════════════════════════════════════════════════════

def GeT_PLayer_InFo(uid, Token):
    """প্লেয়ারের সম্পূর্ণ প্রোফাইল + গিল্ড তথ্য"""
    data = bytes.fromhex(EnC_AEs(f"08{EnC_Uid(uid, Tp='Uid')}1007"))
    url = "https://clientbp.common.ggbluefox.com/GetPlayerPersonalShow"

    headers = DEFAULT_OB_HEADERS.copy()
    headers['Authorization'] = f'Bearer {GeTToK()}'

    response = requests.post(url, headers=headers, data=data, verify=False)

    if response.status_code in (200, 201):
        packet = binascii.hexlify(response.content).decode('utf-8')
        BesTo_data = json.loads(DeCode_PackEt(packet))
        NoCLan = False
        try:
            a1 = str(BesTo_data["1"]["data"]["1"]["data"])
            a2 = BesTo_data["1"]["data"]["21"]["data"]
            a3 = BesTo_data["1"]["data"]["3"]["data"]
            player_server = BesTo_data["1"]["data"]["5"]["data"]
            player_bio    = BesTo_data["9"]["data"]["9"]["data"]
            player_level  = BesTo_data["1"]["data"]["6"]["data"]
            account_date  = datetime.fromtimestamp(BesTo_data["1"]["data"]["44"]["data"]).strftime("%I:%M %p - %d/%m/%y")
            last_login    = datetime.fromtimestamp(BesTo_data["1"]["data"]["24"]["data"]).strftime("%I:%M %p - %d/%m/%y")

            try:
                clan_id         = BesTo_data["6"]["data"]["1"]["data"]
                clan_name       = BesTo_data["6"]["data"]["2"]["data"]
                clan_leader     = BesTo_data["6"]["data"]["3"]["data"]
                clan_level      = BesTo_data["6"]["data"]["4"]["data"]
                clan_members_num= BesTo_data["6"]["data"]["6"]["data"]
                clan_leader_name= BesTo_data["7"]["data"]["3"]["data"]
            except Exception:
                NoCLan = True

            if NoCLan:
                a = f'''
[b][c][90EE90] [SuccessFully] - Get PLayer s'InFo !

[FFFF00][1] - ProFile InFo :
[ffffff]	
 Name : {a3}
 Uid : {xMsGFixinG(a1)}
 Likes : {xMsGFixinG(a2)}
 LeveL : {player_level}
 Server : {player_server}
 Bio : {player_bio}
 Creating : {account_date}
 LasT LoGin : {last_login}
 
  [90EE90]Dev : RAFIN TxT\n'''
                a = a.replace('[i]', '')
                return a

            else:
                a = f'''
[b][c][90EE90] [SuccessFully] - Get PLayer s'InFo !

[FFFF00][1] - ProFile InFo :
[ffffff]	
 Name : {a3}
 Uid : {xMsGFixinG(a1)}
 Likes : {xMsGFixinG(a2)}
 LeveL : {player_level}
 Server : {player_server}
 Bio : {player_bio}
 Creating : {account_date}
 LasT LoGin : {last_login}

[b][c][FFFF00][2] - Guild InFo :
[ffffff]
 Guild Name : {clan_name}
 Guild Uid : {xMsGFixinG(clan_id)}
 Guild LeveL : {clan_level}
 Guild Members : {clan_members_num}
 Leader s'Uid : {xMsGFixinG(clan_leader)}
 Leader s'Name : {clan_leader_name}

  [90EE90]Dev : RAFIN TxT\n'''
                a = a.replace('[i]', '')
                return a

        except Exception:
            return f'\n[b][c][FFD700]FaiLEd GeTinG PLayer InFo !\n'
    else:
        return f'\n[b][c][FFD700]FaiLEd GeTinG PLayer InFo !\n'


# ═══════════════════════════════════════════════════════════════
#              ★ বন্ধু মুছে ফেলা (RAFIN TxT) ★
# ═══════════════════════════════════════════════════════════════

def DeLet_Uid(id, Tok):
    """ফ্রেন্ড লিস্ট থেকে প্লেয়ার রিমুভ করবে"""
    print(f' Done FuckinG > {id} ')
    url = 'https://clientbp.common.ggbluefox.com/RemoveFriend'

    headers = DEFAULT_OB_HEADERS.copy()
    headers['Authorization'] = f'Bearer {Tok}'

    data = bytes.fromhex(EnC_AEs(f"08a7c4839f1e10{EnC_Uid(id, Tp='Uid')}"))
    ResPonse = requests.post(url, headers=headers, data=data, verify=False)

    if ResPonse.status_code == 400 and 'BR_FRIEND_NOT_SAME_REGION' in ResPonse.text:
        return f'[b][c]Id : {xMsGFixinG(id)} Not In Same Region !'
    elif ResPonse.status_code == 200:
        return f'[b][c]Good Response Done Delete Id : {xMsGFixinG(id)} !'
    else:
        return f'[b][c]Erorr !'


# ═══════════════════════════════════════════════════════════════
#              ★ UID ভ্যালিডেশন চেক (RAFIN TxT) ★
# ═══════════════════════════════════════════════════════════════

def ChEck_The_Uid(id):
    """UID এর স্ট্যাটাস ও এক্সপায়ারি চেক করবে"""
    Api = requests.get(UID_API)
    if Api.status_code not in [200, 201]:
        return False

    lines = Api.text.splitlines()
    for i, line in enumerate(lines):
        if f' - Uid : {id}' in line:
            expire, status = None, None
            for sub_line in lines[i:]:
                if "Expire In" in sub_line:
                    expire = re.search(r"Expire In\s*:\s*(.*)", sub_line).group(1).strip()
                if "Status" in sub_line:
                    status = re.search(r"Status\s*:\s*(\w+)", sub_line).group(1)
                if expire and status:
                    return status, expire
            return False
    return False


# ═══════════════════════════════════════════════════════════════
#                    ★ RAFIN TxT — END OF FILE ★
# ═══════════════════════════════════════════════════════════════