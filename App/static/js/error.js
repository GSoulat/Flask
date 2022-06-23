randError =
	(Math.floor(Math.random() * 2) + 4) * 100 + Math.floor(Math.random() * 5);
randNumber = Math.floor(Math.random() * 10000);

urlSearch = "&url=https://127.0.0.1:8000/";

const params = new URLSearchParams(urlSearch);
const errorData = [
	{
		error: "0",
		errorText: "Unkown Error",
		errorSubText: "Somethings wrong, thats for sure."
	},
	{
		error: "400",
		errorText: "Error 400 - Bad Request",
		errorSubText: "The server cannot or will not process this request."
	},
	{
		error: "401",
		errorText: "Error 401 - Unauthorized",
		errorSubText: "You are not authorized to request$errorUrl"
	},
	{
		error: "403",
		errorText: "Error 403 - Forbidden",
		errorSubText: "You are not allowed to request$errorUrl"
	},
	{
		error: "404",
		errorText: "Error 404 - Not Found",
		errorSubText:
			"The requested resource$errorUrl was not found or does not exist."
	},
	{
		error: "500",
		errorText: "Error 500 - Internal Server Error",
		errorSubText: "The server is having problems."
	},
	{
		error: "503",
		errorText: "Error 503 - Service Unavailable",
		errorSubText: "The server could not handle your request right now."
	}
];

error = 0;
errorUrl = "";
if (params.has("error")) {
	error = params.get("error");
} else {
	error = 0;
}
if (params.has("url")) {
	errorUrl = " " + params.get("url");
} else {
	errorUrl = "";
}
index = 0;
for (i = 0; i < errorData.length; i++) {
	//console.log(errorData[i].errorText.replace('$errorUrl',errorUrl))
	if (errorData[i].error == error) {
		index = i;
	}
}

errorText = document.getElementsByClassName("errorText")[0];
errorSubText = document.getElementsByClassName("errorSubText")[0];
redirectText = document.getElementsByClassName("redirect")[0];
secondsText = document.getElementsByClassName("time")[0];

errorText.innerText = errorData[index].errorText;
if (error == 401 || error == 403 || error == 404) {
	errorSubText.innerText = errorData[index].errorSubText.replace(
		"$errorUrl",
		errorUrl
	);
} else {
	errorSubText.innerText = errorData[index].errorSubText;
}

secondsText.innerText = " in 10 seconds";
setTimeout(function () {
	redirectText.classList.add("unhide");
	seconds = 10
	setInterval(function() {
		seconds--;
		if(seconds != 1 && seconds != 0){
			secondsText.innerText = " in " + seconds + " seconds";
		} else if(seconds == 1){
			secondsText.innerText = " in " + seconds + " second";
		}else{
			seconds = 1;
			secondsText.innerText = "";
			//window.location = '';
		}
			
	}, 1000)
}, 1600);