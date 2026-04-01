"""
mIRAcle v3 - Style Football Manager Card System
Interface carte joueur adaptée aux fiches de poste
"""

from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for, session, abort
from pathlib import Path
from collections import defaultdict
from functools import wraps
from datetime import datetime
import time
import sqlite3
import json
import os
import math
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
MIRACLE_ENV = os.getenv("MIRACLE_ENV", "development").lower()
IS_PRODUCTION = MIRACLE_ENV in ("prod", "production")
app.secret_key = os.getenv("MIRACLE_SECRET_KEY", "dev-secret-change-me")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("MIRACLE_SESSION_SECURE", "false").lower() == "true",
)
if IS_PRODUCTION:
    if not app.secret_key or app.secret_key == "dev-secret-change-me":
        raise RuntimeError("MIRACLE_SECRET_KEY must be set in production.")
    if not app.config.get("SESSION_COOKIE_SECURE"):
        raise RuntimeError("MIRACLE_SESSION_SECURE must be true in production.")
    app.config.setdefault("PREFERRED_URL_SCHEME", "https")
FICHES_FOLDER = Path(__file__).parent / "Fiches de postes"
RESOURCES_FOLDER = Path(__file__).parent / "Ressources"
FICHES_LIST = None
FICHES_TITLES_FILE = Path(__file__).parent / "data" / "fiches_titles.json"
FICHES_TITLES = None
DB_PATH = Path(__file__).parent / "data" / "miracle.db"
BETA_WHITELIST_FILE = Path(__file__).parent / "data" / "beta_whitelist.txt"
LOGIN_ATTEMPTS = {}
MAX_LOGIN_ATTEMPTS = int(os.getenv("MIRACLE_LOGIN_MAX_ATTEMPTS", "5"))
LOGIN_WINDOW_SECONDS = int(os.getenv("MIRACLE_LOGIN_WINDOW_SECONDS", "900"))
REGISTER_ATTEMPTS = {}
MAX_REGISTER_ATTEMPTS = int(os.getenv("MIRACLE_REGISTER_MAX_ATTEMPTS", "5"))
REGISTER_WINDOW_SECONDS = int(os.getenv("MIRACLE_REGISTER_WINDOW_SECONDS", "900"))
EMAIL_IP_FAILS = {}
MAX_LOGIN_IPS = int(os.getenv("MIRACLE_LOGIN_MAX_IPS", "3"))
BAN_WINDOW_SECONDS = int(os.getenv("MIRACLE_LOGIN_BAN_WINDOW_SECONDS", "1800"))

# Catégories de domaines normalisées
DOMAINES_MAP = {
    'RESSOURCES HUMAINES': 'RH',
    'BUDGET': 'Budget',
    'JURIDIQUE': 'Juridique',
    'ACHAT PUBLIC': 'Achats',
    'ACHAT': 'Achats',
    'AUTRES': 'Autre',
    'AUTRE': 'Autre',
    'POLITIQUES PUBLIQUES': 'Politiques',
    'POLITIQUE PUBLIQUE': 'Politiques',
    'COMMUNICATION': 'Communication',
    'AUDIT - MAITRISE DES RISQUES': 'Audit/Risques',
    'SÉCURITÉ': 'Sécurité',
}

# Régions administratives
REGIONS = ['HAUTS-DE-FRANCE', 'ÎLE-DE-FRANCE', 'ILE-DE-FRANCE', 'NORMANDIE', 
           'LA REUNION', 'MARTINIQUE', 'GUADELOUPE', 'GUYANE', 'MAYOTTE',
           'AUVERGNE-RHÔNE-ALPES', 'BOURGOGNE-FRANCHE-COMTÉ', 'BRETAGNE',
           'CENTRE-VAL DE LOIRE', 'CORSE', 'GRAND EST', 'NOUVELLE-AQUITAINE',
           'OCCITANIE', 'PAYS DE LA LOIRE', "PROVENCE-ALPES-CÔTE D'AZUR"]

