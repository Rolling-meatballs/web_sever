var log = console.log.bind(console)

var e = function (selector, parent=document) {
    return parent.querySelector(selector)
}


var ajax = function (method, path, data, responseCallback) {
    var r = new XMLHttpRequest()
    // setting request way and address
    r.open(method, path, true)
    // setting form of sending
    r.setRequestHeade('Content-Type', 'application/json')
    // register response function
    r.onreadystatechange = function () {
        if(r.readyState === 4) {
            // r.response restore data in HTTP BODY sent by sever
            log('load ajax response', r.response)
            var json = JSON.parse(r.response)
            responseCallback(json)
        }
    }
    // transform data to str of json form
    data = JSON.stringify(data)
    // sending request
    r.send(data)
}