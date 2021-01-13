import json


def makeStyle(conf):
    d = {"bold": False, "bg_color": "#FFFFFF", "font_size": "14", "display": True}
    for k in d:
        if k in conf:
            d[k] = conf[k]
    return 'style="font-weight:{}; display:{}; font-size:{}px; background-color:{};"'.format(
        "bold" if d['bold'] else "normal", "inline" if d['display'] else "none", d['font_size'], d['bg_color'])


def makeEle(item, tag="span"):
    if "tag" in item and item["tag"] == "blank": return ""
    style = makeStyle(item)
    return "<{} {} class=\"mono\">{{{{i}}}}</{}>".format(tag, style,  tag)


def _makeEle(item, tag="div"):
    if "tag" in item and item["tag"] == "blank": return ""
    style = makeStyle(item)
    if "class" in item and item["class"] != "label" and "tag" in item:
        if item["tag"] in {"date", "date-header"}:
            con = '{{{{_getDate("{:}",{:})}}}}'.format(item["class"], int(item["format"]))
        else:
            con = '{{{{_getVal("{:}")}}}}'.format(item["class"])
    elif "text" in item:
        con = item["text"]
    else:
        con = ""
    return "<{} class=\"m-2 header-in-line\" {}>{}</{}>".format(tag, style, con, tag)



def makeHeader(headerList):
    return ''.join(headerList)


def genF11Temp():
    import re
    a = json.loads(open('pages/f11_industry/conf/f11_industry.json'.format(), 'r', encoding='utf-8-sig').read())[
        "f11_industry"]
    headerList = [_makeEle(i) for i in a[:3]]

    to_replace = '''<template><div class="center"><div class="row">{}</div>
    <div class="row">
    <div class="tab" v-for="i in this.filter('{}','{}',{})">{}
    </div></div></div></template>'''.format(makeHeader(headerList), a[-1]["date_start"], a[-1]["date_end"], "true" if a[-1]["ordering"] else "false",makeEle(a[-1]))

    with open('pages/f11_industry/f11_industry.html'.format(), "r", encoding='utf-8-sig') as fin:
        t = re.sub('<template>[\s\S]*</template>', to_replace, fin.read())

    with open('pages/f11_industry/f11_industry.html'.format(), "w", encoding='utf-8-sig') as fout:
        fout.write(t)


# genF11Temp()
