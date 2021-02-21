set anaconda_dir=C:\Users\agrasso\Anaconda3
set notebook_root=C:\Users\Antonio Grasso\Documents\Projects\covid19\notebook\covid19\regioni
set notebook_bolzano=p.a. bolzano
set notebook_trento=p.a. trento

call %anaconda_dir%\Scripts\activate.bat %anaconda_dir%

call conda activate covid19

%=Visualization Regions Notebooks=%
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\abruzzo.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\basilicata.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\calabria.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\campania.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\emilia-romagna.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\friuli-venezia-giulia.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\lazio.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\liguria.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\lombardia.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\marche.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\molise.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\%notebook_bolzano%"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\%notebook_trento%"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\piemonte.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\puglia.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\sardegna.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\sicilia.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\toscana.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\umbria.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\valle-d-aosta.ipynb"
call start /b jupyter nbconvert --to notebook --inplace --execute "%notebook_root%\veneto.ipynb"
