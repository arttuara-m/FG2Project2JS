"use strict";

async function statupdater() {
  const response = await fetch(`http://127.0.0.1:3000/status`);
  const data = await response.json();
  document.querySelector("#showscore").innerText = "Score: " + data[0];
  document.querySelector("#showmoney").innerText = "Money: " + data[1];
  document.querySelector("#showtimeunits").innerText = "Timeunits: " + data[2];
  document.querySelector("#showairport").innerText = "Airport: " + data[3];
  document.querySelector("#showgthreat").innerText =
    "Global threat: " + data[4];
  document.querySelector("#showlthreat").innerText = "Local threat: " + data[5];
}

async function turnrefresher() {
  const response = await fetch(`http://127.0.0.1:3000/turnupdate`);
  console.log(await response.text());
}

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
    statupdater();

    if (data.length === 2) {
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
          if (bcommand === "use") {
            document.querySelector("#buttonrow2").removeChild(this);
          }
        });
        document.querySelector("#buttonrow2").appendChild(choicebutton);
      }
    }
  });
  //Adding the button to the first buttonrow
  document.querySelector("#buttonrow1").appendChild(infobutton);
}

const moveButton = document.createElement("button");
moveButton.innerText = "move";
moveButton.setAttribute("id", "move");
moveButton.addEventListener("click", async function () {
  const response = await fetch(`http://127.0.0.1:3000/move`);
  const data = await response.json();
  document.querySelector("#buttonrow2").innerHTML = "";
  document.querySelector("#textbox").innerText = data[0];
  if (data.length <= 2) {
    addAirportMarkers(data);
    for (const item of data[1]) {
      console.log("Airport found: " + item[1]);
      const choicebutton1 = document.createElement("button");
      choicebutton1.innerText = item[1];
      choicebutton1.setAttribute("id", item[1]);
      document.querySelector("#buttonrow2").appendChild(choicebutton1);
    }
  }
});

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
  location.reload();
});

turnrefresher();
statupdater();
