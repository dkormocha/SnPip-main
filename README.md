# SnPip

Connecting your machine to the SnPip database stored on in a google cloud instance.

1. log into https://console.cloud.google.com/ using the provided email bellow.

       Email: snpip332022@gmail.com
  
       Password: my-secret-password

2. In the navigation menu (the three bars located on the top left of the website) select SQL, this will bring up the snpip database.

![image](https://user-images.githubusercontent.com/83500298/156592349-08711acf-672c-4824-bec9-d53c6edfa1cb.png)

![image](https://user-images.githubusercontent.com/83500298/156592797-5ac6d947-e451-463c-80d1-b11a9c4114db.png)

3. Select the snpip database (directly bellow the instance ID) This will bring you to the snpip db overview page.

![image](https://user-images.githubusercontent.com/83500298/156595465-cfd2baf1-df24-4ee6-bf4d-28371d254a7e.png)

4. From the overview page select the connections tab

![image](https://user-images.githubusercontent.com/83500298/156596093-bb90b8a8-8ea0-49db-b225-7c40849947cf.png)

5. Once on the connection page scroll down untill you reach ADD NETWORK (Nothing else needs to be interacted with)

![image](https://user-images.githubusercontent.com/83500298/156597057-65f3f5fb-25d7-475a-8fbb-a7625692658f.png)

6. Click on the ADD NETWORK button and input:

         The network name in the name box
         
         Your machines ip address (IPV4) (which can be found here: https://whatismyipaddress.com/) in the ip box
         
![image](https://user-images.githubusercontent.com/83500298/156597489-0070ee45-3073-486b-87bd-b5981e53d0e4.png)

7. Click the DONE button

8. Scroll down till you reach the blue SAVE button and save your newly created network. In the bottom left hand corner of the screen you will notice a window
   showing the time taken for the current operation to execute (in this case it will be saving you newtork), once a green check mark has appaared then the your
   network is saved.
  
   
 Congratulations! You are now authorised to connect to the SnPip database.
 
 
 
 
 Running the Web application!
 
 1) Open your command line or terminal
 2) Check the requirments.txt table for all the dependencies
 3) On command line/terminal install all the dependencies using the pip install command
 4) Once all the dependencies have been installed, cd into the web application folder
 5) Then run command > python main.py to host the Web application locally
 6) Search or click on http://127.0.0.1:5000/ to view web application


 
