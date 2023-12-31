# Presentation 

Drive [https://drive.google.com/drive/folders/1r2R1a2Uh0HGW785TPcJg9Z_YOYWYuKt1?usp=sharing]

----- 

# Installation Guide 

```
sudo apt install git openssh-server
```

----
## Clone repository

Clone the repository to the 'Documents' folder: 

```
cd
cd Documents/
```
```
git clone https://github.com/dialp123/tadhack2023.git
```
## Install Python 3

To install Python 3, in the terminal, run the following command:

```
  sudo apt install python3 python3-pip
```

The system will ask you to confirm the installation and show you the disk space that will be used. If you agree, press "y" and then "Enter" to begin the installation.

Once the installation is complete, you can check the Python 3 version by running the following command:

```
 python3 --version
```

The installed version of Python 3 should be displayed.

And that's it! You have installed Python 3 on your system.


Install the necessary packages to allow apt to use repositories over HTTPS:
   ```
   sudo apt install python3-env python3-flask
   ```

## Install Python dependencies

1. Navigate to the Python project directory, it is the directory called `weekly`.

   ```
   cd
   
   cd Documents/tadhack2023/
   ```

2. To manage Python dependencies, it is recommended to use a virtual environment. This allows you to isolate the project's dependencies from the rest of the system. If you do not have `virtualenv` installed, you can install it by running the following command:
   ```
   sudo apt install python3-virtualenv
   ```
3. Create the '.env' file: run the command `nano .env` and save the following there:
   ```
   nano .env
   ```
   Genered and paste API KEY OPENAI in that file .env
   ```
      OPENAI_API_KEY=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
   ```
   Verify this with:
   ```
   cat .env
   ```
4. Once `virtualenv` is installed, create a new virtual environment by running the following command in the terminal:
   ```
   virtualenv weekly
   ```

This will create a new directory called "env" that will contain the virtual environment.

5. Activate the virtual environment by running the following command:
     ```
     source weekly/bin/activate

6. Once inside the virtual environment, you can install the project dependencies using the `pip` package manager. In the root directory of the project, there is usually a `requirements.txt` file that lists all the necessary dependencies.

    Run the following command to install all project dependencies:

   ```
   pip install -r requirements.txt
   ```
   Congratulations, the project is ready to run

----
# Run the Project  

1. Navigate to the Python project directory, it is the directory called `tadhack2023`.

   ```
   cd
   cd tadhack2023/
   ```
2. Use this command to run the project
   ```
   flask --app app run --debug
   ```
3. In your internet web browser use this link (T):
   ```
   http://localhost:5000/
   ```
