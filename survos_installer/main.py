


import os
import sys
import yaml




# Pytorch is a large dependency that pushes NSIS above its 2GB limit for windows
# The following list should contain pytorch and any packages that depend on pytorch
# to prevent it being distributed within the installer file.
# This can be verified by creating the install environment with the following
# > conda env create -f <yaml file containing environment>
# > conda activate <environment name/ or path>
# and then listing the packages that have pytorch as a dependency using conda-tree
# > conda install -c conda-forge conda-tree
# > conda-tree whoneeds pytorch
#WINDOWS_CONDA_MIGRATION_TO_BATCH = ['pytorch', 'torchvision']


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
                 installer_version = INSTALLER_VERSION):
        self.environment_yaml = environment_yaml
        self.name = name
        self.version = version
        self.channels = channels
        self.license_file = license_file
        if installer_version == "windows":
            self.post_install_file = "post_install.bat"
            self.post_install_template = post_install_template_bash
        else:
            self.post_install_file = "post_install.sh"
            self.post_install_template = post_install_template_windows
        
        self.construct_file = construct_file
        self.installer_version = installer_version
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
        
    
        
    
    def _parse_yaml(self):
        with open(self.environment_yaml) as f:
            #self.environment = yaml.safe_load(f)
            return yaml.safe_load(f)

    

    def _get_conda_dependencies(self):
        #self._parse_yaml()
        yaml_environment = self._parse_yaml()
        #self.conda_dependencies = self.environment['dependencies'][:-1]
        if self.installer_version.lower() == "linux":
            return yaml_environment['dependencies'][:-1]
        
        if self.installer_version.lower() == "windows":
            yaml_dependencies_initial = yaml_environment['dependencies'][:-1]
            for dep in yaml_dependencies_initial:
                pass
            
        
        
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
        
        
        #Linux Version
        if self.installer_version.lower() == 'linux':
            post_install_template = "#!/bin/bash \n"
            for dependency in self._get_pip_dependencies():
                post_install_template += (f"$PREFIX/bin/pip install {dependency}\n")
                
         
        
          
        #Windows Version
        if self.installer_version.lower() == 'windows':
            post_install_template = "call %~dp0..\Scripts\activate.bat\n"
            for dependency in self._get_pip_dependencies():
                post_install_template += (f"pip install {dependency}\n")
        
        with open(self.post_install_template) as f:
            for line in f:
                post_install_template += line
                



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
#ig._generate_constructor_environment_yaml()
#ig._generate_post_install_script()
#ig.run()

