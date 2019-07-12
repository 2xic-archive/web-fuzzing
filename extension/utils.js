
function valid_scope(url, scope){
	var link = document.createElement("a");
	link.href = url;

	for(var i = 0; i < scope.length; i++){
		if(0 <= scope[i].indexOf(link.hostname.replace("www.", ""))){
			return true;
		}
	}
	return false;
}

function get_file_exstension(url){
	var first_split = url.split("?")[0];
	var second_split = first_split.split(".");
	return second_split[second_split.length - 1];
}

function bad_extension(url, bad_file){
	var url_file = get_file_exstension(url);
	for(var i = 0; i < bad_file.length; i++){
		if(0 <= bad_file[i].indexOf(url_file)){
			return true;
		}
	}
	return false;
}

/*
	get_file_exstension("http://test.com/test.html")
	get_file_exstension("http://test.com/test.html?yep=")
*/