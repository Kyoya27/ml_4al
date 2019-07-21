function displayBackContent(type){
	var content = document.getElementById("back-content");
	var request = new XMLHttpRequest();

	request.onreadystatechange = function(){
		if( request.readyState == 4 && request.status == 200){
			content.innerHTML = request.responseText;
		}
	}	
	switch (type) {
    case "comm":
        var link = "comm";
        break;
    case "prod":
        var link = "prod";
        break;
    case "menu":
        var link = "menu";
        break;
    case "prom":
        var link = "prom";
        break;
    case "mea":
        var link = "mea";
        break;
}

	request.open("GET", link+"Content.php");
	request.send();
}

function sendProm(){

	var id = document.getElementById("id_prom").value;
	var description = document.getElementById("description").value;
	var prerequisite = document.getElementById("prerequisite").value;
	var available = document.getElementById("available").value;
	var start_date = document.getElementById("start_date").value;
	var end_date = document.getElementById("end_date").value;

	if(description === "" || prerequisite === "" || start_date === ""  || end_date === "" || available === "" ){
		alert("Champ(s) vide(s)");
	}else{
		if(id !== ""){
			var request = new XMLHttpRequest();

			request.onreadystatechange = function(){
				if( request.readyState == 4 && request.status == 200 ){
					location.relaod();
				}
			}

			var json_data = {
				"description": description,
				"prerequisite": prerequisite,
				"available": available,
				"start_date": start_date,
				"end_date": end_date
			};
			var formatted_json = JSON.stringify(json_data);

			request.open("POST", "http://localhost:8080/promotion/"+id, true);
			request.setRequestHeader("Access-Control-Allow-Origin", "*");
			request.setRequestHeader("Content-type", "application/json");
			request.send(formatted_json);
		}else{
			var request = new XMLHttpRequest();

			request.onreadystatechange = function(){
				if( request.readyState == 4 && request.status == 200 ){
					location.relaod();
				}
			}
			var json_data = {
				"description": description,
				"prerequisite": prerequisite,
				"available": available,
				"start_date": start_date,
				"end_date": end_date
			};
			var formatted_json = JSON.stringify(json_data);

			request.open("POST", "http://localhost:8080/promotion/", true);
			request.setRequestHeader("Content-type", "application/json");
			request.send(formatted_json);
		}
	}
}


function getCommand(){
	const listeCommand = [];
	$.ajax({
		url: "http://localhost:8080/command?done=0",
		type: "GET",
		beforeSend: function(xhr){
			xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
			xhr.setRequestHeader("Content-type", "application/json");
		},
		dataType : 'json',
		async: false,
		success: function(data) {
			for(let i = 0; i < data.length; i++){
				$.ajax({
					url: "http://localhost:8080/command/getCommand?id_command="+data[i].id,
					type: "GET",
					beforeSend: function(xhr){
						xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
						xhr.setRequestHeader("Content-type", "application/json");
					},
					async: false,
					dataType : 'json',
					success: function(commandProduct) {
						let commandTotal = {};
						commandTotal.total = data[i].total;
						commandTotal.id = data[i].id;
						commandTotal.commandResult = [];
						let product = {};
						let menu = {};
						for(let j = 0; j < commandProduct.length; j++){
							if(commandProduct[j].id_menu != 0){
								$.ajax({
									url: "http://localhost:8080/menu?id="+commandProduct[j].id_menu,
									type: "GET",
									beforeSend: function(xhr){
										xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
										xhr.setRequestHeader("Content-type", "application/json");
									},
									dataType : 'json',
									async: false,
									success: function(menuReturn) {
										product = {};
										menu = {};
										menu.name = menuReturn[0].name;
										menu.product = [];
										for(let k = 0; k < menuReturn[0].size; k++){
											$.ajax({
												url: "http://localhost:8080/product/getProduct?id="+commandProduct[k + j].id_product,
												type: "GET",
												async: false,
												beforeSend: function(xhr){
													xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
													xhr.setRequestHeader("Content-type", "application/json");
												},
												dataType : 'json',
												success: function(productReturn) {
													$.ajax({
														url: "http://localhost:8080/menu/findPriceMenu",
														type: "POST",
														data:JSON.stringify({
															"id_menu" : commandProduct[j].id_menu,
															"id_product" : commandProduct[k + j].id_product,
															"position" : k+1
														}),
														dataType:'json',
														async: false,
														beforeSend: function(xhr){
															xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
															xhr.setRequestHeader("Content-type", "application/json");
														},
														success: function(priceReturn) {
															if(priceReturn !== undefined){
																product = {};
																product.name = productReturn.name;
																product.price = priceReturn[0].price;
																menu.product.push(product);	
															}
														}
													});	
												}
											});
										}
										j += menuReturn[0].size;
										commandTotal.commandResult.push(menu);						
									}
								});
							}else{
								$.ajax({
									url: "http://localhost:8080/product/getProduct?id="+commandProduct[j].id_product,
									type: "GET",
									beforeSend: function(xhr){
										xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
										xhr.setRequestHeader("Content-type", "application/json");
									},
									dataType : 'json',
									success: function(productReturn) {
									product = {};
										product.name = productReturn.name;
										product.price = productReturn.price;
										commandTotal.commandResult.push(product);								
									}
								});							
							}

						}
						listeCommand.push(commandTotal);
					}
      			});
			}
		}
      });
	displayCommand(listeCommand);
}

function displayCommand(listeCommand){
	console.log(listeCommand);
	if(listeCommand === undefined || listeCommand.length === 0){
		$("#command_div").html("<center><h2>Aucune Commande !</h2></center>");
	}else{
		$("#command_div").html("");
		for(let i = 0; i < listeCommand.length; i++){

		}
	}
	
}

function fillProm(){
	var content = document.getElementById("choiceProm");
	var fills = content.value.split("|");

	console.log(fills);

	var id = document.getElementById("id_prom").value = fills[0];
	var description = document.getElementById("description").value = fills[1];
	var prerequisite = document.getElementById("prerequisite").value = fills[2];
	var available = document.getElementById("available").options.selectedIndex = fills[3] == "0" ? "2" : fills[3];
	var start_date = document.getElementById("start_date").value = fills[4];
	var end_date = document.getElementById("end_date").value = fills[5];
}

function setHeader(xhr) {
  xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
  xhr.setRequestHeader("Content-type", "application/json");
}
function send_cmd_to_base(cmd) {
  	$.ajax({
      url: "http://localhost:8080/command/add",
      type: "POST",
      data:JSON.stringify(cmd),
      dataType:'json',
      async: false,
      beforeSend: function(xhr){
        xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
        xhr.setRequestHeader("Content-type", "application/json");
      }
    });
}