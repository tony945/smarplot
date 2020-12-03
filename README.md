# smarpot
An IOT project that determines the irrigation frequency and total water applied according to Temperaure, Humidity and Solar Radiation

===
**Deployment**

    1. Import the packages in the requirement.txt with the following command 
	
	    ...........................................
		pip install -r path_to_file/requirement.txt
		...........................................
		
	2. Configure database settings and migrate model to your local db

       1) Configure your database connection in plant/settings.py

       2) Create a database according to your configuration

       3) makemigrations & migrate

           ........................................
           path_to_file/manage.py makemigrations
           path_to_file/manage.py migrate
           ..........................................


    3. Write the following .py file in gui/service/ to crontab for routine execution

        Enter peraonal crontab config
        ......................
        crontab -u username -e
        ......................

        Add the following to file
        .................................................
        */20 * * * * python3 path_to_file/sensors.py
        10 0 * * * python3 path_to_file/dailysensors.py
        10 0 1 * * python3 path_to_file/monthlysensors.py
        .................................................

    4. Bug in Django mysql connection

        When trying to activate django webserver, a bug occurs
        .................................
        path_to_file/manage.py runserver
        ................................

        An alert calls that version of mysql driver is not compatable
        Find the location of the code that triggers this alert and comment out the two lines

    


	