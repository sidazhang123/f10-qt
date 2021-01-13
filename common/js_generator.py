import json


# load data by span id then run generated header and body js

class jsGen:
    def __init__(self, name):
        self.bodyjs = ''
        self.headerjs = ''
        self.header = ''
        self.body = ''
        self.conf = self.getConf(name)

    def getConf(self, name):
        with open(f'pages/{name}/conf/{name}.json', encoding="utf-8") as json_file:
            return json.load(json_file)[name]

    def addHeader(self):

        for h in self.conf[:3]:
            if h['display']:

                self.header += f'''<span id="{h['class']}" style="font-size:{h['font_size']}px;font-weight:{'bold' if h['bold'] else ''};background-color:{h['bg_color']}"></span>'''
                if h['tag'] == 'date':
                    self.headerjs += f'''$("#{h['class']}").text(function(){{ return $(this).text().slice({h['format']}); }});'''

    def addBody(self):

        self.body = ''
        for i in range(0, 64, 8):
            label = ''
            js = ''
            row = ''
            for j in range(i, i + 8):  # every row
                h = self.conf[3:][j]
                if len(h) > 1:  # skip blank
                    if 'class' in h:
                        if h['class'] == 'label':
                            label = f'''<td><span style="font-size:{h['font_size']}px;font-weight:{'bold' if h['bold'] else ''};background-color:{h['bg_color']}">{h['text']}</span></td>'''
                        else:  # data to render
                            if h['tag'] == 'num':
                                id = h['class'] + '@'
                                row += f'''<span id="{id}" style="font-size:{h['font_size']}px;font-weight:{'bold' if h['bold'] else ''};background-color:{h['bg_color']}"></span>'''
                                js += f'''$("#{id}").text(function () {{let num = parseFloat($(this).text());let threshold = {h['threshold']}; let cond = '{h['cond']}';if (num && threshold) {{if ((cond === 'gte' && num >= threshold) || (cond === 'lt' && num < threshold)) {{$(this).css('color', '{h['font_color']}');}}}}}});'''
                            elif h['tag'] == 'date':
                                id = h['class'] + '@'
                                row += f'''<span id="{id}" style="font-size:{h['font_size']}px;font-weight:{'bold' if h['bold'] else ''};background-color:{h['bg_color']}"></span>'''
                                js += f'''$("#{id}").text(function(){{ return $(this).text().slice({h['format']}); }});'''
                            else:
                                row += f'''<span id="{h['class'] + '@'}" style="font-size:{h['font_size']}px;font-weight:{'bold' if h['bold'] else ''};background-color:{h['bg_color']}"></span>'''
                    else:
                        row += f'''<span style="font-size:{h['font_size']}px;font-weight:{'bold' if h['bold'] else ''};background-color:{h['bg_color']}">{h['text']}</span>'''
            self.body += '<tr>' + label

            for col in range(3):
                self.body += '<td style="border: 1px solid #000">' + row.replace('@', str(col)) + '</td>'
                self.bodyjs += js.replace('@', str(col))

            self.body += '</tr>'


if __name__ == '__main__':
    j = jsGen('f10')
    j.addBody()
    j.addHeader()
    print(j.body)
    print(j.bodyjs)
    print(j.headerjs)
