from PyQt5.QtCore import QDir, QUrl


def loadTop(html, path):
    src = "<head>"
    for i in path:
        local = QUrl.fromLocalFile(QDir.current().filePath(i)).toString()
        if i.endswith(".js"):
            src += '<script src="' + local + '"></script>\n'
        elif i.endswith(".css"):
            src += '<link rel="stylesheet" href="' + local + '">\n'
    return html.replace("<head>", src)


def loadBot(html, path):
    src = "</body>"
    for i in path:
        local = QUrl.fromLocalFile(QDir.current().filePath(i)).toString()
        if i.endswith(".js"):
            src = '\n<script src="' + local + '"></script>' + src
        elif i.endswith(".css"):
            src = '\n<link rel="stylesheet" href="' + local + '">' + src
    return html.replace("</body>", src)


def loadF10Conf():
    html = open('pages/f10/f10_conf.html', 'r', encoding="utf8").read()
    return loadBot(
        loadTop(html, ["pages/css/bootstrap.min.css", "pages/js/jquery-3.4.1-slim.min.js", "pages/js/popper.min.js",
                       "pages/js/bootstrap.min.js", "pages/css/bootstrap-colorpicker.min.css",
                       "pages/js/draggable.js", "pages/js/qwebchannel.js", "pages/js/bootstrap-colorpicker.min.js",
                       "pages/f10/conf/conf_helper.js"]),
        ["pages/js/common_bot.js", "pages/f10/context.js"])


def loadF10aSupplementConf():
    html = open('pages/f10a_supplement/f10a_supplement_conf.html', 'r', encoding="utf8").read()
    return loadBot(
        loadTop(html, ["pages/css/bootstrap.min.css", "pages/js/jquery-3.4.1-slim.min.js", "pages/js/popper.min.js",
                       "pages/js/bootstrap.min.js", "pages/css/bootstrap-colorpicker.min.css",
                       "pages/js/draggable.js", "pages/js/qwebchannel.js", "pages/js/bootstrap-colorpicker.min.js",
                       "pages/f10a_supplement/conf/conf_helper.js"]),
        ["pages/js/common_bot.js", "pages/f10a_supplement/context.js"])


def loadF10bShareholderConf():
    html = open('pages/f10b_shareholder/f10b_shareholder_conf.html', 'r', encoding="utf8").read()
    return loadBot(
        loadTop(html, ["pages/css/bootstrap.min.css", "pages/js/jquery-3.4.1-slim.min.js", "pages/js/popper.min.js",
                       "pages/js/bootstrap.min.js", "pages/css/bootstrap-colorpicker.min.css",
                       "pages/js/draggable.js", "pages/js/qwebchannel.js", "pages/js/bootstrap-colorpicker.min.js",
                       "pages/f10b_shareholder/conf/conf_helper.js"]),
        ["pages/js/common_bot.js", "pages/f10b_shareholder/context.js"])


def loadF12Finance():
    html = open('pages/f12_finance/f12_finance_conf.html', 'r', encoding="utf8").read()
    return loadBot(
        loadTop(html, ["pages/css/bootstrap.min.css", "pages/js/jquery-3.4.1-slim.min.js", "pages/js/popper.min.js",
                       "pages/js/bootstrap.min.js", "pages/css/bootstrap-colorpicker.min.css",
                       "pages/js/draggable.js", "pages/js/qwebchannel.js", "pages/js/bootstrap-colorpicker.min.js",
                       "pages/f12_finance/conf/conf_helper.js", "pages/css/bootstrap4-toggle.min.css",
                       "pages/js/bootstrap4-toggle.min.js",
                       "pages/css/bootstrap4-datepicker.css", "pages/js/bootstrap4-datepicker.js"]),
        ["pages/js/common_bot.js", "pages/f12_finance/context.js"])


def loadF11IndustryConf():
    html = open('pages/f11_industry/f11_industry_conf.html', 'r', encoding="utf8").read()
    return loadBot(
        loadTop(html, ["pages/css/bootstrap.min.css", "pages/js/jquery-3.4.1-slim.min.js", "pages/js/popper.min.js",
                       "pages/js/bootstrap.min.js", "pages/css/bootstrap-colorpicker.min.css",
                       "pages/js/qwebchannel.js", "pages/js/bootstrap-colorpicker.min.js",
                       "pages/f11_industry/conf/conf_helper.js", "pages/css/bootstrap4-toggle.min.css",
                       "pages/js/bootstrap4-toggle.min.js",
                       "pages/css/bootstrap4-datepicker.css", "pages/js/bootstrap4-datepicker.js"]),
        ["pages/js/common_bot.js", "pages/f11_industry/context.js"])


def loadMain(boss):
    html = open('pages/home/home.html', 'r', encoding="utf8").read()
    r = loadBot(
        loadTop(html, ["pages/css/bootstrap.min.css", "pages/js/jquery-3.4.1-slim.min.js", "pages/js/popper.min.js",
                       "pages/js/bootstrap.min.js", "pages/js/qwebchannel.js", "pages/css/bootstrap-select.min.css",
                       "pages/js/bootstrap-select.min.js"]),
        ["pages/js/common_bot.js"])

    from re import sub
    r = sub("<label class=\"label label-primary font-weight-bold\"[\s\S]*?</label>", ''''<label class="label label-primary font-weight-bold" for="boss" style="font-size: 16px;"><input
                        class="form-check-input" id="boss" type="checkbox" checked> BOSS </label>''',
            r) if boss else sub("<label class=\"label label-primary font-weight-bold\"[\s\S]*?</label>", ''''<label class="label label-primary font-weight-bold" for="boss" style="font-size: 16px;"><input
                        class="form-check-input" id="boss" type="checkbox"> BOSS </label>''', r)
    return r


def loadReprPage(data, win):
    path = 'pages/{}/{}.html'.format(win, win)
    print(path)
    print(data)
    html = open(path, 'r', encoding="utf8").read()
    html = loadBot(loadTop(html, ["pages/css/bootstrap.min.css",
                                  "pages/js/vue.js", "pages/js/qwebchannel.js"]), ["pages/js/common_bot.js"])
    html = html.replace("</body>", "<script>vm.items={}</script></body>".format(data))
    return html
