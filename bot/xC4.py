# ═══════════════════════════════════════════════════════════════
#   ██████╗  █████╗ ███████╗██╗███╗   ██╗    ████████╗██╗  ██╗████████╗
#   ██╔══██╗██╔══██╗██╔════╝██║████╗  ██║    ╚══██╔══╝╚██╗██╔╝╚══██╔══╝
#   ██████╔╝███████║█████╗  ██║██╔██╗ ██║       ██║    ╚███╔╝    ██║
#   ██╔══██╗██╔══██║██╔══╝  ██║██║╚██╗██║       ██║    ██╔██╗    ██║
#   ██║  ██║██║  ██║██║     ██║██║ ╚████║       ██║   ██╔╝ ██╗   ██║
#   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═══╝       ╚═╝   ╚═╝  ╚═╝   ╚═╝
#
#              ★ PREMIUM BOT CORE — BY RAFIN TxT ★
#              ▌ Free Fire OB55 TCP Bot Engine ▌
#              ▌ Protocol / Packet / Squad / Chat ▌
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
import asyncio

from protobuf_decoder.protobuf_decoder import Parser
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ═══════════════════════════════════════════════════════════════
#              ★ গ্লোবাল ভেরিয়েবল (bot_core ↔ main শেয়ার) ★
# ═══════════════════════════════════════════════════════════════

bot_uid = None
ToKen   = None
region  = None


# ═══════════════════════════════════════════════════════════════
#              ★ AES কী ও IV (API এনক্রিপশন) ★
# ═══════════════════════════════════════════════════════════════

Key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
Iv  = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])


# ═══════════════════════════════════════════════════════════════
#                    ★ AES এনক্রিপশন ইউটিল ★
# ═══════════════════════════════════════════════════════════════

async def EnC_AEs(HeX):
    """API পেলোড এনক্রিপ্ট (hex → hex)"""
    cipher = AES.new(Key, AES.MODE_CBC, Iv)
    return cipher.encrypt(pad(bytes.fromhex(HeX), AES.block_size)).hex()


async def DEc_AEs(HeX):
    """API পেলোড ডিক্রিপ্ট (hex → hex)"""
    cipher = AES.new(Key, AES.MODE_CBC, Iv)
    return unpad(cipher.decrypt(bytes.fromhex(HeX)), AES.block_size).hex()


async def EnC_PacKeT(HeX, K, V):
    """TCP প্যাকেট এনক্রিপ্ট"""
    return AES.new(K, AES.MODE_CBC, V).encrypt(pad(bytes.fromhex(HeX), 16)).hex()


async def DEc_PacKeT(HeX, K, V):
    """TCP প্যাকেট ডিক্রিপ্ট"""
    return unpad(AES.new(K, AES.MODE_CBC, V).decrypt(bytes.fromhex(HeX)), 16).hex()


# ═══════════════════════════════════════════════════════════════
#              ★ UID / Varint এনকোড-ডিকোড ★
# ═══════════════════════════════════════════════════════════════

async def EnC_Uid(H, Tp):
    """UID কে varint এ রূপান্তর"""
    e, H = [], int(H)
    while H:
        e.append((H & 0x7F) | (0x80 if H > 0x7F else 0))
        H >>= 7
    return bytes(e).hex() if Tp == 'Uid' else None


async def EnC_Vr(N):
    """যেকোনো সংখ্যাকে varint বাইটে রূপান্তর"""
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
    """varint hex থেকে আসল সংখ্যায় রূপান্তর"""
    n = s = 0
    for b in bytes.fromhex(H):
        n |= (b & 0x7F) << s
        if not b & 0x80:
            break
        s += 7
    return n


# ═══════════════════════════════════════════════════════════════
#              ★ Protobuf ফিল্ড তৈরি (RAFIN TxT) ★
# ═══════════════════════════════════════════════════════════════

async def CrEaTe_VarianT(field_number, value):
    """Varint ফিল্ড তৈরি"""
    field_header = (field_number << 3) | 0
    return await EnC_Vr(field_header) + await EnC_Vr(value)


