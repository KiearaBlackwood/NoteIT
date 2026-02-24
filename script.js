function loadDoc(url, func){
    let xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        if(xhttp.status != 200) {
            console.log("Error!");
        }else {
            func(xhttp.response);
        }
    }

    xhttp.open("GET", url);
    xhttp.send();
}

function signup() {
    let txtUserName = document.getElementById("txtUserName");
    let txtEmail = document.getElementById("txtEmail");
    let txtPassword= document.getElementById("txtPassword");

    let URL = "/signup?username=" + txtUserName.value + "&email=" + txtEmail.value + "&password=" + txtPassword.value;
    loadDoc(URL, signup_response);
}

function signup_response(response) {
    let data = JSON.parse(response);
    let result= data["result"];

    if (result != "OK") {
        alert(result);
    }else {
        window.location.replace("/home.html");
    }
}

function login() {
    let txtEmail = document.getElementById("txtEmail");
    let txtPassword= document.getElementById("txtPassword");
    let chkRemember = document.getElementById("chkRemember");

    let URL = "/login?email=" + txtEmail.value + "&password=" + txtPassword.value;

    if(chkRemember.checked){
        URL += "&remember=yes";
    }else{
        URL += "&remember=no";
    }

    loadDoc(URL, login_response);
}

function login_response(response) {
    let data = JSON.parse(response);
    let result= data["result"];

    if (result != "OK") {
        alert(result);
    }else {
        window.location.replace("/home.html");
    }
}

function load_editor_Post(username) {
    let URL = "/postitems?username=" + username;
    loadDoc(URL,editor_postitems_response)
}

function editor_postitems_response(response) {
    let data = JSON.parse(response);
    let results= data["result"];

    let temp="";
    for(let i=0; i < results.length; i++){
        var result = results[i];
        temp += "<a href='/post/" + result['PostID'] + "'>reply</a><br/>";
        temp += "<a href='/account/" + result['UserName'] + "'>" + result['UserName'] + "</a><br>";
        temp += result['Text'] + "<br>" + result["Date"] + "<br><a href='/post/" + result['PostID'] + "'>reply</a><br><br>";
    }

    document.getElementById("divPost").innerHTML = temp;
}

function listfeed() {
    let URL = "/postitems";
    loadDoc(URL,listfeed_response)
}

function listfeed_response(response) {
    let data = JSON.parse(response);
    let results= data["result"];

    let temp="";
    for(let i=0; i < results.length; i++){
        var result = results[i];
        temp += "<a href='/post/" + result['PostID'] + "'>reply</a><br/>";
        temp += "<a href='/account/" + result['UserName'] + "'>" + result['UserName'] + "</a><br>";
        temp += result['Text'] + "<br>" + result["Date"] + "<br><br>";
    }

    document.getElementById("divPost").innerHTML = temp;

}
function loadPost(username) {
    let URL = "/postitems?username=" + username;
    loadDoc(URL,postitems_response )
}

function postitems_response(response) {
    let data = JSON.parse(response);
    let results= data["result"];

    let temp="";
    for(let i=0; i < results.length; i++){
        var result = results[i];
        temp += "<a href='/account/" + result['UserName'] + "'>" + result['UserName'] + "</a><br>";
        temp += result['Text'] + "<br>" + result["Date"] + "<br><a href='/post/" + result['PostID'] + "'>reply</a><br><br>";
    }

    document.getElementById("divPost").innerHTML = temp;
}

function addPost() {
    let txtText = document.getElementById("txtText");

    let URL = "/addpost?text="+ txtText.value;

    loadDoc(URL,addPost_response);
}

function addPost_response(response) {
    let data = JSON.parse(response);
    let result= data["result"];

    if (result != "OK") {
        alert(result);
    }else {
        location.reload();
    }
}

function deletePost(postID) {
    let URL = "/deletepost?postid=" + postID;
    loadDoc(URL, deletePost_response);
}

function deletePost_response(response) {
    let data = JSON.parse(response);
    let result= data["result"];

    if (result != "OK") {
        alert(result);
    }else {
         window.location.reload();
    }
}

function addreply(postid) {
    let txtText =  document.getElementById("comment");
    let URL = "/addreply?postid=" + postid + "&text=" + txtText.value;
    loadDoc(URL, addreply_response);
}

function addreply_response(response) {
    let data = JSON.parse(response);
    let result= data["result"];

    if (result != "OK") {
        alert(result);
    }else {
         location.reload();
    }
}

function listreplies(postid) {
    let URL = "/listreplies?postid=" + postid;
    loadDoc(URL, listreplies_response);
}

function listreplies_response(response) {
    let data = JSON.parse(response);
    let results= data["result"];

    let temp="Replies";
    for(let i=0; i < results.length; i++){
        var reply = results[i];
       temp += "<a href='/account/" + reply['UserName'] + "'>" + reply['UserName'] + "</a><br>";
       temp += reply['Text'] + "<br>" + reply["Date"] + "<br><br>";
    }

    document.getElementById("divReplies").innerHTML = temp;
}

function upload_file(){
    let xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        if(xhttp.status != 200) {
            console.log("Error!");
        }else {
            upload_file_response(xhttp.response);
        }
    }

    xhttp.open("POST", "/uploadfile", true);

    var formData = new FormData();
    formData.append("file", document.getElementById("file").files[0]);
    xhttp.send(formData);
}

function upload_file_response(){
    location.reload();
}

function listitems() {
    loadDoc('/listitems', listitems_response);
}

function listitems_response(response) {
    let data = JSON.parse(response);
    let items = data["result"];
    let url = data['url'];

    let temp="";
    for(let i=0; i < items.length; i++){
        temp += "<img src=\"" + url + items[i]['ImageName'] + "\" style=\"width: 160px; height: auto;\">" +"<br/>";
    }

    document.getElementById("divResults").innerHTML = temp;
}

console.log("Script Loaded");