call %~dp0..\Scriptsctivate.bat
conda env update -p%dp0..\..\ --file %survos_directory%\survos2_clean_environment_windows.yml 
echo call %~dp0..\Scripts\activate.bat > %survos_directory%\launcher.bat
echo CD %survos_directory% >> %survos_directory%\launcher.bat
echo python -m survos2.improc.setup build_ext --inplace >> %survos_directory%\launcher.bat
echo python -m survos2.frontend.runner >> %survos_directory%\launcher.bat

