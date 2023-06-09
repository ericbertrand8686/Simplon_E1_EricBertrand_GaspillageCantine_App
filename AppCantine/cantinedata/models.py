from django.db import models

class Fréquentation(models.Model):
    """Modèle représentant une entrée dans le fichier nombre-de-convives-jour"""
    
    TYPE_SITE = (
        ('E', 'Elémentaire'),
        ('M', 'Maternelle'),
        ('M/E', 'Mixte'),
    )
    
    identifiant_site = models.CharField(max_length=200, help_text="Entrez l'idendentifiant du site (e.g. 109)")
    type_site = models.CharField(max_length=3, choices=TYPE_SITE, default='E', help_text='Entrez le type du site (e.g. E, M, M/E)')
    date = models.DateField(auto_now=False, auto_now_add=False, help_text='Entrez la date des repas (e.g. Science Fiction)')
    prevision = models.IntegerField(null=True, help_text='Entrez le nombre de repas prévus (e.g. 31/05/2019)')
    reel = models.IntegerField(null=True, help_text='Entrez le nombre de repas réellement consommés (e.g. 246)')
    nom_site = models.CharField(max_length=200, help_text='Entrez le nom du site  (e.g. GAY LUSSAC)')
    nom_site_syst = models.CharField(max_length=200, help_text='Entrez le nom Système du site  (e.g. GAY LUSSAC PRIM)')
    prevision_syst = models.IntegerField(null=True, help_text='Enter a book genre (e.g. Science Fiction)')
    reel_syst = models.IntegerField(null=True, help_text='Enter a book genre (e.g. Science Fiction)')
    
    def __str__(self):
        """String for representing the Model object."""
        return (self.nom_site + " : " + str(self.date))