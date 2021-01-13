import json


def makeStyle(conf):
    d = {"bold": False, "bg_color": "#FFFFFF", "font_size": "14", "display": True}
    for k in d:
        if k in conf:
            d[k] = conf[k]
    return 'style="font-weight:{}; {}; font-size:{}px; background-color:{};"'.format(
        "bold" if d['bold'] else "normal", "" if d['display'] else "display:none", d['font_size'], d['bg_color'])


def makeEle(item, tag="td", colspan=1):
    if "tag" in item and item["tag"] == "blank": return ""
    style = makeStyle(item)
    vhtml = ""
    if "class" in item and item["class"] != "label" and "tag" in item:
        if item["tag"] == "date":
            con = '{{{{getDate("{:}",t,{:})}}}}'.format(item["class"], int(item["format"]))
        elif item["tag"] == "num":
            con = '<span v-html="getNum(\'{:}\',t,{:},\'{:}\',\'{:}\')"></span>'.format(item["class"],
                                                                                        float(item["threshold"]),
                                                                                        item["cond"],
                                                                                        item["font_color"])
        else:
            vhtml = 'v-html="highlight(getVal(\'{}\',t))"'.format(item["class"])
            con = ""
    else:
        con = ""
    return "<{} {} class=\"mono\" colspan=\"{}\" {}>{}</{}>".format(tag, style, colspan, vhtml, con, tag)


def _makeEle(item, tag="div"):
    if "tag" in item and item["tag"] == "blank": return ""
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


def makeGrid(eleList, rowCap=4):
    c = 0
    s = ""
    t = ""
    for e in eleList:

        t += e
        c += 1
        if c % rowCap == 0:
            s += "<tr >{}</tr>\n".format(t)
            t = ""

    return s


def makeHeader(headerList):
    return ''.join(headerList)


def genF10bTemp():
    import re
    a = json.loads(open('pages/f10b_shareholder/conf/f10b_shareholder.json'.format(), 'r', encoding='utf-8-sig').read())[
        "f10b_shareholder"]
    eleList = [makeEle(i, colspan=4) if "class" in i and i["class"] == "tableString" else makeEle(i) for i in a[3:]]
    headerList = [_makeEle(i) for i in a[:3]]

    to_replace = '''<template><div class="center"><div class="row">{}</div>
    <div class="row">
    <table class="tab" v-for="(n, t) in 5">{}
    </table></div></div></template>'''.format(makeHeader(headerList), makeGrid(eleList))
    print(to_replace)
    with open('pages/f10b_shareholder/f10b_shareholder.html'.format(), "r", encoding='utf-8-sig') as fin:
        t = re.sub('<template>[\s\S]*</template>', to_replace, fin.read())

    with open('pages/f10b_shareholder/f10b_shareholder.html'.format(), "w", encoding='utf-8-sig') as fout:
        fout.write(t)

# genF10bTemp()
