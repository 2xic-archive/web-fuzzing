
function explore() {
	chrome.tabs.query({active:true, currentWindow: true}, function(tabs){
		chrome.tabs.sendMessage(tabs[0].id, "start");
	});
}

function last_explore(){
	chrome.tabs.query({active:true, currentWindow: true}, function(tabs){
		chrome.tabs.sendMessage(tabs[0].id, "last");
	});	
}

document.getElementById('do-explore').onclick = explore;
document.getElementById('last-explore').onclick = last_explore;