$(document).ready(function() {
    $("#sign_in").click(function() {
    	$.ajax({
			url: 'init_oauth',
			dataType: 'json',
			success: function (data) {
				console.log("checking data", data)
				window.location = data.redirect_url;
			}
			});
	});


});