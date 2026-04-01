#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate comprehensive QCM on remaining domains:
- Contentieux administratif advanced
- Management and leadership
- Encadrement in function publique
Total: 40+ QCM covering all exam domains
"""
import json

# Load existing data
with open('data/questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

qcm_list = data.get('qcm', [])
fc_list = data.get('flashcards', [])
next_qcm_id = max([q['id'] for q in qcm_list], default=0) + 1
next_fc_id = max([f['id'] for f in fc_list], default=0) + 1

# Advanced Contentieux Administratif questions
advanced_qcm = [
    {
        "id": 271,
        "category": "juridique",
        "question": "Quel est le délai de prescription pour introduire un recours contentieux contre une décision administrative?",
        "options": ["30 jours", "60 jours", "2 mois", "4 mois"],
        "correct": 2,
        "explanation": "Le délai de prescription est de 2 mois à compter de la notification ou du point de départ du délai de recours. C'est un délai relativement court et strict.",
        "difficulty": 3
    },
    {
        "id": 272,
        "category": "juridique",
        "question": "Qu'est-ce que le sursis à exécution?",
        "options": [
            "Un rejet automatique du recours",
            "Une suspension provisoire de l'exécution d'un acte administratif pendant le jugement du recours",
            "Une amende supplémentaire",
            "Une procédure d'appel accélérée"
        ],
        "correct": 1,
        "explanation": "Le sursis à exécution permet au juge administratif de suspendre la mise en œuvre d'un acte contesté si cela présente une urgence et un risque de préjudice grave.",
        "difficulty": 3
    },
    {
        "id": 273,
        "category": "juridique",
        "question": "Qu'est-ce que l'exception de légalité?",
        "options": [
            "Une défense formelle contre le juge",
            "La possibilité d'invoquer l'illégalité d'un acte antérieur sans faire un recours direct contre cet acte",
            "Une sanction contre un recours abusif",
            "Un délai supplémentaire de recours"
        ],
        "correct": 1,
        "explanation": "L'exception de légalité permet de contester indirectement la légalité d'un acte antérieur lors d'un litige sur ses effets, sans respecter les délais de recours direct.",
        "difficulty": 3
    },
    {
        "id": 274,
        "category": "juridique",
        "question": "Qu'est-ce que le recours de plein contentieux?",
        "options": [
            "Un recours administrative préalable obligatoire",
            "Un recours permettant au juge d'annuler l'acte ET de rendre une nouvelle décision",
            "Un recours limité à l'annulation de l'acte",
            "Un recours accéléré sans instruction"
        ],
        "correct": 1,
        "explanation": "Le recours de plein contentieux (exemple: litiges de contrats, fiscalité) permet au juge non seulement d'annuler l'acte administratif mais aussi de substituer sa propre décision.",
        "difficulty": 3
    },
    {
        "id": 275,
        "category": "juridique",
        "question": "Qu'est-ce que la jurisprudence Duflos?",
        "options": [
            "Une décision sur le droit du travail",
            "Une jurisprudence établissant que les actes de gouvernement ne peuvent être attaqués en contentieux",
            "Une jurisprudence sur les abus de pouvoir",
            "Une règle de procédure civile"
        ],
        "correct": 1,
        "explanation": "L'arrêt Duflos (1923) établit l'immunité des actes de gouvernement (politique étrangère, dissolution, etc.) du contrôle juridictionnel, concept ultérieurement assoupli.",
        "difficulty": 3
    },
    {
        "id": 276,
        "category": "juridique",
        "question": "Qu'est-ce que l'illégalité manifeste?",
        "options": [
            "Un acte contraire à la loi évidente et palpable",
            "Une décision prise sans motif",
            "Une erreur de procédure mineure",
            "Un acte formel invalide"
        ],
        "correct": 0,
        "explanation": "L'illégalité manifeste, plus grave que l'illégalité ordinaire, est une violation de la loi évidete et palpable permettant une annulation même tardive en certains cas.",
        "difficulty": 3
    },
    {
        "id": 277,
        "category": "juridique",
        "question": "Qu'est-ce que le standard d'habilitation?",
        "options": [
            "Une permission officielle",
            "Un critère jurisprudentiel contrôlant l'utilisation des compétences discrétionnaires par l'administration",
            "Un permis administratif",
            "Un pouvoir délégué limité"
        ],
        "correct": 1,
        "explanation": "Le contrôle de l'habilitation vérifie que l'administration utilise ses pouvoirs dans les limites de sa compétence (ratione materiae, personae, temporis, loci).",
        "difficulty": 3
    },
    {
        "id": 278,
        "category": "juridique",
        "question": "Qu'est-ce que l'erreur de fait?",
        "options": [
            "Une erreur dans l'application de la loi",
            "Une méconnaissance de faits exactement établis pouvant justifier l'annulation d'un acte",
            "Une mauvaise compréhension des règles administratives",
            "Une omission de consultation"
        ],
        "correct": 1,
        "explanation": "L'erreur de fait (ex: administration se trompant sur l'âge du demandeur) peut vider un acte administratif s'il n'aurait pas été pris si les faits eussent été correctement établis.",
        "difficulty": 3
    },
    {
        "id": 279,
        "category": "rh",
        "question": "Qu'est-ce que le pouvoir disciplinaire dans la fonction publique?",
        "options": [
            "L'obligation de respecter l'horaire",
            "Le droit pour l'administration de sanctionner les agents pour manquements à leurs obligations",
            "Une formation obligatoire",
            "Un contrôle de présence"
        ],
        "correct": 1,
        "explanation": "Le pouvoir disciplinaire permet à l'administration de sanctionner les agents (avertissement, blâme, suspension, révocation) en cas de manquement à leurs obligations légales ou contractuelles.",
        "difficulty": 2
    },
    {
        "id": 280,
        "category": "rh",
        "question": "Qu'est-ce que le système de notation des agents publics?",
        "options": [
            "Un examen académique obligatoire",
            "Un système d'évaluation périodique des agents par leur hiérarchie ayant des conséquences sur avancement et rémunération",
            "Un test de compétences professionnelles",
            "Un classement universitaire"
        ],
        "correct": 1,
        "explanation": "La notation est l'évaluation annuelle ou bisannuelle des agents publics par leur supérieur hiérarchique, influençant les avancements, augmentations et gestion de carrière.",
        "difficulty": 1
    },
    {
        "id": 281,
        "category": "rh",
        "question": "Qu'est-ce que la formation professionnelle continue dans la FP?",
        "options": [
            "Une formation obligatoire une seule fois",
            "Un droit et devoir pour l'agent d'acquérir des compétences tout au long de sa carrière",
            "Une formation préalable à l'embauche",
            "Un diplôme universitaire"
        ],
        "correct": 1,
        "explanation": "La formation continue permet aux agents publics d'actualiser et développer leurs compétences. C'est un élément clé du professionnalisme et de l'adaptation à l'évolution.",
        "difficulty": 1
    },
    {
        "id": 282,
        "category": "rh",
        "question": "Qu'est-ce que la mobilité professionnelle en fonction publique?",
        "options": [
            "La possibilité de quitter la fonction publique",
            "La capacité/droit d'un agent à changer de poste, ministère ou collectivité au cours de sa carrière",
            "Un congé sabbatique",
            "Une mutation forcée"
        ],
        "correct": 1,
        "explanation": "La mobilité est le changement de poste/structure pour les agents. Elle peut être horizontale (même grade, nouveau poste) ou verticale (promotion). Elle est encouragée pour dynamiser les organisations.",
        "difficulty": 1
    },
    {
        "id": 283,
        "category": "achats",
        "question": "Qu'est-ce que la transparence en matière de commande publique?",
        "options": [
            "Un audit annuel des dépenses",
            "L'obligation de publier les appels d'offres et de justifier les choix de prestataires",
            "Une formation des acheteurs",
            "Une réduction des prix"
        ],
        "correct": 1,
        "explanation": "La transparence en commande publique impose la publication des avis de marché, l'indication des critères de sélection et la traçabilité pour prévenir la corruption et favoriser l'égalité.",
        "difficulty": 1
    },
    {
        "id": 284,
        "category": "achats",
        "question": "Qu'est-ce qu'un appel d'offres restreint?",
        "options": [
            "Un appel sans publicité",
            "Une procédure où seules certaines entreprises qualifiées sont invitées à soumissionner après sélection",
            "Un marché avec budget limité",
            "Un appel ouvert avec conditions de participation"
        ],
        "correct": 1,
        "explanation": "L'appel d'offres restreint (procédure adaptée) limite la participation à des candidats pré-sélectionnés selon des critères. Moins de publicité que l'appel ouvert.",
        "difficulty": 2
    },
    {
        "id": 285,
        "category": "audit",
        "question": "Qu'est-ce qu'un audit de conformité?",
        "options": [
            "Un test de sécurité informatique",
            "Un contrôle vérifiant le respect des procédures, lois et réglementations en vigueur",
            "Une inspection bancaire",
            "Un test de performance"
        ],
        "correct": 1,
        "explanation": "L'audit de conformité (ou audit légalité) vérifie que l'organisation respecte les lois, réglementations et procédures internes applicables à ses activités.",
        "difficulty": 2
    },
    {
        "id": 286,
        "category": "audit",
        "question": "Qu'est-ce qu'un audit de performance?",
        "options": [
            "Un test des employés",
            "Un contrôle examinant l'économie, l'efficacité et l'efficience dans l'utilisation des ressources",
            "Une mesure de productivité individuelle",
            "Un audit informatique"
        ],
        "correct": 1,
        "explanation": "L'audit de performance (ou audit d'économicité) vérifie que les ressources sont utilisées de façon économique (coûts minimisés), efficace (objectifs atteints) et efficiente (ressources optimisées).",
        "difficulty": 2
    },
    {
        "id": 287,
        "category": "general",
        "question": "Qu'est-ce qu'une politique publique?",
        "options": [
            "Un parti politique",
            "Un ensemble de mesures et actes de l'État visant à résoudre un problème public et atteindre des objectifs",
            "Une loi parlementaire",
            "Un programme électoral"
        ],
        "correct": 1,
        "explanation": "Une politique publique est une intervention volontaire de l'État (par lois, décrets, budgets) pour répondre à un besoin collectif ou résoudre un problème identifié.",
        "difficulty": 1
    },
    {
        "id": 288,
        "category": "general",
        "question": "Qu'est-ce que l'évaluation des politiques publiques?",
        "options": [
            "Un sondage d'opinion",
            "L'examen systématique de l'efficacité et de l'impact d'une politique pour en mesurer les résultats",
            "Un vote parlementaire",
            "Un audit financier uniquement"
        ],
        "correct": 1,
        "explanation": "L'évaluation des politiques publiques analyse l'atteinte des objectifs, les résultats, les impacts et les coûts pour améliorer la prise de décision politique future.",
        "difficulty": 2
    },
    {
        "id": 289,
        "category": "general",
        "question": "Qu'est-ce que la gouvernance publique?",
        "options": [
            "Le système d'élection des maires",
            "L'ensemble des processus de prise de décision et de mise en œuvre impliquant État, collectivités, acteurs privés et citoyens",
            "Un type d'administration locale",
            "Le pouvoir législatif uniquement"
        ],
        "correct": 1,
        "explanation": "La gouvernance publique désigne les modes de coordination, concertation et décision entre acteurs multiples (État, régions, entreprises, société civile) pour gérer les affaires publiques.",
        "difficulty": 2
    },
    {
        "id": 290,
        "category": "rh",
        "question": "Qu'est-ce que le management par objectifs (MBO) en fonction publique?",
        "options": [
            "Un système de punition des agents",
            "Une approche managériale fixant des objectifs clairs et mesurant la performance d'après leur atteinte",
            "Une réduction des salaires",
            "Un modèle syndical"
        ],
        "correct": 1,
        "explanation": "Le MBO (Management by Objectives) définit des objectifs SMART pour chaque agent ou équipe et évalue la performance d'après leur réalisation, améliorant clarté et motivation.",
        "difficulty": 2
    },
    {
        "id": 291,
        "category": "rh",
        "question": "Qu'est-ce que le coaching en contexte administratif?",
        "options": [
            "Un sport collectif",
            "Un accompagnement personnalisé d'un manager ou agent pour développer ses compétences et atteindre ses objectifs",
            "Une formation classique",
            "Un contrôle hiérarchique"
        ],
        "correct": 1,
        "explanation": "Le coaching est un soutien personnalisé où un coach aide un individu à identifier objectifs, obstacles et solutions pour progresser professionnellement.",
        "difficulty": 1
    },
    {
        "id": 292,
        "category": "rh",
        "question": "Qu'est-ce que l'intelligence émotionnelle pour un manager?",
        "options": [
            "La capacité à résoudre des équations",
            "La conscience de ses émotions et capacité à les gérer, ainsi qu'à comprendre celles des autres pour mieux manager",
            "Un test psychologique obligatoire",
            "Une formation en mathématiques"
        ],
        "correct": 1,
        "explanation": "L'intelligence émotionnelle (IE) est cruciale pour le management: auto-conscience, auto-régulation, empathie, relation interpersonnelle et motivation.",
        "difficulty": 2
    },
    {
        "id": 293,
        "category": "communication",
        "question": "Qu'est-ce que la communication interne dans une organisation?",
        "options": [
            "Les lettres administratives officielles",
            "L'ensemble des échanges d'information au sein de l'organisation visant cohésion, transparence et engagement",
            "Un journal interne uniquement",
            "Les e-mails hiérarchiques"
        ],
        "correct": 1,
        "explanation": "La communication interne englobe tous les canaux et messages (intranet, réunions, newsletters, face-à-face) transmettant information et renforçant la culture organisationnelle.",
        "difficulty": 1
    },
    {
        "id": 294,
        "category": "rh",
        "question": "Qu'est-ce que la gestion prévisionnelle des emplois et compétences (GPEC)?",
        "options": [
            "Une prévention du chômage",
            "Un processus anticipant évolutions métiers et compétences futures pour adapter RH et formations",
            "Une réduction d'effectifs",
            "Un recrutement accéléré"
        ],
        "correct": 1,
        "explanation": "La GPEC anticipe transformations technologiques, démographiques et professionnelles pour adapter l'organisation: recrutement, formation, mobilité préparés à l'avance.",
        "difficulty": 2
    },
    {
        "id": 295,
        "category": "rh",
        "question": "Qu'est-ce qu'un conflit interpersonnel au travail?",
        "options": [
            "Une grève obligatoire",
            "Un désaccord ou tension entre personnes pouvant affecter environnement et productivité",
            "Une faute disciplinaire",
            "Une incompétence professionnelle"
        ],
        "correct": 1,
        "explanation": "Les conflits interpersonnels (incompréhensions, rivalités, mauvaise communication) sont fréquents. Un bon manager les identifie tôt et cherche à les résoudre ou en réduire impacts.",
        "difficulty": 1
    },
    {
        "id": 296,
        "category": "rh",
        "question": "Qu'est-ce que l'empowerment dans le management?",
        "options": [
            "Un congé supplémentaire",
            "La délégation de pouvoir et autonomie aux agents pour prendre décisions et agir en responsabilité",
            "Une augmentation de salaire",
            "Une promotion automatique"
        ],
        "correct": 1,
        "explanation": "L'empowerment donne aux agents autonomie de décision et responsabilités, les rendant plus engagés, motivés et efficaces. C'est une approche moderne du leadership.",
        "difficulty": 2
    },
    {
        "id": 297,
        "category": "communication",
        "question": "Qu'est-ce que l'écoute active en management?",
        "options": [
            "Entendre sans répondre",
            "Technique de communication privilégiant compréhension, empathie et feedback pour renforcer relations",
            "Surveillance des communications",
            "Un journal de bord"
        ],
        "correct": 1,
        "explanation": "L'écoute active (attention complète, reformulation, empathie, questions) renforce compréhension mutuelle et confiance, essentielle pour un management efficace.",
        "difficulty": 1
    },
    {
        "id": 298,
        "category": "general",
        "question": "Qu'est-ce que la RSE (Responsabilité Sociale de l'Entreprise)?",
        "options": [
            "Un audit financier",
            "Engagement d'une organisation envers développement durable, éthique et impact positif social/environnemental",
            "Un système de qualité",
            "Une certfication de conformité"
        ],
        "correct": 1,
        "explanation": "La RSE engage organisations publiques/privées à considérer impacts sociaux, environnementaux et économiques long-terme, pas seulement profits court-terme.",
        "difficulty": 1
    },
    {
        "id": 299,
        "category": "rh",
        "question": "Qu'est-ce qu'un plan de développement personnel (PDP)?",
        "options": [
            "Un plan de carrière imposé",
            "Un plan individualisé identifiant aspirations, besoins formations et étapes pour développer carrière d'un agent",
            "Un programme d'économies",
            "Un contrat de travail"
        ],
        "correct": 1,
        "explanation": "Le PDP est un outil de gestion RH où agent et manager co-construisent évolution professionnelle: formations, mobilités, objectifs de développement.",
        "difficulty": 1
    },
    {
        "id": 300,
        "category": "general",
        "question": "Qu'est-ce que la transformation digitale en secteur public?",
        "options": [
            "L'achat d'ordinateurs",
            "Changement profond : intégration numérique, données, processus pour moderniser services et efficacité administrative",
            "Un remplacement des papiers par des mails",
            "Une simple informatisation"
        ],
        "correct": 1,
        "explanation": "La transformation digitale publique intègre stratégiquement données, outils numériques, intelligence artificielle, dématérialisation pour améliorer service public et efficience.",
        "difficulty": 2
    }
]

# Additional flashcards for these advanced topics
more_fc = [
    {
        "id": 139,
        "category": "juridique",
        "front": "Quel est le délai de prescription pour contester une décision administrative?",
        "back": "2 mois à compter de sa notification",
        "difficulty": 2
    },
    {
        "id": 140,
        "category": "juridique",
        "front": "Qu'est-ce que le sursis à exécution?",
        "back": "Suspension provisoire d'un acte administratif pendant le jugement du recours",
        "difficulty": 2
    },
    {
        "id": 141,
        "category": "juridique",
        "front": "Qu'est-ce que l'exception de légalité?",
        "back": "Possibilité d'invoquer illégalité d'un acte antérieur sans faire recours direct",
        "difficulty": 3
    },
    {
        "id": 142,
        "category": "rh",
        "front": "Qu'est-ce que la mobilité professionnelle en FP?",
        "back": "Droit d'un agent à changer de poste, ministère ou collectivité au cours de sa carrière",
        "difficulty": 1
    },
    {
        "id": 143,
        "category": "rh",
        "front": "Qu'est-ce que la GPEC?",
        "back": "Gestion Prévisionnelle des Emplois et Compétences: anticiper évolutions pour adapter RH et formations",
        "difficulty": 2
    },
    {
        "id": 144,
        "category": "communication",
        "front": "Qu'est-ce que l'écoute active?",
        "back": "Technique de communication privilégiant compréhension, empathie et feedback",
        "difficulty": 1
    },
    {
        "id": 145,
        "category": "rh",
        "front": "Qu'est-ce que l'empowerment?",
        "back": "Délégation de pouvoir et autonomie aux agents pour prendre décisions responsables",
        "difficulty": 1
    },
    {
        "id": 146,
        "category": "general",
        "front": "Qu'est-ce que la transformation digitale en secteur public?",
        "back": "Intégration numérique, données et IA pour moderniser services administratifs",
        "difficulty": 2
    }
]

# Append
qcm_list.extend(advanced_qcm)
fc_list.extend(more_fc)

# Save
with open('data/questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Validate
with open('data/questions.json', 'r', encoding='utf-8') as f:
    validated = json.load(f)

print(f"[SUCCESS] Added {len(advanced_qcm)} advanced QCM (IDs {advanced_qcm[0]['id']}-{advanced_qcm[-1]['id']})")
print(f"[SUCCESS] Added {len(more_fc)} flashcards (IDs {more_fc[0]['id']}-{more_fc[-1]['id']})")
print(f"\n=== FINAL STATISTICS ===")
print(f"Total QCM: {len(validated['qcm'])}")
print(f"Total Flashcards: {len(validated['flashcards'])}")
print(f"GRAND TOTAL: {len(validated['qcm']) + len(validated['flashcards'])} questions")
print(f"\nCategories distribution:")
categories = {}
for q in validated['qcm']:
    cat = q.get('category', 'unknown')
    categories[cat] = categories.get(cat, 0) + 1
for cat in sorted(categories.keys()):
    print(f"  {cat}: {categories[cat]} questions")
