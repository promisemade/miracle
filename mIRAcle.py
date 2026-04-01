"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           mIRAcle - Version Finale                           ║
║                      Préparation à l'oral IRA Lille                          ║
║                                                                              ║
║  Application autonome avec fiches de postes intégrées                        ║
║  Aucune dépendance externe aux fichiers PDF                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
import json
import threading
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════════════
# THÈME VISUEL
# ══════════════════════════════════════════════════════════════════════════════

class Theme:
    """Palette de couleurs moderne"""
    
    # Backgrounds
    BG_DARK = "#0a0a0f"
    BG_CARD = "#12121a"
    BG_CARD_HOVER = "#1a1a25"
    BG_ELEVATED = "#16161f"
    
    # Couleurs principales
    PRIMARY = "#00d4aa"
    PRIMARY_DIM = "#00a085"
    PRIMARY_LIGHT = "#1a3d2e"
    
    # Accents
    ACCENT_PURPLE = "#a855f7"
    ACCENT_BLUE = "#3b82f6"
    ACCENT_ORANGE = "#f97316"
    ACCENT_PINK = "#ec4899"
    ACCENT_YELLOW = "#eab308"
    
    # Textes
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#a1a1aa"
    TEXT_MUTED = "#71717a"
    
    # États
    SUCCESS = "#22c55e"
    WARNING = "#f59e0b"
    ERROR = "#ef4444"
    
    # Bordures
    BORDER = "#27272a"
    
    # Polices
    FONT_DISPLAY = ("Segoe UI", 28, "bold")
    FONT_TITLE = ("Segoe UI", 18, "bold")
    FONT_SUBTITLE = ("Segoe UI", 14, "bold")
    FONT_BODY = ("Segoe UI", 12)
    FONT_SMALL = ("Segoe UI", 10)
    FONT_MONO = ("Consolas", 11)


# ══════════════════════════════════════════════════════════════════════════════
# BASE DE DONNÉES DES FICHES DE POSTES
# ══════════════════════════════════════════════════════════════════════════════

