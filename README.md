# CarProject
The aim of the project is to redirect automatically multiple drivers accross all the country.
1. The directory is split in multiple applications:
    - [AdminFront](https://github.com/phayusa/CarProject/tree/Test_User_As_Key/AdminFront) application : contains all the templates for manage the data of the site
    - [Back](https://github.com/phayusa/CarProject/tree/Test_User_As_Key/Back) application : contains all the settings of all the project
    - [Back_Sources](https://github.com/phayusa/CarProject/tree/Test_User_As_Key/Back_Source) application : rest service + model classes of the project
    - [Connections](https://github.com/phayusa/CarProject/tree/Test_User_As_Key/Connections) application : used to perform login/logout test
    - [Localisation](https://github.com/phayusa/CarProject/tree/Test_User_As_Key/Localisation) application : used to perform localisation test
    - [Front](https://github.com/phayusa/CarProject/tree/Test_User_As_Key/Front) application : contains all the template for the front site
2. Each application contains django model structure as MVC.
3. Before to make in production  ``` python manage.py collect static``` 
4. The project is linked to [android](https://github.com/phayusa/Car_App) application