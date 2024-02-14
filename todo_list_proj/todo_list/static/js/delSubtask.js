function delSubtask(subtask_id) {
    $.ajax({
        url: 'delete_subtask/',
        method: 'POST',
        dataType: 'json',
        data: {subtask_id: subtask_id},
        success: function(data){
            location.reload();
        }
    });
}
