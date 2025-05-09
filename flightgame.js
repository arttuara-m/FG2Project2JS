"use strict";

async function timeChecker(){
    const response = await fetch(`http://127.0.0.1:3000/checkmoves`)
    //console.log("Checking time...")
    const data = await response.json()
    //console.log(data)
    if (data[0] === false){
        alert("YOU HAVE RUN OUT OF TIME! TIME TO LEAVE!!")
    } else if (data[1] <=2){
        alert("You are soon out of time! Consider leaving soon!")
    }
}

async function statupdater() {
  const response = await fetch(`http://127.0.0.1:3000/status`);
  const data = await response.json();
  document.querySelector("#showscore").innerText = "Score: " + data[0];
  document.querySelector("#showmoney").innerText = "Money: " + data[1];
  document.querySelector("#showtimeunits").innerText = "Timeunits: " + data[2];
  document.querySelector("#showairport").innerText = "Airport: " + data[6];
  document.querySelector("#showgthreat").innerText =  "Global threat: " + data[4];
  document.querySelector("#showlthreat").innerText = "Local threat: " + data[5];
  await timeChecker()
}

async function turnrefresher() {
    console.log("Updating map...")
    await mapUpdater();
    const response = await fetch(`http://127.0.0.1:3000/turnupdate`);
    console.log(await response.text())
}

async function eventChecker(){
    console.log("Checking events...")
    const response = await fetch(`http://127.0.0.1:3000/doevent`)
    const data = await response.json()
    document.querySelector("#textbox").innerText = data[0]
    console.log(data[0])
}

//Command labels for buttons
const commands = ["info", "check", "use", "buy", "work"];
//Creates the first button row
for (const bcommand of commands) {
  //Creating the button
  const infobutton = document.createElement("button");
  infobutton.innerText = bcommand;
  infobutton.setAttribute("id", bcommand);

  //Adding async function to the button
  infobutton.addEventListener("click", async function () {
    const response = await fetch(`http://127.0.0.1:3000/${bcommand}`);
    const data = await response.json();
    document.querySelector("#textbox").innerText = data[0]; //the text content is in the index 0
    document.querySelector("#buttonrow2").innerHTML = "";
    //statupdater(); en usko et tätä tarvii enää?

    if (data.length >= 2) {
      //the program checks if additional data was returned
      for (const item of data[1]) {
        const choicebutton = document.createElement("button");
        choicebutton.innerText = item;
        choicebutton.setAttribute("id", item);
        choicebutton.addEventListener("click", async function () {
          console.log(this.id);
          const response2 = await fetch(
            `http://127.0.0.1:3000/${bcommand}item/${this.id}`,
          );
          const data2 = await response2.json();
          document.querySelector("#textbox").innerText = data2[0];
          statupdater();

          for (let i in data[1] ){
              document.getElementById("buttonrow2").innerHTML = '';
          }
        });
        document.querySelector("#buttonrow2").appendChild(choicebutton);
      }
    }
  });
  //Adding the button to the first buttonrow
  document.querySelector('#buttonrow1').appendChild(infobutton);
}


//Adding a button to move from an airport to another
const moveButton = document.createElement('button')
    moveButton.innerText="move"
    moveButton.setAttribute('id', 'move')
    moveButton.addEventListener('click',async function() {
        const response = await fetch(`http://127.0.0.1:3000/move`)
        const data = await response.json()
        document.querySelector('#buttonrow2').innerHTML = ""
        document.querySelector('#textbox').innerText = data[0]
        if (data.length <= 2){
            addAirportMarkers(data)
            for (const item of data[1]) {
                console.log('Airport found: '+item[1])
                const choicebutton1 = document.createElement('button');
                choicebutton1.innerText = item[1]
                choicebutton1.setAttribute('id', item[1]);
                choicebutton1.addEventListener("click",async function(){
                    console.log(this.id)
                    const response2 = await fetch(
                        `http://127.0.0.1:3000/moveto/${this.id}`,
                    );
                    const data2 = await response2.json()
                    console.log(data2[0])


                    //delete airport buttons
                    for (let i in data[1] ){
                        //these 2 log html data, was used to locate what needed to be deleted
                        //console.log(data[1][i])
                        //console.log( document.getElementById("buttonrow2").children )
                        document.getElementById("buttonrow2").innerHTML = '';
                    }
                    //clear text box
                    document.querySelector('#textbox').innerText = ""


                    //Calls the updatable variable updating functions to update all
                    // the updatable variables sometimes in need of updating
                    // that currently may be needed to be updated to update
                    // these updatable variables that are sometimes updated.
                    //In other words for thee; For all ever so dependable functions which this concerns, the code
                    // it giveth the upmost urgent order to deliver the latest tidings of the realm
                    // for the most sovereign of the highly regarded variables that this occurrence may be of concern.
                    await turnrefresher()
                    await eventChecker()
                    await statupdater()
                    clearMapMarkers()
                    mapUpdater()
                })
                document.querySelector('#buttonrow2').appendChild(choicebutton1)
            }}
   })

document.querySelector("#buttonrow1").appendChild(moveButton);

const resetbutton = document.querySelector("#resetbutton");

resetbutton.addEventListener("click", async function () {
  const confirmReset = window.confirm(
    "Are you sure you want to reset the game?",
  );
  if (!confirmReset) return;

  const response = await fetch(`http://127.0.0.1:3000/resetgame`);
  console.log(await response.text());
  turnrefresher();
  statupdater();
  location.reload()
  console.log("Updating map...")
  mapUpdater();
})


turnrefresher();
statupdater();
