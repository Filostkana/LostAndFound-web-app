let property = document.getElementById("property");
console.log(property.value)
if (property.value == "vehicles")
{
  let inputs = document.getElementsByClassName("searchinput");

  // Get the target elment
  let target = document.getElementById("target");

  // Var for every single input elment
  let condtion = document.getElementById("condtion");

  let searchCondtion = ""
  if (condtion.value == "lost") {searchCondtion = "found"}
  if (condtion.value == "found") {searchCondtion = "lost"}

  let inputType = document.getElementById("inputType");
  let inputBrand = document.getElementById("inputBrand");
  let inputYear = document.getElementById("inputYear");
  let inputColor = document.getElementById("inputColor");
  let inputPlateN = document.getElementById("inputPlateN");
  let inputChassisN = document.getElementById("inputChassisN");
  console.log("input: " + inputType.innerHTML)


  // Aplay a function in every input
  for (let i in inputs) {
    inputs[i].addEventListener('input', async function() {
              let url = "/search?condtion=" + searchCondtion + "&property=" + property.value;
              if (inputType.value) {url += "&type=" + inputType.value}
              if (inputBrand.value) {url += "&brand=" + inputBrand.value}
              if (inputYear.value) {url += "&manufYear=" + inputYear.value}
              if (inputColor.value) {url += "&color=" + inputColor.value}
              if (inputPlateN.value) {url += "&plateNumber=" + inputPlateN.value}
              if (inputChassisN.value) {url += "&chassisNumber=" + inputChassisN.value}
              let response = await fetch(url);
              let vehicles = await response.text();
              document.querySelector('#target').innerHTML = vehicles;
          });


  }
  
}
else
{
  let inputs = document.getElementsByClassName("searchinput");

  // Get the target elment
  let target = document.getElementById("target");

  // Var for every single input elment
  let condtion = document.getElementById("condtion");

  let searchCondtion = ""
  if (condtion.value == "lost") {searchCondtion = "found"}
  if (condtion.value == "found") {searchCondtion = "lost"}

  let inputType = document.getElementById("inputType");
  let inputBrand = document.getElementById("inputBrand");
  let inputYear = document.getElementById("inputYear");
  let inputColor = document.getElementById("inputColor");
  let inputSerialN = document.getElementById("inputSerialN");
      

  // Aplay a function in every input
  for (let i in inputs) {
    inputs[i].addEventListener('input', async function() {
              let url = "/search?condtion=" + searchCondtion + "&property=" + property.value;
              if (inputType.value) {url += "&type=" + inputType.value}
              if (inputBrand.value) {url += "&brand=" + inputBrand.value}
              if (inputYear.value) {url += "&manufYear=" + inputYear.value}
              if (inputColor.value) {url += "&color=" + inputColor.value}
              if (inputSerialN.value) {url += "&serialNumber=" + inputSerialN.value}
              let response = await fetch(url);
              let vehicles = await response.text();
              document.querySelector('#target').innerHTML = vehicles;
          });


  }

}