# Départements français (pour filtrer les lieux des domaines)
DEPARTEMENTS = [
    'AIN', 'AISNE', 'ALLIER', 'ALPES-DE-HAUTE-PROVENCE', 'HAUTES-ALPES',
    'ALPES-MARITIMES', 'ARDÈCHE', 'ARDECHE', 'ARDENNES', 'ARIÈGE', 'ARIEGE', 
    'AUBE', 'AUDE', 'AVEYRON', 'BOUCHES-DU-RHÔNE', 'BOUCHES-DU-RHONE',
    'CALVADOS', 'CANTAL', 'CHARENTE', 'CHARENTE-MARITIME', 'CHER',
    'CORRÈZE', 'CORREZE', 'CORSE-DU-SUD', 'HAUTE-CORSE', "CÔTE-D'OR", "COTE-D'OR",
    "CÔTES-D'ARMOR", "COTES-D'ARMOR", 'CREUSE', 'DORDOGNE', 'DOUBS', 'DRÔME', 'DROME',
    'EURE', 'EURE-ET-LOIR', 'FINISTÈRE', 'FINISTERE', 'GARD', 'HAUTE-GARONNE',
    'GERS', 'GIRONDE', 'HÉRAULT', 'HERAULT', 'ILLE-ET-VILAINE', 'INDRE',
    'INDRE-ET-LOIRE', 'ISÈRE', 'ISERE', 'JURA', 'LANDES', 'LOIR-ET-CHER',
    'LOIRE', 'HAUTE-LOIRE', 'LOIRE-ATLANTIQUE', 'LOIRET', 'LOT', 'LOT-ET-GARONNE',
    'LOZÈRE', 'LOZERE', 'MAINE-ET-LOIRE', 'MANCHE', 'MARNE', 'HAUTE-MARNE',
    'MAYENNE', 'MEURTHE-ET-MOSELLE', 'MEUSE', 'MORBIHAN', 'MOSELLE',
    'NIÈVRE', 'NIEVRE', 'NORD', 'OISE', 'ORNE', 'PAS-DE-CALAIS',
    'PUY-DE-DÔME', 'PUY-DE-DOME', 'PYRÉNÉES-ATLANTIQUES', 'PYRENEES-ATLANTIQUES',
    'HAUTES-PYRÉNÉES', 'HAUTES-PYRENEES', 'PYRÉNÉES-ORIENTALES', 'PYRENEES-ORIENTALES',
    'BAS-RHIN', 'HAUT-RHIN', 'RHÔNE', 'RHONE', 'HAUTE-SAÔNE', 'HAUTE-SAONE',
    'SAÔNE-ET-LOIRE', 'SAONE-ET-LOIRE', 'SARTHE', 'SAVOIE', 'HAUTE-SAVOIE',
    'PARIS', 'SEINE-MARITIME', 'SEINE-ET-MARNE', 'YVELINES', 'DEUX-SÈVRES', 'DEUX-SEVRES',
    'SOMME', 'TARN', 'TARN-ET-GARONNE', 'VAR', 'VAUCLUSE', 'VENDÉE', 'VENDEE',
    'VIENNE', 'HAUTE-VIENNE', 'VOSGES', 'YONNE', 'TERRITOIRE DE BELFORT',
    'ESSONNE', 'HAUTS-DE-SEINE', 'SEINE-SAINT-DENIS', 'VAL-DE-MARNE', "VAL-D'OISE", "VAL-D-OISE"
]

