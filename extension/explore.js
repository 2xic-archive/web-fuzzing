
/*
	To be able to explore well you have to know each state
	of the site and be able to reproduce that state.

		-	actually, I think you can use something like observe in javascript	
			-	if observe always add in the same order (note something might get added late 
				because dependency on the network), the function below could get changed.
*/

function get_all_elements(delta){
	var all = document.getElementsByTagName("*");
	
	var delta_elements = [];
	var hash_state = [];

	for(var i = 0; i < all.length; i++){
		var element_text = all[i].outerHTML;
		var hash = MD5(element_text);

		if(delta[hash] == undefined){
			delta_elements.push(all[i]);
			hash_state.push(hash);
			
			delta[hash] = true;
		}
	}

	var tree = new MerkleTree(hash_state);
	return {
		"state_id":tree.root,
		"delta":delta_elements
	}
}

class state {
	constructor() {
		/*
			The nice thing is that we only have to save the 
			state_index, having that store in the localstorage, it
			is possible to reproduce all the other states. Great!
		*/
		this.state_index = [];
		this.state_info = [];
		this.all_states = {

		};
		this.state_hash = {

		};
		this.done_exploring = false;
	}

	report_state(){
		localStorage.setItem('last_state', JSON.stringify(this.state_index));
	}

	requested_state(){
		var data = localStorage.getItem('last_state');
		if(data == undefined){
			return undefined;
		}
		var response = JSON.parse(data);
		for(var i = 0; i < response.length; i++){
			this.add_new_known_state(response[i], (i + 1) == response.length);
			this.interact_with_latest();
		}
	}

	add_new_known_state(known_index, decrement_before_last){
		var known_index_minus = known_index;
		//	need to go back one level
		if(!decrement_before_last){
			known_index_minus[0]--;
		}

		var new_state = get_all_elements(this.state_hash);
		this.state_index.push(known_index);
		this.state_info.push(new_state["delta"]);
		this.all_states[new_state["state_id"]] = true;
	}

	add_new_state(){
		var new_state = get_all_elements(this.state_hash);
		if(this.all_states[new_state["state_id"]] == undefined && 0 < new_state["delta"].length){
			this.state_index.push([0, new_state["delta"].length]);
			this.state_info.push(new_state["delta"]);
	
			//	already explored, make sure we don't revist a previous state.
			this.all_states[new_state["state_id"]] = true;
		}
	}

	interact_with_element(element){
		console.log(element);
		element.click();
	}

	interact_with_latest(){
		var index = (this.state_index.length - 1);
		//	I think working_index should be -1
		var working_index = this.state_index[index][0];
		console.log(this.state_index[index]);
		var delta_element = this.state_info[index][working_index];
		this.interact_with_element(delta_element);
	}

	upgrade_state(){
		if(0 < this.state_index.length){
			this.interact_with_latest();
			/*
				need to check if the interaction made a new element.
				hooking actionlistener only get you so far, people
				write some crazy javascript code to add new elements
				so doing a full check to be on the safe site. 
			*/
			var index = (this.state_index.length - 1);
			this.state_index[index][0]++;
			this.add_new_state();
			if(this.state_index[index][0] == this.state_index[index][1]){
				this.state_index.pop();
				this.state_info.pop();
				if(this.state_info.length == 0){
					this.done_exploring = true;
				}
			}
		}else if(!this.done_exploring){
			this.add_new_state();
			this.upgrade_state();

			if(this.state_info.length == 0){
				this.done_exploring = true;	
			}
		}
	}

	get exploring(){
		return !this.done_exploring;
	}
}

async function start(){
	var x = new state();
	
	chrome.runtime.sendMessage({"message":{
			"type":"new_target",
			"target":window.location.href
		}
	});
	//	init first state
	x.requested_state();
	while(x.exploring){
		try{
			if(document.readyState == "ready" || document.readyState === "complete"){
				var wait_time = new Promise((resolve, reject) => {
					let wait = setTimeout(() => {
						clearTimeout(wait);
						resolve('done');
					}, 200)
				});

				await wait_time.then(function(value) {
					x.upgrade_state();
				});
			}
		}catch(e){
			// pass
		}
	}
}

chrome.runtime.onMessage.addListener(function(message,sender,sendResponse){
	if(message == "start"){
		start();
	}else if(message == "last"){
		chrome.runtime.sendMessage({"message":{
				"type":"get_target"
			}
		});
	}else{
		console.log("open : " + message);
	//	window.open(message, "_self");
	}
});
