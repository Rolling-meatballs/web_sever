var log = console.log.bind(console, new Data().toLocaleString())

var e = function (selector) {
    return document.querySelector(selector)
};

// var loginTemplate = function (result) {
//     var r = `
//     `<h3>${result}</h3>`;
//
//     return r
// };

var giveresult = function (result) {
    var form = e('h3');
    form.insertAdjacentHTML('beforeEnd', result)
};

var bindEvents = function () {
    var b = e('#id-login-submit');
    b.addEventListener('click', function () {
        log('click');
        var input_name = e('#in-input-username');
        log(input_name);
        log(input_name.value);
        var username = input_name.value;
        var len = username.length;
        var first = username[0];
        var last = username[len - 1];
        if (first < 10 || len < 2 || len > 10) {
            alert('username is wrong')
        }
        else{
            var content = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
            for(var j = 0; j < len; j++){
                var w = username[j];
                for(var i = 0; i < content.length; i++){
                    if(w == content[i]) {
                        break
                    }
                    else if(i == content.length -1) {
                        alert('username is wrong')
                    }
                }

            }
            if(last == '_'){
                alert('username is wrong')
            }
            else{
                giveresult('check')
            }
        }
    })
}


var main = function () {
    bindEvents()
}

main()