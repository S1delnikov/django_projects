var appear = false
function addTask() {
    if (appear == true){
        // appear = false;
        return;
    }
    showForm();
    appear = true;
}


function addingForm(csrftoken, currentDate){
    let html  = `<form class="add-task-form" id="add-form" action="/tasks/new_task/" method="post">`;
    html += `<input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">`;    // Нужен для избежания ошибки 403 
    html += `<div><label class="add-task-form__label">Название:</label><input type="text" name="new-task-name" value=""></div>`;
    html += `<div><label class="add-task-form__label">Начало:</label><input type="datetime-local" value="${currentDate}" name="new-task-startdate"></div>`;
    html += `<div><label class="add-task-form__label">Конец:</label><input type="datetime-local" value="${currentDate}" name="new-task-deadline"></div>`;
    html += `<button class="add-task-form__btn" type="submit">Создать</button>`;
    html += `</form>`;

    return html
}

function showForm() {
    var csrftoken;
    $.ajax({
        data: {},
        url: 'get_csrftoken/',
        type: 'POST',
        dataType: 'json',
        success: function(data) {
            csrftoken = data.csrftoken;
        }

    });
    
    let form = addingForm(csrftoken, currentDate());
    $('#new-tasks-board').append(form);
}

function currentDate() {
    let curDate = new Date().toJSON().slice(0, 19);
    return curDate;
}