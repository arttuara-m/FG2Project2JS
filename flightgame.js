'use strict';

async function statupdater() {
  const response = await fetch(`http://127.0.0.1:3000/status`);
  const data = await response.json();
  document.querySelector('#showscore').innerText = 'Score: ' + data[0];
  document.querySelector('#showmoney').innerText = 'Money: ' + data[1];
  document.querySelector('#showcountry').innerText = 'Country: ' + data[2];
  document.querySelector('#showgthreat').innerText = 'Global threat: '+data[3];
  document.querySelector('#showlthreat').innerText = 'Local threat: ' + data[4];
}

const commands = ['info', 'use', 'buy', 'work', 'status'];
//Creates the first button row
for (const bcommand of commands) {
  //Creating the button
  const infobutton = document.createElement('button');
  infobutton.innerText = bcommand;
  infobutton.setAttribute('id', bcommand);
  //Adding async function to the button
  infobutton.addEventListener('click', async function() {
    const response = await fetch(`http://127.0.0.1:3000/${bcommand}`);
    const data = await response.json();
    document.querySelector('#textbox').innerText = data[0]; //the text content is in the index 0
    document.querySelector('#buttonrow2').innerHTML = ""
    if (data.length === 2) { //the program checks if additional data was returned
      for (const item of data[1]) {
        const choicebutton = document.createElement('button');
        choicebutton.innerText = item;
        choicebutton.setAttribute('id', item);
        document.querySelector('#buttonrow2').appendChild(choicebutton)
      }
    }
  });
  //Adding the button to the first buttonrow
  document.querySelector('#buttonrow1').appendChild(infobutton);
}

statupdater();