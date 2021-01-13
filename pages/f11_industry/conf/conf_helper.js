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
        }
        inp.change();
    }
    modal.find(".tileId").val(id);
    modal.modal('show');
}

function initBox() {
    backend.getConf('f11_industry', setBoxChildren);
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
    block_date.text(date['text']);


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
        ['display', 'bold','ordering'].forEach(function (k) {
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
        ['display', 'bold','ordering'].forEach(function (k) {
            tileConfDict[k] = modal.find('.' + k).prop('checked');
        });

        modal.modal('hide');
        saveConfAndReload();
    });
    $("#dateModalBtn").click(function () {

        let modal = $("#dateModal");

        let tileConfDict = confList[modal.find(".tileId").val()];

        ['bg_color', 'font_size', 'format', 'date_start', 'date_end'].forEach(function (k) {
            tileConfDict[k] = modal.find('.' + k).val();
        });
        ['bold', 'display','ordering'].forEach(function (k) {
            tileConfDict[k] = modal.find('.' + k).prop('checked');
        });

        modal.modal('hide');
        saveConfAndReload();
    });
}

function saveConfAndReload(reload = true) {

    //pass to backend
    backend.saveConf("f11_industry", confList, async function (n) {
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
        backend.nav("home", "f11_industry");
    });
}

function setResetListener() {
    $("#reset").click(function () {
            $(this).prop('disabled', true);
            if (confirm("Confirm to reset?")) {
                backend.resetConf('f11_industry', function (l) {
                    confList = l;
                    document.location.reload();
                });
            }
        }
    );
}