async def CrEaTe_LenGTh(field_number, value):
    """Length-delimited ফিল্ড তৈরি"""
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return await EnC_Vr(field_header) + await EnC_Vr(len(encoded_value)) + encoded_value


async def CrEaTe_ProTo(fields):
    """ডিকশনারি থেকে সম্পূর্ণ protobuf বডি তৈরি"""
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = await CrEaTe_ProTo(value)
            packet.extend(await CrEaTe_LenGTh(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(await CrEaTe_VarianT(field, value))
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(await CrEaTe_LenGTh(field, value))
    return packet


# ═══════════════════════════════════════════════════════════════
#              ★ হেক্স ও প্যাকেট ডিকোডার ★
# ═══════════════════════════════════════════════════════════════

async def DecodE_HeX(H):
    """সংখ্যাকে 2-ডিজিট হেক্সে রূপান্তর"""
    R = hex(H)
    F = str(R)[2:]
    if len(F) == 1:
        F = "0" + F
        return F
    else:
        return F


async def Fix_PackEt(parsed_results):
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
            field_data["data"] = await Fix_PackEt(result.data.results)
        result_dict[result.field] = field_data
    return result_dict


async def DeCode_PackEt(input_text):
    """হেক্স প্যাকেট পার্স করে JSON রিটার্ন"""
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_dict = await Fix_PackEt(parsed_results)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        print(f"error {e}")
        return None


# ═══════════════════════════════════════════════════════════════
#              ★ র্যান্ডম হেল্পার (RAFIN TxT) ★
# ═══════════════════════════════════════════════════════════════

def xMsGFixinG(n):
    """৩ ডিজিট গ্রুপ করে মেসেজ স্প্লিট"""
    return '🗿'.join(str(n)[i:i + 3] for i in range(0, len(str(n)), 3))


async def Ua():
    """র্যান্ডম User-Agent জেনারেটর"""
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
    countries = ['USA', 'MEX', 'BRA', 'IDN', 'RUS', 'VN']
    version = random.choice(versions)
    model = random.choice(models)
    android = random.choice(android_versions)
    lang = random.choice(languages)
    country = random.choice(countries)
    return f"GarenaMSDK/{version}({model};Android {android};{lang};{country};)"


async def ArA_CoLor():
    """র্যান্ডম হেক্স কালার (নামের সামনে বসে)"""
    Tp = [
        "32CD32", "00BFFF", "00FA9A", "90EE90", "FF4500", "FF6347", "FF69B4",
        "FF8C00", "FF6347", "FFD700", "FFDAB9", "F0F0F0", "F0E68C", "D3D3D3",
        "A9A9A9", "D2691E", "CD853F", "BC8F8F", "6A5ACD", "483D8B", "4682B4",
        "9370DB", "C71585", "FF8C00", "FFA07A"
    ]
    return random.choice(Tp)


async def xBunnEr():
    """র্যান্ডম ব্যানার আইডি"""
    bN = [
        902000126, 902000154, 902000003, 902027018, 902027027, 902039014,
        902040027, 902042011, 902048021, 902048018, 902000027, 902000078,
        902000013, 902000093, 902000100, 902000117, 902000111, 902000151,
        902000207, 902000203, 902027016, 902027018, 902033016, 902027018,
        902027018, 902027018, 902027018, 902027018, 902027018
    ]
    return random.choice(bN)


# ═══════════════════════════════════════════════════════════════
#                    ★ চ্যাট প্যাকেট (RAFIN TxT) ★
# ═══════════════════════════════════════════════════════════════

async def xSEndMsg(Msg, Tp, Tp2, id, K, V):
    """চ্যাট / স্কোয়াড মেসেজ প্যাকেট"""
    feilds = {
        1: id, 2: Tp2, 3: Tp, 4: Msg, 5: 1735129800, 7: 2,
        9: {
            1: "xBesTo - C4", 2: int(await xBunnEr()), 3: 901048018, 4: 330,
            5: 909034009, 8: "xBesTo - C4", 10: 1, 11: 1, 13: {1: 2},
            14: {
                1: 12484827014, 2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            12: 0
        },
        10: "en", 13: {3: 1}
    }
    Pk = (await CrEaTe_ProTo(feilds)).hex()
    Pk = "080112" + await EnC_Uid(len(Pk) // 2, Tp='Uid') + Pk
    return await GeneRaTePk(Pk, '1201', K, V)


async def xSEndMsgsQ(Msg, id, K, V, region="BD"):
    """Fixed version - exactly like small bot"""
    
    avatar = await xBunnEr()
    
    fields = {
        1: id, 
        2: id, 
        4: Msg, 
        5: 1756580149, 
        8: 904990072, 
        9: {
            1: "[FFFFFF]RAFINxJISAN",  # আপনার bot name
            2: avatar, 
            3: 2,                 # ⭐ CRITICAL
            4: 329, 
            5: 1001000001, 
            6: 66,
            7: 66,                # ⭐ CRITICAL
            8: "xBe4!sTo - C4", 
            9: 66,
            10: 66, 
            11: 66, 
            12: 66,
            13: {1: 68, 2:67}, 
            14: {
                1: 1158053040, 
                2: 8, 
                3: b"\x10\x15\x08\x0A\x0B\x15\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
            }
        }, 
        10: "en", 
        13: {66: 66, 66: 66},
        14: {                    # ⭐ CRITICAL - এই field টা যোগ করুন
            11: {
                1: 3,
                2: 7,
                3: 170,
                4: 999,
                5: 1,
                6: region,
                7: 2,
                8: 2,
                9: 2
            }
        }
    }
    
    Pk = (await CrEaTe_ProTo(fields)).hex()
    Pk = "080112" + await EnC_Uid(len(Pk) // 2, Tp='Uid') + Pk
    return await GeneRaTePk(Pk, '1201', K, V)



# ═══════════════════════════════════════════════════════════════
#                    ★ Auth প্যাকেট ★
# ═══════════════════════════════════════════════════════════════

async def AuthClan(CLan_Uid, AuTh, K, V):
    """ক্ল্যান অথেনটিকেশন"""
    fields = {1: 3, 2: {1: int(CLan_Uid), 2: 1, 4: str(AuTh)}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '1201', K, V)


async def AutH_GlobAl(K, V):
    """গ্লোবাল চ্যাট অথেনটিকেশন"""
    fields = {1: 3, 2: {2: 5, 3: "en"}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '1215', K, V)


async def AutH_Chat(T, uid, code, K, V):
    """চ্যাট অথেনটিকেশন"""
    fields = {1: T, 2: {1: uid, 3: "en", 4: str(code)}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '1215', K, V)


# ═══════════════════════════════════════════════════════════════
#                    ★ স্কোয়াড প্যাকেট ★
# ═══════════════════════════════════════════════════════════════

async def LagSquad(K, V):
    """স্কোয়াড ল্যাগ চেক"""
    fields = {1: 15, 2: {1: 1124759936, 2: 1}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', K, V)


async def GeT_Status(PLayer_Uid, K, V):
    """প্লেয়ার স্ট্যাটাস চেক"""
    PLayer_Uid = await EnC_Uid(PLayer_Uid, Tp='Uid')
    if len(PLayer_Uid) == 8:
        Pk = f'080112080a04{PLayer_Uid}1005'
    elif len(PLayer_Uid) == 10:
        Pk = f"080112090a05{PLayer_Uid}1005"
    return await GeneRaTePk(Pk, '0f15', K, V)


async def SPam_Room(Uid, Rm, Nm, K, V):
    """রুম স্প্যাম প্যাকেট"""
    fields = {
        1: 78,
        2: {
            1: int(Rm), 2: f"[{ArA_CoLor()}]{Nm}", 3: {2: 1, 3: 1},
            4: 330, 5: 1, 6: 201, 10: xBunnEr(), 11: int(Uid), 12: 1
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0e15', K, V)


async def GenJoinSquadsPacket(code, K, V):
    """স্কোয়াড জয়েন (কোড দিয়ে)"""
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
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', K, V)


async def GenJoinGlobaL(owner, code, K, V):
    """গ্লোবাল স্কোয়াড জয়েন"""
    fields = {
        1: 4,
        2: {1: owner, 6: 1, 8: 1, 13: "en", 15: code, 16: "OR"}
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', K, V)


async def FS(K, V, region):
    """ফ্রেন্ড স্ট্যাটাস / ফায়ার স্ট্যাটাস"""
    fields = {1: 9, 2: {1: 13256361202}}
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, K, V)


async def Emote_k(TarGeT, idT, K, V, region):
    """ইমোট প্যাকেট"""
    fields = {1: 21, 2: {1: 804266360, 2: 909000001, 5: {1: TarGeT, 3: idT}}}
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, K, V)


async def GeTSQDaTa(D):
    """স্কোয়াড ডেটা এক্সট্র্যাক্ট"""
    uid = D['5']['data']['1']['data']
    chat_code = D["5"]["data"]["17"]["data"]
    squad_code = D["5"]["data"]["31"]["data"]
    return uid, chat_code, squad_code


async def Msg_Sq(msg, owner, bot, K, V):
    """স্কোয়াড মেসেজ"""
    fields = {
        1: 1,
        2: 2,
        2: {
            1: bot, 2: owner, 4: msg, 5: 1757799182, 7: 2,
            9: {
                1: "PLongDev", 2: await xBunnEr(), 3: 909000024, 4: 330,
                5: 909000024, 7: 2, 10: 1, 11: 1, 12: 0, 13: {1: 2},
                14: {
                    1: bot, 2: 8,
                    3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
                }
            },
            10: "ar", 13: {3: 1}, 14: ""
        }
    }
    proto_bytes = await CrEaTe_ProTo(fields)
    return await GeneRaTePk(proto_bytes.hex(), '1215', K, V)


async def ghost_packet(player_id, secret_code, K, V):
    """ঘোস্ট প্যাকেট (প্লেয়ার আইডি + সিক্রেট কোড)"""
    fields = {
        1: 61,
        2: {
            1: int(player_id),
            2: {
                1: int(player_id), 2: int(time.time()), 3: "PLongDev",
                5: 12, 6: 9999999, 7: 1,
                8: {2: 1, 3: 1}, 9: 3,
            },
            3: secret_code,
        },
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', K, V)


# ═══════════════════════════════════════════════════════════════
#              ★ মূল প্যাকেট জেনারেটর (RAFIN TxT) ★
# ═══════════════════════════════════════════════════════════════

async def GeneRaTePk(Pk, N, K, V):
    """প্যাকেট এনক্রিপ্ট + হেডার বসিয়ে ফাইনাল বাইট রিটার্ন"""
    PkEnc = await EnC_PacKeT(Pk, K, V)
    _ = await DecodE_HeX(int(len(PkEnc) // 2))
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
#                    ★ স্কোয়াড অপারেশন ★
# ═══════════════════════════════════════════════════════════════

async def CreateNewSquad(K, V, region):
    """নতুন স্কোয়াড তৈরি"""
    fields = {
        1: 1,
        2: {
            2: '011d', 3: 1, 4: 3, 5: 'ar',
            8: {1: 'IDC4', 2: 145, 3: 'ME'},
            9: 1,
            10: '01030407090a0b12191a201d2729',
            11: 1, 13: 1,
            14: {
                1: {6: 56},
                2: 731,
                3: '745d59541601024c01015f02020d0905030304570608570d57060d53540402025f5707545301060613050645775945454c18021c051e1a0306491a4760785c53477d735a53486073421b5d5841075642426f5c63610914084e1f005e721f6001467e0c51634263771f5f554642434556660104040f13050445636e74634379505365047256665e405459657766510f615a5250420d11084858416a0d7a470c720065655c5f5a0370584559584a457f43675f460c16024e477a4258430c6050417a45545c47786456597a7a7163545907714109160849667377607d0b4a07657c5c45045f5d784f5b5665096464065875620411050d4d7f7444766661406a6205545d5b5f74507e0b0b535c67580877607d0a1a0148761e795678487f7871465874697177534971666d5a7574677075550d17034503781a675e60787f4d406d7a625d57797d441b47057b026d1a685a0d1102044b0d60040d706067756547767d66777b7f46007346667e43065e5c780813074c5606764057727546596364037054674d590161467f73416209077108',
                4: 'w]ZP', 6: 11, 7: '140b7d71715b751011',
                8: '1.132.18', 9: 3, 10: 2,
                11: '0362625351363559382b505637416456324b796f566c6364724541566d46795954394b384445494d7a4b646d4b4231562f2b5a727577754a307847426c36712b38683863796b56447967524f4e3676493259347a646974684371364b73464d33724e534a4c4274594f3256565a5465786235484c324c39544a7652514c55374a525663696154544d46776e594e4b4c35353150336c5831475150635668615a77396251674b4d30395a4b6a2f4d675a38656d66757a6e4b356f5a6734367841626a7761363273366235636469637867386a6d4e4944594c383638686e756c3044316a4e445636444a4a69614758456154782b5450696c6f69476f58333638497234563266697a63783934436f5562735039765855683438356a626233356a717a5577504365554c55776374534574456d68426c3957453943524873422b76504a39704863323479517a70446c74644779536f6a6a4f573166433343413733374e617255546d734a70355431686b35635853307134557a6f7a6b75684b6d42423067354f4563634b627a68506c585943712f666a59767531624174504d766437486f4e6e39696e53767679796c6156386e315837636b7978384575626b5868414734565069425961556a75667a2b75675a474164356872324c3156615434613143485745702f6b446142364849434b756f705770706c703151373265463252744f62544957487775305a6753474659514266396f6e48744e7a5035336e72457072366f6c5349455354393839414f494858313471384d4a5763546d514267486d6c3456454c617354426d6f2b36764149525752783664617256692f345147566f4c785944593359477a366e513d3d'
            },
            19: 329, 21: '374f5219', 24: {1: 21}
        }
    }
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, K, V)


async def ChangeSquadTo5(uid, K, V, region):
    """স্কোয়াড সাইজ ৫ এ পরিবর্তন"""
    fields = {
        1: 17,
        2: {1: int(uid), 2: 1, 3: 4, 4: 1, 5: '011d', 8: 1}
    }
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, K, V)


async def SendInvite(target_uid, K, V, region):
    """প্লেয়ারকে স্কোয়াডে ইনভাইট"""
    fields = {
        1: 2,
        2: {1: int(target_uid), 2: 'ME', 4: 1}
    }
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, K, V)


# ─── সংক্ষিপ্ত অ্যালিয়াস (RAFIN TxT) ───
async def OpEnSq(K, V, region):
    return await CreateNewSquad(K, V, region)


async def cHSq(Nu, Uid, K, V, region):
    return await ChangeSquadTo5(Uid, K, V, region)


async def SEnd_InV(Nu, Uid, K, V, region):
    return await SendInvite(Uid, K, V, region)


async def ExiT(idT, K, V):
    """স্কোয়াড থেকে বের হওয়া"""
    fields = {1: 7, 2: {1: idT}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', K, V)


# ═══════════════════════════════════════════════════════════════
#              ★ টিম কোড দিয়ে স্কোয়াড জয়েন ★
# ═══════════════════════════════════════════════════════════════

async def JoinSquadByTeamCode(team_code, K, V, region):
    """টিম কোড দিয়ে সরাসরি স্কোয়াডে জয়েন"""
    hh = {
        1: 4,
        2: {
            4: "\u0001\u0007\t\n\u000b\u0012\u0019 '",
            5: str(team_code),
            6: 6, 8: 1,
            9: {
                1: "08FFF3BE903F27DF0203110111110000006B0003006800169194106F13CF106E4676251411010404dfe9e8b5ca3ca4f96a3119c00000004f03060301cacfa16d",
                2: 130,
                3: "tY_S\u0013\b\u0001M\u0002\u0000T\u0000\u0005\u000e\b\t\u0002\u0000\u0003U\u0003\u0001V\u000fR\u000e\tRQ\u0002\u0004\u0005US\u0003XS\u0005\u0001\u0002\u0011\u0001\u0002JuTAEN\u001e\u0002\u001c\u0002\u001f\u0013\b\u0003M\u001cDbz_Q@}p_QOgsC\u001dYVI\u0004UAAj_ga\u0004\u0012\u0000K\u001d\u0007_t\u0019b\bCx\u0002UeGat\u001fTTCBLER`\u0006\u0001\r\f\u0012\u0006\u0005N^^\u0002acH~r\u0004_\u0003RO|\u000bcd_@~`Rnqrgh\n\u0015\nL\\Nh\u0000~G\u000et\u0000eb]VQ\u0006t^F[ZIGxCdZD\u000b\u0011\u0002OA~LP@\u000fcSDyATQApaT^{|wa]\\\u0001E\u000f\u0013\nJfxve}\u0004J\u0003c{YL\u0007^^yDYQf\bhe\u0005_wg\r\u0010\u0007\bEHpX@||\u0002Z\\uTGyA\u0001JP\u0005t~VkTE\u0000J\\\u000b\u0013\nMr\u0018zTzK}qE]vnvwROuheYvwduvQ\r\u001a\u0005M\u0006z\u001dfXfzvHFc~dXUz}O\u001aB\u0005t\u0002i\u001co_\u0004\u0012\u0003\u0007J\u0006b\u0003\u000eqlfvbEstgu~wB\u0001v@`yI\u0002ZPx\f\u0014\u0003NR\u0002yBZvuD_cd\u0004q]lH]\u0007bD}pCe\t\u0004t\n",
                4: "w^_R", 6: 11, 7: "\u0014\u0004aqrg\u0015\u0013",
                8: "1.132.18", 9: 3, 10: 2,
                11: "\u0003bbSQ6wxegh9qAdV2KyoVleA17yPmYF+yTnOrl+JMknmppeUBe5ZsiHueP2mZZ4KOs6b2Ail1S9z3qIeU9hGFZ2M6PP39/zjIc/RFVPAkgDagySswMVmYaPhkzU5IqNPow2843fyQUz9xI10NdMhl1WiI4Y6wCXBotiUS9wSgujQ4j0fWXUyklCxBWo8r27hyoGSVrPdTPXFMnJJpPRRFFmWqc3fWvMg+BNfxSRJOZRSrkzG0nNvSIJ4uZB2pqAlHIPEYx7bI6zsgwUVDiLZJKTUTyuCGbOd1DegDUFfazFesTG1LJknT5WhgzCsrBIy+f2l+LeJe5DW7wEwNaHambM7ECXcJcLIhB9kJJsW0tFvXkk3HSdcQ8N1K6wjSKWhpkW0kV8Zrjj0jkhS/7AZ6T9GJRIA827YDtTorBvbx1UkXjYrqYI1nSa2GaMexGnqlurc5DE3v1R+mUBI9GqmjEPgTSYVBxyeCdQMHaMXGtspAhvkiO84ToU87sP45pylDEfFOVoc/rcmdzWeqlYPsv6txKRtIHcb0cO+MoVShoU8ZUVRDF3znbqzVrscPIfplBaa79lwvQqzRubLl9XY="
            },
            11: {1: "IDC4", 2: 281, 3: "ME"},
            13: "fr", 16: "7OR\u0019",
            20: "\b\u0015", 27: "\bH\u0010\u0003"
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(hh)).hex(), '0515', K, V)


# ═══════════════════════════════════════════════════════════════
#                ★ RAFIN TxT — END OF bot_core.py ★
# ═══════════════════════════════════════════════════════════════