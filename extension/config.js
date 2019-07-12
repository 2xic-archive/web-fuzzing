

var server_adress = "*YOUR URL*";

var socket = io.connect(server_adress);


var scope = [];
var bad_file_formats = [".zip", ".png", ".jpg"];

function get_scope(){
	var xhr = new XMLHttpRequest();				
	xhr.open("POST", server_adress + "scope", false);
	xhr.send();
	scope = JSON.parse(xhr.responseText);
}

get_scope();

function send_info(info){
	var xhr = new XMLHttpRequest();				
	xhr.open("POST", server_adress, true);
	xhr.send(JSON.stringify(info));
}
