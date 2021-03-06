# Usage

For a simpler execution, we are assuming the command to run this script is aliased to `amt`.  
We need an sftp client on our phone for this to work. We'll be using **primitive sftpd** in this example.  

1.  First, we need to set the correct path of the directory contaning the manga directories.  
    This is done by hardcoding the path to the variable `MANGA_PATH`.

2.  Now it's time to register your sftp credentials. We do this through the command:  
    
        $ amt register

3.  Once this is done, we are ready to transfer manga to our smartphone.  
    We can list available manga by executing:  
    
        $ amt list
    
    After choosing a valid manga, we can transfer chapters by doing:  
    
        $ amt [manga_name] [first_chapter] [last_chapter]
    
    For example, if we want to transfer the chapters 50 through 60 of `dr_stone`, we type:  
    
        $ amt dr_stone 50 60
    
    **OBS.:** If we only need to transfer one chapter, we can do that by providing that chapter number  
    as `[first_chapter]` and no `[last_chapter]`.  
    e.g.:  
    
        $ amt dr_stone 51

