$(function(){
	$('.form-holder').delegate("input", "focus", function(){
		$('.form-holder').removeClass("active");
		$(this).parent().addClass("active");
	})
})

setTimeout(function(){
	$('#message').fadeOut('slow')

}, 4000)