# ═══════════════════════════════════════════════════════════════
#   ██████╗  █████╗ ███████╗██╗███╗   ██╗    ████████╗██╗  ██╗████████╗
#   ██╔══██╗██╔══██╗██╔════╝██║████╗  ██║    ╚══██╔══╝╚██╗██╔╝╚══██╔══╝
#   ██████╔╝███████║█████╗  ██║██╔██╗ ██║       ██║    ╚███╔╝    ██║
#   ██╔══██╗██╔══██║██╔══╝  ██║██║╚██╗██║       ██║    ██╔██╗    ██║
#   ██║  ██║██║  ██║██║     ██║██║ ╚████║       ██║   ██╔╝ ██╗   ██║
#   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═══╝       ╚═╝   ╚═╝  ╚═╝   ╚═╝
#
#               ★ PREMIUM FADAI CORE — BY RAFIN TxT ★
#               ▌ Squad / Chat / Ghost / Protocol ▌
#               ▌ Free Fire OB55 Packet Builder ▌
# ═══════════════════════════════════════════════════════════════
#
#  ▸ মডিউল নাম     : FADAI.py
#  ▸ ব্র্যান্ডিং     : RAFIN TxT
#  ▸ ফিচার           : Squad / Chat / Ghost / Packet Builder
# ═══════════════════════════════════════════════════════════════

import requests
import json
import binascii
import time
import urllib3
import base64
import datetime
import re
import socket
import threading
import random
import os
import sys
import psutil

from protobuf_decoder.protobuf_decoder import Parser
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ═══════════════════════════════════════════════════════════════
#              ★ AES কী ও IV (API এনক্রিপশন) ★
# ═══════════════════════════════════════════════════════════════

Key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
Iv  = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])


# ═══════════════════════════════════════════════════════════════
#              ★ রঙ ও ডিভাইস জেনারেটর (RAFIN TxT) ★
# ═══════════════════════════════════════════════════════════════

def generate_random_color():
    """র্যান্ডম চ্যাট কালার ট্যাগ"""
    color_list = [
        "[00FF00][b][c]", "[FFDD00][b][c]", "[3813F3][b][c]", "[FF0000][b][c]",
        "[0000FF][b][c]", "[FFA500][b][c]", "[DF07F8][b][c]", "[11EAFD][b][c]",
        "[DCE775][b][c]", "[A8E6CF][b][c]", "[7CB342][b][c]", "[FF0000][b][c]",
        "[FFB300][b][c]", "[90EE90][b][c]", "[FF4500][b][c]", "[FFD700][b][c]",
        "[32CD32][b][c]", "[87CEEB][b][c]", "[9370DB][b][c]", "[FF69B4][b][c]",
        "[8A2BE2][b][c]", "[00BFFF][b][c]", "[1E90FF][b][c]", "[20B2AA][b][c]",
        "[00FA9A][b][c]", "[008000][b][c]", "[FFFF00][b][c]", "[FF8C00][b][c]",
        "[DC143C][b][c]", "[FF6347][b][c]", "[FFA07A][b][c]", "[FFDAB9][b][c]",
        "[CD853F][b][c]", "[D2691E][b][c]", "[BC8F8F][b][c]", "[F0E68C][b][c]",
        "[556B2F][b][c]", "[808000][b][c]", "[4682B4][b][c]", "[6A5ACD][b][c]",
        "[7B68EE][b][c]", "[8B4513][b][c]", "[C71585][b][c]", "[4B0082][b][c]",
        "[B22222][b][c]", "[228B22][b][c]", "[8B008B][b][c]", "[483D8B][b][c]",
        "[556B2F][b][c]", "[800000][b][c]", "[008080][b][c]", "[000080][b][c]",
        "[800080][b][c]", "[808080][b][c]", "[A9A9A9][b][c]", "[D3D3D3][b][c]", "[F0F0F0][b][c]"
    ]
    return random.choice(color_list)


