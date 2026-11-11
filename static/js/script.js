      console.log("JS is connected!");



      let revertList = [];
      let curLocationId = null;
      let lastLocationId = null;
      //  pathList contains locations, reset on new maze
      let pathList = [];
      pathList.push(startingCoords);


      function formatString(x)
      {
        return "(" + x[0] + ", " + x[1] + ")";
      }

      
        // aft turning in the needed location, send a post request to the server to get the next possible locations 
    //   async function myCoords(coords) { 
    //     let response =  await fetch("http://127.0.0.1:5000", {
    //       method: "POST",
    //       headers: {"Content-Type": "application/json"},
    //       body : JSON.stringify(coords)
    //     });

    //   let newList = await response.json();
    //   console.log(newList)
    //   startPath(newList);   
    // }    


    // new version of my coords

    function myCoords(coords)
    {
      console.log(coords)
      let choosingList = [];
      function checkPoint(yCoords,xCoords)
      {
        console.log(curLocationId)
        if (mazeMap[yCoords][xCoords] == 1)
        {
          
          choosingList.push([xCoords,yCoords]);
        }  
      }
      checkPoint(coords[1], coords[0] + 1);
      checkPoint(coords[1], coords[0] - 1);
      checkPoint(coords[1] - 1, coords[0]);
      checkPoint(coords[1] + 1, coords[0]);
      console.log(choosingList);
      startPath(choosingList);
      
    }

      function revert(revertList)
      {
        // reverses the prev eventListeners and temp chnages(orange)
        // needs the prev things that was changed -> revertList
        while(revertList.length != 0)
      {
        let elem = document.getElementById(revertList.pop());
        if (elem.style.backgroundColor != "green")
        {
          elem.style.backgroundColor = "black";
        }  
        let newElem = elem.cloneNode(true);
        elem.parentNode.replaceChild(newElem,elem);
        elem = newElem;
        // instead of removing event listener, possible to store the last two ele touched, letting only these two be touched + any orange? 
      }
      revertList = []
        // clear the revertList
      }

      function turnGreen(coords, formattedString)
    {
      let elem = document.getElementById(formattedString)
      lastLocationId = curLocationId;
      curLocationId = elem.id;
      if (elem.style.backgroundColor == "green")
    {
      pathList.pop();
      document.getElementById(lastLocationId).style.backgroundColor = "orange";
      revert(revertList);
      myCoords(coords);
      return;
    }
      pathList.push(coords);
      elem.style.backgroundColor = "green"; 
      revert(revertList);
      myCoords(coords);
    } 

  function startPath(cLs)
  {
    for ( let i = cLs.length; i > 0; i--)
    {
          let x = cLs[i-1];
          let formattedString = "(" + x[0] + ", " + x[1] + ")";
          let elem = document.getElementById(formattedString);
          if ( elem.style.backgroundColor != "green")
          {
            elem.style.backgroundColor = "orange";
          }
          revertList.push(formattedString);
          elem.addEventListener("click", function(){turnGreen(x, formattedString)});
    }
  }
  document.getElementById(formatString(startingCoords)).style.backgroundColor = "green";
  document.getElementById(formatString(endingCoords)).style.backgroundColor = "red";
  startPath(choosingList);



  function reset()
  {
    console.log("Resetting");
      while (revertList != 0)
      {
        let elem = document.getElementById(revertList.pop());
        elem.style.backgroundColor = "black";
        let newElem = elem.cloneNode(true);
        elem.parentNode.replaceChild(newElem,elem);
        elem = newElem;
      }
      curLocationId = null;
      lastLocationId = null;
      //  pathList contains locations, reset on new maze
      while (pathList.length != 0)
      {
        let elem = document.getElementById(formatString(pathList.pop()));
        elem.style.backgroundColor = "black";
        let newElem = elem.cloneNode(true);
        elem.parentNode.replaceChild(newElem,elem);
        elem = newElem;
      }
      pathList = [startingCoords];
      // TODO: to figure out why double pressing reset causes failure
      document.getElementById(formatString(startingCoords)).addEventListener("click",reset);
      document.getElementById(formatString(startingCoords)).style.backgroundColor = "green";
      startPath(choosingList);
  }
  document.getElementById("reset").addEventListener("click",reset);
  document.getElementById(formatString(startingCoords)).addEventListener("click",reset);



  async function endTurn(){
    // checks for correct end
    console.log(pathList);
    let response =  await fetch("http://127.0.0.1:5000", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body : JSON.stringify(pathList)
    });

    let x = await response.json();
    if (x == true)
    { 
      // gets data for new maze
      // console.log("getting new maze")
      let response2 =  await fetch("http://127.0.0.1:5000",{
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body : JSON.stringify("new map")
      });
      let y = await response2.json();
      mazeMap = y[0];
      choosingList = JSON.parse(y[1]);
      
      startingCoords = y[2];
      endingCoords = y[3];
      
    const newTable = document.createElement('table');
    for (i = 1; i < mazeMap.length - 1 ; i++)
    {
      // starts from 1 and ends at max - 1 to not include the boundaries
      const newRow = document.createElement('tr');
      for (j = 1; j < mazeMap[i].length - 1; j++)
      {
        // same as above
        const newData = document.createElement('td');
        newData.id = formatString([j, i]);
        if (mazeMap[i][j] == 3)
        {
          newData.innerText= "X";
        }
        newRow.appendChild(newData);
      }
      newTable.appendChild(newRow);
    }

    const oldMaze = document.getElementById("maze");
    oldMaze.remove();
    mazeContainer = document.getElementById("container");
    newTable.className = "maze";
    newTable.id = "maze";
    mazeContainer.appendChild(newTable);
// To add after changing html
    document.getElementById(formatString(startingCoords)).style.backgroundColor = "green";
    document.getElementById(formatString(endingCoords)).style.backgroundColor = "red";
    document.getElementById(formatString(endingCoords)).addEventListener("click", endTurn); 
    document.getElementById(formatString(startingCoords)).addEventListener("click",reset);
    pathList = [startingCoords];
    startPath(choosingList);

  }


  }
  document.getElementById(formatString(endingCoords)).addEventListener("click", function() {endTurn(pathList)});