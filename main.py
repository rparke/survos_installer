#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import yaml


class Installation_Generator():
    
    def __init__(self, environment_yaml):
        self.environment_yaml = environment_yaml
    
    
    def run(self):
        
        #Create the environment.yaml and post_install.sh temp files
        #to be used by conda constructor and save them in the installation directory
        self._generate_constructor_environment_yaml()
        self._generate_post_install_script()
        
        # Call conda constructor on the temp yaml and sh files created above
        # and create an installer in the same directory
        self._run_constructor()
    
    
    def print_parameters(self):
        pass
    
    def _parse_yaml(self):
        with open(self.environment_yaml) as f:
            self.environment = yaml.load(f)
    
    
    def _get_conda_dependencies(self):
        self._parse_yaml()
        
        
    def _get_pip_dependenceis(self):
        self._parse_yaml()
        
        
    def _generate_constructor_environment_yaml(self):
        pass
    
    
    def _generate_post_install_script(self):
        pass


    def _run_constructor(self):
        pass
    