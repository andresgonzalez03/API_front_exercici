# Prova de l'apartat 1
Aquesta part és on s'ha afegit el fetch dins del fitxer script.js per conectar-se a l'API i executar el endpoint /alumne/list

![Foto prova de la pàgina index.html](imatges/prova1.png)

# Prova de l'apartat 2
Aquesta part és on s'ha creat l'endpoint que permeten utilitzar tant els paràmeters de query, com sinó vols utilitzar-ho. En aquest cas, retornarà el mateix cas de l'apartat 
anterior però, si indiques algun paràmetre, per exemple un orderby = desc, te'ls ordenarà de manera descendent.


![Foto prova d'aquest apartat utilitzant el swagger](imatges/prova2swagger.png)
![Foto prova d'aquest apartat utilitzant els endpoints manualment](imatges/prova2normal.png)

# Prova de l'apartat 3
Aquesta part és on es fa la càrrega a partir d'un fitxer CSV, seguint sempre que el format del CSV sigui (DescAula, Edifici, Pis, NomAlumne, Cicle, Curs, Grup), si no existeix l'aula la crea i si existeix, va directament a afegir l'alumne on també verifica si aquest alumne existeix, sinó existeix, el crea també. Finalment, li mostra a l'usuari un missatge de que el fitxer s'ha carregat correctament.

![Foto que mostra el contingut del meu CSV a utilitzar](imatges/contingutCSV.png)
![Foto del contingut de la base de dades abans de fer la càrrega](imatges/contingutBBDDAbans.png)
![Foto que mostra el missatge de la càrrega](imatges/missatgeCarrega.png)
![Foto del contingut de la base de dades després de fer la càrrega](imatges/contingutBBDDDespres.png)

