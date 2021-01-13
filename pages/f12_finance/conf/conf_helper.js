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
        if (typeof value === "boolean") {
            modal.find("." + key).prop("checked", value);

        } else {
            modal.find("." + key).val(value);
            modal.find("." + key).trigger('change');
        }
    }
    modal.find(".tileId").val(id);
    modal.modal('show');
}

function initBox() {
    backend.getConf('f12_finance', setBoxChildren);
}

function setBoxChildren(l) {
    confList = l;
    for (let i = 0; i < 3; i++) {
        let p = confList[i];

        switch (p['tag']) {
            case 'text':

                $('.row-header').append(`<div id="${i}" tag="text" style="font-size:${p['font_size']}px;font-weight: ${p['bold'] ? 'bold' : ''};background-color:${p['bg_color']}" class="block">${p['display'] ? p['text'] : ''}</div>`);
                break;
            case 'date-header':

                $('.row-header').append(`<div id="${i}" tag="date-header" style="font-size:${p['font_size']}px;font-weight: ${p['bold'] ? 'bold' : ''};background-color:${p['bg_color']}" class="block">${p['display'] ? p['text'].slice(p['format']) : ''}</div>`);
                break;
        }
    }

    let date = l[3];
    let block_date = $('.block-date');
    block_date.attr('id', '3');
    block_date.attr('style', `font-size:${date['font_size']}px;font-weight: ${date['bold'] ? 'bold' : ''};background-color:${date['bg_color']}`);
    block_date.text(date['text'].slice(date['format']));

    let box = $("#dragBox");
        for (let i = 4; i < confList.length; i++) {
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
    setSaveListener();
    setModalSaveListener();
    setQuitListener();
    setResetListener();
}

function setSaveListener() {
    $("#save").click(function () {
        saveConfAndReload(true);
    })
}

function setModalSaveListener() {

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
    $("#date-headerModalBtn").click(function () {

        let modal = $("#date-headerModal");

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
    $("#dateModalBtn").click(function () {

        let modal = $("#dateModal");

        let tileConfDict = confList[modal.find(".tileId").val()];

        ['bg_color', 'font_size', 'format', 'date_start', 'date_end'].forEach(function (k) {
            tileConfDict[k] = modal.find('.' + k).val();
        });
        ['ordering', 'bold'].forEach(function (k) {
            tileConfDict[k] = modal.find('.' + k).prop('checked');
        });

        // backend.printList(confList);
        modal.modal('hide');
        saveConfAndReload();
    });
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
}

function saveConfAndReload(reload = true) {
    //reorder
    let header_ids = $('.row-header div').map(function () {
        return $(this).attr('id');
    }).get();
    header_ids.push('3');
    let col_ids = $('#dragBox li').map(function () {
        return $(this).attr('id');
    }).get();
    let ids = $.merge(header_ids, col_ids);
    confList = ids.map(i => confList[i]);
    //pass to backend
    backend.saveConf("f12_finance", confList, async function (n) {
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
        backend.nav("home", "f12_finance");
    });
}

function setResetListener() {
    $("#reset").click(function () {
            $(this).prop('disabled', true);
            if (confirm("Confirm to reset?")) {
                backend.resetConf('f12_finance', function (l) {
                    confList = l;
                    document.location.reload();
                });
            }
        }
    );
}

