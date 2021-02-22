from survos_installer import mainimport pytestimport yamlTEST_YAML_FILE = "survos2_clean_environment_linux.yml"def test_parse_yaml():    with open(TEST_YAML_FILE) as f:        correct_parsing = yaml.safe_load(f)        ig = main.Installation_Generator(TEST_YAML_FILE)    ig._parse_yaml()    assert(ig.environment == correct_parsing)            def test_get_conda_dependencies():    with open(TEST_YAML_FILE) as f:        yaml_full = yaml.safe_load(f)    conda_dependencies = yaml_full['dependencies'][:-1]        ig = main.Installation_Generator(TEST_YAML_FILE)    ig._get_conda_dependencies()    assert(conda_dependencies == ig.conda_dependencies)def test_get_pip_dependencies():    with open(TEST_YAML_FILE) as f:        yaml_full = yaml.safe_load(f)    pip_dependencies = list(yaml_full['dependencies'][-1].values())[0]    ig = main.Installation_Generator(TEST_YAML_FILE)    ig._get_pip_dependenceis()    assert(pip_dependencies == ig.pip_dependencies)test_parse_yaml()test_get_conda_dependencies()test_get_pip_dependencies()