def Device():
    """র্যান্ডম ডিভাইস প্রোফাইল (ভবিষ্যতে ব্যবহারের জন্য)"""
    versions = [
        '4.0.18P6', '4.0.19P7', '4.0.20P1', '4.1.0P3', '4.1.5P2', '4.2.1P8',
        '4.2.3P1', '5.0.1B2', '5.0.2P4', '5.1.0P1', '5.2.0B1', '5.2.5P3',
        '5.3.0B1', '5.3.2P2', '5.4.0P1', '5.4.3B2', '5.5.0P1', '5.5.2P3'
    ]
    models = [
        'SM-A125F', 'SM-A225F', 'SM-A325M', 'SM-A515F', 'SM-A725F', 'SM-M215F', 'SM-M325FV',
        'Redmi 9A', 'Redmi 9C', 'POCO M3', 'POCO M4 Pro', 'RMX2185', 'RMX3085',
        'moto g(9) play', 'CPH2239', 'V2027', 'OnePlus Nord', 'ASUS_Z01QD',
    ]
    android_versions = ['9', '10', '11', '12', '13', '14']
    languages = ['en-US', 'es-MX', 'pt-BR', 'id-ID', 'ru-RU', 'hi-IN']
    countries = ['USA', 'MEX', 'BRA', 'IDN', 'RUS', 'IND']
    return (
        random.choice(versions),
        random.choice(models),
        random.choice(android_versions),
        random.choice(languages),
        random.choice(countries),
    )


# ═══════════════════════════════════════════════════════════════
#              ★ AES এনক্রিপশন / ডিক্রিপশন ★
# ═══════════════════════════════════════════════════════════════

def EnC_AEs(HeX):
    """API পেলোড এনক্রিপ্ট (hex → hex)"""
    cipher = AES.new(Key, AES.MODE_CBC, Iv)
    return cipher.encrypt(pad(bytes.fromhex(HeX), AES.block_size)).hex()


def DEc_AEs(HeX):
    """API পেলোড ডিক্রিপ্ট (hex → hex)"""
    cipher = AES.new(Key, AES.MODE_CBC, Iv)
    return unpad(cipher.decrypt(bytes.fromhex(HeX)), AES.block_size).hex()


def EnC_PacKeT(HeX, K, V):
    """TCP প্যাকেট এনক্রিপ্ট"""
    return AES.new(K, AES.MODE_CBC, V).encrypt(pad(bytes.fromhex(HeX), 16)).hex()


def DEc_PacKeT(HeX, K, V):
    """TCP প্যাকেট ডিক্রিপ্ট"""
    return unpad(AES.new(K, AES.MODE_CBC, V).decrypt(bytes.fromhex(HeX)), 16).hex()


# ═══════════════════════════════════════════════════════════════
#              ★ UID / Varint এনকোড-ডিকোড ★
# ═══════════════════════════════════════════════════════════════

def EnC_Uid(H, Tp):
    """UID কে varint hex এ রূপান্তর"""
    e, H = [], int(H)
    while H:
        e.append((H & 0x7F) | (0x80 if H > 0x7F else 0))
        H >>= 7
    return bytes(e).hex() if Tp == 'Uid' else None


def EnC_Vr(N):
    """সংখ্যাকে varint বাইটে রূপান্তর"""
    if N < 0:
        return b''
    H = []
    while True:
        BesTo = N & 0x7F
        N >>= 7
        if N:
            BesTo |= 0x80
        H.append(BesTo)
        if not N:
            break
    return bytes(H)


def DEc_Uid(H):
    """varint hex থেকে আসল সংখ্যায়"""
    n = s = 0
    for b in bytes.fromhex(H):
        n |= (b & 0x7F) << s
        if not b & 0x80:
            break
        s += 7
    return n


