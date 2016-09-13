# Creating CONNECT PDFS

## Requirements
### Server
This script is intended to run with the [CTData Report Server](https://github.com/CT-Data-Collaborative/reports) already running somewhere. As of writing, it is set up to run with the PDF server running locally - ie download the report server repository, navigate to it and run `vagrant up` to launch it. If you have deployed this server in a different fashion, you will have to update the endpoints in the `make_pdfs.py` script.

### Local
##### Python
1.   Requests - http://docs.python-requests.org/en/master/
      +   `sudo pip install requests`
##### Data
1.   The data file that contains all the town profile data should be in the same directory as the `make_pdfs.py` script.
      +   **N.B** this must be the request data *as the pdf server expects it!* This file should be called `pdf-request.json` and should be same level in the directory as the python script. This can be generated using the tools provided in the [Connect Data repository](https://github.com/CT-Data-Collaborative/connect-data).


## Instructions
1.   Make sure the pdf server is running.
      + This should be as simple as `vagrant up` in the `reports` project directory, unless there have been any major changes to that project or its repository. The server will automatically start the process and serve pdf responses.
      + **N.B.** If you've changed your vagrant script and are not using the pre-set IP address for your virtual machine, you will need to change the IP addresses used in `make_pdfs.py`.
2.   Run the included python script.
      + Navigate to this directory in your command line and execute `python make_pdfs.py`, remember that the data file needs to be in the same directory, at the same level, and named `pdf-request.json`.

## Under the hood
1.   The python script will iterate through each Region, pulling out that regions data from each viz object in the request, and making a new request with just that regions data.
2.   As it iterates, the script will save each newly formed request JSON to file.
3.   Finally, each iteration will also send the request to the pdf server. Barring any errors (there shouldn't be any!) it will receive the pdf response, and save that to file. Your newly created pdfs will be named for the region they represent.
