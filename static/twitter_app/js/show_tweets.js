$(document).ready(function() {
    console.log( "on ready!__________________" );

	$(document).on('click', '#tweet', function () {
    	$.ajax({
    		type: 'POST',
			url: 'post_tweet',
			data: {"message" :$("#comment").val(), "user_id":$("#tweet-post").attr("user-id")},
			dataType: 'json',
			success: function (data) {
				if (data.message == "success"){
					$('#myModal').modal("toggle");
				}
			}
		});
	});


});