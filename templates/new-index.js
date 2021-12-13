
const express = require


function cards() {
    var car;
    fetch("projects.json")
        .then(response => response.json())
        .then(data => {
            console.log(data);

            var list = data["items"]



            const container = document.getElementById('ca');
            list.forEach(function (item, index) {
                const card = `<div class="card-view">
                            <div class="rounded-img"><img src="`+ item["img"] + `" alt="" height="400px" width="350px"> </div>
                            <div class="pr-name">
                            <a href="`+item["link"]+`"><h1>`+ item["name"] + `</h1></a>                           
                            <div class="hideable-content">
                            <p>`+ item["desc"] + `</p>
                            <div class="links">
                                <a href="`+ item["gitrepo"] + `"><img src="images/Projects/git-icon.png" alt="github"></a>
                                <a href="`+ item["yt"]+`"><img src="images/Projects/YouTube.png" alt="" ></a>
                            </div>
                            
                            
                            
                            </div>
                            </div> `

                container.innerHTML += card


            });

        })
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function openImg() {
    const class_c = document.getElementsByClassName("rounded-img-btn")

}

function toabout(){
    window.location.href("#about")
}


function getDetails() {
    var name = 
        document.forms["projects"]["name"];
    var disc = 
        document.forms["projects"]["disc"];
    var img = 
        document.forms["projects"]["img"];
    var password = 
        document.forms["projects"]["Pass"];
    

    if (name.value == "") {
        window.alert("Please enter your name.");
        name.focus();
        return false;
    }

    console.log(name)

    

    
    return true;
}
