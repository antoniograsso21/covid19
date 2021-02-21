set anaconda_dir=C:\Users\agrasso\Anaconda3
set notebook_root="C:\Users\Antonio Grasso\Documents\Projects\covid19\notebook\covid19"

call %anaconda_dir%\Scripts\activate.bat %anaconda_dir%

call conda activate covid19

%=Pre-processing Notebooks=%
call jupyter nbconvert --to notebook --inplace --execute %notebook_root%\andamento_nazionale_preproc.ipynb
call jupyter nbconvert --to notebook --inplace --execute %notebook_root%\regioni_preproc.ipynb
call jupyter nbconvert --to notebook --inplace --execute %notebook_root%\province_preproc.ipynb

%=Visualization Notebooks=%
call start /b jupyter nbconvert --to notebook --inplace --execute %notebook_root%\andamento_nazionale_visual.ipynb
call start /b jupyter nbconvert --to notebook --inplace --execute %notebook_root%\regioni_visual.ipynb
call start /b jupyter nbconvert --to notebook --inplace --execute %notebook_root%\province_visual.ipynb