# ═══════════════════════════════════════════════════════════════
#              ★ Protobuf ফিল্ড বিল্ডার (RAFIN TxT) ★
# ═══════════════════════════════════════════════════════════════

def CrEaTe_VarianT(field_number, value):
    """Varint ফিল্ড তৈরি"""
    field_header = (field_number << 3) | 0
    return EnC_Vr(field_header) + EnC_Vr(value)


def CrEaTe_LenGTh(field_number, value):
    """Length-delimited ফিল্ড তৈরি"""
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return EnC_Vr(field_header) + EnC_Vr(len(encoded_value)) + encoded_value


def CrEaTe_ProTo(fields):
    """ডিকশনারি → protobuf বডি"""
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = CrEaTe_ProTo(value)
            packet.extend(CrEaTe_LenGTh(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(CrEaTe_VarianT(field, value))
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(CrEaTe_LenGTh(field, value))
    return packet


# ═══════════════════════════════════════════════════════════════
#              ★ হেক্স ও প্যাকেট ডিকোডার ★
# ═══════════════════════════════════════════════════════════════

def DecodE_HeX(H):
    """সংখ্যা → 2-ডিজিট হেক্স স্ট্রিং"""
    R = hex(H)
    F = str(R)[2:]
    if len(F) == 1:
        F = "0" + F
        return F
    else:
        return F


def Fix_PackEt(parsed_results):
    """protobuf পার্স রেজাল্ট ফিক্স"""
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data['wire_type'] = result.wire_type
        if result.wire_type == "varint":
            field_data['data'] = result.data
        if result.wire_type == "string":
            field_data['data'] = result.data
        if result.wire_type == "bytes":
            field_data['data'] = result.data
        elif result.wire_type == 'length_delimited':
            field_data["data"] = Fix_PackEt(result.data.results)
        result_dict[result.field] = field_data
    return result_dict


def DeCode_PackEt(input_text):
    """হেক্স প্যাকেট পার্স করে JSON রিটার্ন"""
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_dict = Fix_PackEt(parsed_results)
        return json.dumps(parsed_results_dict)
    except Exception as e:
        print(f"error {e}")
        return None


# ═══════════════════════════════════════════════════════════════
#              ★ হেল্পার — ব্যানার, কালার, মেসেজ ★
# ═══════════════════════════════════════════════════════════════

def xBunnEr():
    """ব্যানার আইডি রিটার্ন"""
    bN = [902000306]
    return random.choice(bN)


def xMsgPr(Msg, Tp, Tp2, id, K, V):
    """চ্যাট মেসেজ প্যাকেট (RAFIN TxT)"""
    feilds = {
        1: id,
        2: Tp2,
        3: Tp,
        4: Msg,
        5: 1735129800,
        7: 2,
        9: {
            1: "xBesTo - C4",
            2: xBunnEr(),
            3: 901048018,
            4: 330,
            5: 909000014,
            8: "xBesTo - C4",
            10: 1,
            11: random.choice([1]),
            13: {1: 2, 2: 1},
            14: {
                1: 1158053040,
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0015\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            }
        },
        10: "en",
        13: {2: 1, 3: 1},
        14: {}
    }
    Pk = str(CrEaTe_ProTo(feilds).hex())
    Pk = "080112" + EnC_Uid(len(Pk) // 2, Tp='Uid') + Pk
    return GeneRaTePk(str(Pk), '1215', K, V)


def ArA_CoLor():
    """লাইট-কালার র্যান্ডম হেক্স"""
    Tp = [
        "FF9999", "99FF99", "99CCFF", "FFD700", "FFB6C1", "FFA07A",
        "98FB98", "E6E6FA", "AFEEEE", "F0E68C", "FFE4B5", "D8BFD8",
        "FFFACD", "87CEFA", "FFDEAD", "B0E0E6", "FFDAB9", "E0FFFF",
        "F5DEB3", "FFC0CB", "FFF0F5", "ADD8E6"
    ]
    return random.choice(Tp)


# ═══════════════════════════════════════════════════════════════
#              ★ চ্যাট / স্কোয়াড প্যাকেট ★
# ═══════════════════════════════════════════════════════════════

def OpenCh(idT, sq, K, V):
    """চ্যাট ওপেন"""
    fields = {1: 3, 2: {1: idT, 3: "fr", 4: sq}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '1215', K, V)


def OpenSq(K, V):
    """স্কোয়াড ওপেন"""
    fields = {
        1: 1,
        2: {2: "\u0001", 3: 1, 4: 1, 5: "en", 9: 1, 11: 1, 13: 1,
            14: {2: 5756, 6: 11, 8: "1.132.18", 9: 2, 10: 4}}
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', K, V)


def ChSq(Nu, Uid, K, V):
    """স্কোয়াড সাইজ পরিবর্তন"""
    fields = {
        1: 17,
        2: {1: int(Uid), 2: 1, 3: int(Nu - 1), 4: 62, 5: "\u001a", 8: 5, 13: 329}
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', K, V)


def ExitSq(id, K, V):
    """স্কোয়াড থেকে বের হওয়া"""
    fields = {1: 7, 2: {1: int(11037044965)}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', K, V)


def MsqSq(msg, idT, K, V):
    """স্কোয়াড মেসেজ"""
    fields = {
        1: 1,
        2: {
            1: 12404281032,
            2: idT,
            4: msg,
            7: 2,
            10: "fr",
            9: {
                1: "C4 TEAM",
                2: xBunnEr(),
                4: 330,
                5: 909000014,
                8: "C4 TEAM",
                10: 1,
                11: 1,
                12: {1: 2},
                14: {
                    1: 1158053040,
                    2: 8,
                    3: "\u0010\u0015\b\n\u000b\u0015\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
                }
            },
            13: {1: 2, 2: 1},
            14: {}
        }
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '1215', K, V)


def SendSq(Nu, Uid, K, V):
    """স্কোয়াড ইনভাইট পাঠানো"""
    fields = {1: 2, 2: {1: int(Uid), 2: "ME", 4: int(Nu)}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', K, V)


def JoinSq(code, key, iv):
    """টিম কোড দিয়ে স্কোয়াড জয়েন"""
    fields = {}
    fields[1] = 4
    fields[2] = {}
    fields[2][4] = bytes.fromhex("01090a0b121920")
    fields[2][5] = str(code)
    fields[2][6] = 6
    fields[2][8] = 1
    fields[2][9] = {}
    fields[2][9][2] = 800
    fields[2][9][6] = 11
    fields[2][9][8] = "1.132.18"
    fields[2][9][9] = 5
    fields[2][9][10] = 1
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', key, iv)


def GhostSq(player_id, nm, secret_code, key, iv):
    """ঘোস্ট স্কোয়াড প্যাকেট"""
    fields = {
        1: 61,
        2: {
            1: int(player_id),
            2: {
                1: int(player_id),
                2: 1159,
                3: f"[b][c][{ArA_CoLor()}]{nm}",
                5: 12,
                6: 999,
                7: 1,
                8: {2: 1, 3: 1},
                9: 3,
            },
            3: secret_code,
        },
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0515', key, iv)


# ═══════════════════════════════════════════════════════════════
#              ★ UID ফরম্যাটার ও প্রোটো পার্সার ★
# ═══════════════════════════════════════════════════════════════

def xMsGFixinG(n):
    """৩ ডিজিট গ্রুপ করে UID সুন্দর দেখাবে"""
    return '🗿'.join(str(n)[i:i + 3] for i in range(0, len(str(n)), 3))


def _V(b, i):
    """varint রিডার (ইন্টারনাল)"""
    r = s = 0
    while True:
        c = b[i]
        i += 1
        r |= (c & 0x7F) << s
        if c < 0x80:
            break
        s += 7
    return r, i


def PrOtO(hx):
    """লো-লেভেল protobuf পার্সার"""
    b, i, R = bytes.fromhex(hx), 0, {}
    while i < len(b):
        H, i = _V(b, i)
        F, T = H >> 3, H & 7
        if T == 0:
            R[F], i = _V(b, i)
        elif T == 2:
            L, i = _V(b, i)
            S = b[i:i + L]
            i += L
            try:
                R[F] = S.decode()
            except Exception:
                try:
                    R[F] = PrOtO(S.hex())
                except Exception:
                    R[F] = S
        elif T == 5:
            R[F] = int.from_bytes(b[i:i + 4], 'little')
            i += 4
        else:
            raise ValueError(f'Unknown wire type: {T}')
    return R


def GeT_KEy(obj, target):
    """যেকোনো ডিকশনারি থেকে নির্দিষ্ট key খুঁজে বের করে"""
    values = []

    def collect(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == target:
                    values.append(v)
                collect(v)
        elif isinstance(o, list):
            for v in o:
                collect(v)

    collect(obj)
    return values[-1] if values else None


# ═══════════════════════════════════════════════════════════════
#              ★ মূল প্যাকেট জেনারেটর (RAFIN TxT) ★
# ═══════════════════════════════════════════════════════════════

def GeneRaTePk(Pk, N, K, V):
    """প্যাকেট এনক্রিপ্ট + হেডার বসিয়ে ফাইনাল বাইট"""
    PkEnc = EnC_PacKeT(Pk, K, V)
    _ = DecodE_HeX(int(len(PkEnc) // 2))
    if len(_) == 2:
        HeadEr = N + "000000"
    elif len(_) == 3:
        HeadEr = N + "00000"
    elif len(_) == 4:
        HeadEr = N + "0000"
    elif len(_) == 5:
        HeadEr = N + "000"
    else:
        print('ErroR => GeneRatinG ThE PacKeT !!')
        return None
    return bytes.fromhex(HeadEr + _ + PkEnc)


# ═══════════════════════════════════════════════════════════════
#              ★ গিল্ড অ্যাক্সেস চেক ★
# ═══════════════════════════════════════════════════════════════

def GuiLd_AccEss(Tg, Nm, Uid, BLk, OwN, AprV):
    """গিল্ড অ্যাক্সেস যাচাই"""
    return Tg in Nm and Uid not in BLk and Uid in (OwN | AprV)


def ChEck_Commande(id):
    """কমান্ডে ভুল ক্যারেক্টার চেক"""
    return "<" not in id and ">" not in id and "[" not in id and "]" not in id


# ═══════════════════════════════════════════════════════════════
#              ★ বট রিস্টার্ট ও টাইম হেল্পার ★
# ═══════════════════════════════════════════════════════════════

def ResTarT_BoT():
    """এরর হলে বট নিজেই রিস্টার্ট করে"""
    print('\nError In Src! ')
    p = psutil.Process(os.getpid())
    open_files = p.open_files()
    connections = p.net_connections()
    for handler in open_files:
        try:
            os.close(handler.fd)
        except Exception:
            pass
    for conn in connections:
        try:
            conn.close()
        except Exception:
            pass
    sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))
    python = sys.executable
    os.execl(python, python, *sys.argv)


def GeT_Time(timestamp):
    """টাইমস্ট্যাম্প থেকে দিন/ঘণ্টা/মিনিট/সেকেন্ড বের করবে"""
    last_login = datetime.fromtimestamp(timestamp)
    now = datetime.now()
    diff = now - last_login
    d = diff.days
    h, rem = divmod(diff.seconds, 3600)
    m, s = divmod(rem, 60)
    return d, h, m, s


# ═══════════════════════════════════════════════════════════════
#                    ★ RAFIN TxT — END OF FILE ★
# ═══════════════════════════════════════════════════════════════