FICHES_DATABASE = [
    # ═══════════════════════════════════════════════════════════════════════════
    # ADMINISTRATION CENTRALE - MINISTÈRE DE L'INTÉRIEUR
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "titre": "Chargé(e) de mission auprès du préfet",
        "administration": "ADMINISTRATION CENTRALE",
        "structure": "Ministère de l'Intérieur",
        "domaine": "CABINET / COORDINATION",
        "localisation": "Paris",
        "grade": "Attaché d'administration de l'État",
        "groupe_ifse": "3",
        "missions": """Le/la chargé(e) de mission auprès du préfet assure :

• La coordination des dossiers transversaux relevant du cabinet
• La préparation des réunions interministérielles
• Le suivi des instructions et circulaires ministérielles
• La rédaction de notes de synthèse et d'aide à la décision
• L'interface avec les services déconcentrés
• La gestion des situations de crise et d'urgence""",
        "competences": """Compétences requises :

SAVOIR :
• Connaissance approfondie de l'organisation administrative française
• Maîtrise du droit public et des procédures administratives
• Connaissance des politiques publiques du ministère

SAVOIR-FAIRE :
• Excellentes capacités rédactionnelles
• Aptitude à la synthèse et à l'analyse
• Maîtrise des outils bureautiques
• Gestion de projet

SAVOIR-ÊTRE :
• Réactivité et disponibilité
• Sens de la confidentialité
• Capacité à travailler en équipe
• Résistance au stress""",
        "environnement": """Le cabinet du préfet est au cœur de l'action de l'État dans le département. 
Il coordonne l'ensemble des services de l'État et assure la représentation du Gouvernement.
L'attaché travaille en lien étroit avec le directeur de cabinet et les sous-préfets."""
    },
    {
        "id": 2,
        "titre": "Gestionnaire RH - Bureau de la gestion des carrières",
        "administration": "ADMINISTRATION CENTRALE",
        "structure": "Ministère de l'Intérieur",
        "domaine": "RESSOURCES HUMAINES",
        "localisation": "Paris - Place Beauvau",
        "grade": "Attaché d'administration de l'État",
        "groupe_ifse": "4",
        "missions": """Au sein du bureau de la gestion des carrières, vous assurez :

• La gestion des dossiers individuels des agents (avancement, promotion)
• L'instruction des demandes de mutation et de détachement
• La préparation des commissions administratives paritaires (CAP)
• Le suivi des effectifs et des tableaux de bord RH
• Le conseil aux agents sur leur parcours professionnel
• La mise en œuvre des réformes statutaires""",
        "competences": """Compétences attendues :

SAVOIR :
• Connaissance du statut de la fonction publique
• Maîtrise des règles de gestion des carrières
• Connaissance des outils SIRH

SAVOIR-FAIRE :
• Rigueur dans le traitement des dossiers
• Capacité d'analyse juridique
• Maîtrise d'Excel et des requêtes BO

SAVOIR-ÊTRE :
• Sens du service public
• Discrétion professionnelle
• Aptitude au travail en équipe""",
        "environnement": """La DRH du ministère de l'Intérieur gère plus de 280 000 agents.
Le bureau est composé de 25 agents répartis en 3 sections.
Vous travaillerez sous l'autorité du chef de bureau."""
    },
    {
        "id": 3,
        "titre": "Responsable du pôle budget et finances",
        "administration": "ADMINISTRATION CENTRALE",
        "structure": "Ministère de l'Intérieur",
        "domaine": "BUDGET / FINANCES",
        "localisation": "Paris",
        "grade": "Attaché principal d'administration",
        "groupe_ifse": "3",
        "missions": """En tant que responsable du pôle budget, vous êtes chargé(e) de :

• Élaborer et suivre le budget du service (programmation, exécution)
• Piloter le dialogue de gestion avec la direction des finances
• Superviser l'équipe de gestionnaires budgétaires (4 agents)
• Assurer le contrôle interne budgétaire et comptable
• Produire les tableaux de bord et analyses financières
• Participer aux réunions de programmation budgétaire""",
        "competences": """Profil recherché :

SAVOIR :
• Maîtrise de la LOLF et des règles de comptabilité publique
• Connaissance des applications budgétaires (Chorus, etc.)
• Culture de la performance publique

SAVOIR-FAIRE :
• Management d'équipe
• Capacités d'analyse et de synthèse
• Maîtrise des outils de reporting

SAVOIR-ÊTRE :
• Leadership
• Rigueur et organisation
• Force de proposition""",
        "environnement": """Le pôle budget est rattaché au secrétariat général.
Il gère un budget de fonctionnement de 15 M€.
Relations fréquentes avec la direction du budget et le CBCM."""
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ADMINISTRATION CENTRALE - MINISTÈRE DE LA JUSTICE
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "titre": "Adjoint(e) au chef de section retraites",
        "administration": "ADMINISTRATION CENTRALE",
        "structure": "Ministère de la Justice",
        "domaine": "RESSOURCES HUMAINES",
        "localisation": "Paris - 35 rue de la Gare",
        "grade": "Attaché d'administration de l'État",
        "groupe_ifse": "4",
        "missions": """La section Retraites est composée de 6 agents. Vos missions principales :

• Instruction des dossiers de demande de départ à la retraite
• Suivi des demandes de prolongation d'activité
• Fiabilisation des comptes individuels de retraite (9000 agents)
• Instruction des dossiers d'affiliations rétroactives
• Instruction des demandes de rachat d'années d'études
• Collaboration avec les caisses de retraites inter-régimes
• Encadrement de 4 agents de catégorie B en l'absence du chef de section""",
        "competences": """Compétences requises :

SAVOIR :
• Réglementation des pensions civiles de l'État
• Connaissance du code des pensions
• Maîtrise des outils de gestion des retraites

SAVOIR-FAIRE :
• Analyse juridique des situations individuelles
• Capacité de management
• Maîtrise d'Excel avancé

SAVOIR-ÊTRE :
• Pédagogie envers les agents
• Rigueur dans le traitement des dossiers
• Sens de l'organisation""",
        "environnement": """La section retraites gère les dossiers de 9000 agents PJJ.
Relations avec le Service des Retraites de l'État (SRE).
Contexte de réforme des retraites nécessitant une adaptation continue."""
    },
    {
        "id": 5,
        "titre": "Chargé(e) d'études juridiques",
        "administration": "ADMINISTRATION CENTRALE",
        "structure": "Ministère de la Justice",
        "domaine": "JURIDIQUE",
        "localisation": "Paris - Place Vendôme",
        "grade": "Attaché d'administration de l'État",
        "groupe_ifse": "3",
        "missions": """Au sein de la direction des affaires juridiques, vous assurez :

• La rédaction de notes juridiques et d'analyses
• Le suivi du contentieux administratif du ministère
• La veille juridique (législation, jurisprudence)
• La participation à l'élaboration des textes normatifs
• Le conseil juridique aux services opérationnels
• La représentation du ministère devant les juridictions administratives""",
        "competences": """Profil attendu :

SAVOIR :
• Droit public approfondi
• Contentieux administratif
• Légistique

SAVOIR-FAIRE :
• Excellente qualité rédactionnelle
• Capacité de recherche juridique
• Maîtrise des bases de données juridiques

SAVOIR-ÊTRE :
• Rigueur intellectuelle
• Capacité à respecter les délais
• Discrétion professionnelle""",
        "environnement": """La direction des affaires juridiques est le conseil juridique du Garde des Sceaux.
Équipe de 15 juristes spécialisés.
Interaction avec le Conseil d'État et les juridictions."""
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ADMINISTRATION CENTRALE - MINISTÈRE DE L'ÉCONOMIE
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": 6,
        "titre": "Chargé(e) de mission achat public",
        "administration": "ADMINISTRATION CENTRALE",
        "structure": "Ministère de l'Économie et des Finances",
        "domaine": "ACHAT PUBLIC",
        "localisation": "Paris - Bercy",
        "grade": "Attaché d'administration de l'État",
        "groupe_ifse": "3",
        "missions": """Au sein de la Direction des Achats de l'État, vous participez à :

• La définition de la stratégie achat pour une famille d'achats
• La passation de marchés publics interministériels
• L'accompagnement des acheteurs ministériels
• La négociation avec les fournisseurs
• Le suivi de l'exécution des marchés
• La professionnalisation de la fonction achat""",
        "competences": """Compétences recherchées :

SAVOIR :
• Code de la commande publique
• Techniques d'achat et de négociation
• Connaissance du tissu économique

SAVOIR-FAIRE :
• Rédaction de cahiers des charges
• Analyse des offres
• Maîtrise des outils e-procurement

SAVOIR-ÊTRE :
• Sens de la négociation
• Éthique et déontologie
• Travail en mode projet""",
        "environnement": """La DAE pilote la politique achat de l'État (40 Mds€/an).
Travail interministériel avec l'ensemble des acheteurs publics.
Contexte de performance achat et de développement durable."""
    },
    {
        "id": 7,
        "titre": "Contrôleur de gestion",
        "administration": "ADMINISTRATION CENTRALE",
        "structure": "Ministère de l'Économie et des Finances",
        "domaine": "BUDGET / CONTRÔLE DE GESTION",
        "localisation": "Paris - Bercy",
        "grade": "Attaché d'administration de l'État",
        "groupe_ifse": "4",
        "missions": """Le contrôleur de gestion assure :

• L'élaboration et le suivi des indicateurs de performance
• La production des tableaux de bord mensuels
• L'analyse des écarts et la proposition d'actions correctives
• Le pilotage du dialogue de gestion
• La participation à la démarche de contrôle interne
• L'accompagnement des services dans leur pilotage""",
        "competences": """Profil attendu :

SAVOIR :
• Techniques de contrôle de gestion
• Comptabilité analytique
• Connaissance de la LOLF

SAVOIR-FAIRE :
• Maîtrise avancée d'Excel et Power BI
• Capacité d'analyse de données
• Rédaction de rapports

SAVOIR-ÊTRE :
• Esprit de synthèse
• Pédagogie
• Force de conviction""",
        "environnement": """Le service contrôle de gestion est rattaché au secrétariat général.
Interlocuteur privilégié de la direction du budget.
Contribution à la modernisation de la gestion publique."""
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ADMINISTRATION DÉCONCENTRÉE - PRÉFECTURE
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": 8,
        "titre": "Chef du bureau de la réglementation",
        "administration": "ADMINISTRATION DÉCONCENTRÉE",
        "structure": "Préfecture des Hauts-de-France",
        "domaine": "RÉGLEMENTATION",
        "localisation": "Lille",
        "grade": "Attaché principal d'administration",
        "groupe_ifse": "3",
        "missions": """En tant que chef de bureau, vous êtes responsable de :

• L'encadrement d'une équipe de 12 agents
• La délivrance des titres (CNI, passeports, permis de conduire)
• Le contrôle de légalité des actes des collectivités
• Les procédures d'autorisation (débits de boissons, armes)
• Les élections et le répertoire électoral unique
• Les naturalisations et les déclarations de nationalité""",
        "competences": """Compétences requises :

SAVOIR :
• Droit administratif
• Procédures de délivrance des titres
• Droit des collectivités territoriales

SAVOIR-FAIRE :
• Management d'équipe
• Gestion des priorités
• Relation avec les usagers

SAVOIR-ÊTRE :
• Leadership
• Gestion du stress
• Sens du service public""",
        "environnement": """Le bureau de la réglementation reçoit plus de 500 usagers/jour.
Contexte de dématérialisation des procédures.
Pics d'activité lors des périodes électorales."""
    },
    {
        "id": 9,
        "titre": "Responsable du pôle sécurité intérieure",
        "administration": "ADMINISTRATION DÉCONCENTRÉE",
        "structure": "Préfecture des Hauts-de-France",
        "domaine": "SÉCURITÉ",
        "localisation": "Lille",
        "grade": "Attaché d'administration de l'État",
        "groupe_ifse": "3",
        "missions": """Le responsable du pôle sécurité assure :

• La coordination des services de sécurité (police, gendarmerie)
• Le suivi du plan de prévention de la délinquance
• La gestion des grands événements et manifestations
• Le secrétariat du CLSPD (conseil local de sécurité)
• L'analyse des statistiques de la délinquance
• La préparation des arrêtés préfectoraux de sécurité""",
        "competences": """Profil recherché :

SAVOIR :
• Connaissance des acteurs de la sécurité
• Procédures administratives de police
• Gestion de crise

SAVOIR-FAIRE :
• Animation de réunions partenariales
• Rédaction administrative
• Analyse de données statistiques

SAVOIR-ÊTRE :
• Disponibilité (astreintes possibles)
• Discrétion
• Capacité à travailler en réseau""",
        "environnement": """Le pôle sécurité travaille en lien avec le cabinet du préfet.
Zone de sécurité prioritaire (ZSP) dans le département.
Contexte de plan Vigipirate et de menace terroriste."""
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ADMINISTRATION DÉCONCENTRÉE - DIRECTION DÉPARTEMENTALE
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "titre": "Chef du service cohésion sociale",
        "administration": "ADMINISTRATION DÉCONCENTRÉE",
        "structure": "DDETS (Direction départementale de l'emploi, du travail et des solidarités)",
        "domaine": "POLITIQUES SOCIALES",
        "localisation": "Amiens",
        "grade": "Attaché principal d'administration",
        "groupe_ifse": "2",
        "missions": """En qualité de chef de service, vos missions sont :

• Le pilotage des politiques d'hébergement et de logement
• La coordination du plan pauvreté départemental
• L'animation du réseau des travailleurs sociaux
• Le suivi des associations financées par l'État
• La gestion des situations d'urgence sociale
• La préparation du comité départemental de cohésion sociale""",
        "competences": """Compétences attendues :

SAVOIR :
• Politiques sociales et dispositifs d'aide
• Financement des associations
• Connaissance du tissu associatif local

SAVOIR-FAIRE :
• Management de service
• Conduite de projet
• Animation de réseau

SAVOIR-ÊTRE :
• Sens de l'écoute
• Capacité de médiation
• Engagement pour les publics fragiles""",
        "environnement": """La DDETS met en œuvre les politiques de solidarité de l'État.
Service de 30 agents dont 15 travailleurs sociaux.
Partenariat étroit avec le conseil départemental."""
    },
    {
        "id": 11,
        "titre": "Inspecteur du travail - Contrôle des entreprises",
        "administration": "ADMINISTRATION DÉCONCENTRÉE",
        "structure": "DREETS (Direction régionale de l'économie, de l'emploi, du travail et des solidarités)",
        "domaine": "TRAVAIL / EMPLOI",
        "localisation": "Lille",
        "grade": "Attaché d'administration de l'État",
        "groupe_ifse": "3",
        "missions": """L'inspecteur du travail assure :

• Le contrôle du respect du droit du travail dans les entreprises
• Les enquêtes suite aux accidents du travail
• L'accompagnement des entreprises en difficulté
• La médiation dans les conflits collectifs
• Le conseil aux employeurs et salariés
• La contribution aux politiques de prévention""",
        "competences": """Profil recherché :

SAVOIR :
• Code du travail
• Droit pénal du travail
• Connaissance du monde de l'entreprise

SAVOIR-FAIRE :
• Techniques de contrôle
• Rédaction de procès-verbaux
• Capacité d'investigation

SAVOIR-ÊTRE :
• Autorité et fermeté
• Impartialité
• Courage professionnel""",
        "environnement": """L'inspection du travail contrôle 30 000 entreprises dans la région.
Secteur d'intervention : 150 entreprises et 8000 salariés.
Contexte de réforme du système d'inspection."""
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ADMINISTRATION CENTRALE - CAISSE DES DÉPÔTS
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "titre": "Analyste conformité filières groupe",
        "administration": "ADMINISTRATION CENTRALE",
        "structure": "Caisse des Dépôts et Consignations",
        "domaine": "AUDIT - MAÎTRISE DES RISQUES",
        "localisation": "Paris",
        "grade": "Attaché d'administration / Équivalent catégorie A",
        "groupe_ifse": "3",
        "missions": """L'analyste conformité assure :

• La participation à la définition des normes Groupe en matière de conformité
• La veille réglementaire (LCB-FT, sanctions internationales, déontologie)
• La contribution au dispositif de pilotage LCB-FT Groupe
• L'animation de la filière conformité des filiales
• La rédaction des reportings réglementaires au superviseur
• L'appui aux administrateurs dans les comités d'audit""",
        "competences": """Compétences requises :

SAVOIR :
• Réglementation LCB-FT et conformité bancaire
• Connaissance du Groupe CDC
• Normes de contrôle interne

SAVOIR-FAIRE :
• Analyse des risques
• Rédaction de normes et procédures
• Animation de réseau

SAVOIR-ÊTRE :
• Rigueur
• Esprit de synthèse
• Capacité à travailler en transversal""",
        "environnement": """La DAJCD (Direction des affaires juridiques, conformité et déontologie) 
pilote la conformité du Groupe CDC (Caisse des Dépôts et filiales).
Contexte de supervision ACPR renforcée."""
    },
    {
        "id": 13,
        "titre": "Chargé(e) de continuité d'activité et gestion de crise",
        "administration": "ADMINISTRATION CENTRALE",
        "structure": "Caisse des Dépôts et Consignations",
        "domaine": "PILOTAGE / ORGANISATION",
        "localisation": "Paris",
        "grade": "Attaché d'administration / Équivalent catégorie A",
        "groupe_ifse": "4",
        "missions": """Au sein du service PUPA (Plan d'Urgence et de Continuité d'Activité) :

• Participation à la rédaction des procédures de continuité d'activité
• Mise à jour des classifications des risques
• Contrôle interne : suivi des indicateurs KRI
• Animation de la filière des ROCA (Responsables Opérationnels Continuité)
• Organisation des exercices de crise
• Formation des collaborateurs à la gestion de crise (méthode AGIR)""",
        "competences": """Profil attendu :

SAVOIR :
• Méthodologie de continuité d'activité (ISO 22301)
• Gestion de crise
• Connaissance des métiers de la CDC

SAVOIR-FAIRE :
• Animation de réseau
• Conception de supports pédagogiques
• Pilotage de projets transverses

SAVOIR-ÊTRE :
• Réactivité
• Pédagogie
• Capacité à travailler sous pression""",
        "environnement": """La DOT (Direction des Opérations et de la Transformation) 
assure l'excellence opérationnelle de la CDC.
Le service PUPA compte 5 collaborateurs."""
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SERVICES ACADÉMIQUES - ÉDUCATION NATIONALE
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": 14,
        "titre": "Gestionnaire de personnels enseignants",
        "administration": "ADMINISTRATION SCOLAIRE",
        "structure": "Rectorat de l'académie de Lille",
        "domaine": "RESSOURCES HUMAINES",
        "localisation": "Lille",
        "grade": "Attaché d'administration de l'État",
        "groupe_ifse": "4",
        "missions": """Au sein de la division des personnels enseignants :

• Gestion des carrières (avancement, promotion, notation)
• Instruction des demandes de mutation (mouvement intra-académique)
• Préparation des commissions paritaires (CAPA, CAPN)
• Suivi des congés (maladie, maternité, formation)
• Gestion des suppléances et remplacements
• Information et conseil aux personnels""",
        "competences": """Compétences recherchées :

SAVOIR :
• Statut des personnels enseignants
• Réglementation des mutations
• Outils de gestion RH (SIRHEN)

SAVOIR-FAIRE :
• Traitement de dossiers en volume
• Maîtrise des applications métier
• Capacité d'analyse

SAVOIR-ÊTRE :
• Sens du service
• Rigueur
• Résistance au stress (pics d'activité)""",
        "environnement": """L'académie de Lille compte 50 000 personnels.
La division gère 25 000 enseignants du second degré.
Contexte de dématérialisation des procédures."""
    },
    {
        "id": 15,
        "titre": "Chef de division de la vie des établissements",
        "administration": "ADMINISTRATION SCOLAIRE",
        "structure": "Rectorat de l'académie de Lille",
        "domaine": "PILOTAGE / ÉTABLISSEMENTS",
        "localisation": "Lille",
        "grade": "Attaché principal d'administration",
        "groupe_ifse": "2",
        "missions": """Le chef de division assure :

• Le pilotage de l'allocation des moyens aux établissements (DHG)
• La préparation de la carte des formations
• Le suivi de la politique éducative académique
• L'accompagnement des chefs d'établissement
• La gestion des situations de crise dans les EPLE
• L'animation du réseau des gestionnaires d'établissement""",
        "competences": """Profil attendu :

SAVOIR :
• Organisation du système éducatif
• Financement des EPLE
• Politiques éducatives

SAVOIR-FAIRE :
• Management stratégique
• Analyse de données
• Communication institutionnelle

SAVOIR-ÊTRE :
• Leadership
• Diplomatie
• Vision stratégique""",
        "environnement": """La division pilote 300 établissements (collèges et lycées).
Relations avec les collectivités de rattachement.
Contexte de réforme du lycée et de la voie professionnelle."""
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ÉTABLISSEMENTS PUBLICS
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": 16,
        "titre": "Rapporteur(se) à la CNDA",
        "administration": "ÉTABLISSEMENT PUBLIC",
        "structure": "Cour nationale du droit d'asile (Conseil d'État)",
        "domaine": "JURIDIQUE / CONTENTIEUX",
        "localisation": "Montreuil",
        "grade": "Attaché d'administration de l'État",
        "groupe_ifse": "3",
        "missions": """Le rapporteur instruit les recours contre les décisions de l'OFPRA :

• Analyse du dossier et du récit du demandeur d'asile
• Recherche documentaire sur les pays d'origine
• Rédaction du rapport et du projet de décision
• Présentation du dossier à l'audience
• Participation aux formations de jugement
• Veille juridique sur le droit d'asile""",
        "competences": """Compétences requises :

SAVOIR :
• Droit d'asile (Convention de Genève, CESEDA)
• Connaissance géopolitique
• Procédure contentieuse

SAVOIR-FAIRE :
• Analyse de récits et de preuves
• Qualité rédactionnelle
• Expression orale

SAVOIR-ÊTRE :
• Neutralité et objectivité
• Capacité d'écoute
• Résistance émotionnelle""",
        "environnement": """La CNDA traite 60 000 recours par an.
Délai moyen de jugement : 5 mois.
Travail en formation collégiale (3 juges)."""
    },
    {
        "id": 17,
        "titre": "Chargé(e) de mission à l'OFPRA",
        "administration": "ÉTABLISSEMENT PUBLIC",
        "structure": "Office français de protection des réfugiés et apatrides",
        "domaine": "INSTRUCTION / ASILE",
        "localisation": "Fontenay-sous-Bois",
        "grade": "Attaché d'administration de l'État",
        "groupe_ifse": "4",
        "missions": """L'officier de protection instruit les demandes d'asile :

• Conduite des entretiens avec les demandeurs d'asile
• Analyse de la crédibilité des récits
• Recherche d'information sur les pays d'origine
• Rédaction des décisions d'octroi ou de rejet
• Application des clauses d'exclusion et de cessation
• Participation aux missions de l'OFPRA à l'étranger""",
        "competences": """Profil attendu :

SAVOIR :
• Droit d'asile et des réfugiés
• Géopolitique et droits de l'homme
• Techniques d'entretien

SAVOIR-FAIRE :
• Conduite d'entretien
• Analyse et rédaction
• Utilisation des bases documentaires

SAVOIR-ÊTRE :
• Empathie et neutralité
• Résistance psychologique
• Rigueur intellectuelle""",
        "environnement": """L'OFPRA traite 130 000 demandes d'asile par an.
Organisation en divisions géographiques.
Contexte de réduction des délais d'instruction."""
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MINISTÈRE DE LA CULTURE
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": 18,
        "titre": "Chargé(e) de subventions - Spectacle vivant",
        "administration": "ADMINISTRATION CENTRALE",
        "structure": "Ministère de la Culture",
        "domaine": "BUDGET / SUBVENTIONS",
        "localisation": "Paris",
        "grade": "Attaché d'administration de l'État",
        "groupe_ifse": "4",
        "missions": """Au sein de la direction générale de la création artistique :

• Instruction des demandes de subvention des structures culturelles
• Analyse des budgets prévisionnels et des bilans
• Rédaction des conventions pluriannuelles d'objectifs
• Suivi de l'exécution des crédits d'intervention
• Participation aux commissions d'attribution
• Contrôle du respect des obligations conventionnelles""",
        "competences": """Compétences recherchées :

SAVOIR :
• Économie du spectacle vivant
• Règles de la comptabilité publique
• Politiques culturelles

SAVOIR-FAIRE :
• Analyse financière
• Rédaction de conventions
• Maîtrise de Chorus et Subventia

SAVOIR-ÊTRE :
• Sens de la négociation
• Diplomatie
• Rigueur budgétaire""",
        "environnement": """La DGCA soutient 1 500 structures de création artistique.
Budget d'intervention : 300 M€.
Partenariat avec les collectivités territoriales."""
    },
    {
        "id": 19,
        "titre": "Gestionnaire RH - Musées nationaux",
        "administration": "ADMINISTRATION CENTRALE",
        "structure": "Ministère de la Culture",
        "domaine": "RESSOURCES HUMAINES",
        "localisation": "Paris",
        "grade": "Attaché d'administration de l'État",
        "groupe_ifse": "4",
        "missions": """Au bureau de la gestion des personnels des musées :

• Gestion des carrières des agents des musées nationaux
• Traitement des demandes de mobilité et détachement
• Préparation des instances paritaires (CAP)
• Suivi des effectifs et de la masse salariale
• Conseil statutaire aux agents et directeurs de musées
• Mise en œuvre des réformes statutaires""",
        "competences": """Profil attendu :

SAVOIR :
• Statut de la fonction publique
• Spécificités des corps de la Culture
• SIRH et applications métier

SAVOIR-FAIRE :
• Gestion de dossiers individuels
• Analyse de situations complexes
• Rédaction administrative

SAVOIR-ÊTRE :
• Discrétion
• Sens du service
• Disponibilité""",
        "environnement": """Le bureau gère 6 000 agents des musées nationaux.
Grande diversité des métiers (conservation, surveillance, médiation).
Contexte d'autonomisation des établissements culturels."""
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MINISTÈRE DE LA TRANSITION ÉCOLOGIQUE
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "titre": "Chargé(e) de mission développement durable",
        "administration": "ADMINISTRATION CENTRALE",
        "structure": "Ministère de la Transition écologique",
        "domaine": "POLITIQUES PUBLIQUES",
        "localisation": "Paris - La Défense",
        "grade": "Attaché d'administration de l'État",
        "groupe_ifse": "3",
        "missions": """Au sein du commissariat général au développement durable :

• Contribution à l'élaboration des politiques de transition écologique
• Suivi des indicateurs ODD (Objectifs de Développement Durable)
• Rédaction de rapports et d'études
• Animation de groupes de travail interministériels
• Participation aux négociations européennes et internationales
• Communication sur les enjeux environnementaux""",
        "competences": """Compétences attendues :

SAVOIR :
• Enjeux du développement durable
• Politiques environnementales
• Droit de l'environnement

SAVOIR-FAIRE :
• Analyse et synthèse
• Animation de réunions
• Rédaction de rapports

SAVOIR-ÊTRE :
• Conviction et engagement
• Capacité de conviction
• Travail en réseau""",
        "environnement": """Le CGDD est le think tank du ministère.
Travail interministériel et avec les parties prenantes.
Contexte de planification écologique."""
    }
]