# Set pour recherche rapide (sans accents et en majuscules)
LIEUX_SET = set([r.upper() for r in REGIONS] + [d.upper() for d in DEPARTEMENTS])

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'viewer',
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sources (
                id TEXT PRIMARY KEY,
                domain TEXT,
                source_title TEXT,
                source_type TEXT,
                source_org TEXT,
                source_date TEXT,
                source_url TEXT,
                tags TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                json_id INTEGER,
                category TEXT,
                question TEXT,
                options TEXT,
                correct INTEGER,
                explanation TEXT,
                difficulty INTEGER,
                source_id TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                json_id INTEGER,
                category TEXT,
                front TEXT,
                back TEXT,
                difficulty INTEGER,
                source_id TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                email TEXT,
                page_url TEXT,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

def seed_db_from_json():
    if not QUIZ_DATA_FILE.exists():
        return
    payload = json.loads(QUIZ_DATA_FILE.read_text(encoding="utf-8"))
    with get_db() as conn:
        # ── Sources: upsert (insert or update) ──
        for s in payload.get("sources", []):
            exists = conn.execute("SELECT 1 FROM sources WHERE id = ?", (s.get("id"),)).fetchone()
            row = (
                s.get("domain"),
                s.get("source_title"),
                s.get("source_type"),
                s.get("source_org"),
                s.get("source_date"),
                s.get("source_url"),
                json.dumps(s.get("tags", []), ensure_ascii=False),
            )
            if exists:
                conn.execute(
                    """
                    UPDATE sources SET domain=?, source_title=?, source_type=?, source_org=?, source_date=?, source_url=?, tags=?
                    WHERE id=?
                    """,
                    row + (s.get("id"),)
                )
            else:
                conn.execute(
                    """
                    INSERT INTO sources (id, domain, source_title, source_type, source_org, source_date, source_url, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (s.get("id"),) + row,
                )

        # ── Questions: sync based on json_id ──
        existing_json_ids = {r[0] for r in conn.execute("SELECT json_id FROM questions WHERE json_id IS NOT NULL").fetchall()}
        for q in payload.get("qcm", []):
            qid = q.get("id")
            row = (
                qid,
                q.get("category"),
                q.get("question"),
                json.dumps(q.get("options", []), ensure_ascii=False),
                q.get("correct"),
                q.get("explanation"),
                q.get("difficulty"),
                q.get("source_id"),
            )
            if qid in existing_json_ids:
                conn.execute(
                    """
                    UPDATE questions SET category=?, question=?, options=?, correct=?, explanation=?, difficulty=?, source_id=?
                    WHERE json_id=?
                    """,
                    row[1:] + (qid,)
                )
            else:
                conn.execute(
                    """
                    INSERT INTO questions (json_id, category, question, options, correct, explanation, difficulty, source_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    row,
                )

        # ── Flashcards: sync based on json_id ──
        existing_fc_ids = {r[0] for r in conn.execute("SELECT json_id FROM flashcards WHERE json_id IS NOT NULL").fetchall()}
        for fc in payload.get("flashcards", []):
            fid = fc.get("id")
            row = (
                fid,
                fc.get("category"),
                fc.get("front"),
                fc.get("back"),
                fc.get("difficulty"),
                fc.get("source_id"),
            )
            if fid in existing_fc_ids:
                conn.execute(
                    """
                    UPDATE flashcards SET category=?, front=?, back=?, difficulty=?, source_id=?
                    WHERE json_id=?
                    """,
                    row[1:] + (fid,)
                )
            else:
                conn.execute(
                    """
                    INSERT INTO flashcards (json_id, category, front, back, difficulty, source_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    row,
                )

def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    with get_db() as conn:
        row = conn.execute("SELECT id, email, role FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None

def get_beta_whitelist():
    env_value = os.getenv("MIRACLE_BETA_WHITELIST", "").strip()
    emails = set()
    if env_value:
        emails.update([e.strip().lower() for e in env_value.split(",") if e.strip()])
    if BETA_WHITELIST_FILE.exists():
        file_emails = [
            line.strip().lower()
            for line in BETA_WHITELIST_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        emails.update(file_emails)
    return emails

def is_email_allowed(email):
    whitelist = get_beta_whitelist()
    if not whitelist:
        return True
    return email.lower() in whitelist

def _login_key(email, ip_addr):
    return f"{email.lower()}|{ip_addr or 'unknown'}"

def _register_key(email, ip_addr):
    return f"{email.lower()}|{ip_addr or 'unknown'}"

def is_login_rate_limited(email, ip_addr):
    key = _login_key(email, ip_addr)
    now = time.time()
    window_start = now - LOGIN_WINDOW_SECONDS
    attempts = [ts for ts in LOGIN_ATTEMPTS.get(key, []) if ts >= window_start]
    LOGIN_ATTEMPTS[key] = attempts
    return len(attempts) >= MAX_LOGIN_ATTEMPTS

def record_login_attempt(email, ip_addr):
    key = _login_key(email, ip_addr)
    now = time.time()
    attempts = LOGIN_ATTEMPTS.get(key, [])
    attempts.append(now)
    LOGIN_ATTEMPTS[key] = attempts
    record_email_failure(email, ip_addr)

def clear_login_attempts(email, ip_addr):
    key = _login_key(email, ip_addr)
    LOGIN_ATTEMPTS.pop(key, None)

def is_register_rate_limited(email, ip_addr):
    key = _register_key(email, ip_addr)
    now = time.time()
    window_start = now - REGISTER_WINDOW_SECONDS
    attempts = [ts for ts in REGISTER_ATTEMPTS.get(key, []) if ts >= window_start]
    REGISTER_ATTEMPTS[key] = attempts
    return len(attempts) >= MAX_REGISTER_ATTEMPTS

def record_register_attempt(email, ip_addr):
    key = _register_key(email, ip_addr)
    now = time.time()
    attempts = REGISTER_ATTEMPTS.get(key, [])
    attempts.append(now)
    REGISTER_ATTEMPTS[key] = attempts

def clear_register_attempts(email, ip_addr):
    key = _register_key(email, ip_addr)
    REGISTER_ATTEMPTS.pop(key, None)

def record_email_failure(email, ip_addr):
    if not email:
        return
    norm_email = email.lower()
    now = time.time()
    failures = EMAIL_IP_FAILS.get(norm_email, [])
    failures.append((now, ip_addr or "unknown"))
    EMAIL_IP_FAILS[norm_email] = failures

def clear_email_failures(email):
    if not email:
        return
    EMAIL_IP_FAILS.pop(email.lower(), None)

def is_email_banned(email):
    if not email:
        return False
    norm_email = email.lower()
    now = time.time()
    window_start = now - BAN_WINDOW_SECONDS
    failures = [item for item in EMAIL_IP_FAILS.get(norm_email, []) if item[0] >= window_start]
    EMAIL_IP_FAILS[norm_email] = failures
    ip_set = {ip for _, ip in failures}
    return len(ip_set) >= MAX_LOGIN_IPS and len(failures) >= MAX_LOGIN_ATTEMPTS

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user():
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper

def api_login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user():
            return jsonify({"error": "auth_required"}), 401
        return fn(*args, **kwargs)
    return wrapper

def role_required(roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = current_user()
            if not user or user.get("role") not in roles:
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def clean_text(text):
    """Nettoie un texte: underscores → espaces, puis restaure les apostrophes"""
    text = text.replace('_', ' ').replace("'", "'")
    # Restaurer les apostrophes: " l " → "l'", " d " → "d'", " n " → "n'", " s " → "s'"
    text = re.sub(r"\b([ldnsLDNS]) ", r"\1'", text)
    return ' '.join(text.split())

def load_fiches_titles():
    global FICHES_TITLES
    if FICHES_TITLES is not None:
        return FICHES_TITLES
    if not FICHES_TITLES_FILE.exists():
        FICHES_TITLES = {}
        return FICHES_TITLES
    try:
        FICHES_TITLES = json.loads(FICHES_TITLES_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        FICHES_TITLES = {}
    return FICHES_TITLES

def is_lieu(text):
    """Vérifie si le texte est un lieu (région ou département)"""
    # Nettoyer le texte
    clean = text.upper().replace('_', '-').replace("'", "'")
    # Enlever les numéros entre parenthèses ex: "NORD (59)"
    clean = re.sub(r'\s*\(\d+\)\s*', '', clean).strip()
    return clean in LIEUX_SET

def normalize_domaine(raw):
    """Normalise un domaine"""
    raw_upper = raw.upper()
    # D'abord vérifier si c'est un lieu
    if is_lieu(raw):
        return None  # Sera filtré
    # Ensuite chercher dans la map
    for key, val in DOMAINES_MAP.items():
        if key in raw_upper:
            return val
    # Si trop long ou inconnu
    if len(raw) > 25:
        return 'Autre'
    return raw.title() if raw else 'Autre'

def extract_region(parts):
    """Extrait la région ou département si présent"""
    for p in parts:
        if is_lieu(p):
            return p.replace('_', '-').replace("'", "'").title()
    return None

def load_all_fiches():
    global FICHES_LIST
    if FICHES_LIST is not None:
        return FICHES_LIST
    
    fiches = []
    titles_map = load_fiches_titles()
    seen = set()
    fid = 0
    
    for pdf in sorted(FICHES_FOLDER.rglob("*.pdf")):
        try:
            rel = pdf.relative_to(FICHES_FOLDER)
            parts = list(rel.parts)
            if len(parts) < 2:
                continue
            
            key = str(rel)
            if key in seen:
                continue
            seen.add(key)
            
            admin = clean_text(parts[0])
            structure = clean_text(parts[1])
            region = extract_region(parts)
            
            # Domaine = dernier dossier avant le fichier (si pas un lieu)
            raw_domaine = parts[-2] if len(parts) > 2 else "Général"
            domaine = normalize_domaine(raw_domaine)
            # Si c'est un lieu, chercher un vrai domaine dans le path
            if domaine is None:
                for p in reversed(parts[:-1]):
                    d = normalize_domaine(p)
                    if d is not None:
                        domaine = d
                        break
                if domaine is None:
                    domaine = 'Autre'
            
            # Nettoyer le titre
            rel_path = str(rel).replace('\\', '/')
            raw_title = titles_map.get(rel_path, pdf.stem)
            titre = clean_text(raw_title).replace('.e', '(e)')
            
            fiches.append({
                'id': fid,
                'titre': titre,
                'administration': admin,
                'structure': structure,
                'region': region,
                'domaine': domaine,
                'path': rel_path
            })
            fid += 1
        except:
            pass
    
    FICHES_LIST = fiches
    print(f"[OK] {len(fiches)} fiches chargées")
    return fiches

def build_index_context():
    fiches = load_all_fiches()
    stats = {
        'total': len(fiches),
        'centrale': len([f for f in fiches if 'CENTRALE' in f['administration']]),
        'deconcentree': len([f for f in fiches if 'DÉCONCENTRÉE' in f['administration']]),
        'scolaire': len([f for f in fiches if 'SCOLAIRE' in f['administration']])
    }
    structures = sorted(set(f['structure'] for f in fiches if f['structure'].upper() not in [r.upper() for r in REGIONS]))
    domaines = sorted(set(f['domaine'] for f in fiches if f['domaine']))
    regions = sorted(set(f['region'] for f in fiches if f['region']))
    return {
        'stats': stats,
        'structures': structures,
        'domaines': domaines,
        'regions': regions,
    }

@app.route('/')
@login_required
def index():
    ctx = build_index_context()
    return render_template('app.html', default_view='fiches', **ctx)

@app.route('/api/fiches')
@api_login_required
def get_fiches():
    fiches = load_all_fiches()
    search = request.args.get('search', '').lower()
    admin = request.args.get('administration', '')
    struct = request.args.get('structure', '')
    dom = request.args.get('domaine', '')
    
    return jsonify([f for f in fiches if
        (not search or search in f['titre'].lower() or search in f['structure'].lower() or search in f['domaine'].lower()) and
        (not admin or admin in f['administration']) and
        (not struct or struct == f['structure']) and
        (not dom or dom == f['domaine'])
    ])

@app.route('/api/fiche/<int:fid>')
@api_login_required
def get_fiche(fid):
    for f in load_all_fiches():
        if f['id'] == fid:
            return jsonify(f)
    return jsonify({'error': 'Non trouvée'}), 404

@app.route('/pdf/<path:filepath>')
@login_required
def serve_pdf(filepath):
    full = FICHES_FOLDER / filepath
    return send_file(full, mimetype='application/pdf') if full.exists() else ("Not found", 404)

@app.route('/resource/<path:filepath>')
@login_required
def serve_resource(filepath):
    full = RESOURCES_FOLDER / filepath
    return send_file(full) if full.exists() else ("Not found", 404)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()
        ip_addr = request.headers.get("X-Forwarded-For", request.remote_addr)
        if is_register_rate_limited(email or "unknown", ip_addr):
            return render_template('auth.html', mode='register', error='Trop de tentatives. Réessayez plus tard.')
        if not email or not password:
            record_register_attempt(email or "unknown", ip_addr)
            return render_template('auth.html', mode='register', error='Email et mot de passe requis.')
        if not is_email_allowed(email):
            record_register_attempt(email, ip_addr)
            return render_template('auth.html', mode='register', error="Email non autorisé pour la bêta privée.")
        with get_db() as conn:
            existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
            if existing:
                record_register_attempt(email, ip_addr)
                return render_template('auth.html', mode='register', error='Compte déjà existant.')
            first_user = conn.execute("SELECT COUNT(1) FROM users").fetchone()[0] == 0
            role = 'admin' if first_user else 'viewer'
            conn.execute(
                "INSERT INTO users (email, password_hash, role, created_at) VALUES (?, ?, ?, ?)",
                (email, generate_password_hash(password), role, datetime.utcnow().isoformat())
            )
        clear_register_attempts(email, ip_addr)
        return redirect(url_for('login'))
    return render_template('auth.html', mode='register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()
        ip_addr = request.headers.get("X-Forwarded-For", request.remote_addr)
        if is_email_banned(email):
            return render_template('auth.html', mode='login', error='Trop de tentatives. Réessayez plus tard.')
        if is_login_rate_limited(email, ip_addr):
            return render_template('auth.html', mode='login', error='Trop de tentatives. Réessayez plus tard.')
        if not is_email_allowed(email):
            record_login_attempt(email, ip_addr)
            return render_template('auth.html', mode='login', error='Identifiants invalides.')
        with get_db() as conn:
            row = conn.execute("SELECT id, password_hash, role FROM users WHERE email = ?", (email,)).fetchone()
        if not row or not check_password_hash(row['password_hash'], password):
            record_login_attempt(email, ip_addr)
            return render_template('auth.html', mode='login', error='Identifiants invalides.')
        clear_login_attempts(email, ip_addr)
        clear_email_failures(email)
        session['user_id'] = row['id']
        session['role'] = row['role']
        return redirect(url_for('admin'))
    return render_template('auth.html', mode='login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    user = current_user()
    page_url = request.args.get('from', '').strip()
    if request.method == 'POST':
        message = request.form.get('message', '').strip()
        page_url = request.form.get('page_url', '').strip()
        if not message:
            return render_template('feedback.html', error='Message requis.', page_url=page_url)
        with get_db() as conn:
            conn.execute(
                """
                INSERT INTO feedback (user_id, email, page_url, message, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    user.get('id') if user else None,
                    user.get('email') if user else None,
                    page_url or None,
                    message,
                    datetime.utcnow().isoformat(),
                )
            )
        return render_template('feedback.html', success=True, page_url=page_url)
    return render_template('feedback.html', page_url=page_url)

def load_categories():
    if QUIZ_DATA_FILE.exists():
        payload = json.loads(QUIZ_DATA_FILE.read_text(encoding='utf-8'))
        return payload.get('categories', [])
    with get_db() as conn:
        rows = conn.execute("SELECT DISTINCT category FROM questions").fetchall()
    return [{'id': r['category'], 'name': r['category']} for r in rows]

def parse_page(value, default=1):
    try:
        page = int(value)
    except (TypeError, ValueError):
        return default
    return max(page, 1)

def parse_per_page(value, default=100, max_value=500):
    if value in (None, ''):
        return default
    if str(value).lower() in ('all', '0'):
        return None
    try:
        per_page = int(value)
    except (TypeError, ValueError):
        return default
    return max(1, min(per_page, max_value))

@app.route('/admin')
@login_required
def admin():
    qcm_query = request.args.get('qcm_query', '').strip()
    qcm_page = parse_page(request.args.get('qcm_page'), 1)
    qcm_per_page = parse_per_page(request.args.get('qcm_per_page'), 100, 500)

    fc_query = request.args.get('fc_query', '').strip()
    fc_page = parse_page(request.args.get('fc_page'), 1)
    fc_per_page = parse_per_page(request.args.get('fc_per_page'), 100, 500)

    ministeres = load_ministeres()

    with get_db() as conn:
        sources = conn.execute("SELECT * FROM sources ORDER BY id").fetchall()
        qcm_where = ""
        qcm_params = []
        if qcm_query:
            qcm_where = "WHERE question LIKE ? OR category LIKE ? OR source_id LIKE ?"
            like = f"%{qcm_query}%"
            qcm_params = [like, like, like]

        qcm_total = conn.execute(
            f"SELECT COUNT(1) FROM questions {qcm_where}",
            qcm_params,
        ).fetchone()[0]

        qcm_pages = 1
        qcm_offset = 0
        qcm_limit_sql = ""
        qcm_page_params = []
        if qcm_per_page:
            qcm_pages = max(1, math.ceil(qcm_total / qcm_per_page))
            qcm_page = min(qcm_page, qcm_pages)
            qcm_offset = (qcm_page - 1) * qcm_per_page
            qcm_limit_sql = "LIMIT ? OFFSET ?"
            qcm_page_params = [qcm_per_page, qcm_offset]

        questions = conn.execute(
            f"SELECT * FROM questions {qcm_where} ORDER BY id DESC {qcm_limit_sql}",
            qcm_params + qcm_page_params,
        ).fetchall()

        fc_where = ""
        fc_params = []
        if fc_query:
            fc_where = "WHERE front LIKE ? OR back LIKE ? OR category LIKE ? OR source_id LIKE ?"
            like = f"%{fc_query}%"
            fc_params = [like, like, like, like]

        fc_total = conn.execute(
            f"SELECT COUNT(1) FROM flashcards {fc_where}",
            fc_params,
        ).fetchone()[0]

        fc_pages = 1
        fc_offset = 0
        fc_limit_sql = ""
        fc_page_params = []
        if fc_per_page:
            fc_pages = max(1, math.ceil(fc_total / fc_per_page))
            fc_page = min(fc_page, fc_pages)
            fc_offset = (fc_page - 1) * fc_per_page
            fc_limit_sql = "LIMIT ? OFFSET ?"
            fc_page_params = [fc_per_page, fc_offset]

        flashcards = conn.execute(
            f"SELECT * FROM flashcards {fc_where} ORDER BY id DESC {fc_limit_sql}",
            fc_params + fc_page_params,
        ).fetchall()
        users = conn.execute("SELECT id, email, role, created_at FROM users ORDER BY id DESC").fetchall()
    return render_template(
        'admin.html',
        categories=load_categories(),
        sources=[dict(s) for s in sources],
        questions=[dict(q) for q in questions],
        flashcards=[dict(fc) for fc in flashcards],
        users=[dict(u) for u in users],
        ministeres=ministeres,
        qcm_query=qcm_query,
        qcm_page=qcm_page,
        qcm_pages=qcm_pages,
        qcm_per_page=qcm_per_page or 'all',
        qcm_total=qcm_total,
        fc_query=fc_query,
        fc_page=fc_page,
        fc_pages=fc_pages,
        fc_per_page=fc_per_page or 'all',
        fc_total=fc_total,
        current_user=current_user()
    )

@app.route('/admin/questions', methods=['POST'])
@role_required(['admin', 'editor'])
def admin_questions():
    action = request.form.get('action')
    q_id = request.form.get('id')
    options_text = request.form.get('options', '')
    options = [o.strip() for o in options_text.splitlines() if o.strip()]
    payload = (
        request.form.get('category'),
        request.form.get('question'),
        json.dumps(options, ensure_ascii=False),
        int(request.form.get('correct', 0)),
        request.form.get('explanation'),
        int(request.form.get('difficulty', 1)),
        request.form.get('source_id') or None,
    )
    with get_db() as conn:
        if action == 'create':
            conn.execute(
                """
                INSERT INTO questions (category, question, options, correct, explanation, difficulty, source_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                payload
            )
        elif action == 'update' and q_id:
            conn.execute(
                """
                UPDATE questions
                SET category = ?, question = ?, options = ?, correct = ?, explanation = ?, difficulty = ?, source_id = ?
                WHERE id = ?
                """,
                payload + (q_id,)
            )
        elif action == 'delete' and q_id:
            conn.execute("DELETE FROM questions WHERE id = ?", (q_id,))
    return redirect(url_for('admin'))

@app.route('/admin/flashcards', methods=['POST'])
@role_required(['admin', 'editor'])
def admin_flashcards():
    action = request.form.get('action')
    fc_id = request.form.get('id')
    payload = (
        request.form.get('category'),
        request.form.get('front'),
        request.form.get('back'),
        int(request.form.get('difficulty', 1)),
        request.form.get('source_id') or None,
    )
    with get_db() as conn:
        if action == 'create':
            conn.execute(
                """
                INSERT INTO flashcards (category, front, back, difficulty, source_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                payload
            )
        elif action == 'update' and fc_id:
            conn.execute(
                """
                UPDATE flashcards
                SET category = ?, front = ?, back = ?, difficulty = ?, source_id = ?
                WHERE id = ?
                """,
                payload + (fc_id,)
            )
        elif action == 'delete' and fc_id:
            conn.execute("DELETE FROM flashcards WHERE id = ?", (fc_id,))
    return redirect(url_for('admin'))

@app.route('/admin/sources', methods=['POST'])
@role_required(['admin', 'editor'])
def admin_sources():
    action = request.form.get('action')
    source_id = request.form.get('id')
    tags_text = request.form.get('tags', '')
    tags = [t.strip() for t in tags_text.split(',') if t.strip()]
    payload = (
        request.form.get('domain'),
        request.form.get('source_title'),
        request.form.get('source_type'),
        request.form.get('source_org'),
        request.form.get('source_date'),
        request.form.get('source_url'),
        json.dumps(tags, ensure_ascii=False),
    )
    with get_db() as conn:
        if action == 'create' and source_id:
            conn.execute(
                """
                INSERT INTO sources (id, domain, source_title, source_type, source_org, source_date, source_url, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (source_id,) + payload
            )
        elif action == 'update' and source_id:
            conn.execute(
                """
                UPDATE sources
                SET domain = ?, source_title = ?, source_type = ?, source_org = ?, source_date = ?, source_url = ?, tags = ?
                WHERE id = ?
                """,
                payload + (source_id,)
            )
        elif action == 'delete' and source_id:
            conn.execute("DELETE FROM sources WHERE id = ?", (source_id,))
    return redirect(url_for('admin'))

@app.route('/admin/users', methods=['POST'])
@role_required(['admin'])
def admin_users():
    user_id = request.form.get('id')
    role = request.form.get('role')
    if user_id and role in ['admin', 'editor', 'viewer']:
        with get_db() as conn:
            conn.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
    return redirect(url_for('admin'))

@app.route('/admin/ministeres', methods=['POST'])
@role_required(['admin', 'editor'])
def admin_ministeres():
    action = request.form.get('action')
    ministere_id = request.form.get('id')
    if action != 'update' or not ministere_id:
        return redirect(url_for('admin'))

    ministeres = load_ministeres()
    target = None
    for ministere in ministeres:
        if ministere.get('id') == ministere_id:
            target = ministere
            break
    if target is None:
        abort(404)

    try:
        details_json = json.loads(request.form.get('details_json') or '{}')
        grandes_lois_json = json.loads(request.form.get('grandes_lois_json') or '[]')
        sources_json = json.loads(request.form.get('sources_json') or '[]')
    except json.JSONDecodeError:
        abort(400, description="JSON invalide pour details/grandes_lois/sources")

    target['name'] = request.form.get('name', '').strip()
    target['short_name'] = request.form.get('short_name', '').strip()
    target['site_url'] = request.form.get('site_url', '').strip()
    target['resume'] = request.form.get('resume', '').strip()
    target['missions'] = parse_lines(request.form.get('missions'))
    target['competences'] = parse_lines(request.form.get('competences'))
    target['politiques_publiques'] = parse_lines(request.form.get('politiques_publiques'))
    target['chiffres_cles'] = parse_lines(request.form.get('chiffres_cles'))
    target['organigramme'] = parse_lines(request.form.get('organigramme'))
    target['operateurs'] = parse_lines(request.form.get('operateurs'))
    target['budget'] = parse_lines(request.form.get('budget'))
    target['notes'] = request.form.get('notes', '').strip()
    target['details'] = details_json
    target['grandes_lois'] = grandes_lois_json
    target['sources'] = sources_json

    save_ministeres(ministeres)
    return redirect(url_for('admin'))

@app.route('/api/stats')
@api_login_required
def get_stats():
    fiches = load_all_fiches()
    by_struct = defaultdict(int)
    by_dom = defaultdict(int)
    by_admin = defaultdict(int)
    for f in fiches:
        by_struct[f['structure']] += 1
        by_dom[f['domaine']] += 1
        by_admin[f['administration']] += 1
    return jsonify({
        'total': len(fiches),
        'by_administration': dict(by_admin),
        'by_structure': dict(sorted(by_struct.items(), key=lambda x: -x[1])),
        'by_domaine': dict(sorted(by_dom.items(), key=lambda x: -x[1]))
    })

@app.route('/api/random')
@api_login_required
def get_random():
    import random
    return jsonify(random.choice(load_all_fiches()))

# ══════════ QUIZ / FLASHCARDS ══════════
QUIZ_DATA_FILE = Path(__file__).parent / "data" / "questions.json"
MINISTERES_DATA_FILE = Path(__file__).parent / "data" / "ministeres.json"
init_db()
seed_db_from_json()

def load_ministeres():
    if not MINISTERES_DATA_FILE.exists():
        return []
    payload = json.loads(MINISTERES_DATA_FILE.read_text(encoding="utf-8"))
    return payload.get("ministeres", [])

def save_ministeres(ministeres):
    payload = {"ministeres": ministeres}
    MINISTERES_DATA_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

def parse_lines(text):
    return [line.strip() for line in (text or "").splitlines() if line.strip()]

@app.route('/quiz')
@login_required
def quiz_page():
    return render_template('quiz.html')

@app.route('/ministeres')
@login_required
def ministeres_page():
    ministeres = load_ministeres()
    return render_template('ministeres.html', ministeres=ministeres)

@app.route('/training')
@login_required
def training_page():
    ctx = build_index_context()
    return render_template('app.html', default_view='training', **ctx)

@app.route('/stats')
@login_required
def stats_page():
    ctx = build_index_context()
    return render_template('app.html', default_view='stats', **ctx)

@app.route('/api/quiz/data')
@api_login_required
def get_quiz_data():
    categories = load_categories()
    with get_db() as conn:
        sources_rows = conn.execute("SELECT * FROM sources ORDER BY id").fetchall()
        sources = [dict(s) for s in sources_rows]
        sources_by_id = {s['id']: s for s in sources}

        qcm_rows = conn.execute("SELECT * FROM questions ORDER BY id").fetchall()
        qcm = []
        for q in qcm_rows:
            item = dict(q)
            item['id'] = item.pop('json_id') or item['id']
            item['options'] = json.loads(item.get('options') or '[]')
            if item.get('source_id') in sources_by_id:
                item['source_url'] = sources_by_id[item['source_id']].get('source_url')
            qcm.append(item)

        fc_rows = conn.execute("SELECT * FROM flashcards ORDER BY id").fetchall()
        flashcards = []
        for fc in fc_rows:
            item = dict(fc)
            item['id'] = item.pop('json_id') or item['id']
            if item.get('source_id') in sources_by_id:
                item['source_url'] = sources_by_id[item['source_id']].get('source_url')
            flashcards.append(item)

    return jsonify({'categories': categories, 'sources': sources, 'qcm': qcm, 'flashcards': flashcards})

if __name__ == '__main__':
    print("═" * 50)
    print("  mIRAcle v3 - Fiches + Quiz")
    print("═" * 50)
    load_all_fiches()
    print("  → Fiches: http://localhost:5000")
    print("  → Quiz:   http://localhost:5000/quiz")
    app.run(debug=True, host='0.0.0.0', port=5000)
