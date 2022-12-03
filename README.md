# KStore Frontend
## Launching
The front end is served using a Node.JS server.  
To launch said Node server, run:  
```
npm install
npm run start
```

e Python dependencies for the local server using `python -m pip install -r requirements.txt`. Once you do this once, you won't have to do it again until the `requirements.txt` file is changed.
1. In a terminal, run the command `./runDatabase.sh`. This will initialize and run the MySQL server for as long as the window is open.
	- It might also ask for some additional setup before running! Watch for green text and non-zero exits. You might need to supply the path you downloaded MariaDB to in the `.mariadb_path` file.
	- If everything goes well, the script will print `Running MySQL Server at port <PORT>! Press Ctrl+C in terminal to stop.` and it will start listening for connections.
1. In another terminal, run `python main.py`. This will communicate with MySQL and 
