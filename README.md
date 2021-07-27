# cs180project-021-hackerman
cs180project-021-hackerman created by GitHub Classroom      

### Description
This project is a data store that analyzes information about YouTube video data in different countries, and how each country's information compares with others (e.g. which videos are more popular between the United States and Germany). This project uses data from four countries: the United States (US), Germany (DE), Canda (CA), and the United Kingdom (UK).

### IMPORTANT 
Please Download Docker Desktop first and docker extension in Visual Studio Code before running docker. 

### Setting Up the Server and Running It within Docker
To turn on the website, the user needs to do the following commands in the terminal:

`cd cs180project-021-hackerman/mysite`

`source venv/bin/activate`

If this is your first time downloading this, you need to install the following things. Otherwise, you can skip this step:
## Download Docker 
Download Docker for Windows: https://www.docker.com/products/docker-desktop

Download Docker for Mac: https://hub.docker.com/editions/community/docker-ce-desktop-mac?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header
 
Download Docker for Linux: https://hub.docker.com/search?offering=community&operating_system=linux&q=&type=edition

Download Docker Extension for VS Code: https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker

### Steps to run the server by using Docker
To run the server, First build the docker image in Visual Studio Code or any terminal

`docker build --tag python-django . `

Then, check if the image has been built correctly

`docker images`

Last, run the docker image

`docker run --publish 8000:8000 python-django`

Once the command prompt has it up and running, go to `localhost:8000`.

Viola, The website is up and running within Docker!

### Turning Off the Server
To deactivate the website, you need to run `deactivate` in the terminal command line. Do this before exiting the terminal! 
Another way to deactivate the website, press control+c on command line and it will kill the program.

## Authors and Contributor List

* Christian Campos - https://github.com/ccamp032
* Chris Daniels - https://github.com/ChairMane
* Sameh Fazli - https://github.com/sfazli96
* Alexander Ku - https://github.com/aku006
