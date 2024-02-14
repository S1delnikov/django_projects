function delTask(task_id){
    $.ajax({
        url: 'delete_task/',
        method: 'post',
        dataType: 'json',
        data: {'task_id': task_id},
        success: function(data){
            location.reload();
        },
    });
}