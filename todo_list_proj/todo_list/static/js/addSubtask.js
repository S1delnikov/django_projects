// import { usingMasonry } from "./usingMasonry.js";
function usingMasonry() {
    $('.tasks-board').masonry({
      // options
      itemSelector: '.task-card',
      columnWidth: 0,
      gutter: 50
    });
}

function addSubtask(task_id) {
    let formContainer = document.getElementById(task_id);

    let inputElement = document.createElement('input');
    inputElement.type = 'text';
    inputElement.style = 'display: block;';
    inputElement.name = 'subtask_' + task_id;
    inputElement.size = 20;

    let confirmElement = document.createElement('input');
    confirmElement.type = 'submit';
    confirmElement.name = 'confirmBtn';
    confirmElement.className = 'task-card__task-button';
    confirmElement.value = 'Подтвердить';
    confirmElement.size = 20;
    confirmElement.addEventListener("click", _ => {
         $.ajax({
            data: {subtask_text: inputElement.value, task_id: task_id, },
            url: 'new_subtask/',
            type: 'POST',
            dataType: 'json',
            success: function(data) {
                csrftoken = data.csrftoken;
                new_subtask_id = data.new_subtask_id;
                var html = newFormSubtask(csrftoken, task_id, new_subtask_id, inputElement.value);
                $('#'+task_id).append(html);
                
                formContainer.removeChild(inputElement);
                formContainer.removeChild(confirmElement);

                usingMasonry();
            },
        }); 
    });

    formContainer.appendChild(inputElement);
    formContainer.appendChild(confirmElement);
    usingMasonry();
}


function newFormSubtask(csrftoken, task_id, subtask_id, subtask_text, subtask_status=false) {
    let html = `<form action="/tasks/update_task/${task_id}/${subtask_id}/${subtask_text}/" method="post">`;
    html += `<input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">`;    // Нужен для избежания ошибки 403 
    html += `<p>`;
    html += `<input type="checkbox" onclick="location.href='/tasks/${task_id}/${subtask_id}/${subtask_status}/'">`;
    html += `<input type="text" value="${subtask_text}" name="subtask_text"> `;
    // html += `${subtask_status}`;
    html += `</p>`;
    html += `<button class="task-card__task-button" type="submit">Изменить</button>`;
    html += `</form>`;
    html += `<button class="task-card__task-button" type="button" onclick="delSubtask({{ ${subtask_id} }})">Удалить</button>`;

    return html
}

// const xhr = new XMLHttpRequest();
// без '\' в конце = GET запрос
// xhr.open('POST', "new_subtask/");
// xhr.send()

/*
function check(inputElement) {
    console.log(inputElement.value);
    $.ajax({
        data: {qwerty: 'hi)'},
        url: 'new_subtask/',
        type: 'POST',
        dataType: 'json',
        success: function(data) {
            // Обработка полученных данных
            alert(data.name);
        }
    }); 
}
*/

/*

$.ajax({
        data: "qwerty", // получаем данные формы
        type: $(this).attr('method'), // GET или POST
        url: 'new_subtask',
        // если успешно, то
        success: function (response) {
            alert("Спасибо, что обратились к нам " + response.name);
            // location.reload();
            console.log("success!");
        },
        // если ошибка, то
        error: function (response) {
            // предупредим об ошибке
            alert(response.responseJSON.errors);
            console.log(response.responseJSON.errors)
        }
    });
    return false;

*/