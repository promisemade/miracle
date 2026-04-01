#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate comprehensive QCM from Finances Publiques content
Target: 40+ new QCM + 20+ flashcards
"""
import json
from ebooklib import epub
from bs4 import BeautifulSoup

# Load existing data
with open('data/questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

qcm_list = data.get('qcm', [])
next_qcm_id = max([q['id'] for q in qcm_list], default=0) + 1
next_fc_id = max([data.get('flashcards', []) and max([f['id'] for f in data.get('flashcards', [])], default=0) or 0], default=0) + 1

# New comprehensive QCM on finances publiques topics
new_qcm = [
    {
        "id": 217,
        "category": "budget",
        "question": "Qu'est-ce que la LOLF?",
        "options": [
            "Loi d'Orientation et de Lesion des Finances",
            "Loi Organique relative aux Lois de Finances",
            "Loi d'Obligation Légale pour les Finances",
            "Loi Organisationnelle des Lois Financières"
        ],
        "correct": 1,
        "explanation": "La LOLF (Loi Organique relative aux Lois de Finances) du 1er août 2001 a réformé la présentation et l'exécution du budget de l'État, en remplaçant le vieux système des chapitres par une nouvelle logique de missions et programmes.",
        "difficulty": 2
    },
    {
        "id": 218,
        "category": "budget",
        "question": "Combien de temps dure l'exercice budgétaire de l'État?",
        "options": ["6 mois", "1 an (année civile)", "18 mois", "2 ans"],
        "correct": 1,
        "explanation": "L'exercice budgétaire coïncide avec l'année civile (du 1er janvier au 31 décembre). C'est une règle fondamentale du droit budgétaire français.",
        "difficulty": 1
    },
    {
        "id": 219,
        "category": "budget",
        "question": "Qu'est-ce qu'un PAP (Projet Annuel de Performance)?",
        "options": [
            "Un document de présentation des crédits budgétaires par programme avec objectifs et indicateurs",
            "Un plan d'action des politiques",
            "Une procédure d'audit public",
            "Un protocole d'accès aux prix"
        ],
        "correct": 0,
        "explanation": "Le PAP est un document qui présente, pour chaque programme, les objectifs, les indicateurs de performance et les crédits prévus. C'est un outil clé de la LOLF pour la transparence budgétaire.",
        "difficulty": 2
    },
    {
        "id": 220,
        "category": "budget",
        "question": "Qu'est-ce que le RAP (Rapport Annuel de Performance)?",
        "options": [
            "Le rapport de l'audit public régional",
            "Un document de restitution des réalisations et résultats atteints par rapport aux objectifs du PAP",
            "Un rapport annuel des prix",
            "Un rapport administratif personnel"
        ],
        "correct": 1,
        "explanation": "Le RAP est produit après l'exécution du budget et présente les résultats obtenus comparés aux objectifs fixés dans le PAP. C'est un outil d'évaluation de la performance publique.",
        "difficulty": 2
    },
    {
        "id": 221,
        "category": "finances",
        "question": "Qu'est-ce qu'une recette publique?",
        "options": [
            "Un billet de caisse enregistrée",
            "Un mouvement financier d'argent entrant dans les comptes publics",
            "Un reçu administratif",
            "Une facture payée par l'État"
        ],
        "correct": 1,
        "explanation": "Les recettes publiques sont des mouvements d'argent qui entrent dans les comptes des administrations publiques. Elles incluent les impôts, les cotisations sociales, les emprunts et autres revenus.",
        "difficulty": 1
    },
    {
        "id": 222,
        "category": "finances",
        "question": "Qu'est-ce qu'une dépense publique?",
        "options": [
            "Un investissement en bourse",
            "Un montant d'argent versé par l'administration publique pour fonctionner ou investir",
            "Une perte comptable",
            "Une allocation de ressources non utilisées"
        ],
        "correct": 1,
        "explanation": "Les dépenses publiques représentent l'ensemble des sommes versées par les administrations pour leur fonctionnement (salaires, fournitures) ou pour investir (infrastructures, équipements).",
        "difficulty": 1
    },
    {
        "id": 223,
        "category": "finances",
        "question": "Quelle est la différence entre le déficit budgétaire et la dette publique?",
        "options": [
            "Aucune, c'est la même chose",
            "Le déficit est un manque annuel; la dette est l'accumulation cumulée des déficits",
            "Le déficit concerne l'État; la dette concerne les collectivités",
            "La dette est plus grave que le déficit"
        ],
        "correct": 1,
        "explanation": "Le déficit budgétaire annuel correspond au manque entre dépenses et recettes sur un exercice. La dette publique est l'accumulation cumulée de tous les déficits antérieurs non remboursés.",
        "difficulty": 2
    },
    {
        "id": 224,
        "category": "finances",
        "question": "Qu'est-ce que la trésorerie publique?",
        "options": [
            "L'endroit où est stocké l'or de l'État",
            "L'ensemble de la dette publique",
            "L'administration en charge de la gestion des flux financiers de l'État au jour le jour",
            "La réserve monétaire du gouvernement"
        ],
        "correct": 2,
        "explanation": "La trésorerie (gérée par la Direction générale des finances publiques) assure la gestion au jour le jour des flux monétaires de l'État, y compris la collecte des impôts et le paiement des dépenses.",
        "difficulty": 2
    },
    {
        "id": 225,
        "category": "budget",
        "question": "Quel article de la Constitution parle de la loi de finances?",
        "options": ["Article 32", "Article 34", "Article 37", "Article 41"],
        "correct": 1,
        "explanation": "L'article 34 de la Constitution réserve au domaine de la loi les dispositions relatives aux lois de finances. C'est un principe fondamental de la séparation des pouvoirs.",
        "difficulty": 3
    },
    {
        "id": 226,
        "category": "budget",
        "question": "Qui propose la loi de finances initiale?",
        "options": ["L'Assemblée nationale", "Le Gouvernement", "Le Sénat", "Le Président de la République"],
        "correct": 1,
        "explanation": "C'est le Gouvernement (notamment via le ministre des Finances) qui élabore et propose la loi de finances initiale au Parlement. L'Assemblée nationale en est le premier destinataire.",
        "difficulty": 2
    },
    {
        "id": 227,
        "category": "budget",
        "question": "Quel est le délai d'examen de la loi de finances par l'Assemblée nationale?",
        "options": ["15 jours", "40 jours", "60 jours", "90 jours"],
        "correct": 1,
        "explanation": "L'Assemblée nationale dispose d'un délai de 40 jours pour examiner et voter la loi de finances initiale (dispositions LOLF). Ce délai peut être réduit.",
        "difficulty": 3
    },
    {
        "id": 228,
        "category": "budget",
        "question": "Qu'est-ce qu'une loi de finances rectificative?",
        "options": [
            "Une loi qui corrige une erreur de calcul",
            "Une loi votée en cours d'année pour ajuster les prévisions budgétaires",
            "Une loi qui annule la loi de finances initiale",
            "Une loi régulièrement votée en septembre"
        ],
        "correct": 1,
        "explanation": "Les lois de finances rectificatives (LFR) modifient la loi de finances initiale en cours d'année pour adapter les crédits aux réalités économiques ou aux changements de priorités politiques.",
        "difficulty": 2
    },
    {
        "id": 229,
        "category": "finances",
        "question": "Comment s'appellent les administrations publiques qui gèrent les fonds sans contrôle budgétaire direct?",
        "options": [
            "Les organismes de droit privé",
            "Les organismes publics de type autonome",
            "Les établissements publics",
            "Les entreprises nationales"
        ],
        "correct": 2,
        "explanation": "Les établissements publics (EPA, EPIC) sont des structures administratives ou industrielles et commerciales publiques ayant une autonomie juridique et financière, avec un budget distinct de l'État.",
        "difficulty": 2
    },
    {
        "id": 230,
        "category": "finances",
        "question": "Quel est l'objectif principal de la Cour des comptes?",
        "options": [
            "Collecter les impôts",
            "Exercer le contrôle des finances publiques et de la régularité des comptes",
            "Fixer les taux d'imposition",
            "Géreri les salaires des fonctionnaires"
        ],
        "correct": 1,
        "explanation": "La Cour des comptes contrôle les finances des administrations publiques et rend compte au Parlement. Elle exerce un contrôle de régularité, de performance et d'économie.",
        "difficulty": 2
    },
    {
        "id": 231,
        "category": "budget",
        "question": "Qu'est-ce qu'une mission budgétaire selon la LOLF?",
        "options": [
            "Une task-force du ministère des Finances",
            "Un ensemble de programmes concourant à un objectif politique commun",
            "Un audit budgétaire spécialisé",
            "Un groupe de travail parlementaire"
        ],
        "correct": 1,
        "explanation": "Dans la LOLF, une mission est un regroupement de programmes sous un même ministre, visant à atteindre une politique publique définie. Exemple: Mission 'Sécurité' regroupant plusieurs programmes de police et gendarmerie.",
        "difficulty": 3
    },
    {
        "id": 232,
        "category": "budget",
        "question": "Qu'est-ce qu'un programme budgétaire selon la LOLF?",
        "options": [
            "Une liste de dépenses d'un ministère",
            "Une unité regroupant crédits et objectifs de performance pour une action spécifique",
            "Un planning de travail administratif",
            "Un rapport mensuel d'exécution"
        ],
        "correct": 1,
        "explanation": "Chaque programme regroupe les crédits destinés à une action spécifique avec ses propres objectifs, indicateurs et responsable (gestionnaire). Exemple: Programme 'Formation initiale' au ministère de l'Éducation.",
        "difficulty": 3
    },
    {
        "id": 233,
        "category": "finances",
        "question": "Quels sont les trois blocs principaux de l'administration publique française?",
        "options": [
            "Gouvernement, Parlement, Cours de justice",
            "État, Collectivités territoriales, Sécurité sociale",
            "Ministères, Préfectures, Universités",
            "Gouvernement, Régions, Mairies"
        ],
        "correct": 1,
        "explanation": "Les trois blocs du secteur public en finances publiques sont: (1) L'État et ses administrations, (2) Les collectivités territoriales et leurs groupements, (3) Le système de sécurité sociale.",
        "difficulty": 2
    },
    {
        "id": 234,
        "category": "finances",
        "question": "Quelle est la principale source de financement de la sécurité sociale?",
        "options": [
            "L'impôt sur le revenu",
            "Les cotisations sociales des employeurs et salariés",
            "Les droits d'accises",
            "L'emprunt public"
        ],
        "correct": 1,
        "explanation": "La sécurité sociale est principalement financée par les cotisations sociales (patronales et salariales), complétées depuis peu par des ressources fiscales (CSG, impôts divers).",
        "difficulty": 1
    },
    {
        "id": 235,
        "category": "finances",
        "question": "Qu'est-ce qu'une subvention publique?",
        "options": [
            "Un prêt sans intérêt",
            "Une aide financière sans contrepartie directe versée à une personne physique ou morale",
            "Une allocation de chômage",
            "Un remboursement d'impôt"
        ],
        "correct": 1,
        "explanation": "Une subvention est une aide financière fournie par les administrations publiques à des entités (personnes, entreprises, associations) pour soutenir des activités d'intérêt public, sans obligation directe de remboursement.",
        "difficulty": 1
    },
    {
        "id": 236,
        "category": "budget",
        "question": "En quel mois le gouvernement présente-t-il traditionnellement le projet de loi de finances?",
        "options": ["Juillet", "Septembre", "Octobre", "Novembre"],
        "correct": 2,
        "explanation": "Le projet de loi de finances est traditionnellement présenté en octobre au Parlement pour être voté avant la fin de l'année civile et entrer en vigueur le 1er janvier.",
        "difficulty": 1
    },
    {
        "id": 237,
        "category": "finances",
        "question": "Quel est le rôle principal du ministre des Finances?",
        "options": [
            "Organiser les élections",
            "Proposer la politique budgétaire et assurer l'exécution des finances publiques",
            "Nommer les juges",
            "Contrôler les collectivités territoriales"
        ],
        "correct": 1,
        "explanation": "Le ministre des Finances (ou des Comptes publics) propose au Gouvernement la politique budgétaire, élabore les lois de finances et assure leur exécution sous le contrôle du Parlement.",
        "difficulty": 1
    },
    {
        "id": 238,
        "category": "budget",
        "question": "Qu'est-ce que l'équilibre budgétaire?",
        "options": [
            "Quand les recettes égalent les dépenses",
            "Quand la dette diminue",
            "Quand les impôts augmentent",
            "Quand les dépenses sont supérieures aux recettes"
        ],
        "correct": 0,
        "explanation": "L'équilibre budgétaire correspond à une situation où les recettes publiques égalent les dépenses publiques. Un budget est en déficit quand les dépenses dépassent les recettes.",
        "difficulty": 1
    },
    {
        "id": 239,
        "category": "finances",
        "question": "Qu'est-ce qu'une opération de trésorerie?",
        "options": [
            "Une dépense inutile",
            "Un mouvement monétaire sans impact direct sur le résultat budgétaire (comme l'emprunt ou le remboursement de dette)",
            "Une collecte d'impôts",
            "Une subvention versée"
        ],
        "correct": 1,
        "explanation": "Les opérations de trésorerie (emprunts, remboursements de dette, gestion de trésorerie) ne modifient pas directement le résultat budgétaire (déficit/excédent) mais affectent la trésorerie immédiate.",
        "difficulty": 3
    },
    {
        "id": 240,
        "category": "budget",
        "question": "Quel est l'objectif de la transparence budgétaire instaurée par la LOLF?",
        "options": [
            "Réduire le coût de la fonction publique",
            "Permettre au Parlement et aux citoyens de mieux comprendre et contrôler les finances publiques",
            "Augmenter les dépenses de l'État",
            "Éliminer la fraude fiscale"
        ],
        "correct": 1,
        "explanation": "La LOLF a introduit une nouvelle transparence avec la logique missions/programmes, les PAP et RAP, pour donner au Parlement et aux citoyens une meilleure visibilité sur l'utilisation des fonds publics.",
        "difficulty": 2
    },
    {
        "id": 241,
        "category": "finances",
        "question": "Qu'est-ce qu'un impôt progressif?",
        "options": [
            "Un impôt qui augmente chaque année",
            "Un impôt dont le taux augmente avec la base imposable",
            "Un impôt payé progressivement pendant l'année",
            "Un impôt sans augmentation de taux"
        ],
        "correct": 1,
        "explanation": "Un impôt progressif a un taux qui augmente avec la base imposable (exemple: impôt sur le revenu). C'est l'opposé de l'impôt proportionnel ou régressif.",
        "difficulty": 2
    },
    {
        "id": 242,
        "category": "budget",
        "question": "Qu'est-ce qui différencie un budget en 'dépenses réelles' d'un budget en 'flux de trésorerie'?",
        "options": [
            "Rien, c'est identique",
            "Le budget réel enregistre les engagement des dépenses; le budget trésorerie enregistre les paiements effectifs",
            "Un concerne l'État, l'autre les collectivités",
            "C'est une différence d'échelle seulement"
        ],
        "correct": 1,
        "explanation": "Le budget en dépenses enregistre l'engagement de dépenser (achat commandé); le budget trésorerie enregistre le décaissement effectif. La différence peut être importante en trésorerie.",
        "difficulty": 3
    },
    {
        "id": 243,
        "category": "finances",
        "question": "Comment appelle-t-on les revenus générés par l'exploitation d'un bien ou service public?",
        "options": [
            "Les impôts directs",
            "Les produits et charges",
            "Les revenus domaniaux et les redevances publiques",
            "Les emprunts publics"
        ],
        "correct": 2,
        "explanation": "Les revenus domaniaux (location d'immeubles publics) et les redevances (frais de fréquentation, péages) constituent des sources de financement alternatives aux impôts pour l'administration publique.",
        "difficulty": 2
    },
    {
        "id": 244,
        "category": "budget",
        "question": "Quel document gouvernemental présente les objectifs de la politique budgétaire de l'année?",
        "options": [
            "Le rapport d'audit annuel",
            "Le rapport du Président au Parlement",
            "Le projet de loi de finances et sa lettre de cadrage",
            "L'évaluation de la dette publique"
        ],
        "correct": 2,
        "explanation": "Le projet de loi de finances (PLF) et sa lettre de cadrage présentent les grands principes et objectifs de la politique budgétaire pour l'année à venir.",
        "difficulty": 2
    },
    {
        "id": 245,
        "category": "finances",
        "question": "Qu'est-ce que le secteur institutionnel des APU (Administrations Publiques)?",
        "options": [
            "Un type de banque publique",
            "L'ensemble des administrations publiques incluant État, collectivités et sécurité sociale",
            "Une commission parlementaire",
            "Un service du ministère des Finances"
        ],
        "correct": 1,
        "explanation": "Dans la comptabilité nationale, les APU (Administrations Publiques) désignent collectivement l'État, les collectivités territoriales et organismes de sécurité sociale. C'est un secteur institutionnel de la comptabilité nationale.",
        "difficulty": 2
    }
]

# Add new flashcards
new_flashcards = [
    {
        "id": 115,
        "category": "budget",
        "front": "Que signifie l'acronyme LOLF?",
        "back": "Loi Organique relative aux Lois de Finances (réforme budgétaire de 2001)",
        "difficulty": 2
    },
    {
        "id": 116,
        "category": "budget",
        "front": "Qu'est-ce qu'un PAP (Projet Annuel de Performance)?",
        "back": "Document présentant les objectifs, indicateurs et crédits budgétaires d'un programme",
        "difficulty": 2
    },
    {
        "id": 117,
        "category": "budget",
        "front": "Quel est le délai d'examen de la loi de finances par l'Assemblée nationale?",
        "back": "40 jours (délai constitutionnel LOLF)",
        "difficulty": 2
    },
    {
        "id": 118,
        "category": "finances",
        "front": "Quelle est la différence entre déficit budgétaire et dette publique?",
        "back": "Le déficit = manque annuel; la dette = accumulation cumulée des déficits",
        "difficulty": 2
    },
    {
        "id": 119,
        "category": "finances",
        "front": "Quels sont les trois blocs de l'administration publique française?",
        "back": "État, Collectivités territoriales, Système de sécurité sociale",
        "difficulty": 1
    },
    {
        "id": 120,
        "category": "budget",
        "front": "Qu'est-ce qu'une mission budgétaire selon la LOLF?",
        "back": "Ensemble de programmes concourant à un objectif politique commun sous un ministre",
        "difficulty": 3
    },
    {
        "id": 121,
        "category": "finances",
        "front": "Quel est le rôle de la Cour des comptes?",
        "back": "Contrôler les finances publiques, la régularité des comptes et rendre compte au Parlement",
        "difficulty": 1
    },
    {
        "id": 122,
        "category": "finances",
        "front": "Qu'est-ce qu'une opération de trésorerie?",
        "back": "Mouvement monétaire sans impact direct sur le résultat budgétaire (emprunt, remboursement de dette)",
        "difficulty": 3
    },
    {
        "id": 123,
        "category": "budget",
        "front": "En quel mois le gouvernement présente-t-il traditionnellement le PLF?",
        "back": "Octobre (pour vote avant fin d'année et entrée en vigueur 1er janvier)",
        "difficulty": 1
    },
    {
        "id": 124,
        "category": "finances",
        "front": "Qu'est-ce qu'un impôt progressif?",
        "back": "Impôt dont le taux augmente avec la base imposable",
        "difficulty": 1
    },
    {
        "id": 125,
        "category": "finances",
        "front": "Qu'est-ce que les revenus domaniaux et redevances?",
        "back": "Revenus publics générés par l'exploitation de bien ou services (loyers, péages)",
        "difficulty": 2
    },
    {
        "id": 126,
        "category": "budget",
        "front": "Qu'est-ce qu'une loi de finances rectificative (LFR)?",
        "back": "Loi votée en cours d'année pour ajuster les prévisions budgétaires initiales",
        "difficulty": 1
    }
]

# Append to existing data
qcm_list.extend(new_qcm)
data['flashcards'].extend(new_flashcards)

# Validate and save
print(f"[*] Adding {len(new_qcm)} new QCM (IDs {new_qcm[0]['id']}-{new_qcm[-1]['id']})")
print(f"[*] Adding {len(new_flashcards)} new flashcards (IDs {new_flashcards[0]['id']}-{new_flashcards[-1]['id']})")

with open('data/questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Validate
with open('data/questions.json', 'r', encoding='utf-8') as f:
    validated = json.load(f)
    
print(f"\n[OK] JSON validated!")
print(f"Total QCM: {len(validated['qcm'])}")
print(f"Total Flashcards: {len(validated['flashcards'])}")
print(f"Total questions: {len(validated['qcm']) + len(validated['flashcards'])}")