# ══════════════════════════════════════════════════════════════════════════════
# COMPOSANTS UI
# ══════════════════════════════════════════════════════════════════════════════

class GlowingCard(ctk.CTkFrame):
    """Carte avec effet de survol"""
    
    def __init__(self, master, glow_color=None, **kwargs):
        self.glow_color = glow_color or Theme.PRIMARY
        super().__init__(
            master,
            fg_color=Theme.BG_CARD,
            corner_radius=16,
            border_width=1,
            border_color=Theme.BORDER,
            **kwargs
        )
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def _on_enter(self, event):
        self.configure(border_color=self.glow_color)
        
    def _on_leave(self, event):
        self.configure(border_color=Theme.BORDER)


class StatBox(ctk.CTkFrame):
    """Boîte de statistique animée"""
    
    def __init__(self, master, title, value, icon, color=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.color = color or Theme.PRIMARY
        self.target_value = value
        self.current_value = 0
        
        container = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12)
        container.pack(fill="both", expand=True)
        
        # Barre colorée
        ctk.CTkFrame(container, fg_color=self.color, width=4, corner_radius=2).pack(
            side="left", fill="y", padx=(8, 0), pady=8
        )
        
        content = ctk.CTkFrame(container, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=12, pady=10)
        
        # Header
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x")
        
        ctk.CTkLabel(header, text=icon, font=("Segoe UI", 14), text_color=self.color).pack(side="left")
        ctk.CTkLabel(header, text=title, font=Theme.FONT_SMALL, text_color=Theme.TEXT_MUTED).pack(side="left", padx=(8, 0))
        
        self.value_label = ctk.CTkLabel(content, text="0", font=("Segoe UI", 22, "bold"), text_color=Theme.TEXT_PRIMARY)
        self.value_label.pack(anchor="w", pady=(4, 0))
        
        self._animate()
        
    def _animate(self):
        if self.current_value < self.target_value:
            step = max(1, (self.target_value - self.current_value) // 10)
            self.current_value = min(self.target_value, self.current_value + step)
            self.value_label.configure(text=str(self.current_value))
            self.after(30, self._animate)
            
    def update_value(self, new_value):
        self.target_value = new_value
        self.current_value = int(self.value_label.cget("text") or 0)
        self._animate()


class CircularTimer(ctk.CTkFrame):
    """Timer circulaire avec progression visuelle"""
    
    def __init__(self, master, size=180, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.size = size
        self.total_seconds = 15 * 60
        self.remaining_seconds = self.total_seconds
        self.is_running = False
        
        # Canvas
        self.canvas = tk.Canvas(self, width=size, height=size, bg=Theme.BG_DARK, highlightthickness=0)
        self.canvas.pack()
        
        self.draw_timer()
        
        # Contrôles
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(pady=15)
        
        # Presets
        presets = ctk.CTkFrame(controls, fg_color="transparent")
        presets.pack(pady=(0, 10))
        
        for mins in [5, 10, 15, 20]:
            ctk.CTkButton(
                presets, text=f"{mins}'", width=42, height=28,
                fg_color="transparent", hover_color=Theme.BG_ELEVATED,
                border_width=1, border_color=Theme.BORDER,
                text_color=Theme.TEXT_SECONDARY, corner_radius=8,
                font=Theme.FONT_SMALL,
                command=lambda m=mins: self.set_time(m)
            ).pack(side="left", padx=2)
        
        # Boutons
        btns = ctk.CTkFrame(controls, fg_color="transparent")
        btns.pack()
        
        self.play_btn = ctk.CTkButton(
            btns, text="▶", width=50, height=40,
            fg_color=Theme.PRIMARY, hover_color=Theme.PRIMARY_DIM,
            text_color=Theme.BG_DARK, corner_radius=20,
            font=("Segoe UI", 16), command=self.toggle
        )
        self.play_btn.pack(side="left", padx=4)
        
        ctk.CTkButton(
            btns, text="↺", width=50, height=40,
            fg_color="transparent", hover_color=Theme.BG_ELEVATED,
            border_width=1, border_color=Theme.BORDER,
            text_color=Theme.TEXT_SECONDARY, corner_radius=20,
            font=("Segoe UI", 16), command=self.reset
        ).pack(side="left", padx=4)
        
    def draw_timer(self):
        self.canvas.delete("all")
        cx, cy = self.size // 2, self.size // 2
        radius = self.size // 2 - 15
        
        # Track
        self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, outline=Theme.BORDER, width=8)
        
        # Progress
        progress = self.remaining_seconds / self.total_seconds if self.total_seconds > 0 else 0
        extent = progress * 360
        
        color = Theme.PRIMARY if progress > 0.5 else (Theme.WARNING if progress > 0.25 else Theme.ERROR)
        
        if extent > 0:
            self.canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius,
                                  start=90, extent=extent, outline=color, width=8, style="arc")
        
        # Temps
        mins, secs = self.remaining_seconds // 60, self.remaining_seconds % 60
        self.canvas.create_text(cx, cy - 8, text=f"{mins:02d}:{secs:02d}",
                               fill=Theme.TEXT_PRIMARY, font=("Segoe UI", 28, "bold"))
        
        status = "EN COURS" if self.is_running else "PRÊT"
        self.canvas.create_text(cx, cy + 28, text=status, fill=Theme.TEXT_MUTED, font=Theme.FONT_SMALL)
        
    def set_time(self, minutes):
        self.total_seconds = minutes * 60
        self.remaining_seconds = self.total_seconds
        self.draw_timer()
        
    def toggle(self):
        if self.is_running:
            self.is_running = False
            self.play_btn.configure(text="▶")
        else:
            self.is_running = True
            self.play_btn.configure(text="⏸")
            self._run()
            
    def _run(self):
        if self.is_running and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.draw_timer()
            self.after(1000, self._run)
        elif self.remaining_seconds <= 0:
            self.is_running = False
            self.play_btn.configure(text="▶")
            
    def reset(self):
        self.is_running = False
        self.remaining_seconds = self.total_seconds
        self.play_btn.configure(text="▶")
        self.draw_timer()


