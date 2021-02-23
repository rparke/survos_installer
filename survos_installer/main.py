


import os
import sys
import yaml



YAML_ENVIRONMENT = "/Users/richardparke/Documents/survos_installer/tests/survos2_clean_environment_linux.yml"
NAME = "survos_installer"
VERSION = "0.0.1"
CHANNELS = ['pytorch', 'anaconda', 'defaults', 'conda-forge']
LICENSE_FILE = "license.txt"


class Installation_Generator():
    
    def __init__(self, 
                 environment_yaml,
                 name,
                 version,
                 channels,
                 license_file,
                 post_install_file = "post_install.sh",
                 construct_file = "construct.yaml"):
        self.environment_yaml = environment_yaml
        self.name = name
        self.version = version
        self.channels = channels
        self.license_file = license_file
        self.post_install_file = post_install_file
        self.construct_file = construct_file
        
        #Parameters for the construct.yaml template
        
    
    
    def run(self):
        
        #Create the environment.yaml and post_install.sh temp files
        #to be used by conda constructor and save them in the installation directory
        self._generate_constructor_environment_yaml()
        self._generate_post_install_script()
        
        # Call conda constructor on the temp yaml and sh files created above
        # and create an installer in the same directory
        self._run_constructor()
        
        
        #Clean up temporary install scripts
        self._cleanup_environment_yaml()
        self._cleanup_post_install_script()
    
    
    
    def print_parameters(self):
        self._parse_yaml()
        
        print(f"name = {self.name}")
        print(f"version = {self.version}")
        print(f"license_file = {self.license_file}")
        
    
    def _print_current_working_directory(self):
        print(f"Current working directory: {os.getcwd()}")
        answer = input("Is this the directory containing your environment.yml file?")
        if answer == "yes" or answer == "y":
            pass
        else:
            new_directory = input("Type in the name of your new directory")
            os.chdir(new_directory)
        print(f"Executing from current working directory: {os.getcwd()}")
        
    
    def _parse_yaml(self):
        with open(self.environment_yaml) as f:
            #self.environment = yaml.safe_load(f)
            return yaml.safe_load(f)

    
    
    def _get_conda_dependencies(self):
        #self._parse_yaml()
        yaml_environment = self._parse_yaml()
        #self.conda_dependencies = self.environment['dependencies'][:-1]
        return yaml_environment['dependencies'][:-1]
        
        
    def _get_pip_dependencies(self):
        #self._parse_yaml()
        yaml_environment = self._parse_yaml()
        #self.pip_dependencies = list(self.environment['dependencies'][-1].values())[0]
        return list(yaml_environment['dependencies'][-1].values())[0]
        
        
    def _generate_constructor_environment_yaml(self):
        #self._get_conda_dependencies()
        yaml_template = {'name': self.name,
                         'version': self.version,
                         'channels': self.channels,
                         'specs': self._get_conda_dependencies(),
                         'license_file': self.license_file,
                         'post_install': self.post_install_file}
        

        
        with open(self.construct_file, "w") as f:
            yaml.dump(yaml_template, f)
    
    
    def _generate_post_install_script(self):
        self._get_pip_dependencies()
        
        #bash preable
        post_install_template = "#!/bin/bash \n"
        #message indicating start of pip installation
        post_install_template += 'echo "starting install of pip dependencies" \n'
        
        #Add pip install commands to the script
        for dependency in self._get_conda_dependencies():
            post_install_template += (f"$PREFIX/bin/pip install {dependency}\n")
            
        #save the post install script to file
        with open(self.post_install_file, "w") as f:
            f.write(post_install_template)
            
    def _cleanup_environment_yaml(self):
        os.system(f"rm {self.construct_file}")
    
    def _cleanup_post_install_script(self):
        os.system(f"rm {self.post_install_file}")


    def _run_constructor(self):
        os.system("constructor")
    
    
ig = Installation_Generator(YAML_ENVIRONMENT, NAME, VERSION,CHANNELS, LICENSE_FILE)  
ig._generate_constructor_environment_yaml()
ig._generate_post_install_script()

