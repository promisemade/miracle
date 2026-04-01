#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final batch of QCM on practical management topics from guides
- Team dynamics, conflict resolution, change management, decision-making
- Practical scenarios and best practices
Total: 20+ final questions to reach 500+
"""
import json

# Load existing
with open('data/questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

qcm_list = data.get('qcm', [])
fc_list = data.get('flashcards', [])
next_qcm_id = max([q['id'] for q in qcm_list], default=0) + 1

# Final batch: Management scenarios, change, teams, decision-making
final_qcm = [
    {
        "id": 301,
        "category": "rh",
        "question": "Qu'est-ce que la dynamique de groupe?",
        "options": [
            "Une activité sportive collectivité",
            "L'ensemble des interactions, normes et processus d'une équipe influençant son fonctionnement",
            "Une hiérarchie stricte",
            "Un classement de performance"
        ],
        "correct": 1,
        "explanation": "La dynamique de groupe (cohésion, normes informelles, leadership émergent) affecte la productivité. Un manager doit comprendre et favoriser une dynamique positive.",
        "difficulty": 2
    },
    {
        "id": 302,
        "category": "rh",
        "question": "Qu'est-ce qu'un conflit de rôles?",
        "options": [
            "Un désaccord entre collègues",
            "Une situation où les attentes concernant le rôle d'une personne sont contradictoires ou ambiguës",
            "Une problématique hiérarchique",
            "Un malentendu situationnel"
        ],
        "correct": 1,
        "explanation": "Le conflit de rôles survient quand un agent reçoit des demandes incompatibles (ex: être à la fois spécialiste et généraliste) créant stress et confusion.",
        "difficulty": 2
    },
    {
        "id": 303,
        "category": "rh",
        "question": "Qu'est-ce que la gestion du changement organisationnel?",
        "options": [
            "Un congé administratif",
            "Processus planifié conduisant à transformations (structure, technologie) avec accompagnement et implication des agents",
            "Une réduction de personnel",
            "Une simple décision top-down"
        ],
        "correct": 1,
        "explanation": "La gestion du changement implique: analyse, communication transparente, formation, implication équipes pour réduire résistances et assurer succès.",
        "difficulty": 2
    },
    {
        "id": 304,
        "category": "rh",
        "question": "Qu'est-ce que la résistance au changement?",
        "options": [
            "Une opposition systématique",
            "Réaction naturelle aux changements due à peur de l'inconnu, perte de repères ou sentiment de menace",
            "Une manifestation syndicale",
            "Un défaut de compétence"
        ],
        "correct": 1,
        "explanation": "La résistance au changement est compréhensible: perte de certitudes, de pouvoir, crainte de incompétence. Un bon manager l'anticipe et la gère.",
        "difficulty": 2
    },
    {
        "id": 305,
        "category": "rh",
        "question": "Qu'est-ce que la prise de décision participative?",
        "options": [
            "Décisions prises uniquement par la direction",
            "Processus associant équipes à la réflexion et décision pour meilleure acceptation et pertinence",
            "Vote systématique de toutes décisions",
            "Délégation totale au personnel"
        ],
        "correct": 1,
        "explanation": "La décision participative (consultation, délibération) augmente légitimité, engagement et qualité décisionnelle. C'est plus efficace que l'autoritarisme pur.",
        "difficulty": 1
    },
    {
        "id": 306,
        "category": "communication",
        "question": "Qu'est-ce qu'une communication non-violente?",
        "options": [
            "L'absence de cris et disputes",
            "Approche de communication basée sur observation, sentiments, besoins et demandes clairs sans jugement",
            "Une communication courtoise",
            "Un silence respectueux"
        ],
        "correct": 1,
        "explanation": "La Communication NonViolente (CNV) privilégie empathie et authenticité, évitant jugements moralisants pour résoudre conflits constructivement.",
        "difficulty": 2
    },
    {
        "id": 307,
        "category": "rh",
        "question": "Qu'est-ce que l'assertivité en management?",
        "options": [
            "L'agressivité verbale",
            "Capacité à exprimer ses besoins, opinions et limites sans agressivité ni soumission",
            "L'autorité absolue",
            "La passivité acceptante"
        ],
        "correct": 1,
        "explanation": "L'assertivité équilibrée (ni agressif ni passif) permet communication claire, respect mutuel et résolution constructive des conflits.",
        "difficulty": 2
    },
    {
        "id": 308,
        "category": "rh",
        "question": "Qu'est-ce que la motivation intrinsèque?",
        "options": [
            "Seul l'argent motive",
            "Motivation provenant de sources internes (intérêt pour tâche, autonomie, sens du travail)",
            "Motivation basée sur punition/récompense externe",
            "Absence totale de motivation"
        ],
        "correct": 1,
        "explanation": "La motivation intrinsèque (passion, sens, autonomie, compétence) dure plus longtemps que récompenses externes. Un manager doit la cultiver.",
        "difficulty": 1
    },
    {
        "id": 309,
        "category": "communication",
        "question": "Qu'est-ce que le feedback constructif?",
        "options": [
            "Une critique négative",
            "Retour factuel sur performance aidant amélioration sans décourager ou juger la personne",
            "Un compliment sans fondement",
            "Une remarque ironique"
        ],
        "correct": 1,
        "explanation": "Le feedback constructif (spécifique, factuel, orienté amélioration) renforce apprentissage et confiance. C'est un outil de développement clé.",
        "difficulty": 1
    },
    {
        "id": 310,
        "category": "rh",
        "question": "Qu'est-ce que l'effet Pygmalion en organisation?",
        "options": [
            "Un type de maladie professionnelle",
            "Phénomène où attentes d'un manager envers agent influencent réellement sa performance",
            "Un style de leadership",
            "Une théorie psychologique sans application"
        ],
        "correct": 1,
        "explanation": "L'effet Pygmalion: si manager croit en agent, celui-ci tend à progresser. Inverse: basses attentes induisent faible performance. Le manager doit croire en ses agents.",
        "difficulty": 2
    },
    {
        "id": 311,
        "category": "rh",
        "question": "Qu'est-ce que le burn-out professionnel?",
        "options": [
            "Une démission soudaine",
            "État d'épuisement physique/émotionnel/mental dû surcharge travail prolongée sans récupération",
            "Une paresse au travail",
            "Un manque de congés"
        ],
        "correct": 1,
        "explanation": "Le burn-out résulte surcharge chronique, manque contrôle, manque reconnaissance. Manager doit prévenir: charge réaliste, reconnaissance, support.",
        "difficulty": 1
    },
    {
        "id": 312,
        "category": "rh",
        "question": "Qu'est-ce que le mentoring en organisation?",
        "options": [
            "Une formation classique",
            "Relation où mentor expérimenté guide et soutient mentoré dans développement professionnel long-terme",
            "Un coaching ponctuel",
            "Une supervision directe"
        ],
        "correct": 1,
        "explanation": "Le mentoring (relation personnalisée avec expert) favorise développement professionnel, intégration organisationnelle et transmission de culture.",
        "difficulty": 1
    },
    {
        "id": 313,
        "category": "general",
        "question": "Qu'est-ce que l'agilité organisationnelle?",
        "options": [
            "Rapidité des mouvements",
            "Capacité d'une organisation à s'adapter rapidement aux changements d'environnement",
            "Un type de danse",
            "Une compétence informatique"
        ],
        "correct": 1,
        "explanation": "L'agilité organisationnelle (flexibilité, adaptation rapide, apprentissage continu) est critique face turbulences économiques et technologiques.",
        "difficulty": 1
    },
    {
        "id": 314,
        "category": "rh",
        "question": "Qu'est-ce que la justice organisationnelle?",
        "options": [
            "Un tribunal interne",
            "Perception équité dans allocation ressources, processus décisionnels et traitement par organisation",
            "Un système judiciaire administratif",
            "Une égalité de salaires"
        ],
        "correct": 1,
        "explanation": "Justice organisationnelle (distributive, procédurale, interpersonnelle) affecte engagement, confiance et performance. Manager doit assurer équité perçue.",
        "difficulty": 2
    },
    {
        "id": 315,
        "category": "general",
        "question": "Qu'est-ce que l'intelligence collective?",
        "options": [
            "Somme des QI individuels",
            "Capacité d'un groupe à résoudre problèmes et innover grâce diversité et collaboration",
            "Une compétition intellectuelle",
            "Un test de connaissance générale"
        ],
        "correct": 1,
        "explanation": "L'intelligence collective émerge de diversité + communication + confiance + conflit productif. Manager doit créer conditions: inclusion, psychologicalsafety.",
        "difficulty": 2
    },
    {
        "id": 316,
        "category": "rh",
        "question": "Qu'est-ce que le leadership situationnel?",
        "options": [
            "Leadership basé lieu géographique",
            "Style adapté à maturité, compétence et motivation de chaque collaborateur pour situation donnée",
            "Leadership improvisé",
            "Leadership d'urgence"
        ],
        "correct": 1,
        "explanation": "Leadership situationnel adapte directivité/soutien selon agent: directif pour novice, coaching pour apprenti, soutien pour compétent, délégation pour expert.",
        "difficulty": 2
    },
    {
        "id": 317,
        "category": "communication",
        "question": "Qu'est-ce qu'une runion efficace?",
        "options": [
            "Réunion longue avec beaucoup de participants",
            "Réunion avec objectif clair, ordre du jour, durée définie, décisions documentées",
            "Réunion informelle sans agenda",
            "Réunion avec le maximum de documentation"
        ],
        "correct": 1,
        "explanation": "Réunion efficace: invitation ciblée, agenda partagé avant, timeboxing, décisions/actions claires, PV diffusé. Sinon perte temps ressources.",
        "difficulty": 1
    },
    {
        "id": 318,
        "category": "rh",
        "question": "Qu'est-ce que la reconnaissance au travail?",
        "options": [
            "Un bonus monétaire obligatoire",
            "Actes et paroles montrant appréciation contributions agent (compliments, responsabilités, visibilité)",
            "Une promotion rapide",
            "Une augmentation salariale"
        ],
        "correct": 1,
        "explanation": "Reconnaissance (crédits publics, responsabilités enrichissantes, feedback positif) coûte peu mais augmente énormément motivation, engagement et rétention.",
        "difficulty": 1
    },
    {
        "id": 319,
        "category": "general",
        "question": "Qu'est-ce que la sécurité psychologique en équipe?",
        "options": [
            "Absence de conflits",
            "Climat de confiance où agents peuvent prendre risques (parler, innover, se tromper) sans crainte représailles",
            "Protection contre stress externe",
            "Isolation physique"
        ],
        "correct": 1,
        "explanation": "Sécurité psychologique (créée par leader inclusif) permet innovationsent erreurs productives essentielles apprentissage et performance équipe.",
        "difficulty": 2
    },
    {
        "id": 320,
        "category": "rh",
        "question": "Qu'est-ce que la diversité et inclusion en organisation?",
        "options": [
            "Embauche de personnes handicapées obligatoire",
            "Environnement valorisant différences (genre, origine, âge) et donnant égal accès opportunités/voix",
            "Une politique RH cosmétique",
            "Un programme d'égalité des salaires"
        ],
        "correct": 1,
        "explanation": "Diversité + inclusion (respect différences, égalité traitement, voix valorisées) améliorent innovation, performance et image organisationnelle.",
        "difficulty": 1
    }
]

# Final flashcards
final_fc = [
    {
        "id": 147,
        "category": "rh",
        "front": "Qu'est-ce que le conflit de rôles?",
        "back": "Situation où attentes concernant rôle sont contradictoires ou ambiguës",
        "difficulty": 2
    },
    {
        "id": 148,
        "category": "rh",
        "front": "Qu'est-ce que la gestion du changement?",
        "back": "Processus planifié conduisant transformations avec accompagnement et implication des agents",
        "difficulty": 2
    },
    {
        "id": 149,
        "category": "rh",
        "front": "Qu'est-ce que la motivation intrinsèque?",
        "back": "Motivation provenant de sources internes: intérêt pour tâche, autonomie, sens du travail",
        "difficulty": 1
    },
    {
        "id": 150,
        "category": "communication",
        "front": "Qu'est-ce que le feedback constructif?",
        "back": "Retour factuel sur performance aidant amélioration sans juger la personne",
        "difficulty": 1
    },
    {
        "id": 151,
        "category": "rh",
        "front": "Qu'est-ce que le burn-out?",
        "back": "Épuisement physique/émotionnel/mental dû surcharge travail prolongée",
        "difficulty": 1
    },
    {
        "id": 152,
        "category": "general",
        "front": "Qu'est-ce que l'agilité organisationnelle?",
        "back": "Capacité organisation à s'adapter rapidement aux changements d'environnement",
        "difficulty": 1
    },
    {
        "id": 153,
        "category": "general",
        "front": "Qu'est-ce que la sécurité psychologique?",
        "back": "Climat de confiance où agents peuvent prendre risques sans crainte représailles",
        "difficulty": 2
    },
    {
        "id": 154,
        "category": "rh",
        "front": "Qu'est-ce que la diversité et inclusion?",
        "back": "Environnement valorisant différences avec égal accès opportunités et voix",
        "difficulty": 1
    }
]

# Append
qcm_list.extend(final_qcm)
fc_list.extend(final_fc)

# Save
with open('data/questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Final validation
with open('data/questions.json', 'r', encoding='utf-8') as f:
    validated = json.load(f)

total_qcm = len(validated['qcm'])
total_fc = len(validated['flashcards'])
total = total_qcm + total_fc

print(f"[FINAL] Added {len(final_qcm)} QCM + {len(final_fc)} flashcards\n")
print(f"{'='*60}")
print(f"       FINAL DATABASE STATISTICS - PROJECT COMPLETE")
print(f"{'='*60}")
print(f"\nTotal QCM:        {total_qcm:>3} questions")
print(f"Total Flashcards: {total_fc:>3} questions")
print(f"GRAND TOTAL:      {total:>3} questions")
print(f"\nCategory breakdown:")
categories = {}
for q in validated['qcm']:
    cat = q.get('category', 'unknown')
    categories[cat] = categories.get(cat, 0) + 1

for cat in sorted(categories.keys(), key=lambda x: categories[x], reverse=True):
    pct = (categories[cat] / total_qcm) * 100
    print(f"  • {cat:<15} {categories[cat]:>3} QCM ({pct:>5.1f}%)")

print(f"\n{'='*60}")
print(f"Domains covered: 9 (RH, Budget, Finances, Juridique, Politiques,")
print(f"                   Achats, Audit, Communication, General)")
print(f"\nYou now have a comprehensive exam prep database covering:")
print(f"  • Finances publiques (budget, LOLF, PAP/RAP, fiscal)")
print(f"  • Contentieux administratif (procedure, case law)")
print(f"  • GRH (time work, recruitment, management)")
print(f"  • Commande publique (seuils 2026-2027 updated!)")
print(f"  • Leadership & Management")
print(f"  • Ethical & Professional practices")
print(f"{'='*60}\n")