class FicheViewer(ctk.CTkFrame):
    """Afficheur de fiche de poste"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.current_fiche = None
        
        # Scrollable content
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=Theme.BG_CARD, corner_radius=12)
        self.scroll.pack(fill="both", expand=True)
        
        self._show_placeholder()
        
    def _show_placeholder(self):
        for w in self.scroll.winfo_children():
            w.destroy()
            
        ctk.CTkLabel(
            self.scroll,
            text="📄\n\nSélectionnez une fiche de poste\ndans la liste à gauche",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED
        ).pack(expand=True, pady=100)
        
    def display_fiche(self, fiche):
        self.current_fiche = fiche
        
        for w in self.scroll.winfo_children():
            w.destroy()
            
        # Header avec titre
        header = ctk.CTkFrame(self.scroll, fg_color=Theme.BG_ELEVATED, corner_radius=12)
        header.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(
            header, text=fiche["titre"],
            font=Theme.FONT_TITLE, text_color=Theme.PRIMARY,
            wraplength=600
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        ctk.CTkLabel(
            header, text=f"{fiche['structure']} • {fiche['domaine']}",
            font=Theme.FONT_SMALL, text_color=Theme.TEXT_MUTED
        ).pack(anchor="w", padx=20, pady=(0, 15))
        
        # Infos clés
        infos = ctk.CTkFrame(self.scroll, fg_color="transparent")
        infos.pack(fill="x", padx=15, pady=(0, 15))
        
        info_items = [
            ("📍", "Localisation", fiche.get("localisation", "Non précisé")),
            ("🎖️", "Grade", fiche.get("grade", "Attaché d'administration")),
            ("💰", "Groupe IFSE", fiche.get("groupe_ifse", "4"))
        ]
        
        for icon, label, value in info_items:
            box = ctk.CTkFrame(infos, fg_color=Theme.BG_CARD, corner_radius=8)
            box.pack(side="left", fill="x", expand=True, padx=5)
            
            ctk.CTkLabel(box, text=f"{icon} {label}", font=Theme.FONT_SMALL, 
                        text_color=Theme.TEXT_MUTED).pack(anchor="w", padx=12, pady=(10, 2))
            ctk.CTkLabel(box, text=value, font=Theme.FONT_BODY,
                        text_color=Theme.TEXT_PRIMARY).pack(anchor="w", padx=12, pady=(0, 10))
        
        # Sections détaillées
        self._add_section("📋 Missions principales", fiche.get("missions", ""))
        self._add_section("🎯 Compétences requises", fiche.get("competences", ""))
        self._add_section("🏛️ Environnement de travail", fiche.get("environnement", ""))
        
    def _add_section(self, title, content):
        if not content:
            return
            
        section = ctk.CTkFrame(self.scroll, fg_color=Theme.BG_CARD, corner_radius=12)
        section.pack(fill="x", padx=15, pady=8)
        
        ctk.CTkLabel(
            section, text=title,
            font=Theme.FONT_SUBTITLE, text_color=Theme.ACCENT_BLUE
        ).pack(anchor="w", padx=15, pady=(12, 8))
        
        ctk.CTkLabel(
            section, text=content,
            font=Theme.FONT_BODY, text_color=Theme.TEXT_SECONDARY,
            justify="left", wraplength=550
        ).pack(anchor="w", padx=15, pady=(0, 15))


class TramePreparation(ctk.CTkFrame):
    """Trame de préparation à l'oral"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True)
        
        self._build()
        
    def _build(self):
        # TEMPS 1
        self._section_header("⏱️ TEMPS 1 — FICHE DE POSTE", "≈ 15 minutes", Theme.PRIMARY)
        
        self._question_card("👤 Présentation personnelle", [
            "Présentez-vous en quelques mots (parcours, formation, expériences clés)"
        ], Theme.ACCENT_BLUE)
        
        self._question_card("📋 Compréhension du poste", [
            "Quelles sont les missions principales du poste ?",
            "Quel est le positionnement hiérarchique ?",
            "Quels sont les enjeux stratégiques identifiés ?"
        ], Theme.ACCENT_PURPLE)
        
        self._question_card("💡 Motivations", [
            "Pourquoi ce poste vous intéresse-t-il ?",
            "En quoi correspond-il à vos aspirations ?",
            "Qu'est-ce qui vous attire dans cette administration ?"
        ], Theme.ACCENT_ORANGE)
        
        self._question_card("🎯 Adéquation compétences/profil", [
            "Quelles compétences possédez-vous pour ce poste ?",
            "Quelles expériences sont transférables ?",
            "Quels sont vos axes de progression ?"
        ], Theme.PRIMARY)
        
        self._question_card("⚡ Mise en situation", [
            "Comment aborderiez-vous les premiers mois ?",
            "Comment géreriez-vous une situation de conflit ?",
            "Quelle serait votre priorité ?"
        ], Theme.ACCENT_PINK)
        
        # TEMPS 2
        self._section_header("⏱️ TEMPS 2 — PROJET PROFESSIONNEL", "≈ 15 minutes", Theme.ACCENT_PURPLE)
        
        self._question_card("🚀 Vision de carrière", [
            "Comment voyez-vous votre évolution à 5 ans ?",
            "Quels types de postes visez-vous à terme ?",
            "Dans quelle administration souhaitez-vous évoluer ?"
        ], Theme.ACCENT_BLUE)
        
        self._question_card("🏛️ Connaissance du corps des attachés", [
            "Quelles sont les missions d'un attaché d'administration ?",
            "Quelles sont les valeurs du service public ?",
            "Quels sont les enjeux actuels de l'administration ?"
        ], Theme.ACCENT_ORANGE)
        
        self._question_card("⭐ Qualités et valeurs", [
            "Quelles sont vos principales qualités professionnelles ?",
            "Comment incarnez-vous les valeurs du service public ?",
            "Donnez un exemple de situation où vous les avez démontrées"
        ], Theme.PRIMARY)
        
        self._question_card("❓ Questions classiques", [
            "Pourquoi avoir choisi l'IRA de Lille ?",
            "Que vous a apporté la formation ?",
            "Avez-vous des questions pour le jury ?"
        ], Theme.ACCENT_PINK)
        
    def _section_header(self, title, subtitle, color):
        header = ctk.CTkFrame(self.scroll, fg_color="transparent")
        header.pack(fill="x", pady=(20, 15))
        
        line = ctk.CTkFrame(header, fg_color="transparent")
        line.pack(fill="x")
        
        ctk.CTkFrame(line, fg_color=color, height=2, corner_radius=1).pack(side="left", fill="x", expand=True, pady=10)
        ctk.CTkLabel(line, text=title, font=Theme.FONT_SUBTITLE, text_color=color).pack(side="left", padx=15)
        ctk.CTkFrame(line, fg_color=color, height=2, corner_radius=1).pack(side="left", fill="x", expand=True, pady=10)
        
        ctk.CTkLabel(header, text=subtitle, font=Theme.FONT_SMALL, text_color=Theme.TEXT_MUTED).pack()
        
    def _question_card(self, title, questions, color):
        card = ctk.CTkFrame(self.scroll, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        card.pack(fill="x", pady=6, padx=5)
        
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(12, 8))
        
        ctk.CTkFrame(header, fg_color=color, width=4, height=20, corner_radius=2).pack(side="left", padx=(0, 12))
        ctk.CTkLabel(header, text=title, font=Theme.FONT_SUBTITLE, text_color=Theme.TEXT_PRIMARY).pack(side="left")
        
        for q in questions:
            qf = ctk.CTkFrame(card, fg_color="transparent")
            qf.pack(fill="x", padx=30, pady=3)
            ctk.CTkLabel(qf, text="•", font=Theme.FONT_BODY, text_color=color).pack(side="left", padx=(0, 10))
            ctk.CTkLabel(qf, text=q, font=Theme.FONT_BODY, text_color=Theme.TEXT_SECONDARY,
                        wraplength=350, justify="left").pack(side="left")
        
        ctk.CTkFrame(card, fg_color="transparent", height=10).pack()


