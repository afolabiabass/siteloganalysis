# Log  Analysis Project
This project is on mining data of articles visited on a website to get must populous article, its author and to see on which days visit led to errors.

## Requirements

* Vagrant
* VirtualBox
* Python v2.7
* PostgreSQL
* psycopg2

## Instructions
To run this analysis follow the instructions given below

* Once you have Vagrant and VirtualBox installed on your computer
* Download the contents of this file 
* From the command line, navigate to the folder containing the contant of this file 
* Power up the virtual machine by typing: vagrant up note: this may take a couple minutes to complete
* Once the virtual machine is done booting, log into it by typing: vagrant ssh
* Download the log data to be used for analysis. This can be found here
[here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
* Place the log data sql file after extracting it and place it in your working directory.
* Now that you are logged into the virtual machine go to the directory shared directory /vagrant
* Run the psql -d news -f newsdata.sql to load the data in to the database
* Finally run python log.py
