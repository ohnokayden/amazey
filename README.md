# YOUR PROJECT TITLE
#### Video Demo:  <https://youtu.be/vvRVvrsHjEw>

#### Description:
#### Main Ideation
My project is called mazey and the idea behind it is an automatic maze generator that randomly generates a maze of size 10x10 (or any other dimension set by me). This is seen by the user which is able to interact with it through a 'window' in the front end, which communicates with the back end in order to refresh the back end and let the user solve new mazes and load new mazes.


#### Python and backend
This maze is generated, where first a blank slate, which is a 2d array is first generated, then a starting point is randomly generated using the random library. From there, I utilised a recursive function, called `choosePath`, where pathing of the maze is done recursively, where from one point, a direction is chosen and a path is created, from the new point, another random direction is chosen, this repeats until it can no longer, when the `checkValid` function returns `False` which is when it hits an outer wall or is met by a path already with an adjacent path. Since it is a perfect maze, there can be no loops and therefore, if 2 different branches were to meet, it would create a loop and no longer be perfect, therefore, such a restriction is necessary. After this, it would return to the caller function, which would then exhaust the other 3 directions in which it can go in a random order, eventually, the original caller function on the starting square would be called. Thus, creating the maze of the desired size. This is all done in python, which is then combined with the flask framework, in order to integrate it into a web app environment.


#### HTML front end design and integration
By utilising HTML and another popular framework called Bootstrap, I created a calming homepage, where users would be able to interact with the maze I had created. This maze was dynamically generated using the tools provided in Flask, more specifically, using functions like `render_template` combined with Jinja in Flask which allowed me to combine both front and backend. The main bulk of elements are present on the maze, which utilises Jinja's for loops and if conditionals to create the elements and give it its corresponding id. This was then decorated with CSS, with the main colour scheme being in black and words being in a blanched almond colour. Other instances of CSS where also used to position certain elements, and bootstrap was also used to integrate a modal pop-up to teach new users about how to use the website. However, a large majority of focus was instead spent on the back-end and front-end coding instead of making the website look pretty. For the front-end Javascript was used due to its synergy with HTML and how it can be event based.


#### Javascript
In my Javascript code, I wrote a few functions and retroactively denoted the start and end points with green and red respectively.


`formatString(x)`\
Takes in as input a list of coordinates, and then formats them in a way that they are the same as in the given id of the individual elements of the maze, this is essential for use with the built in `findElementById()` in Javascript.


`startPath(x)`\
This functions takes in as input an array which is from the backend of the next possible paths, the list is iterated through, and the next potential elements, highlighted are each made orange and given a event listener to run `turnGreen`, with the arguments of the coords and the formatted string, with `addEventListener` on a click.


`turnGreen(coords, formattedString)`\
This function is run when an element is clicked, and turns the clicked element green, when it turns green, the coords of the element is also passed into an array which will contain the list of elements clicked, which will later be used for server side validation in `endTurn`. It also is responsible for the "backspace" feature, where if the previously clicked on square is clicked, the square itr will reverted, calling the `revert` function and also reversing the addition of that coordinate to the answer array called `pathList`.


`revert(revertList)`\
This not only reverts the added coordinate to the answer array, but it also removes the added eventListeners to the previous potential paths, which is updated and kept in the `revertList`, and is also used both for choosing a new path and reversing the chosen path. This needs to be reassigned to an empty list after every function call.


`myCoords(coords)`\
This function serves to request new data from the server, it uses the inputted new chosen coordinate, uses the fetch api to send a POST request to the server, the server takes the chosen coordinate, and returns with the next possible positions according to its generated maze.


`reset()`\
This functions serves to refresh the whole maze when the user makes a big mistake in choosing their squares, it refreshes all of the important variables like `curLocationId` to its initial values, and ensures that all eventListeners added are removed and any new necessary ones are added, lastly, the answer array is also reset.  


`endTurn()`\
This function is added to the end coordinates and used to send the answer for server side validation, preventing malicious users from contaminating the result, if the server returns the the answer is valid, it will then send the essential information for a new maze to be generated. The new maze is created using the `createElement` function and the required information is all parsed using `JSON.parse` and `.json` for the responses themselves. After the new maze is created, the old maze is removed and the new maze is added in its same position with the same class and id as the previous maze in the same container. Lastly, all required event listeners are created again, and then the `startPath` function is once again called for the new starting coordinate.

