# Project Challenge
It was a project to automate email signatures in the google gsuite/workspace domain. He was getting stuck on the last part though, which is profile pictures. He was using GAM to request a list of users and their profile picture URL, which is saved into a CSV. Unfortunately, the way google tokenizes their profile pictures makes it so if he sent an email with the private URL, the recipient receives a silhouette image instead. However, if he resolves the private URL while logged into my google account he is able to resolve the profile picture.

The requirement was a python script that posts a request to the private URL and parses the response for the public-facing photo URL then replaces the private value with the parsed public value - repeat this process for each record.

<br><br>
# Solution
First, uses a feature that exists in GAM that downloads all user profile pictures locally each labeled with its user name, then iterates through all the Pics in a given directory to upload it to google drive, makes its permission public then append its link to the CSV. 

It also automate GAM process to setting and pushing users signatures. 

