## Glue Job

A pyspark application used to curate or perform client-specific, function-specific, and/or highly customized transformations. 

## Development

### Prerequisites

1. Docker version 23.0.3 or greater
2. Tested on ubuntu 20.04.4 LTS
3. Git version 2.25.1 or greater
4. Visual Studio Code bu - Dev Containers v0.288.1
5. AWS IAM Credentials to access integrated AWS resources

### Installation

1. Clone the project repository.
   ```sh
   git clone git@gitlab.com:importgenius/data-engineering/importgenius-glue-libraries.git
   ```
2. Within the service's root directory, under .devcontainer subfolder, copy devcontainer.json.dist to devcontainer.json. Replace the values enclosed by angle braces with valid configuration values.
3. Open the VS Code's Command Palette and choose "Dev Containers: Open Folder in Container".
4. Select the folder containing the .devcontainer subfolder.
5. VS code will open a new window and install all softwares, tools, extensions, and dependencies based on .devcontainer.json to build a full-time dev container to be used for development. This includes AWS Glue ETL Libraries, PySpark engine, Git and git auto-completion feature, VS code extensions, and all other OS packages and dependencies.
6. Install package dependencies from lock file by executing
   ```sh
      poetry install
   ```

### Setup Guidelines
The following guidelines have been tested using the specified version of Ubuntu under the Prerequisites Section.
1. The container's default user, glue_user, has complete access to the packages, folders, and files installed in the container to develop AWS Glue Job and PySpark Applications. Therefore, it is recommended to avoid changing the file ownership settings and the glue_user's GID/UID.
2. Since the host owns the workspace or project folder that has been mounted to a container's directory, which is usually /workspaces/, glue_user might not have enough permission to access the folder if it has a different UID/GID than the host user.
3. This can be resolved by creating a new user account in the host system with the same UID/GID as the glue_user in the container.
4. Then execute the following command. Replace </path/to/folder> with the path of the project folder in the host
   ```sh
      sudo setfacl -R -m u:glue_user:rwx </path/to/project-repository>
   ```
5. Do the same for the aws config folder.
   ```sh
      sudo setfacl -R -m u:glue_user:rwx </path/to/aws-config-folder>
   ```
6. Test whether your development environment is properly configured by running test_glue_setup.py file within the project directory.

7. If it runs successfully, then you're all set. Happy coding!

### Spark History Server

To run spark history server, execute the following command.

```sh
/home/glue_user/spark/sbin/start-history-server.sh
```

The application will be running at port 18080 by default. You may open the browser of your choosing to access it.


### Recommendations
1. If you are using VS Code as your IDE, you may utilize configurations under .vscode folder to streamline development and debugging. Create JSON copies of the .dist files then provide valid configuration values.
2. In order for the launch.json to work when running the scripts in debugging mode, ensure that Poetry created the virtual environment in .venv/bin/python. This can be achieved or rectified by executing the following command(s).
   - Delete the cached, existing virtual environment for the project if any.
      ```sh
         rm -rf ~/.cache/pypoetry/virtualenvs/<virtual-env>
      ```
   - After that, specify a new environment directory.
      ```sh
         poetry config virtualenvs.in-project true
         poetry install
      ```
      This will create a .venv directory.

## Deployment

### Curation Package
At the time of writing, AWS Glue can manage a job's package dependencies that could be custom and internal via wheel files. To create a wheel file using poetry, execute
```sh
   poetry build --format wheel
```