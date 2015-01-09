$(function(){
    	NBViewer = {}
	NBViewer.notebooks = (function(){
		var ajax_load = function(url,data){
 			$.ajax({
				url:url,
				method:'GET',
				data:data,
				success:function(resp){
					$('body').append(resp)
			    	//$("form#generic-ajax-form").bind("submit",handle_ajax_form)
 					//$(".cancel_button, div#popup_overlay").click(function(){ 
                    //disabled the ability to close popup by clicking on the overlay
                    $(".cancel_button").click(function(){ 
						$('form').submit(function(){return false});
						$("div#popup_overlay, div#popup_content").remove();
					})
                    $(document).keydown(function(e) {
                        if (e.which == 27){
                            $('form').submit(function(){return false});
                            $("div#popup_overlay, div#popup_content").remove();
                        }
                    });
                    
                    $("div#popup_overlay").mousedown(function(){
                      $('form').submit(function(){return false});
                      $("div#popup_overlay, div#popup_content").remove();
                    });
				}
			})
		}	

		var handle_remote_loading = function(href){
            console.log(href)
			var h = href.slice(1);
			ajax_load(h)
			return false 
		}
		var loader = function(){
			//$("#spinner,#popup_overlay").bind("ajaxSend", function() {
            $("#spinner").bind("ajaxSend", function() {
		        	$(this).show();
           		}).bind("ajaxStop", function() {
 		        	$(this).hide();
	        	}).bind("ajaxError", function() {
		        	$(this).hide();
	        	});
		} 
   		var init = function(){
            $("a.ajax-load").click(function(){
                handle_remote_loading($(this).attr('href'))
            })
            loader();
		}
        return {init:init}
	}())
    NBViewer.notebooks.init()
})