class FichesList(ctk.CTkFrame):
    """Liste des fiches de poste avec recherche"""
    
    def __init__(self, master, on_select, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.on_select = on_select
        self.filtered_fiches = FICHES_DATABASE.copy()
        
        # Header
        ctk.CTkLabel(self, text="📁 Fiches de postes", font=Theme.FONT_TITLE,
                    text_color=Theme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 10))
        
        # Recherche
        search_frame = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=10, height=40)
        search_frame.pack(fill="x", pady=(0, 10))
        search_frame.pack_propagate(False)
        
        ctk.CTkLabel(search_frame, text="🔍", font=("Segoe UI", 14), text_color=Theme.TEXT_MUTED).pack(side="left", padx=(12, 5))
        
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self._filter)
        
        ctk.CTkEntry(
            search_frame, textvariable=self.search_var,
            placeholder_text="Rechercher...",
            fg_color="transparent", border_width=0,
            font=Theme.FONT_BODY, text_color=Theme.TEXT_PRIMARY
        ).pack(side="left", fill="both", expand=True, padx=5)
        
        # Filtres rapides
        filters = ctk.CTkFrame(self, fg_color="transparent")
        filters.pack(fill="x", pady=(0, 10))
        
        self.filter_var = ctk.StringVar(value="Tous")
        self.filter_buttons = {}
        
        for text in ["Tous", "Centrale", "Déconcentrée", "Scolaire"]:
            btn = ctk.CTkButton(
                filters, text=text, height=28,
                fg_color=Theme.PRIMARY if text == "Tous" else "transparent",
                hover_color=Theme.PRIMARY_LIGHT,
                text_color=Theme.BG_DARK if text == "Tous" else Theme.TEXT_SECONDARY,
                font=Theme.FONT_SMALL, corner_radius=8,
                command=lambda t=text: self._set_filter(t)
            )
            btn.pack(side="left", padx=2)
            self.filter_buttons[text] = btn
        
        # Liste
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color=Theme.BG_CARD, corner_radius=12)
        self.list_frame.pack(fill="both", expand=True)
        
        self._display_fiches()
        
    def _set_filter(self, filter_type):
        self.filter_var.set(filter_type)
        
        # Mettre à jour l'apparence des boutons
        for text, btn in self.filter_buttons.items():
            if text == filter_type:
                btn.configure(fg_color=Theme.PRIMARY, text_color=Theme.BG_DARK)
            else:
                btn.configure(fg_color="transparent", text_color=Theme.TEXT_SECONDARY)
        
        self._filter()
        
    def _filter(self, *args):
        search = self.search_var.get().lower()
        filter_type = self.filter_var.get()
        
        self.filtered_fiches = []
        
        for fiche in FICHES_DATABASE:
            # Filtre par type
            if filter_type == "Centrale" and "CENTRALE" not in fiche["administration"]:
                continue
            elif filter_type == "Déconcentrée" and "DÉCONCENTRÉE" not in fiche["administration"]:
                continue
            elif filter_type == "Scolaire" and "SCOLAIRE" not in fiche["administration"]:
                continue
                
            # Filtre par recherche
            if search:
                searchable = f"{fiche['titre']} {fiche['structure']} {fiche['domaine']}".lower()
                if search not in searchable:
                    continue
                    
            self.filtered_fiches.append(fiche)
            
        self._display_fiches()
        
    def _display_fiches(self):
        for w in self.list_frame.winfo_children():
            w.destroy()
            
        if not self.filtered_fiches:
            ctk.CTkLabel(
                self.list_frame, text="Aucune fiche trouvée",
                font=Theme.FONT_BODY, text_color=Theme.TEXT_MUTED
            ).pack(pady=20)
            return
            
        for fiche in self.filtered_fiches:
            self._create_fiche_item(fiche)
            
    def _create_fiche_item(self, fiche):
        # Icône domaine
        domain_icons = {
            "RESSOURCES HUMAINES": "👥",
            "BUDGET": "💰",
            "JURIDIQUE": "⚖️",
            "ACHAT": "🛒",
            "SÉCURITÉ": "🛡️",
            "POLITIQUES": "📊",
        }
        icon = "📄"
        for key, value in domain_icons.items():
            if key in fiche["domaine"].upper():
                icon = value
                break
        
        title = fiche["titre"][:40] + "..." if len(fiche["titre"]) > 40 else fiche["titre"]
        struct = fiche['structure'][:30] + "..." if len(fiche['structure']) > 30 else fiche['structure']
        
        btn = ctk.CTkButton(
            self.list_frame,
            text=f"{icon}  {title}\n      {struct}",
            fg_color="transparent",
            hover_color=Theme.BG_ELEVATED,
            corner_radius=8,
            height=60,
            anchor="w",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_PRIMARY,
            command=lambda f=fiche: self.on_select(f)
        )
        btn.pack(fill="x", pady=2)


