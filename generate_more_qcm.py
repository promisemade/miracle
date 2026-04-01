#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate additional QCM from finances publiques knowledge base
Target: 25+ more QCM on budget procedures, organic laws, parliamentary process
"""
import json

# Load existing data
with open('data/questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

qcm_list = data.get('qcm', [])
fc_list = data.get('flashcards', [])
next_qcm_id = max([q['id'] for q in qcm_list], default=0) + 1
next_fc_id = max([f['id'] for f in fc_list], default=0) + 1

# Additional QCM on budget procedures, parliamentary process, and finance controls
more_qcm = [
    {
        "id": 246,
        "category": "budget",
        "question": "Quel organe parlementaire est responsable de l'examen initial du projet de loi de finances?",
        "options": ["Commission des finances du Sénat", "Commission des finances de l'Assemblée nationale", "Commission mixte paritaire", "Commission de défense"],
        "correct": 1,
        "explanation": "La Commission des finances de l'Assemblée nationale est responsable de l'examen initial du projet de loi de finances. Le Sénat l'examine ensuite.",
        "difficulty": 2
    },
    {
        "id": 247,
        "category": "budget",
        "question": "Qui fixe le taux de TVA en France?",
        "options": ["Le ministre des Finances", "Le Parlement par la loi", "La Commission européenne", "Les collectivités territoriales"],
        "correct": 1,
        "explanation": "Les taux de TVA sont fixés par le Parlement dans la loi de finances. Il existe des taux normaux, réduits et super-réduits.",
        "difficulty": 1
    },
    {
        "id": 248,
        "category": "finances",
        "question": "Qu'est-ce que l'impôt sur le revenu (IR)?",
        "options": [
            "Un impôt foncier",
            "Un impôt direct prélevé sur le revenu des personnes physiques",
            "Un impôt indirect sur la consommation",
            "Une taxe professionnelle"
        ],
        "correct": 1,
        "explanation": "L'impôt sur le revenu (IR) est un impôt direct et progressif prélevé annuellement sur le revenu global des personnes physiques résidentes en France.",
        "difficulty": 1
    },
    {
        "id": 249,
        "category": "finances",
        "question": "Qu'est-ce que l'impôt sur les sociétés (IS)?",
        "options": [
            "Une taxe sur l'emploi",
            "Un impôt prélevé sur les bénéfices réalisés par les sociétés et personnes morales",
            "Un impôt foncier spécialisé",
            "Une contribution sociale"
        ],
        "correct": 1,
        "explanation": "L'impôt sur les sociétés (IS) est un impôt direct prélevé sur le bénéfice fiscal des entreprises et autres personnes morales. Le taux normal est d'environ 25% (2022).",
        "difficulty": 1
    },
    {
        "id": 250,
        "category": "finances",
        "question": "Qu'est-ce que la TVA?",
        "options": [
            "Une taxe d'habitation sur les immeubles",
            "Un impôt indirect sur la consommation prélevé à chaque stade de la production/distribution",
            "Une contribution aux assurances",
            "Un droit de mutation immobilière"
        ],
        "correct": 1,
        "explanation": "La Taxe sur la Valeur Ajoutée (TVA) est un impôt indirect sur la consommation, prélevé à chaque étape du processus de production/distribution.",
        "difficulty": 1
    },
    {
        "id": 251,
        "category": "budget",
        "question": "Quel taux de TVA s'applique généralement sur les produits alimentaires?",
        "options": ["20%", "10%", "5.5%", "2.1%"],
        "correct": 2,
        "explanation": "Le taux réduit de 5.5% s'applique à la plupart des produits alimentaires, sauf les boissons alcoolisées et certains produits spécifiques.",
        "difficulty": 2
    },
    {
        "id": 252,
        "category": "finances",
        "question": "Qu'est-ce que la CSG (Contribution Sociale Généralisée)?",
        "options": [
            "Un impôt foncier sur les sociétés",
            "Une contribution sociale prélevée sur les revenus pour financer la sécurité sociale",
            "Un droit d'enregistrement",
            "Une taxe professionnelle"
        ],
        "correct": 1,
        "explanation": "La CSG est une contribution sociale généralisée prélevée à taux unique sur la plupart des revenus (salaires, revenus de placement, pensions) pour financer la sécurité sociale.",
        "difficulty": 1
    },
    {
        "id": 253,
        "category": "budget",
        "question": "Qu'est-ce que le GFP (Groupe de financement public)?",
        "options": [
            "Un organisme de contrôle budgétaire",
            "Une structure permettant aux communes de mutualiser leurs ressources et services",
            "Un ministère spécialisé",
            "Un organe du Parlement"
        ],
        "correct": 1,
        "explanation": "Un GFP (Groupement de financement public) est une structure permettant aux collectivités (communes surtout) de mutualiser leurs besoins financiers et d'optimiser leurs ressources.",
        "difficulty": 2
    },
    {
        "id": 254,
        "category": "finances",
        "question": "Qu'est-ce qu'une dotation de l'État aux collectivités?",
        "options": [
            "Un prêt avec intérêt",
            "Une aide financière versée par l'État pour couvrir une part des dépenses des collectivités territoriales",
            "Un impôt local collecté par l'État",
            "Une subvention d'entreprise"
        ],
        "correct": 1,
        "explanation": "Les dotations de l'État (DGF, DCTP, etc.) sont des aides financières versées aux collectivités territoriales pour compenser les inégalités et couvrir une part de leurs dépenses.",
        "difficulty": 1
    },
    {
        "id": 255,
        "category": "budget",
        "question": "Qu'est-ce que la DGCL?",
        "options": [
            "Direction Générale de la Concurrence et de la Liberté",
            "Direction Générale des Collectivités Locales (sous-direction des finances des collectivités)",
            "Délégation Générale pour le Commerce Libre",
            "Direction Générale des Contributions Locales"
        ],
        "correct": 1,
        "explanation": "La DGCL (Direction Générale des Collectivités Locales) est un service du ministère des Collectivités territoriales responsable des relations financières État-collectivités.",
        "difficulty": 2
    },
    {
        "id": 256,
        "category": "finances",
        "question": "Qu'est-ce qu'une concession?",
        "options": [
            "Un remboursement fiscal",
            "Un contrat par lequel une collectivité confie à un concessionnaire la gestion d'un service ou d'une infrastructure publics",
            "Un droit d'exercer une profession",
            "Un emprunt bancaire public"
        ],
        "correct": 1,
        "explanation": "Une concession est un type de partenariat public-privé où un concessionnaire gère, entretient et investit dans une infrastructure/service public (routes, eau, énergie) moyennant une rémunération.",
        "difficulty": 2
    },
    {
        "id": 257,
        "category": "budget",
        "question": "Quel est le rôle de la CNAMTS?",
        "options": [
            "Gérer les finances de la Police Nationale",
            "Gérer les dépenses d'assurance maladie du régime général de la Sécurité sociale",
            "Contrôler les budgets des ministères",
            "Collecter les impôts locaux"
        ],
        "correct": 1,
        "explanation": "La CNAMTS (Caisse Nationale de l'Assurance Maladie des Travailleurs Salariés) gère les prestations et finances du régime d'assurance maladie du régime général.",
        "difficulty": 2
    },
    {
        "id": 258,
        "category": "finances",
        "question": "Qu'est-ce que la 'niche fiscale'?",
        "options": [
            "Une petite succursale du fisc",
            "Un rétrécissement des bases fiscales à cause de la fraude",
            "Un avantage fiscal réduisant les rentrées (ex: réductions d'impôt, exonérations)",
            "Une zone franche d'imposition"
        ],
        "correct": 2,
        "explanation": "Une niche fiscale est un dispositif d'avantage fiscal (réduction, crédit, exonération) qui réduit les rentrées publiques attendues. Exemple: réduction d'impôt pour travaux écologiques.",
        "difficulty": 2
    },
    {
        "id": 259,
        "category": "budget",
        "question": "Quel article de la Constitution interdit les votes bloqués du Parlement?",
        "options": ["Article 31", "Article 44", "Article 49", "Article 52"],
        "correct": 1,
        "explanation": "L'article 44 de la Constitution permet au Gouvernement de demander un vote unique sur tout ou partie d'un texte. Cela limite les amendements parlementaires.",
        "difficulty": 3
    },
    {
        "id": 260,
        "category": "finances",
        "question": "Qu'est-ce que la cotisation sociales?",
        "options": [
            "Un impôt sur les sociétés",
            "Une contribution prélevée sur les salaires pour financer la Sécurité sociale",
            "Un droit d'inscription",
            "Une taxe professionnelle"
        ],
        "correct": 1,
        "explanation": "Les cotisations sociales sont des prélèvements obligatoires versés par les salariés et les employeurs au système de Sécurité sociale pour financer la maladie, retraite, etc.",
        "difficulty": 1
    },
    {
        "id": 261,
        "category": "budget",
        "question": "Qu'est-ce que l'article 45 de la Constitution?",
        "options": [
            "Article sur la dissolution de l'Assemblée nationale",
            "Article précisant les étapes du vote d'une loi",
            "Article sur l'incompatibilité des mandats",
            "Article protégeant la liberté d'expression"
        ],
        "correct": 1,
        "explanation": "L'article 45 de la Constitution décrit la procédure législative: examen en commission, en séance, vote, transmission au Sénat, procédure de conciliation.",
        "difficulty": 3
    },
    {
        "id": 262,
        "category": "finances",
        "question": "Qu'est-ce qu'un décret budgétaire?",
        "options": [
            "Un acte du Président de la République",
            "Un acte réglementaire d'exécution du budget voté par le Parlement",
            "Une décision de la Cour des comptes",
            "Un veto parlementaire"
        ],
        "correct": 1,
        "explanation": "Les décrets budgétaires sont des actes réglementaires (notamment les décrets de report de crédits) qui modifient l'exécution du budget votéans cadre des compétences du Gouvernement.",
        "difficulty": 2
    },
    {
        "id": 263,
        "category": "budget",
        "question": "Qu'est-ce que la 'condition suspensive' dans une loi de finances?",
        "options": [
            "Un délai d'application d'une dispositionf",
            "Une clause subjordonnant la mise en œuvre à certaines conditions",
            "Une restriction des pouvoirs du Parlement",
            "Un amendement rejeté"
        ],
        "correct": 1,
        "explanation": "Une condition suspensive dans une loi (ex: 'cette subvention sera versée si l'état d'urgence est déclaré') rend l'application d'une disposition dépendante d'un événement futur.",
        "difficulty": 3
    },
    {
        "id": 264,
        "category": "finances",
        "question": "Qu'est-ce que le déficit structurel?",
        "options": [
            "Un déficit dû à une crise ponctuelle",
            "Le déficit qui persisterait même en situation économique normale",
            "L'absence de budget structuré",
            "Un déficit des collectivités territoriales"
        ],
        "correct": 1,
        "explanation": "Le déficit structurel (ou déficit primaire ajusté) est le déficit qui persisterait même si l'économie était au plein emploi. Différent du déficit cyclique.",
        "difficulty": 3
    },
    {
        "id": 265,
        "category": "budget",
        "question": "Qu'est-ce que la règle du '3%' de déficit?",
        "options": [
            "Une règle française obligatoire",
            "Un critère d'adhésion à l'euro limitant le déficit budgétaire à 3% du PIB",
            "Un ratio d'endettement obligatoire",
            "Un pourcentage de TVA"
        ],
        "correct": 1,
        "explanation": "Le critère des 3% (de Maastricht) limite le déficit budgétaire public à 3% du PIB pour les États membres de la zone euro. La règle de la dette limite l'endettement à 60% du PIB.",
        "difficulty": 2
    },
    {
        "id": 266,
        "category": "finances",
        "question": "Qu'est-ce qu'une enveloppe budgétaire plafonnée?",
        "options": [
            "Un budget qui peut être augmenté sans limite",
            "Un budget limité à un montant maximum fixé à l'avance",
            "Un budget sans contrôle",
            "Un budget d'aide d'urgence"
        ],
        "correct": 1,
        "explanation": "Une enveloppe budgétaire plafonnée fixe un montant maximum de dépenses pour une action. Dépassements interdits sauf par amendement votant plus de crédits.",
        "difficulty": 1
    },
    {
        "id": 267,
        "category": "budget",
        "question": "Qui est responsable de la mise en œuvre du budget de l'État?",
        "options": ["Le Parlement", "Le Gouvernement", "La Cour des comptes", "L'opposition"],
        "correct": 1,
        "explanation": "Le Gouvernement, via le ministre des Finances et les ministres gestionnaires, est responsable de l'exécution du budget voté par le Parlement.",
        "difficulty": 1
    },
    {
        "id": 268,
        "category": "finances",
        "question": "Qu'est-ce qu'un 'engagement de dépense'?",
        "options": [
            "Un paiement effectué",
            "L'acte administratif créant une obligation de payer (commande, convention de subvention)",
            "Un emprunt contracté",
            "Une facture reçue"
        ],
        "correct": 1,
        "explanation": "L'engagement est l'acte par lequel l'administration s'oblige à engager une dépense (ex: signature d'un marché). C'est distinct du décaissement effectif.",
        "difficulty": 2
    },
    {
        "id": 269,
        "category": "budget",
        "question": "Qu'est-ce qu'une 'mandatement'?",
        "options": [
            "Une nomination à un mandat électif",
            "L'ordre de paiement d'une dépense publique",
            "Un mandat de dépôt judiciaire",
            "Une délégation de pouvoir"
        ],
        "correct": 1,
        "explanation": "Le mandatement est l'acte administratif ordonnant le paiement d'une dépense. C'est l'ordre donné au comptable public de décaisser les fonds.",
        "difficulty": 2
    },
    {
        "id": 270,
        "category": "finances",
        "question": "Qu'est-ce qu'un 'titre de recette'?",
        "options": [
            "Un billet de banque",
            "L'acte administratif constatant une créance publique",
            "Un bon d'achat du secteur public",
            "Un reçu fiscal"
        ],
        "correct": 1,
        "explanation": "Le titre de recette est l'acte administratif émis par l'ordonnateur (ministre) constatant une créance de l'État ou d'une collectivité (ex: titre de perception d'un impôt).",
        "difficulty": 3
    }
]

# Additional flashcards
more_fc = [
    {
        "id": 127,
        "category": "budget",
        "front": "Quel organe exécute les dépenses budgétaires en premier lieu?",
        "back": "L'ordonnateur (ministre) qui engage, mandate et liquide les dépenses publiques",
        "difficulty": 2
    },
    {
        "id": 128,
        "category": "finances",
        "front": "Qu'est-ce que l'impôt sur le revenu (IR)?",
        "back": "Impôt direct et progressif prélevé sur le revenu global des personnes physiques",
        "difficulty": 1
    },
    {
        "id": 129,
        "category": "finances",
        "front": "Qu'est-ce que l'impôt sur les sociétés (IS)?",
        "back": "Impôt prélevé sur le bénéfice des sociétés et personnes morales (taux ~25%)",
        "difficulty": 1
    },
    {
        "id": 130,
        "category": "finances",
        "front": "Qu'est-ce que la TVA?",
        "back": "Taxe indirecte sur la consommation prélevée à chaque stade de production/distribution",
        "difficulty": 1
    },
    {
        "id": 131,
        "category": "budget",
        "front": "Quel taux de TVA s'applique sur les produits alimentaires?",
        "back": "Taux réduit de 5.5% (sauf boissons alcoolisées)",
        "difficulty": 1
    },
    {
        "id": 132,
        "category": "finances",
        "front": "Qu'est-ce que la CSG?",
        "back": "Contribution Sociale Généralisée: contribution prélevée sur les revenus pour la Sécurité sociale",
        "difficulty": 1
    },
    {
        "id": 133,
        "category": "budget",
        "front": "Qu'est-ce qu'une dotation de l'État aux collectivités?",
        "back": "Aide financière versée par l'État pour couvrir une part des dépenses locales",
        "difficulty": 1
    },
    {
        "id": 134,
        "category": "finances",
        "front": "Qu'est-ce qu'une concession en finances publiques?",
        "back": "Contrat confiant à un privé la gestion d'un service public moyennant rémunération",
        "difficulty": 2
    },
    {
        "id": 135,
        "category": "budget",
        "front": "Qu'est-ce que le critère des 3% de Maastricht?",
        "back": "Limite du déficit budgétaire à 3% du PIB pour les États de la zone euro",
        "difficulty": 2
    },
    {
        "id": 136,
        "category": "finances",
        "front": "Qu'est-ce qu'un engagement de dépense?",
        "back": "Acte administratif créant l'obligation de payer (ex: signature d'un marché)",
        "difficulty": 2
    },
    {
        "id": 137,
        "category": "budget",
        "front": "Qu'est-ce qu'un titre de recette?",
        "back": "Acte administratif constatant une créance publique (ex: impôt, amende)",
        "difficulty": 3
    },
    {
        "id": 138,
        "category": "finances",
        "front": "Qu'est-ce qu'une niche fiscale?",
        "back": "Dispositif d'avantage fiscal réduisant les rentrées publiques (ex: réductions d'impôt)",
        "difficulty": 2
    }
]

# Append
qcm_list.extend(more_qcm)
fc_list.extend(more_fc)

# Save
with open('data/questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Validate
with open('data/questions.json', 'r', encoding='utf-8') as f:
    validated = json.load(f)

print(f"[OK] Added {len(more_qcm)} QCM (IDs {more_qcm[0]['id']}-{more_qcm[-1]['id']})")
print(f"[OK] Added {len(more_fc)} flashcards (IDs {more_fc[0]['id']}-{more_fc[-1]['id']})")
print(f"\nTotal statistics:")
print(f"  QCM: {len(validated['qcm'])}")
print(f"  Flashcards: {len(validated['flashcards'])}")
print(f"  TOTAL: {len(validated['qcm']) + len(validated['flashcards'])} questions")
