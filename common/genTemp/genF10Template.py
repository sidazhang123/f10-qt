import json


def makeStyle(conf):
    d = {"bold": False, "bg_color": "#FFFFFF", "font_size": "14", "display": True}
    for k in d:
        if k in conf:
            d[k] = conf[k]
    whitespace=""
    if "class" in conf and conf["class"] in {"质押股东","股东控股"}:
        whitespace="white-space:pre-wrap;"
    return 'style="font-weight:{}; display:{}; font-size:{}px; background-color:{};{}"'.format(
        "bold" if d['bold'] else "normal", "inline" if d['display'] else "none", d['font_size'], d['bg_color'],whitespace)


def makeEle(item, tag="td"):
    style = makeStyle(item)
    vif = "v-if='getVal(\"{:}\",t).length>0'".format(item["check_fn"]) if "check_fn" in item else ""
    if "class" in item and item["class"] != "label" and "tag" in item:
        if item["tag"] == "date":
            con = '{{{{getDate("{:}",t,{:})}}}}'.format(item["class"], int(item["format"]))
        elif item["tag"] == "num":
            con = '<span v-html="getNum(\'{:}\',t,{:},\'{:}\',\'{:}\')"></span>'.format(item["class"],
                                                                                        float(item["threshold"]),
                                                                                        item["cond"],
                                                                                        item["font_color"])
        else:
            con = '{{{{getVal("{:}",t)}}}}'.format(item["class"])
    elif "text" in item:
        con = item["text"]
    else:
        con = ""
    return "<{} {}>{}</{}>".format(tag, style, con, tag), vif


def _makeEle(item, tag="div"):
    style = makeStyle(item)
    if "class" in item and item["class"] != "label" and "tag" in item:
        if item["tag"] == "date":
            con = '{{{{_getDate("{:}",{:})}}}}'.format(item["class"], int(item["format"]))
        else:
            con = '{{{{_getVal("{:}")}}}}'.format(item["class"])
    elif "text" in item:
        con = item["text"]
    else:
        con = ""
    return "<{} class=\"m-2 header-in-line\" {}>{}</{}>".format(tag, style, con, tag)


def makeGrid(eleList, rowCap=8):
    c = 0
    s = ""
    t = ""
    vif = ""
    for e, _vif in eleList:
        if len(_vif) > 0: vif = _vif
        t += e
        c += 1
        if c % rowCap == 0:
            s += "<tr {}>{}</tr>\n".format(vif, t)
            t = ""
            vif = ""
    return s


def makeHeader(headerList):
    return ''.join(headerList)


def genF10Temp():
    import re
    a = json.loads(open('pages/f10/conf/f10.json'.format(), 'r', encoding='utf-8-sig').read())["f10"]
    eleList = [makeEle(i) for i in a[3:]]
    headerList = [_makeEle(i) for i in a[:3]]

    to_replace = '''<template><div class="center"><div class="row">{}</div>
    <div class="row">
    <table class="tab" v-for="(n, t) in 5">{}
    </table></div></div></template>'''.format(makeHeader(headerList), makeGrid(eleList))
    print(to_replace)
    with open('pages/f10/f10.html'.format(), "r", encoding='utf-8-sig') as fin:
        t = re.sub('<template>[\s\S]*</template>', to_replace, fin.read())

    with open('pages/f10/f10.html'.format(), "w", encoding='utf-8-sig') as fout:
        fout.write(t)

# genF10Temp()