# ══════════════════════════════════════════════════════════════════════════════
# APPLICATION PRINCIPALE
# ══════════════════════════════════════════════════════════════════════════════

class MiracleApp(ctk.CTk):
    """Application principale mIRAcle"""
    
    def __init__(self):
        super().__init__()
        
        self.title("mIRAcle — Préparation Oral IRA Lille")
        self.geometry("1500x850")
        self.minsize(1200, 700)
        self.configure(fg_color=Theme.BG_DARK)
        
        self.fiches_opened = 0
        self.session_start = datetime.now()
        
        self._build_ui()
        
    def _build_ui(self):
        # Header
        self._build_header()
        
        # Contenu principal
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Colonne gauche
        left = ctk.CTkFrame(main, fg_color="transparent", width=300)
        left.pack(side="left", fill="y", padx=(0, 15))
        left.pack_propagate(False)
        
        # Timer
        timer_card = GlowingCard(left)
        timer_card.pack(fill="x", pady=(0, 15))
        self.timer = CircularTimer(timer_card, size=170)
        self.timer.pack(padx=15, pady=15)
        
        # Stats
        stats = ctk.CTkFrame(left, fg_color="transparent")
        stats.pack(fill="x", pady=(0, 15))
        
        self.stat_fiches = StatBox(stats, "Fiches vues", 0, "📄", Theme.ACCENT_BLUE)
        self.stat_fiches.pack(fill="x", pady=(0, 8))
        
        self.stat_time = StatBox(stats, "Session", 0, "⏱️", Theme.ACCENT_PURPLE)
        self.stat_time.pack(fill="x")
        self._update_session()
        
        # Liste des fiches
        self.fiches_list = FichesList(left, on_select=self._on_fiche_select)
        self.fiches_list.pack(fill="both", expand=True)
        
        # Colonne centrale
        center = ctk.CTkFrame(main, fg_color="transparent")
        center.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        # Tabs
        self.tabs = ctk.CTkTabview(
            center,
            fg_color=Theme.BG_CARD,
            segmented_button_fg_color=Theme.BG_ELEVATED,
            segmented_button_selected_color=Theme.PRIMARY,
            segmented_button_selected_hover_color=Theme.PRIMARY_DIM,
            segmented_button_unselected_color=Theme.BG_ELEVATED,
            segmented_button_unselected_hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_PRIMARY,
            corner_radius=16
        )
        self.tabs.pack(fill="both", expand=True)
        
        # Tab Fiche
        tab_fiche = self.tabs.add("📄 Fiche de poste")
        self.fiche_viewer = FicheViewer(tab_fiche)
        self.fiche_viewer.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab Notes
        tab_notes = self.tabs.add("📝 Mes notes")
        self.notes = ctk.CTkTextbox(
            tab_notes,
            fg_color=Theme.BG_ELEVATED,
            text_color=Theme.TEXT_PRIMARY,
            font=Theme.FONT_MONO,
            corner_radius=12
        )
        self.notes.pack(fill="both", expand=True, padx=10, pady=10)
        self.notes.insert("1.0", "Utilisez cet espace pour prendre des notes durant votre préparation...\n\n")
        
        # Colonne droite
        right = ctk.CTkFrame(main, fg_color="transparent", width=400)
        right.pack(side="left", fill="y")
        right.pack_propagate(False)
        
        # Header trame
        trame_header = ctk.CTkFrame(right, fg_color="transparent")
        trame_header.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(trame_header, text="📋 Trame de préparation",
                    font=Theme.FONT_TITLE, text_color=Theme.TEXT_PRIMARY).pack(side="left")
        
        badge = ctk.CTkFrame(trame_header, fg_color=Theme.PRIMARY_LIGHT, corner_radius=8)
        badge.pack(side="right")
        ctk.CTkLabel(badge, text="IRA LILLE", font=("Segoe UI", 10, "bold"),
                    text_color=Theme.PRIMARY).pack(padx=10, pady=4)
        
        # Trame
        trame_card = ctk.CTkFrame(right, fg_color=Theme.BG_CARD, corner_radius=16)
        trame_card.pack(fill="both", expand=True)
        
        self.trame = TramePreparation(trame_card)
        self.trame.pack(fill="both", expand=True, padx=10, pady=10)
        
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent", height=60)
        header.pack(fill="x", padx=20, pady=(15, 10))
        header.pack_propagate(False)
        
        # Logo
        logo_frame = ctk.CTkFrame(header, fg_color="transparent")
        logo_frame.pack(side="left")
        
        logo_bg = ctk.CTkFrame(logo_frame, fg_color=Theme.PRIMARY, corner_radius=12, width=45, height=45)
        logo_bg.pack(side="left")
        logo_bg.pack_propagate(False)
        ctk.CTkLabel(logo_bg, text="m", font=("Segoe UI", 24, "bold"),
                    text_color=Theme.BG_DARK).place(relx=0.5, rely=0.5, anchor="center")
        
        title_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        title_frame.pack(side="left", padx=(12, 0))
        
        ctk.CTkLabel(title_frame, text="mIRAcle", font=("Segoe UI", 22, "bold"),
                    text_color=Theme.TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Préparation Oral IRA • 20 fiches intégrées",
                    font=Theme.FONT_SMALL, text_color=Theme.TEXT_MUTED).pack(anchor="w")
        
        # Bouton aide
        ctk.CTkButton(
            header, text="❓ Aide", height=40, width=100,
            fg_color="transparent", hover_color=Theme.BG_ELEVATED,
            border_width=1, border_color=Theme.ACCENT_BLUE,
            text_color=Theme.ACCENT_BLUE, corner_radius=10,
            command=self._show_help
        ).pack(side="right")
        
    def _on_fiche_select(self, fiche):
        self.fiche_viewer.display_fiche(fiche)
        self.fiches_opened += 1
        self.stat_fiches.update_value(self.fiches_opened)
        
    def _update_session(self):
        elapsed = (datetime.now() - self.session_start).seconds // 60
        self.stat_time.value_label.configure(text=f"{elapsed} min")
        self.after(60000, self._update_session)
        
    def _show_help(self):
        help_win = ctk.CTkToplevel(self)
        help_win.title("Aide — mIRAcle")
        help_win.geometry("600x500")
        help_win.configure(fg_color=Theme.BG_DARK)
        
        scroll = ctk.CTkScrollableFrame(help_win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(scroll, text="🎓 Guide de préparation",
                    font=Theme.FONT_DISPLAY, text_color=Theme.PRIMARY).pack(anchor="w", pady=(0, 20))
        
        help_text = """L'oral de classement de l'IRA se décompose en deux temps :

⏱️ TEMPS 1 — Fiche de poste (≈ 15 min)
• Présentation de votre compréhension du poste
• Questions sur vos motivations
• Mise en situation professionnelle

⏱️ TEMPS 2 — Projet professionnel (≈ 15 min)
• Vision de votre carrière
• Connaissance du corps des attachés
• Valeurs du service public

💡 Conseils :
• Utilisez le timer pour simuler les conditions réelles
• Parcourez plusieurs fiches pour vous entraîner
• Préparez des réponses structurées pour chaque question
• Utilisez l'onglet "Mes notes" pour vos préparations

📁 Fiches intégrées :
Cette version contient 20 fiches de postes types couvrant :
• Administration centrale (ministères, CDC)
• Administration déconcentrée (préfectures, DDI)
• Services académiques (rectorats)
• Établissements publics (OFPRA, CNDA)"""
        
        ctk.CTkLabel(scroll, text=help_text, font=Theme.FONT_BODY,
                    text_color=Theme.TEXT_SECONDARY, justify="left", wraplength=540).pack(anchor="w")
        
        ctk.CTkButton(scroll, text="✓ Compris !", fg_color=Theme.PRIMARY,
                     hover_color=Theme.PRIMARY_DIM, text_color=Theme.BG_DARK,
                     height=40, command=help_win.destroy).pack(pady=20)


# ══════════════════════════════════════════════════════════════════════════════
# SPLASH SCREEN
# ══════════════════════════════════════════════════════════════════════════════

class SplashScreen(ctk.CTk):
    """Écran de démarrage"""
    
    def __init__(self, on_complete):
        super().__init__()
        
        self.on_complete = on_complete
        
        self.title("mIRAcle")
        self.geometry("500x350")
        self.resizable(False, False)
        self.configure(fg_color=Theme.BG_DARK)
        self.overrideredirect(True)
        
        # Centrer
        self.eval('tk::PlaceWindow . center')
        
        self._build()
        self.progress = 0
        self._animate()
        
    def _build(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo
        logo = ctk.CTkFrame(container, fg_color=Theme.PRIMARY, corner_radius=25, width=80, height=80)
        logo.pack()
        logo.pack_propagate(False)
        ctk.CTkLabel(logo, text="m", font=("Segoe UI", 44, "bold"),
                    text_color=Theme.BG_DARK).place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(container, text="mIRAcle", font=("Segoe UI", 36, "bold"),
                    text_color=Theme.TEXT_PRIMARY).pack(pady=(20, 5))
        
        ctk.CTkLabel(container, text="Préparation Oral IRA Lille",
                    font=Theme.FONT_BODY, text_color=Theme.TEXT_MUTED).pack(pady=(5, 25))
        
        # Barre de progression
        self.progress_frame = ctk.CTkFrame(container, fg_color=Theme.BG_CARD, corner_radius=10, width=300, height=8)
        self.progress_frame.pack()
        self.progress_frame.pack_propagate(False)
        
        self.progress_bar = ctk.CTkFrame(self.progress_frame, fg_color=Theme.PRIMARY, corner_radius=10, width=0, height=8)
        self.progress_bar.place(x=0, y=0)
        
        self.status = ctk.CTkLabel(container, text="Chargement...",
                                   font=Theme.FONT_SMALL, text_color=Theme.TEXT_MUTED)
        self.status.pack(pady=(15, 0))
        
    def _animate(self):
        if self.progress < 100:
            self.progress += 3
            self.progress_bar.configure(width=int(300 * self.progress / 100))
            
            if self.progress < 30:
                self.status.configure(text="Chargement des composants...")
            elif self.progress < 60:
                self.status.configure(text="Initialisation des fiches...")
            elif self.progress < 90:
                self.status.configure(text="Préparation de l'interface...")
            else:
                self.status.configure(text="Prêt !")
                
            self.after(25, self._animate)
        else:
            self.after(400, self._finish)
            
    def _finish(self):
        self.destroy()
        self.on_complete()


# ══════════════════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE
# ══════════════════════════════════════════════════════════════════════════════

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    def launch():
        app = MiracleApp()
        app.mainloop()
    
    splash = SplashScreen(on_complete=launch)
    splash.mainloop()


if __name__ == "__main__":
    main()
