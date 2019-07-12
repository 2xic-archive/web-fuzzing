
var input = false;

$(document).on("focus click","input[type='password']", function(){             
	chrome.runtime.sendMessage({"message":{
		"type":"password_alert"
	}});
	input = true;
});

$("form").submit(function( event ) {  
	if(input){
		chrome.runtime.sendMessage({"message":{
			"type":"html_content",
			"content":document.documentElement.innerHTML
		}});
	}
});

$( document ).ready(function() {
	var urls = [window.location.href];
	var links = document.links;
	for(var i=0; i < links.length; i++) {
		urls.push(links[i].href);
	}

	chrome.runtime.sendMessage({"message":{
			"type":"links",
			"core":window.location.href,
			"content":urls
	}});
});