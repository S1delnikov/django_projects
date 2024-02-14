function updateTask(task_id){
    add_date = document.getElementById('add-date_' + task_id).value;
    deadline = document.getElementById('deadline_' + task_id).value;
    task_name = document.getElementById('task-name_' + task_id).value;
    $.ajax({
        url: 'update_task_data/',
        method: 'POST',
        dataType: 'json',
        data: {
            'task_id': task_id, 
            'add_date': add_date, 
            'deadline': deadline,
            'task_name': task_name,
        },
        success: function(data){
            location.reload();
        },
    });
}
