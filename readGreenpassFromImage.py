from pyzbar.pyzbar import decode
import sys
import cbor2
import base45
import zlib
import json
from cose.messages import CoseMessage, Sign1Message  # type: ignore
from PIL import Image

if len(sys.argv) != 2:
    print("Usage: {} <image>".format(sys.argv[0]))
    exit(1)

decoded = decode(Image.open(sys.argv[1]))[0].data.decode()

compressed = base45.b45decode(decoded[4:])
cose = zlib.decompress(compressed)

msg = CoseMessage.decode(cose)

obj = cbor2.loads(msg.payload)

print(json.dumps(obj, indent=4))
