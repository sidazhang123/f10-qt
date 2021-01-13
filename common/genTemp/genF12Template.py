import json


def makeStyle(conf):
    d = {"bold": False, "bg_color": "#FFFFFF", "font_size": "14", "display": True}
    for k in d:
        if k in conf:
            d[k] = conf[k]
    return 'style="font-weight:{}; {}; font-size:{}px; background-color:{};"'.format(
        "bold" if d['bold'] else "normal", "" if d['display'] else "display:none", d['font_size'], d['bg_color'])


def makeDateHeader(item, tab, tag="th"):
    style = makeStyle(item)
    vfor = "v-for='date in ordered_sliced_datesY'" if tab == "YTab" else "v-for='date in ordered_sliced_datesQ'"
    con = '{{date.slice(' + str(int(item["format"])) + ')}}'
    return '<thead><tr><th {}></th><{} {} {}>{}</{}></tr></thead>'.format(style, tag, style, vfor, con, tag)


def makeEle(item, tab, tag="td"):
    style = makeStyle(item)
    vfor = "v-for='date in ordered_sliced_datesY'" if tab == "YTab" else "v-for='date in ordered_sliced_datesQ'"
    vif = "v-if='checkVal(\"{:}\",\"{:}\")'".format(tab, item["check_fn"]) if "check_fn" in item else ""
    vhtml = ""
    if "class" in item and item["class"] != "label" and "tag" in item:
        if item["tag"] == "num":
            vhtml = 'v-html="getNum(\'{:}\',\'{:}\',date,{:},\'{:}\',\'{:}\')"'.format(tab,
                                                                                       item["class"],
                                                                                       float(item[
                                                                                                 "threshold"]),
                                                                                       item["cond"],
                                                                                       item["font_color"])
            con = ""
        else:
            con = '{{{{getVal("{:}","{:}",date)}}}}'.format(tab, item["class"])
    elif "text" in item:
        con = item["text"]
        vfor = ""
    else:
        return None

    return "<{} {} {} {}>{}</{}>".format(tag, vhtml, vfor, style, con, tag), vif


def makeGrid(eleList, rowCap=2):
    c = 0
    s = ""
    t = ""
    vif = ""
    for ele in eleList:
        if not ele: continue
        e, _vif = ele
        if len(_vif) > 0: vif = _vif
        t += e
        c += 1
        if c % rowCap == 0:
            s += "<tr {}>{}</tr>\n".format(vif, t)
            t = ""
            vif = ""
    return "<tbody>" + s + "</tbody>"


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


def genF12Temp():
    import re
    a = json.loads(open('pages/f12_finance/conf/f12_finance.json'.format(), 'r', encoding='utf-8-sig').read())[
        "f12_finance"]
    headerList = [_makeEle(i) for i in a[:3]]

    YGrid, QGrid = makeDateHeader(a[3], "YTab") + makeGrid([makeEle(i, "YTab") for i in a[4:]]), makeDateHeader(a[3],
                                                                                                                "QTab") + makeGrid(
        [makeEle(i, "QTab") for i in a[4:]])

    order, start, end = "true" if a[3]["ordering"] else "false", a[3]["date_start"], a[3][
        "date_end"]
    js_to_replace = '''<script tag="preset-params">
    let start="{}",end="{}",ordering="{}";
</script>'''.format(start, end, order)
    temp_to_replace = '''<template><div class="center"><div class="row">{}</div>
    <div class="row">
    <table class="table table-bordered" style="border:2px solid blue;">{}</table>
    <table class="table table-bordered">{}</table>
    </div></div></template>'''.format(makeHeader(headerList), YGrid, QGrid)
    # print(js_to_replace)
    # print(temp_to_replace)
    with open('pages/f12_finance/f12_finance.html'.format(), "r", encoding='utf-8-sig') as fin:
        t = re.sub('<template>[\s\S]*</template>', temp_to_replace, fin.read())
        t = re.sub('<script tag="preset-params">[\s\S]*?</script>', js_to_replace, t)

    with open('pages/f12_finance/f12_finance.html'.format(), "w", encoding='utf-8-sig') as fout:
        fout.write(t)

# genF12Temp()
