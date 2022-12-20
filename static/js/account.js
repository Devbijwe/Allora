let inputState = document.getElementById("inputState");
let inputCity = document.getElementById("inputCity");
async function statesLoader() {
    let fetching = await fetch("/static/ds/states.json");
    let data = await fetching.json();
    return data;
}


let a = statesLoader();
a.then(data => statesAdder(data))
let html = "";

function statesAdder(data) {
    Array.from(data).forEach((elem, index) => {
        html += `<option class="state"> ${elem.name} </option>`
    });
    inputState.innerHTML += html;
}
let state = document.getElementsByClassName("state")
Array.from(state).forEach(elem => {
    elem.addEventListener("select")
})




let selectedState;

function stateselector() {
    selectedState = inputState.value;
    async function cityLoader() {
        let fetching = await fetch("/static/ds/districts.json");
        let data = await fetching.json();
        return data;
    }

    let b = cityLoader();
    b.then(data => cityAdder(data))
        // let html2 = "";
    console.log(inputState.value);
}
let html2 = "";

function cityAdder(data) {
    // console.log(data.states)
    html2 = "";
    inputCity.innerHTML = `<option class="city"> Select Your City </option>`;
    Array.from(data.states).forEach((element, index) => {

        if (element.state.toLowerCase() == selectedState.toLowerCase()) {
            Array.from(element.districts).forEach(elem => {
                // html2+="" 
                html2 += `<option class="city"> ${elem} </option>`
                console.log(elem)
            })

        }
        // html += `<option> ${elem.name} </option>`
    });
    inputCity.innerHTML += html2;
}