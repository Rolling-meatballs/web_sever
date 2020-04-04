var log = console.log.bind(console, new Date().toLocaleString())

var e = function (selector) {
    return document.querySelector(selector)
}

var todoTemplate = function (todo) {
    var t =`
    <div class="todo-cell">
        <span>${todo}</span>
    </div>
    `
    return t
}


var insertTodo = function (todoCell) {
    var form = document.querySelector('#id-todo-list')
    form.insertAdjacentHTML('beforeEnd', todoCell)
}

var loadTodos = function () {
    ajax('POST', '/todo/ajax/all', {}, function (json) {
        log('get ajax response')
        log('response data', json)
        for (var i = 0; i < json.length; i++) {
            log('json for', json[i], json)
            var todo = json[i].title
            var todoCall = todoTemplate(todo)
            log(todoCall)
            insertTodo(todoCall)
        }
    })
}

var bindEvents = function () {
    var b = e('#id-button-add')
    b.addEventListener('click', function () {
        log('click')
        var input = e('#id-input-todo')
        log(input)
        log(input.value)
        var todo_title = input.value
        var todoCell = todoTemplate(todo_title)
        log(todoCell)

        var data = {
            title: todo_title
        }
        ajax('POST', '/todo/ajax/add', data, function (json) {
            log('get ajax response')
            var message = json.message
            alert(message)
            insertTodo(todoCell)
        })
    })
}

var main = function () {
    loadTodos()
    bindEvents()
}

main()