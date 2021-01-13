import json


def makeStyle(conf):
    d = {"bold": False, "bg_color": "#FFFFFF", "font_size": "14", "display": True}
    for k in d:
        if k in conf:
            d[k] = conf[k]
    return 'style="font-weight:{}; display:{}; font-size:{}px; background-color:{};"'.format(
        "bold" if d['bold'] else "normal", "inline" if d['display'] else "none", d['font_size'], d['bg_color'])


def makeEle(item, tag="td"):
    style = makeStyle(item)
    vif = "v-if='getVal(\"{:}\",t).length>0'".format(item["check_fn"]) if "check_fn" in item else ""
    vhtml,con="",""
    if "class" in item and item["class"] != "label" and "tag" in item:
        if item["tag"] == "date":
            con = '{{{{getDate("{:}",t,{:})}}}}'.format(item["class"], int(item["format"]))
        elif item["tag"] == "num":
            vhtml = 'v-html="getNum(\'{:}\',t,{:},\'{:}\',\'{:}\')"'.format(item["class"],
                                                                                        float(item["threshold"]),
                                                                                        item["cond"],
                                                                                        item["font_color"])
        else:
            vhtml = "v-html='highlight(getVal(\"{}\",t))'".format(item["class"])
    elif "text" in item:
        con = item["text"]

    return "<{} {} {}>{}</{}>".format(tag, style,vhtml, con, tag), vif


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


def makeGrid(eleList, rowCap=13):
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


def genF10aTemp():
    import re
    a = json.loads(open('pages/f10a_supplement/conf/f10a_supplement.json'.format(), 'r', encoding='utf-8-sig').read())["f10a_supplement"]
    eleList = [makeEle(i) for i in a[3:]]
    headerList = [_makeEle(i) for i in a[:3]]

    to_replace = '''<template><div class="center"><div class="row">{}</div>
    <div class="row">
    <table class="tab" v-for="(n, t) in 5">{}
    </table></div></div></template>'''.format(makeHeader(headerList), makeGrid(eleList))
    print(to_replace)
    with open('pages/f10a_supplement/f10a_supplement.html'.format(), "r", encoding='utf-8-sig') as fin:
        t = re.sub('<template>[\s\S]*</template>', to_replace, fin.read())

    with open('pages/f10a_supplement/f10a_supplement.html'.format(), "w", encoding='utf-8-sig') as fout:
        fout.write(t)

# genF10aTemp()
