# afpa_meca
Projet application web Pôle mécanique AFPA


Pre-requis :    -pip install -r requirements.txt pour être à jour au niveau des librairies 

                -créer database.py dans "afpa_meca/afpa_meca/"

                -ajouter dans database.py : 
                
                        import os

                        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

                        DATABASES_DEV= {
                                'default': {
                                'ENGINE': 'django.db.backends.sqlite3',
                                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
                                }
                            }

                -puis dans settings.py :

                        from .database import DATABASES_DEV
                        ...
                        DATABASES=DATABASES_DEV
                    

                -renommer db.sqlite3_test en db.sqlite3 pour avoir une BDD pré-remplie



pseudo Gaetan : Gama

