import json
import zlib
import base64
import cbor2  # type: ignore
import cose.algorithms  # type: ignore
import cose.keys.curves  # type: ignore
import cose.keys.keytype  # type: ignore
import requests


def valueSetFormatter(valuesets):
    for x in valuesets["v"]:
        x["v"] = json.loads(x["v"])
    return valuesets


def rulesFormatter(rules):
    for x in rules["r"]:
        x["r"] = json.loads(x["r"])
    return rules


def trustlistFormatter(trustlist):
    for x in trustlist["c"]:
        x["i"] = base64.b64encode(x["i"]).decode('utf-8')
        x["c"] = base64.b64encode(x["c"]).decode('utf-8')
    return trustlist


items = [
    {'name': "trustlist", 'formatter': trustlistFormatter},
    {'name': "rules", 'formatter': rulesFormatter},
    {'name': "valuesets", 'formatter': valueSetFormatter},
]

obj = {}

for i in items:
    response = requests.get("https://dgc-trust.qr.gv.at/" + i['name'])
    if not response.ok:
        print("Download failed: status code {}\n{}".format(
            response.status_code, response.text))
        exit

    cbor = cbor2.loads(response.content)

    obj[i['name']] = i['formatter'](cbor)

    with open(f"output/{i['name']}.json", "w") as outfile:
        json.dump(obj[i['name']], outfile, indent=4)

with open(f"output/rules-AT-BG.json", "w") as outfile:

   json.dump([o['r'] for o in obj['rules']['r']
             if o['r']['Country'] == 'AT' and o['r']['Region'] == 'BG'], outfile, indent=4)
