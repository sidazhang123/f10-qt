function setTileDbclickListener() {
    $(".block").dblclick(function () {

        let tileId = $(this).attr('id');
        setModalAttr(tileId);
    });
}

function setModalAttr(id) {
    let liConf = confList[id];
    let modal = $(`#${liConf['tag']}Modal`);
    for (const [key, value] of Object.entries(liConf)) {
        let inp = modal.find("." + key);
        if (typeof value === "boolean") {
            inp.prop("checked", value);
        } else {
            inp.val(value);
            if (key === "text" && (["date", "name", "code", "date"].includes(liConf["class"]))) {
                inp.prop('disabled', true);
            } else {
                inp.prop('disabled', false);
            }
        }
        inp.change();
    }
    modal.find(".tileId").val(id)
    modal.modal('show');
}

function initBox() {
    backend.getConf('f10b_shareholder', setBoxChildren);
}

function setBoxChildren(l) {
    confList = l;
    for (let i = 2; i > -1; i--) {
        let p = confList[i];
        switch (p['tag']) {
            case 'text':
                $('.row-header').prepend(`<div id="${i}" tag="text" style="font-size:${p['font_size']}px;font-weight: ${p['bold'] ? 'bold' : ''};background-color:${p['bg_color']}" class="block">${p['display'] ? p['text'] : ''}</div>`);
                break;
            case 'date':
                $('.row-header').prepend(`<li id="${i}" tag="date" style="font-size:${p['font_size']}px;font-weight: ${p['bold'] ? 'bold' : ''};background-color:${p['bg_color']}" class="block">${p['display'] ? p['text'].slice(p['format']) : ''}</li>`);
                break;
        }
    }
    let box = $("#dragBox");
    for (let i = 3; i < confList.length; i++) {
        let p = confList[i];
        switch (p['tag']) {
            case 'blank':
                box.append(`<li id="${i}" tag="blank" class="block"></li>`);
                break;
            case 'text':
                box.append(`<li id="${i}" tag="text" style="font-size:${p['font_size']}px;font-weight: ${p['bold'] ? 'bold' : ''};background-color:${p['bg_color']}" class="block">${p['display'] ? p['text'] : ''}</li>`);
                break;
            case 'date':
                box.append(`<li id="${i}" tag="date" style="font-size:${p['font_size']}px;font-weight: ${p['bold'] ? 'bold' : ''};background-color:${p['bg_color']}" class="block">${p['display'] ? p['text'].slice(p['format']) : ''}</li>`);
                break;
            case 'num':
                let num = parseFloat(p['text']);
                let threshold = parseFloat(p['threshold']);
                let color = "";
                if (num && threshold) {
                    if ((p['cond'] === 'gte' && num >= threshold) || (p['cond'] === 'lt' && num < threshold)) {
                        color = p['font_color'];
                    }
                }
                box.append(`<li id="${i}" tag="num" style="font-size:${p['font_size']}px;font-weight: ${p['bold'] ? 'bold' : ''};background-color:${p['bg_color']};color:${color};" class="block">${p['display'] ? p['text'] : ''}</li>`);
                break;
        }
    }
    setDraggable();
    setTileDbclickListener();
    setModalSaveListener();
    setSaveListener();
    setQuitListener();
    setResetListener();
}

function setSaveListener() {
    $("#save").click(function () {
        saveConfAndReload(true);
    })
}

function setModalSaveListener() {
    $("#numModalBtn").click(function () {

        let modal = $("#numModal");

        let tileConfDict = confList[modal.find(".tileId").val()];

        ['bg_color', 'font_size', 'font_color', 'threshold'].forEach(function (k) {
            tileConfDict[k] = modal.find('.' + k).val();
        });
        ['display', 'bold'].forEach(function (k) {
            tileConfDict[k] = modal.find('.' + k).prop('checked');
        });

        tileConfDict['cond'] = modal.find('.cond option:selected').val();

        modal.modal('hide');
        saveConfAndReload();
    });
    $("#textModalBtn").click(function () {

        let modal = $("#textModal");

        let tileConfDict = confList[modal.find(".tileId").val()];

        ['bg_color', 'font_size', 'text'].forEach(function (k) {
            tileConfDict[k] = modal.find('.' + k).val();
        });
        ['display', 'bold'].forEach(function (k) {
            tileConfDict[k] = modal.find('.' + k).prop('checked');
        });

        modal.modal('hide');
        saveConfAndReload();
    });
    $("#dateModalBtn").click(function () {

        let modal = $("#dateModal");

        let tileConfDict = confList[modal.find(".tileId").val()];

        ['bg_color', 'font_size', 'format'].forEach(function (k) {
            tileConfDict[k] = modal.find('.' + k).val();
        });
        ['display', 'bold'].forEach(function (k) {
            tileConfDict[k] = modal.find('.' + k).prop('checked');
        });

        // backend.printList(confList);
        modal.modal('hide');
        saveConfAndReload();
    });
}

function saveConfAndReload(reload = true) {
    //reorder
    var ids = $('#dragBox li').map(function () {
        return $(this).attr('id');
    }).get();
    ids.unshift('2');
    ids.unshift('1');
    ids.unshift('0');
    confList = ids.map(i => confList[i]);
    //pass to backend
    backend.saveConf("f10b_shareholder", confList, async function (n) {
        if (n) {
            let toast = $('#toast');
            toast.modal('show');
            await new Promise(r => setTimeout(r, 500));
            toast.modal('hide');
            if (reload) {
                document.location.reload();
            }

        }
    });
}

function setQuitListener() {
    $("#home").click(function () {
        backend.nav("home", "f10b_shareholder");
    });
}

function setResetListener() {
    $("#reset").click(function () {
            $(this).prop('disabled', true);
            if (confirm("Confirm to reset?")) {
                backend.resetConf('f10b_shareholder', function (l) {
                    confList = l;
                    document.location.reload();
                });
            }
        }
    );
}

