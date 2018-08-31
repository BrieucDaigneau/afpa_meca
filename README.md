# afpa_meca
Projet application web Pôle mécanique AFPA


Pre-requis :    -pip install -r requirements.txt pour être à jour au niveau des librairies 
                -créer database.py dans "afpa_meca/afpa_meca/"
                -renommer db.sqlite3_test en db.sqlite3 pour avoir une BDD pré-remplie
                -dans business.application.py, passer la valeur de vehicle à "car" pour créer des voitures ou "bike" pour créer des motos/vélos.
                -ajouter dans database.py (pour sqlite3): 
                
                                import os

                                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

                                DATABASES_DEV= {
                                        'default': {
                                        'ENGINE': 'django.db.backends.sqlite3',
                                        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
                                        }
                                    }


                                



pseudo Gaetan : Gama

