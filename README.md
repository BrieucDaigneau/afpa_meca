# afpa_meca
Projet application web Pôle mécanique AFPA


Pre-requis :    -pip install -r requirements.txt pour être à jour au niveau des librairies 

                -créer database.py dans "afpa_meca/afpa_meca/"

                -ajouter dans database.py (pour sqlite3): 
                
                                import os

                                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

                                DATABASES_DEV= {
                                        'default': {
                                        'ENGINE': 'django.db.backends.sqlite3',
                                        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
                                        }
                                    }


                -renommer db.sqlite3_test en db.sqlite3 pour avoir une BDD pré-remplie

                -créer business_application.py (fichier de config) dans afpa_meca/afpa_meca/

                -ajouter dans business_application.py :

                                VehicleConfig = {
                                    'vehicle': 'car' ou 'bike' selon le pôle méca concerné
                                    }



pseudo Gaetan : Gama

