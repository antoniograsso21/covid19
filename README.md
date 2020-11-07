# COVID-19 in Italia
Questa repository contiene Jupyter Notebook per la visualizzazione dei dati relativi alla pandemia da COVID-19 in Italia.
I dati sull'andamento della pandemia in Italia sono liberamente tratti dalla repository [COVID-19](https://github.com/pcm-dpc/COVID-19), messa a disposizione dal Dipartimento della Protezione Civile sotto licenza [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/deed.it).

## Struttura repository
La repository contiene attualmente 6 Jupyter Notebook, organizzati nel seguente modo:
- 3 Jupyter Notebook per il **pre-processing** dei dati:
    - [Pre-processing nazionale](national_preproc.ipynb)
    - [Pre-processing regionale](regional_preproc.ipynb)
    - [Pre-processing provinciale](province_preproc.ipynb)
- 3 Jupyter Notebook per la **visualizzazione** dei dati:
    - [Visualizzazione nazionale](national_visualize.ipynb)
    - [Visualizzazione regionale](regional_visualize.ipynb)
    - [Visualizzazione provinciale](province_visualize.ipynb)

### Grafici 

#### Andamento Nazionale
I grafici relativi all'andamento **nazionale** dei dati sono disponibili per:
- [ultimi 2 mesi](md/grafici/andamento-nazionale/60gg/README.md)
- [ultimo mese](md/grafici/andamento-nazionale/30gg/README.md)
- [ultima settimana](md/grafici/andamento-nazionale/07gg/README.md)

### Mappe
Per la visualizzazione dei dati regionali e provinciali relativi all'ultima data disponibile sono state generate [mappe coropletiche](https://it.wikipedia.org/wiki/Mappa_coropletica).
<!-- I dati relativi alla popolazione regionale fanno riferimento ai [dati ISTAT](http://demo.istat.it/pop2020/index3.html) al 1° Gennaio 2020. -->

#### Andamento Regionale
Le mappe coropletiche relative all'andamento **regionale** dei dati sono consultabili alla seguente pagina: [mappe regionali](md/mappe/regioni/README.md)

#### Andamento Provinciale
Le mappe coropletiche relative all'andamento **provinciale** dei dati sono consultabili alla seguente pagina: [mappe provinciali](md/mappe/province/README.md)