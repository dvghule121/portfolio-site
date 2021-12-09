
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
                            <h1>`+ item["name"] + `</h1>
                            <p>`+ item["desc"] + `</p>
                            </div>
                            </div> `

                    container.innerHTML += card


                });

            })
    }

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function openImg(){
        const class_c = document.getElementsByClassName("rounded-img-btn")
        
    }

