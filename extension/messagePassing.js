var hook_next_form = false;

var last_state = undefined;



chrome.runtime.onMessage.addListener(function(message,sender,sendResponse){
	var messageParsed = message["message"];
	if(messageParsed["type"] == "password_alert"){
		hook_next_form = true;
	}else if(messageParsed["type"] == "html_content"){
		console.log(messageParsed["content"]);
	}else if(messageParsed["type"] == "new_target"){
/*		chrome.storage.sync.set({page: messageParsed["target"]}, function() {
			console.log('Value is set to ' + messageParsed["target"]);
		});
*/
		var value = messageParsed["target"];
		chrome.storage.local.set({key: value}, function() {
			console.log('Last page is set to ' + value);
		});

	}else if(messageParsed["type"] == "get_target"){
		chrome.storage.local.get(["key"], function(result) {
			chrome.tabs.query({active:true, currentWindow: true}, function(tabs){
				chrome.tabs.sendMessage(tabs[0].id, result.key);
			});	
		});
	}else if(messageParsed["type"] == "links"){
		if(valid_scope(messageParsed["core"], scope)){
			//queue = queue.concat(messageParsed["content"]);
			socket.emit("urls", messageParsed["content"]);
		}
	}
});

chrome.webRequest.onBeforeRequest.addListener(function(details) {
	if(hook_next_form && details.requestBody != undefined){
		var keys = Object.keys(details.requestBody);
		if(keys.indexOf("formData") != -1){
		//	console.log(details.url);
		//	console.log(details.requestBody);
			socket.emit("login",{
				"type":"login_profile",
				"url":details.url,
				"data":details.requestBody["formData"]
			});
		}

		hook_next_form = false;
	}
},{
		urls: ["<all_urls>"],
		types: ["main_frame", "sub_frame", "stylesheet", "script", "image", "object", "xmlhttprequest", "other"]
	},
	["blocking", "requestBody"]
);
