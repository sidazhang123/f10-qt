//channel - start
var backend;
var confList;
new QWebChannel(qt.webChannelTransport, function (channel) {
    backend = channel.objects.backend;
});
