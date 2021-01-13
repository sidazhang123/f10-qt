import configparser,json,re,pymongo
from os import path
from sshtunnel import SSHTunnelForwarder


class Db:
    def __init__(self):
        self._server = SSHTunnelForwarder(
            "",
            ssh_username="",
            ssh_password="",
            remote_bind_address=('127.0.0.1', 27017)
        )
        self._server.start()
        self._client = pymongo.MongoClient(
            "mongodb://{}:{}@{}:{}".format("", "", "127.0.0.1", self._server.local_bind_port))

    def get(self): return self._client

    def close(self): return [self._client.close(), self._server.close()]


class F10b:
    def __init__(self, client):
        self.vips = list()

        col = client.get_database("").get_collection("rules")
        cur = col.find({"channel": "", "tarCol": ""},
                       {"_id": 0, "cond2": 0, "key": 0, "channel": 0, "tarCol": 0})
        for doc in cur:
            for i in doc['cond1']:
                i = i.strip()
                if len(i) > 0:
                    self.vips.append(i)
            self.vips.append('')

    def exportVips2File(self):
        from itertools import chain
        from pypinyin import pinyin, Style
        def to_pinyin(s):
            return ''.join(chain.from_iterable(pinyin(s, style=Style.TONE3)))

        with open('', 'w') as f:
            for i in sorted(self.vips, key=to_pinyin):
                if 0 < len(i) < 5:
                    f.write(i + '\n')
        with open('', 'w') as f:
            for i in self.vips:
                if 0 < len(i) < 5:
                    f.write(i + '\n')
                elif len(i) == 0:
                    f.write('===================\n')

    def writeContextQuery(self, jsPath="pages/f10b_shareholder/context.js"):
        vips = list(set(self.vips))
        vips.remove('')
        with open(jsPath, "w", encoding='utf-8-sig') as f:
            f.write("this.query=[{}]".format(','.join(vips)))


class F10A:
    def __init__(self, client):
        self.conf = []
        self.cfg(client)

    def cfg(self, client):
        cfn = ''
        if not path.exists(cfn):
            return False
        config = configparser.RawConfigParser()
        config.read_file(open(cfn, "r", encoding="utf-8-sig"))
        for segment in config.items():
            if segment[0] == "DEFAULT":
                continue
            elif segment[0] == "AppRule":
                col = client.get_database("").get_collection("rules")
                cur = col.find({"tarCol": "latest_tips"})
                for doc in cur:
                    self.conf.append({"color": segment[1]["color"],
                                      "bgcolor": segment[1]["bgcolor"],
                                      "incl": [i for i in doc['cond1'] if i is not None] if doc[
                                                                                                'cond1'] is not None else [],
                                      "excl": [i for i in doc['cond2'] if i is not None] if doc[
                                                                                                'cond2'] is not None else []})
            else:
                self.conf.append({"incl": [i for i in segment[1]["include"].split("/") if i],
                                  "excl": [i for i in segment[1]["exclude"].split("/") if i],
                                  "color": segment[1]["color"],
                                  "bgcolor": segment[1]["bgcolor"], })

    def writeContextQuery(self, jsPath="pages/f10a_supplement/context.js"):
        with open(jsPath, "w", encoding='utf-8-sig') as f:
            f.write("this.query={}".format(json.dumps(self.conf, ensure_ascii=False)))


class F12:
    def __init__(self,notify_console_fn):
        self.notify_console_fn=notify_console_fn
        cfn = ''
        if not path.exists(cfn):
            notify_console_fn("'")
            return
        config = configparser.RawConfigParser()
        config.read_file(open(cfn, "r", encoding="utf-8-sig"))
        self.conf = []
        for i in config.items():
            if i[0] not in {"DEFAULT"}:

                self.conf.append({'': [*self.splitThreshold(i[1]['']), float(i[1]['']),
                                         *self.splitThreshold(i[1][''])],
                             '': [*self.splitThreshold(i[1]['']), float(i[1]['']),
                                        *self.splitThreshold(i[1][''])]})

    def writeContextQuery(self, jsPath="pages/f12_finance/context.js"):
        with open(jsPath, "w", encoding='utf-8-sig') as f:
            f.write("this.query={}".format(json.dumps(self.conf, ensure_ascii=False)))

    def splitThreshold(self, s):
        try:
            s = s.split('/')
            if len(s) != 2:
                raise Exception
            t = []
            for i in s:
                i = i.strip()
                if len(i) == 0:
                    t.append(float("inf"))
                else:
                    t.append(float(i))
            return max(t) if float("inf") != max(t) else "inf", min(t)
        except Exception as e:
            self.notify_console_fn(str(e))

def apply_strat(notify_console_fn):
    db = Db()
    notify_console_fn("making alert msg f10b")
    f10b = F10b(db.get())
    f10b.exportVips2File()
    f10b.writeContextQuery()
    notify_console_fn("making alert msg f12")

    f12 = F12(notify_console_fn)
    f12.writeContextQuery()

    notify_console_fn("making alert msg f10a")
    f10a = F10A(db.get())
    if len(f10a.conf) == 0:
        notify_console_fn("")
    f10a.writeContextQuery()
    notify_console_fn("making alert msg accomplished")
    db.close()
