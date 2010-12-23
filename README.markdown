#[Funky Log Seer (FLS)](https://github.com/joshsziegler/funky_log_seer)  

##License  
Copyright 2010 Josh Ziegler  
  
This file is part of Funky Log Seer (FLS)  
  
Funky Log Seer (FLS) is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, either version 3 of the License, or  
(at your option) any later version.  
  
Funky Log Seer (FLS) is distributed in the hope that it will be useful,  
but WITHOUT ANY WARRANTY; without even the implied warranty of  
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the  
GNU General Public License for more details.  
  
You should have received a copy of the GNU General Public License  
along with Funky Log Seer (FLS). If not, see <http://www.gnu.org/licenses/>.  
  
##About  
Funky Log Seer (FLS) is basically a web interface for grep.  It doesn't actually use grep, as it is pure Python, but that's the easiest way to understand it.  I built this because I wanted to easily search all of our server logs (which were being pushed to a central server via syslog) using a simple web interface.  I had used [Clarity](https://github.com/tobi/clarity) and loved its simplicity, but couldn't stomach its security problems.  Plus I have a bias towards Python. :)   
    
FLS allows you to use Python's powerful regular expression syntax to search files in a given directory (minus the plus sign, ampersand, and questions mark).  It also has basic options for selecting an individual file, limiting output, reversing the search order, and updating the search results every 10 seconds (using asynchronous requests).  A simple help page includes information on the options and some basic expressions for searching typical syslog entries.  
  
**Note:** FLS does not do event correlation, alerts, graphing, or anything besides search.  

## Performance
At my last job, we ran FLS on a dedicated VM which could search logs for a dozen servers/appliances without issue.  I have not done any serious testing beyond that, but it seems to be roughly equivalent in speed to grepping the same files at the command line.   
  
# Security / Information Assurance  
No user input is executed at the command line, and everything is checked for validity/length. While FLS allows you to search any file in a specified directory, it does not take the user's input as a file name.  It only passes back the base of the file name (sans ".log") and looks that up in a dictionary of acceptable files.   
  
I am not aware of a method which the regex input can be exploited as it is checked for length (max 50 chars) and passed to `re.compile()` which should handle invalid input just fine.  If anyone can take a look at my code and help me out here, it would be appreciated.   
  
##System Requirements  
- Apache    
- Python 2.5    
- [Mako Templates](http://www.makotemplates.org/)   
    
  
##Setup / Installation  
FLS is a simple CGI application, so if you like, you can simply drop it in your /var/www/html/ directory and the example Apache config file in /etc/httpd/conf.d/ and be done with it.  Running FLS under mod_python should give you a speed boost, but I have yet to do this.  
  
##Setup / Installation
FLS is a simple CGI application, so if you like, you can simply drop it and the example Apache config file in and be done with it.  Running FLS under mod_python should give you a speed boost, but I have yet to do this.  
    
###Basic Install  
**Note: These instructions assume you have Apache and Python 2.5 already installed.**  
1. `git clone git://github.com/joshsziegler/funky_log_seer.git`   
2. `sudo cp funky\_log\_seer/fls /var/www/html/`  
3. `sudo cp funky\_log\_seer/fls/fls.conf /etc/httpd/conf.d/`  
4. `sudo /etc/init.d/apache restart`  
  
##Thanks  
- Tobias Lütke - The entire look of FLS was taken from [Tobi's](https://github.com/tobi) [Clarity]() tool.  I am not a web developer, nor am I artistic, so I deeply appreciate his work and open source code!  I owe you Tobi...   
- Chad Myslinsky - For supporting me while developing FLS and giving me the resources to put it into action at work. Thanks for letting me do my thing Chad..  
