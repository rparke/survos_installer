
#first create a conda environment containing python, constructor, pyyaml
# conda env create --name <environment name>
# conda activate <environment name>
# conda install python, constructor, pyyaml

import os
import sys
import yaml





#Load the config file
CONFIG_FILE = "config.yaml"
with open(CONFIG_FILE, "r") as f:
    config_data = yaml.safe_load(f)
YAML_ENVIRONMENT = config_data['YAML_ENVIRONMENT']
NAME = config_data['NAME']
VERSION = config_data['VERSION']
CHANNELS = config_data["CHANNELS"]
LICENSE_FILE = config_data["LICENSE_FILE"]
POST_INSTALL_TEMPLATE_BASH = config_data["POST_INSTALL_TEMPLATE_BASH"]
POST_INSTALL_TEMPLATE_WINDOWS = config_data["POST_INSTALL_TEMPLATE_WINDOWS"]
INSTALLER_VERSION = config_data["INSTALLER_VERSION"]
WINDOWS_RELOCATE = config_data["WINDOWS_RELOCATE"]





class Installation_Generator():
    
    def __init__(self, 
                 environment_yaml,
                 name,
                 version,
                 channels,
                 license_file,
                 construct_file = "construct.yaml",
                 post_install_template_bash = POST_INSTALL_TEMPLATE_BASH,
                 post_install_template_windows = POST_INSTALL_TEMPLATE_WINDOWS,
                 installer_version = INSTALLER_VERSION,
                 windows_relocate = WINDOWS_RELOCATE,
                 windows_yaml_file_name = "windows_update.yaml"):
        self.environment_yaml = environment_yaml
        self.name = name
        self.version = version
        self.channels = channels
        self.license_file = license_file
        if installer_version == "windows":
            self.post_install_file = "post_install.bat"
            self.post_install_template = post_install_template_windows
        else:
            self.post_install_file = "post_install.sh"
            self.post_install_template = post_install_template_bash
        
        self.construct_file = construct_file
        self.installer_version = installer_version
        self.windows_relocate = windows_relocate
        self.windows_yaml_file_name = windows_yaml_file_name
        #Parameters for the construct.yaml template
        
    
    
    def run(self):
        
        #Create the environment.yaml and post_install.sh temp files
        #to be used by conda constructor and save them in the installation directory
        
        #creates construct.yaml file used to define conda dependencies
        self._generate_constructor_environment_yaml()
        #generates post_install script used to handly installation of pip dependencies
        #and generation of launcher
        self._generate_post_install_script()
        
        if self.installer_version.lower() == "windows":
            self._generate_windows_yaml_update(self.windows_yaml_file_name)
        
        # Call conda constructor on the temp yaml and sh files created above
        # and create an installer in the same directory
        self._run_constructor()
        
        
        #Clean up temporary install scripts
        self._cleanup_environment_yaml()
        self._cleanup_post_install_script()
    
    
    

        
    
        
    
    def _parse_yaml(self):
        with open(self.environment_yaml) as f:
            #self.environment = yaml.safe_load(f)
            return yaml.safe_load(f)

    

    def _get_conda_dependencies(self):
        if self.installer_version.lower() == "linux":
            yaml_environment = self._parse_yaml()
            return yaml_environment['dependencies'][:-1]
    
        if self.installer_version.lower() == "windows":
            yaml_environment = self._parse_yaml()
            conda_dependencies =  yaml_environment['dependencies'][:-1]
            conda_dependencies_final = []
            for dependency in conda_dependencies:
                add_to_list = True
                for migrated_dependency in self.windows_relocate:
                    if dependency == migrated_dependency:
                        add_to_list = False
                if add_to_list:
                    conda_dependencies_final.append(dependency)
            return conda_dependencies_final 
        
    def _get_pip_dependencies(self):
        yaml_environment = self._parse_yaml()
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
        if self.installer_version == 'linux':
            post_install_template = "#!/bin/bash \n"
       
            #Add pip install commands to the script
            for dependency in self._get_pip_dependencies():
                post_install_template += (f"$PREFIX/bin/pip install {dependency}\n")
    
                  
        
        if self.installer_version == 'windows':
            
            #Create install spinner.
            #This is needed to set the correct environment variable for the
            #top level directory of the survos repo
            self.install_spinner = "install.bat"
            with open(self.install_spinner, "w") as f:
                spinner_text = "set survos_directory=%CD%\n"
                spinner_text += f"call {self.name}-{self.version}-Windows-x86_64.exe"
                f.write(spinner_text)
            
            
            #Generate post_install script to manage installation of pip dependencies
            #activate conda environment
            post_install_template = "call %~dp0..\Scripts\activate.bat\n"
            
            
            for dependency in self._get_pip_dependencies():
                post_install_template += (f"pip install {dependency}\n")
                

        #Write template text to post_install file

        with open(self.post_install_template) as f:
            for line in f:
                post_install_template += line




        #save the post install script to file
        with open(self.post_install_file, "w") as f:
            f.write(post_install_template)


            

    def _generate_windows_yaml_update(self, name):
        yaml_environment=self._parse_yaml()
        with open(name, "w") as f:
            yaml.dump(yaml_environment, f)
            
    def _cleanup_environment_yaml(self):
        os.system(f"rm {self.construct_file}")
    
    def _cleanup_post_install_script(self):
        os.system(f"rm {self.post_install_file}")


    def _run_constructor(self):
        os.system("constructor")
    
    
ig = Installation_Generator(YAML_ENVIRONMENT, NAME, VERSION,CHANNELS, LICENSE_FILE)  
#ig._generate_constructor_environment_yaml()
ig._generate_post_install_script()
#ig.run()

