
const infobutton = document.querySelector('#info');
infobutton.addEventListener('click', async function() {
  const response = await fetch('http://127.0.0.1:3000/info');
  const info = await response.text();
  document.querySelector('#textbox').innerText = info;
});