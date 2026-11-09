# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════
#   ██████╗  █████╗ ███████╗██╗███╗   ██╗    ████████╗██╗  ██╗████████╗
#   ██╔══██╗██╔══██╗██╔════╝██║████╗  ██║    ╚══██╔══╝╚██╗██╔╝╚══██╔══╝
#   ██████╔╝███████║█████╗  ██║██╔██╗ ██║       ██║    ╚███╔╝    ██║
#   ██╔══██╗██╔══██║██╔══╝  ██║██║╚██╗██║       ██║    ██╔██╗    ██║
#   ██║  ██║██║  ██║██║     ██║██║ ╚████║       ██║   ██╔╝ ██╗   ██║
#   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═══╝       ╚═╝   ╚═╝  ╚═╝   ╚═╝
#
#       ★ RemoveFriend_Req.proto — RAFIN TxT EDITION ★
#       ▌ স্বয়ংক্রিয়ভাবে তৈরি Protobuf মডিউল ▌
#       ▌ Free Fire — বন্ধু মুছে ফেলার রিকোয়েস্ট ▌
# ═══════════════════════════════════════════════════════════════
#
#  ▸ সোর্স ফাইল  : RemoveFriend_Req.proto
#  ▸ Protobuf ভার্সন : 4.25.1
#  ▸ ব্র্যান্ডিং    : RAFIN TxT
#
#  ⚠ সতর্কতা : এই ফাইলটি অটো-জেনারেটেড — হাতে এডিট করবেন না।
#              আসল descriptor byte data হুবহু রাখা হয়েছে।
# ═══════════════════════════════════════════════════════════════

"""Generated protocol buffer code — RAFIN TxT Edition."""

# ─── Protobuf কোর ইমপোর্ট ───
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)


# ═══════════════════════════════════════════════════════════════
#              ★ সিম্বল ডেটাবেস ইনিশিয়ালাইজ ★
# ═══════════════════════════════════════════════════════════════

_sym_db = _symbol_database.Default()


# ═══════════════════════════════════════════════════════════════
#        ★ Descriptor সংজ্ঞা (RemoveFriend মেসেজ) ★
# ═══════════════════════════════════════════════════════════════
#
#  মেসেজ কাঠামো :
#  ┌─────────────────────────────────────────┐
#  │  RemoveFriend                           │
#  ├─────────────────────────────────────────┤
#  │  AuthorUid  : int64  (field 1)          │
#  │  TargetUid  : int64  (field 2)          │
#  └─────────────────────────────────────────┘
#
#  AuthorUid → যে বন্ধু মুছবে তার UID
#  TargetUid → যে বন্ধুকে মুছে ফেলা হবে তার UID
# ═══════════════════════════════════════════════════════════════

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x16RemoveFriend_Req.proto'
    b'\"4\n\x0cRemoveFriend'
    b'\x12\x11\n\tAuthorUid\x18\x01 \x01(\x03'
    b'\x12\x11\n\tTargetUid\x18\x02 \x01(\x03'
    b'b\x06proto3'
)


# ═══════════════════════════════════════════════════════════════
#              ★ মেসেজ ও এনাম বিল্ডার (RAFIN TxT) ★
# ═══════════════════════════════════════════════════════════════

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'RemoveFriend_Req_pb2', _globals)


# ═══════════════════════════════════════════════════════════════
#              ★ C-Descriptor সাপোর্ট চেক ★
# ═══════════════════════════════════════════════════════════════

if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None

    # RemoveFriend মেসেজের serialized range সেট করা
    _globals['_REMOVEFRIEND']._serialized_start = 26
    _globals['_REMOVEFRIEND']._serialized_end   = 78


# @@protoc_insertion_point(module_scope)


# ═══════════════════════════════════════════════════════════════
#                    ★ RAFIN TxT — END OF FILE ★
# ═══════════════════════════════════════════════════════════════