from flask import Flask, render_template, request, jsonify, url_for, send_from_directory, send_file
import json
import os
from werkzeug.utils import secure_filename
import datetime

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/media'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Extensions autorisées
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm', 'ogg', 'avi', 'mov'}
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_VIDEO_EXTENSIONS


def create_directories():
    directories = [
        'static/media',
        'static/media/projects',
        'static/media/profile',
        'static/media/videos',
        'static/media/thumbnails',
        'static/cv',
        'templates'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


create_directories()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS


def media_exists(filename, folder='projects'):
    """Vérifie si un fichier média existe physiquement"""
    return os.path.exists(f'static/media/{folder}/{filename}')


def get_media_url(filename, folder='projects'):
    """Génère l'URL pour un fichier média.
    Retourne None si le fichier n'existe pas (au lieu d'un placeholder),
    ce qui permet au template de générer une carte SVG stylisée à la place.
    """
    if filename and media_exists(filename, folder):
        return url_for('static', filename=f'media/{folder}/{filename}')
    return None


def save_contact_message(data):
    """Sauvegarde les messages de contact"""
    messages_file = 'contact_messages.json'

    if not os.path.exists(messages_file):
        with open(messages_file, 'w') as f:
            json.dump([], f)

    with open(messages_file, 'r') as f:
        messages = json.load(f)

    data['timestamp'] = datetime.datetime.now().isoformat()
    messages.append(data)

    with open(messages_file, 'w') as f:
        json.dump(messages, f, indent=2)


def get_portfolio_data_fr():
    return {
        'about': {
            'name': 'Mialy Anderson RAKOTONDRADANO',
            'title': 'Développeur Full Stack & Gameplay',
            # Hero plus spécifique : on parle de ce que tu fais réellement
            # plutôt qu'un slogan générique.
            'headline': 'Je développe des <em>jeux</em>,<br>des <em>outils logiciels</em><br>et des <em>applications web</em>.',
            'tagline': 'Gameplay programmer (Unity, Unreal) et développeur full stack (Java/Spring, Flask). Basé à Montréal.',
            'description': 'Spécialisé en programmation gameplay sur Unity et Unreal Engine, et en développement full stack avec Java/Spring Boot, Angular et Python/Flask. Récemment programmeur gameplay sur CUBI 2026 (concours Ubisoft Game Lab).',
            'email': 'andyrakotondradano@gmail.com',
            'phone': '+1 579 372 6108',
            'location': 'Montréal, QC',
            'profile_image': get_media_url('profile.png', 'profile'),
            'cv_available': os.path.exists('static/cv/cv.pdf')
        },
        # Compétences regroupées par niveau de maîtrise plutôt que par
        # pourcentages arbitraires. Plus crédible auprès des recruteurs tech.
        'skill_groups': [
            {
                'level': 'Maîtrise solide',
                'description': 'Technologies utilisées sur des projets complets, en production ou en compétition.',
                'skills': [
                    {'name': 'Unity', 'category': 'Jeux'},
                    {'name': 'C#', 'category': 'Jeux'},
                    {'name': 'Java', 'category': 'Backend'},
                    {'name': 'Python', 'category': 'Backend'},
                    {'name': 'C++', 'category': 'Système'},
                    {'name': 'Git', 'category': 'Outils'},
                    {'name': 'Spring Boot', 'category': 'Backend'},
                    {'name': 'Flask', 'category': 'Backend'},
                ]
            },
            {
                'level': 'Confortable',
                'description': 'Utilisé sur plusieurs projets, à l\'aise pour livrer.',
                'skills': [
                    {'name': 'Unreal Engine', 'category': 'Jeux'},
                    {'name': 'JavaScript', 'category': 'Frontend'},
                    {'name': 'Angular', 'category': 'Frontend'},
                    {'name': 'HTML/CSS', 'category': 'Frontend'},
                    {'name': 'TypeScript', 'category': 'Frontend'},
                    {'name': 'SQL / MySQL', 'category': 'Backend'},
                    {'name': 'C', 'category': 'Système'},
                ]
            },
            {
                'level': 'En apprentissage',
                'description': 'Utilisé pour des projets ciblés, en cours d\'approfondissement.',
                'skills': [
                    {'name': 'React', 'category': 'Frontend'},
                    {'name': 'Django', 'category': 'Backend'},
                    {'name': 'OCaml', 'category': 'Système'},
                    {'name': 'Node.js', 'category': 'Backend'},
                ]
            }
        ],
        'experience': [
            {
                'id': 1,
                'title': 'Programmeur Gameplay — Concours Ubisoft Game Lab 2026 (UQAM)',
                'company': 'Ubisoft Montréal',
                'location': 'Montréal, QC',
                'type': 'Compétition étudiante',
                'period': 'Janvier 2026 — Avril 2026',
                'duration': '4 mois',
                'description': 'Participation au concours Ubisoft Game Lab 2026 avec le développement d\'un beat-em-up nommé A GLITCH IN TIME, intégrant le thème "années 80-90". Encadrement par des moniteurs Ubisoft. Prototype présenté chez Ubisoft Montréal devant un jury de professionnels de l\'industrie.',
                'responsibilities': [
                    'Développement gameplay : système de combat avec combos, dash avec effets visuels, mécaniques de plateforme',
                    'Programmation d\'IA : ennemis avec NavMesh et système d\'object pooling pour optimiser les performances',
                    'Implémentation de l\'accessibilité : remapping des touches via ApplyBindingOverride, vibrations haptiques pour manettes',
                    'Création d\'un système d\'animation hybride : frame-swap mesh animation custom pour le personnage 80s et Mixamo/Humanoid pour le 90s',
                    'Développement d\'effets visuels : trails de dash, slash effects, particules pour les attaques',
                    'Gestion d\'interface : menu pause avec navigation D-pad, système d\'UI accessible'
                ],
                'activities': [
                    'Collaboration en équipe de 8',
                    'Résolution de conflits Git lors de merges complexes',
                    'Debugging de problèmes techniques',
                    'Présentation du prototype chez Ubisoft Montréal',
                    'Itérations rapides basées sur les feedbacks de l\'équipe',
                    'Architecture orientée objet avec hiérarchies de classes abstraites'
                ],
                'technologies': ['Unity 6.1', 'C#', 'Input System', 'NavMesh AI', 'Animation Events', 'Mixamo', 'VFX Graph', 'Cinemachine', 'Object Pooling', 'Git'],
                'achievements': [
                    'Prototype finalisé et présenté chez Ubisoft Montréal',
                    'Implémentation de deux systèmes d\'animation distincts dans un même jeu',
                    'Système d\'accessibilité complet (remapping + haptics)',
                    'Architecture modulaire avec classes abstraites réutilisables',
                    'Collaboration efficace en équipe de 8 sur 4 mois'
                ]
            },
            {
                'id': 2,
                'title': 'Développeur Full Stack Java Spring / Angular',
                'company': 'Shop Imerina',
                'location': 'Antananarivo, Madagascar',
                'type': 'Télétravail',
                'period': 'Septembre 2023 — Présent',
                'duration': 'En cours',
                'description': 'Développement d\'applications de gestion pour le commerce en ligne spécialisé dans les produits malgaches.',
                'responsibilities': [
                    # Correction : le doublon "facturation" a été retiré.
                    'Gestion d\'approvisionnement : entrées et sorties de stock, bons de commande, bons de livraison, facturation, tableaux de bord',
                    'Gestion de stock : système de suivi des mouvements selon la méthode FIFO, inventaire en temps réel, tableaux de bord dynamiques',
                    'Génération automatique des bons de commande et bons de livraison'
                ],
                'activities': [
                    'Développement, tests d\'intégration et de performance',
                    'Bonnes pratiques de sécurité et protection des données sensibles',
                    'Déploiement et mise en production des applications',
                    'Rédaction de manuels d\'utilisation et maintenance applicative',
                    'Débogage et résolution de bugs complexes',
                    'Analyse des besoins utilisateurs et définition des spécifications techniques',
                    'Maintenance évolutive et corrective',
                    'Revue de code et feedbacks constructifs'
                ],
                'technologies': ['Java', 'Spring Boot', 'Angular', 'TypeScript', 'MySQL', 'Git', 'REST API', 'Maven', 'IntelliJ IDEA'],
                'achievements': [
                    'Système complet de gestion des stocks avec méthode FIFO',
                    'Système de facturation automatisé',
                    'Optimisation des performances des requêtes de base de données',
                    'Implémentation de bonnes pratiques de sécurité'
                ]
            }
        ],
        'project_categories': [
            {
                'id': 'games',
                'name': 'Jeux Vidéo',
                'description': 'Créations ludiques avec Unreal Engine et Unity',
                'icon': 'fas fa-gamepad',
                'accent': '#e85d4a'
            },
            {
                'id': 'software',
                'name': 'Logiciels',
                'description': 'Applications desktop et outils spécialisés',
                'icon': 'fas fa-desktop',
                'accent': '#3b82c4'
            },
            {
                'id': 'web',
                'name': 'Sites Web',
                'description': 'Applications web modernes et responsives',
                'icon': 'fas fa-globe',
                'accent': '#2da868'
            },
            {
                'id': 'ai',
                'name': 'Intelligence Artificielle',
                'description': 'IA, Machine Learning et Deep Learning',
                'icon': 'fas fa-brain',
                'accent': '#8b5cf6'
            }
        ],
        'projects': {
            'games': [
                {
                    'id': 1,
                    'title': 'CUBI 2026 — Beat-em-up Ubisoft Game Lab',
                    'description': 'Beat-em-up développé pour le concours Ubisoft Game Lab 2026. Deux personnages distincts (style 80s et 90s), système de combat avancé avec combos, dash avec effets visuels, ennemis IA NavMesh, et accessibilité complète. Systèmes hybrides : animation custom frame-swap pour le 80s, Mixamo/Humanoid pour le 90s.',
                    'technologies': ['Unity 6.1', 'C#', 'Input System', 'NavMesh AI', 'Animation Events', 'Object Pooling', 'VFX Graph', 'Cinemachine', 'Mixamo'],
                    'images': [get_media_url('cubi_1.jpg', 'projects')],
                    'videos': [get_media_url('cubi_demo.mp4', 'videos')],
                    'main_image': get_media_url('cubi_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/CUBI-GameLab2026.git',
                    'demo': None,
                    'category': 'games',
                    'featured': True
                },
                {
                    'id': 2,
                    'title': 'Simulateur de conduite 3D — Unreal Engine + Chaos Vehicle',
                    'description': 'Simulateur de conduite sous Unreal Engine 5.5 avec physique réaliste basée sur ChaosVehicle. Contrôle complet du véhicule (freinage, marche arrière, caméra dynamique), matériaux personnalisés et système d\'entrée en C++ sans Blueprint parent.',
                    'technologies': ['Unreal Engine 5.5', 'C++', 'Chaos Vehicle', 'Niagara', 'Blueprint', 'Skeletal Mesh', 'Enhanced Input System'],
                    'images': [get_media_url('simulateur_1.jpg', 'projects'), get_media_url('simulateur_2.jpg', 'projects')],
                    'videos': [get_media_url('simulateur_demo.mp4', 'videos')],
                    'main_image': get_media_url('simulateur_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/SimulateurVoiture.git',
                    'demo': None,
                    'category': 'games',
                    'featured': True
                },
                {
                    'id': 3,
                    'title': 'JeuAventure — Jeu d\'aventure 3D avec IA Unity',
                    'description': 'Jeu d\'aventure/plateforme 3D avec système de collection, sauvetage d\'amis et combat contre des ennemis intelligents. Mécaniques physiques réalistes, effets visuels avancés et IA basée sur NavMesh.',
                    'technologies': ['Unity 6.1', 'C#', 'Universal Render Pipeline', 'NavMesh AI', 'iTween', 'Post-Processing', 'Terrain Tools', 'Particle Systems'],
                    'images': [get_media_url('jeuaventure_1.jpg', 'projects'), get_media_url('jeuaventure_2.jpg', 'projects')],
                    'videos': [get_media_url('jeuaventure_demo.mp4', 'videos')],
                    'main_image': get_media_url('jeuaventure_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/JeuAventure.git',
                    'demo': None,
                    'category': 'games'
                },
                {
                    'id': 4,
                    'title': 'Aventure 3D — Exploration et collecte (Unreal Engine)',
                    'description': 'Jeu d\'aventure 3D développé entièrement avec le système Blueprint d\'Unreal Engine 5.5. Le joueur explore un monde ouvert, collecte des pièces, utilise un système de vol pour atteindre des zones élevées, et résout des énigmes clé-porte.',
                    'technologies': ['Unreal Engine 5.5', 'Blueprint Visual Scripting', 'Third Person Character', 'Enhanced Input System', 'Collision Detection', 'Level Design', 'Animation Blueprint', 'Particle Systems'],
                    'images': [get_media_url('aventure3d_1.jpg', 'projects'), get_media_url('aventure3d_2.jpg', 'projects'), get_media_url('aventure3d_3.jpg', 'projects')],
                    'videos': [get_media_url('aventure3d_demo.mp4', 'videos')],
                    'main_image': get_media_url('aventure3d_1.jpg', 'projects'),
                    'demo': None,
                    'category': 'games'
                },
                {
                    'id': 5,
                    'title': 'Aventure Open World — Unity',
                    'description': 'Jeu d\'aventure open world en développement sous Unity avec système de quêtes immersif. Map complète et système de mouvement avancé du personnage avec physiques réalistes (marche, course, saut), animations fluides et effets visuels.',
                    'technologies': ['Unity 6.1', 'C#', 'Rigidbody Physics', 'Animator Controller', 'Particle Systems', 'Audio System', 'Input System', 'LayerMask', 'Raycast Detection'],
                    'images': [get_media_url('openworld_1.jpg', 'projects'), get_media_url('openworld_2.jpg', 'projects')],
                    'videos': [get_media_url('openworld_demo.mp4', 'videos')],
                    'main_image': get_media_url('openworld_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/OpenWorld.git',
                    'demo': None,
                    'status': 'En développement',
                    'category': 'games'
                },
                {
                    'id': 6,
                    'title': 'Jeu de tir TPS/FPS — Unreal Engine',
                    'description': 'Jeu de tir hybride avec vue à la 3e personne, basculant en vue FPS lors du tir. Animations complètes du personnage, gestion de la caméra dynamique, impact des tirs, modes de tir (unique et rafale). IA ennemie en cours.',
                    'technologies': ['Unreal Engine 5.5', 'C++', 'Blueprints', 'Animation Blueprint', 'State Machines', 'Line Trace', 'Niagara FX'],
                    'images': [get_media_url('fps_tps_1.jpg', 'projects'), get_media_url('fps_tps_2.jpg', 'projects')],
                    'videos': [get_media_url('fps_tps_demo.mp4', 'videos')],
                    'main_image': get_media_url('fps_tps_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/JeuTir.git',
                    'demo': None,
                    'status': 'En développement',
                    'category': 'games'
                }
            ],
            'software': [
                {
                    'id': 7,
                    'title': 'Bataille Navale — C',
                    'description': 'Implémentation complète du jeu de bataille navale en langage C avec interface console interactive. Plateau 6x6, placement des navires, système de tir, détection des coulés et statistiques.',
                    'technologies': ['C', 'Console Interface', 'Data Structures', 'Game Logic', 'File I/O', 'Makefile', 'Memory Management'],
                    'images': [],
                    'main_image': None,
                    'github': 'https://github.com/MialyAnderson/BatailleNavale.git',
                    'category': 'software'
                },
                {
                    'id': 8,
                    'title': 'SpaceTaxi Tower Defense — Java Swing',
                    'description': 'Tower defense en Java avec interface graphique complète. Le joueur défend son château contre des vagues d\'ennemis. Système de génération d\'ennemis, gestion des projectiles, UI interactive, économie de jeu.',
                    'technologies': ['Java', 'Swing', 'AWT', 'Graphics2D', 'Game Development', 'Object-Oriented Design', 'Event Handling'],
                    'images': [],
                    'main_image': None,
                    'github': 'https://github.com/MialyAnderson/SpaceTaxiTowerDefense.git',
                    'category': 'software'
                },
                {
                    'id': 9,
                    'title': 'Automates Cellulaires Unidimensionnels — OCaml',
                    'description': 'Automates cellulaires en programmation fonctionnelle avec OCaml. Simulation d\'automates comme Sierpinski et chaos, fonctions d\'évolution, mémoïsation pour l\'optimisation, interface CLI.',
                    'technologies': ['OCaml', 'Functional Programming', 'Cellular Automata', 'Dune', 'Pattern Matching', 'Memoization'],
                    'images': [],
                    'main_image': None,
                    'github': 'https://github.com/MialyAnderson/CellularAutomata.git',
                    'category': 'software'
                }
            ],
            'web': [
                {
                    'id': 10,
                    'title': 'Jeux by Anderson — Plateforme de jeux en ligne',
                    'description': 'Plateforme de jeux de société en ligne. Tic-Tac-Toe, Échecs et Shogi (échecs japonais) avec interface interactive et gameplay multijoueur via Socket.io.',
                    'technologies': ['HTML', 'CSS', 'JavaScript', 'Node.js', 'Socket.io', 'Express.js'],
                    'images': [],
                    'main_image': None,
                    'github': 'https://github.com/MialyAnderson/JeuxByAnderson.git',
                    'demo': 'https://jeuxbyanderson-5yke.onrender.com/',
                    'category': 'web',
                    'featured': True
                },
                {
                    'id': 11,
                    'title': 'Contraventions Montréal',
                    'description': 'Application web pour rechercher les contraventions alimentaires des restaurants de Montréal. Interface de recherche rapide avec affichage détaillé des infractions (établissement, dates, montants).',
                    'technologies': ['HTML', 'CSS', 'JavaScript', 'Node.js', 'Express.js', 'API Integration', 'Bootstrap'],
                    'images': [],
                    'main_image': None,
                    'github': 'https://github.com/MialyAnderson/ContraventionsMontreal.git',
                    'demo': 'https://contravention-montreal-wlpz.onrender.com/',
                    'category': 'web'
                },
                {
                    'id': 12,
                    'title': 'FillGood — Boutique de créations au crochet',
                    'description': 'Site e-commerce spécialisé dans la vente de créations artisanales au crochet et macramé. Catalogue diversifié (vêtements bébé, accessoires, amigurumi).',
                    'technologies': ['HTML', 'CSS', 'JavaScript', 'Python', 'Flask', 'SQLite', 'Bootstrap'],
                    'images': [],
                    'main_image': None,
                    'github': 'https://github.com/MialyAnderson/FillGood-Crochet.git',
                    'demo': 'http://fillgood-decobyat-4n9e.onrender.com/',
                    'category': 'web'
                }
            ],
            'ai': [
                {
                    'id': 13,
                    'title': 'Jeu ±123D — Bot IA Minimax',
                    'description': 'Bot intelligent pour le jeu ±123D utilisant l\'algorithme Minimax avec élagage alpha-beta. Jeu de stratégie à deux joueurs sur plateau 1D avec drapeau.',
                    'technologies': ['Java', 'Minimax', 'Alpha-Beta Pruning', 'Game AI', 'Strategy Game'],
                    'main_image': None,
                    'images': [],
                    'github': 'https://github.com/MialyAnderson/PlusMinus123D.git',
                    'category': 'ai'
                },
                {
                    'id': 14,
                    'title': 'Monde des Wumpus — MDP & Itération par valeurs',
                    'description': 'Agent intelligent pour naviguer dans le monde des Wumpus en utilisant un Processus de Décision Markovien (MDP). Algorithme d\'itération par valeurs pour optimiser la collecte d\'or dans un environnement stochastique.',
                    'technologies': ['Python', 'MDP', 'Value Iteration', 'Reinforcement Learning', 'AI Planning'],
                    'images': [],
                    'main_image': None,
                    'github': 'https://github.com/MialyAnderson/WumpusWorldMDP.git',
                    'category': 'ai'
                },
                {
                    'id': 15,
                    'title': 'Prédiction immobilière — KNN',
                    'description': 'Système de prédiction des valeurs immobilières utilisant l\'algorithme des k plus proches voisins. Entraînement sur données historiques, calcul d\'erreur quadratique moyenne pour évaluer la précision.',
                    'technologies': ['Python', 'Java', 'C++', 'KNN', 'Machine Learning', 'Data Analysis'],
                    'images': [],
                    'main_image': None,
                    'github': 'https://github.com/MialyAnderson/RealEstatePredictionKNN.git',
                    'category': 'ai'
                }
            ]
        }
    }


# ====== CONTENU BILINGUE ======
# La version française reste la source principale. La version anglaise reprend
# les mêmes médias, liens GitHub et identifiants, puis remplace seulement les
# textes visibles.

UI_TRANSLATIONS = {
    'fr': {
        'nav_home': 'Accueil', 'nav_about': 'À propos', 'nav_experience': 'Expérience',
        'nav_skills': 'Compétences', 'nav_projects': 'Projets', 'nav_contact': 'Contact',
        'hero_meta': 'Programmeur gameplay · Full stack', 'view_projects': 'Voir mes projets',
        'contact_me': 'Me contacter', 'download_cv': 'Télécharger le CV', 'available': 'Disponible',
        'available_projects': 'Disponible pour de nouveaux projets', 'stat_projects': 'Projets réalisés',
        'stat_engines': 'Moteurs de jeu maîtrisés', 'stat_cubi': 'Mois sur CUBI 2026',
        'about_number': '01 / À PROPOS', 'about_title_before': 'Le', 'about_title_em': 'parcours',
        'about_subtitle': "Diplômé en génie logiciel à Montréal, passionné de gameplay programming et d'architecture logicielle.",
        'contact_info': 'Coordonnées', 'experience_number': '02 / EXPÉRIENCE',
        'experience_title_before': "Là où j'ai", 'experience_title_em': 'livré',
        'experience_subtitle': 'Compétitions, mandats et projets en équipe.',
        'main_responsibilities': 'Responsabilités principales', 'technical_activities': 'Activités techniques',
        'technologies': 'Technologies', 'achievements': 'Réalisations',
        'tech_stack': 'Stack technique', 'key_achievements': 'Réalisations clés',
        'skills_number': '03 / COMPÉTENCES', 'skills_title_before': 'La', 'skills_title_em': 'boîte à outils',
        'skills_subtitle': 'Regroupées par niveau de maîtrise réelle, pas par chiffres arbitraires.',
        'projects_number': '04 / PROJETS', 'projects_title_before': "Ce que j'ai", 'projects_title_em': 'construit',
        'projects_subtitle': "Une sélection de jeux, applications web et projets d'IA.",
        'featured_projects': 'Projets phares', 'selections': 'sélections', 'featured': 'Phare',
        'other_projects': 'Autres projets', 'all': 'Tous', 'code': 'Code', 'demo': 'Démo', 'media': 'Médias',
        'contact_number': '05 / CONTACT', 'contact_title_before': 'On', 'contact_title_em': 'collabore ?',
        'contact_subtitle': "Stage, mandat, projet de jeu — n'hésite pas.",
        'direct_contact': 'Contact direct', 'phone': 'Téléphone', 'location': 'Localisation', 'on_web': 'Sur le web',
        'footer': 'Construit avec Flask, du café et beaucoup de Git', 'project_media': 'Médias du projet',
        'loading': 'Chargement...', 'no_media': 'Aucun média disponible.', 'loading_error': 'Erreur de chargement.',
        'image_alt': 'Image'
    },
    'en': {
        'nav_home': 'Home', 'nav_about': 'About', 'nav_experience': 'Experience',
        'nav_skills': 'Skills', 'nav_projects': 'Projects', 'nav_contact': 'Contact',
        'hero_meta': 'Gameplay programmer · Full stack', 'view_projects': 'View my projects',
        'contact_me': 'Contact me', 'download_cv': 'Download CV', 'available': 'Available',
        'available_projects': 'Available for new projects', 'stat_projects': 'Completed projects',
        'stat_engines': 'Game engines used', 'stat_cubi': 'Months on CUBI 2026',
        'about_number': '01 / ABOUT', 'about_title_before': 'The', 'about_title_em': 'journey',
        'about_subtitle': 'Software engineering student in Montreal, passionate about gameplay programming and software architecture.',
        'contact_info': 'Contact details', 'experience_number': '02 / EXPERIENCE',
        'experience_title_before': 'Where I', 'experience_title_em': 'delivered',
        'experience_subtitle': 'Competitions, mandates and team projects.',
        'main_responsibilities': 'Main responsibilities', 'technical_activities': 'Technical activities',
        'technologies': 'Technologies', 'achievements': 'Achievements',
        'tech_stack': 'Technical stack', 'key_achievements': 'Key achievements',
        'skills_number': '03 / SKILLS', 'skills_title_before': 'The', 'skills_title_em': 'toolbox',
        'skills_subtitle': 'Grouped by real proficiency level, not arbitrary numbers.',
        'projects_number': '04 / PROJECTS', 'projects_title_before': 'What I have', 'projects_title_em': 'built',
        'projects_subtitle': 'A selection of games, web applications and AI projects.',
        'featured_projects': 'Featured projects', 'selections': 'selections', 'featured': 'Featured',
        'other_projects': 'Other projects', 'all': 'All', 'code': 'Code', 'demo': 'Demo', 'media': 'Media',
        'contact_number': '05 / CONTACT', 'contact_title_before': 'Let’s', 'contact_title_em': 'collaborate?',
        'contact_subtitle': 'Internship, mandate, game project — feel free to reach out.',
        'direct_contact': 'Direct contact', 'phone': 'Phone', 'location': 'Location', 'on_web': 'On the web',
        'footer': 'Built with Flask, coffee and a lot of Git', 'project_media': 'Project media',
        'loading': 'Loading...', 'no_media': 'No media available.', 'loading_error': 'Loading error.',
        'image_alt': 'Image'
    }
}


def add_ui(data, lang):
    data['ui'] = UI_TRANSLATIONS[lang]
    data['lang'] = lang
    data['other_lang'] = 'en' if lang == 'fr' else 'fr'
    data['other_lang_label'] = 'EN' if lang == 'fr' else 'FR'
    if lang == 'fr':
        data['about_paragraphs'] = [
            'Je suis Mialy Anderson, diplômé en génie logiciel de l’Université du Québec à Montréal (UQAM), basé à Montréal. Mon parcours universitaire m’a donné une base solide en programmation, conception logicielle, bases de données, développement web, algorithmique et architecture d’applications.',

            'Je développe plusieurs types de projets : des jeux vidéo avec Unity et Unreal Engine, des applications web back/front avec Java/Spring, Angular et Flask, ainsi que des outils logiciels et projets techniques en C, Java, Python et OCaml.',

            'Mon plus récent projet : <strong>CUBI 2026</strong>, un beat-em-up développé en équipe de 8 pour le concours Ubisoft Game Lab 2026, présenté chez Ubisoft Montréal devant un jury de l’industrie. J’y ai contribué au système de combat, à l’IA NavMesh, au système d’animation hybride, aux effets visuels gameplay et à l’accessibilité (remapping, haptics).',

            'J’ai également développé des applications de gestion en Java/Spring/Angular pour Shop Imerina entre septembre 2023 et septembre 2025. Cette expérience m’a permis de travailler sur la gestion de stock, les bons de commande, les bons de livraison, la facturation, les tableaux de bord et la maintenance applicative.'
        ]
    else:
        data['about_paragraphs'] = [
            'I am Mialy Anderson, a software engineering graduate from the Université du Québec à Montréal (UQAM), based in Montreal. My academic background gave me a solid foundation in programming, software design, databases, web development, algorithms and application architecture.',

            'I develop different types of projects: video games with Unity and Unreal Engine, front/back web applications with Java/Spring, Angular and Flask, as well as software tools and technical projects in C, Java, Python and OCaml.',

            'My most recent project is <strong>CUBI 2026</strong>, a beat-em-up developed in a team of 8 for the Ubisoft Game Lab 2026 competition and presented at Ubisoft Montreal in front of an industry jury. I contributed to the combat system, NavMesh AI, hybrid animation system, gameplay visual effects and accessibility features (remapping, haptics).',

            'I also developed Java/Spring/Angular management applications for Shop Imerina from September 2023 to September 2025. This experience allowed me to work on inventory management, purchase orders, delivery notes, invoicing, dashboards and application maintenance.'
        ]
    return data


def get_portfolio_data_en():
    data = get_portfolio_data_fr()
    data['about'].update({
        'title': 'Full Stack & Gameplay Developer',
        'headline': 'I build <em>games</em>,<br><em>software tools</em><br>and <em>web applications</em>.',
        'tagline': 'Gameplay programmer on Unity and Unreal Engine, and full stack developer with Java/Spring and Flask. Based in Montreal.',
        'description': 'Specialized in gameplay programming with Unity and Unreal Engine, and full stack development with Java/Spring Boot, Angular and Python/Flask. Recently worked as a gameplay programmer on CUBI 2026 for the Ubisoft Game Lab competition.',
        'location': 'Montreal, QC'
    })
    data['skill_groups'][0].update({'level': 'Strong proficiency', 'description': 'Technologies used on complete projects, in production or in competition.'})
    data['skill_groups'][1].update({'level': 'Comfortable', 'description': 'Used on several projects and comfortable enough to deliver.'})
    data['skill_groups'][2].update({'level': 'Currently learning', 'description': 'Used on targeted projects and currently being improved.'})
    category_map = {'Jeux': 'Games', 'Système': 'Systems', 'Outils': 'Tools'}
    for group in data['skill_groups']:
        for skill in group['skills']:
            skill['category'] = category_map.get(skill['category'], skill['category'])
    data['experience'][0].update({
        'title': 'Gameplay Programmer — Ubisoft Game Lab 2026 Competition (UQAM)',
        'company': 'Ubisoft Montreal', 'location': 'Montreal, QC', 'type': 'Student competition',
        'period': 'January 2026 — April 2026', 'duration': '4 months',
        'description': 'Participation in the Ubisoft Game Lab 2026 competition through the development of a beat-em-up called A GLITCH IN TIME, based on an 80s/90s theme. Mentored by Ubisoft monitors. Prototype presented at Ubisoft Montreal in front of a jury of industry professionals.',
        'responsibilities': ['Gameplay development: combat system with combos, dash with visual effects, platforming mechanics', 'AI programming: enemies using NavMesh and object pooling to optimize performance', 'Accessibility implementation: input remapping with ApplyBindingOverride and controller haptic feedback', 'Creation of a hybrid animation system: custom frame-swap mesh animation for the 80s character and Mixamo/Humanoid for the 90s character', 'Visual effects development: dash trails, slash effects and attack particles', 'UI implementation: pause menu with D-pad navigation and accessible UI system'],
        'activities': ['Collaboration in a team of 8', 'Resolution of Git conflicts during complex merges', 'Debugging technical issues such as Mixamo Y-axis offset and animation timing', 'Presentation of the prototype at Ubisoft Montreal', 'Fast iterations based on team feedback', 'Object-oriented architecture using abstract class hierarchies such as PlayerBase and MovementBase'],
        'achievements': ['Final prototype completed and presented at Ubisoft Montreal', 'Implementation of two distinct animation systems in the same game', 'Complete accessibility system with remapping and haptics', 'Modular architecture with reusable abstract classes', 'Effective collaboration in an 8-person team over 4 months']
    })
    data['experience'][1].update({
        'title': 'Full Stack Developer Java Spring / Angular', 'location': 'Antananarivo, Madagascar', 'type': 'Remote',
        'period': 'September 2023 — Present', 'duration': 'Ongoing',
        'description': 'Development of management applications for an e-commerce business specialized in Malagasy products.',
        'responsibilities': ['Procurement management: stock entries and exits, purchase orders, delivery notes, invoicing and dashboards', 'Inventory management: movement tracking using the FIFO method, real-time inventory and dynamic dashboards', 'Automatic generation of purchase orders and delivery notes'],
        'activities': ['Development, integration testing and performance testing', 'Security best practices and protection of sensitive data', 'Deployment and production release of applications', 'Writing user manuals and application maintenance documentation', 'Debugging and resolution of complex bugs', 'User needs analysis and technical specification definition', 'Corrective and evolutionary maintenance', 'Code review and constructive feedback'],
        'achievements': ['Complete inventory management system using the FIFO method', 'Automated invoicing system', 'Optimization of database query performance', 'Implementation of security best practices']
    })
    data['project_categories'] = [
        {'id': 'games', 'name': 'Games', 'description': 'Game projects made with Unreal Engine and Unity', 'icon': 'fas fa-gamepad', 'accent': '#e85d4a'},
        {'id': 'software', 'name': 'Software', 'description': 'Desktop applications and specialized tools', 'icon': 'fas fa-desktop', 'accent': '#3b82c4'},
        {'id': 'web', 'name': 'Websites', 'description': 'Modern and responsive web applications', 'icon': 'fas fa-globe', 'accent': '#2da868'},
        {'id': 'ai', 'name': 'Artificial Intelligence', 'description': 'AI, Machine Learning and Deep Learning', 'icon': 'fas fa-brain', 'accent': '#8b5cf6'}
    ]
    translations = {
        1: ('CUBI 2026 — Ubisoft Game Lab Beat-em-up', 'Beat-em-up developed for the Ubisoft Game Lab 2026 competition. Two distinct characters with 80s and 90s styles, advanced combat system with combos, dash with visual effects, NavMesh AI enemies and complete accessibility. Hybrid systems: custom frame-swap animation for the 80s character, Mixamo/Humanoid for the 90s character.'),
        2: ('3D Driving Simulator — Unreal Engine + Chaos Vehicle', 'Driving simulator built with Unreal Engine 5.5 and realistic physics based on ChaosVehicle. Complete vehicle controls, braking, reverse driving, dynamic camera, custom materials and C++ input system without a Blueprint parent.'),
        3: ('JeuAventure — 3D Adventure Game with Unity AI', '3D adventure/platform game with collection mechanics, friend rescue and combat against intelligent enemies. Realistic physics mechanics, advanced visual effects and NavMesh-based AI.'),
        4: ('3D Adventure — Exploration and Collection (Unreal Engine)', '3D adventure game developed entirely with Unreal Engine 5.5 Blueprint system. The player explores an open world, collects coins, uses a flying system to reach elevated areas and solves key-door puzzles.'),
        5: ('Open World Adventure — Unity', 'Open world adventure game in development with Unity and an immersive quest system. Complete map and advanced character movement system with realistic physics, walking, running, jumping, smooth animations and visual effects.'),
        6: ('TPS/FPS Shooter — Unreal Engine', 'Hybrid shooter with third-person view that switches to FPS view while shooting. Complete character animations, dynamic camera management, bullet impacts and single/burst fire modes. Enemy AI in progress.'),
        7: ('Battleship — C', 'Complete implementation of Battleship in C with an interactive console interface. 6x6 board, ship placement, shooting system, sunk-ship detection and statistics.'),
        8: ('SpaceTaxi Tower Defense — Java Swing', 'Tower defense game in Java with a complete graphical interface. The player defends a castle against waves of enemies. Enemy spawning, projectile management, interactive UI and in-game economy.'),
        9: ('One-dimensional Cellular Automata — OCaml', 'Cellular automata in functional programming with OCaml. Simulation of automata such as Sierpinski and chaos, evolution functions, memoization for optimization and CLI interface.'),
        10: ('Jeux by Anderson — Online Game Platform', 'Online board game platform. Tic-Tac-Toe, Chess and Shogi with interactive interface and multiplayer gameplay using Socket.io.'),
        11: ('Montreal Food Violations', 'Web application to search food inspection violations for restaurants in Montreal. Fast search interface with detailed violation display including establishment, dates and amounts.'),
        12: ('FillGood — Crochet Creations Shop', 'E-commerce website specialized in handmade crochet and macramé creations. Diverse catalog including baby clothes, accessories and amigurumi.'),
        13: ('±123D Game — Minimax AI Bot', 'Intelligent bot for the ±123D game using the Minimax algorithm with alpha-beta pruning. Two-player strategy game on a 1D board with a flag.'),
        14: ('Wumpus World — MDP & Value Iteration', 'Intelligent agent navigating the Wumpus world using a Markov Decision Process. Value iteration algorithm to optimize gold collection in a stochastic environment.'),
        15: ('Real Estate Prediction — KNN', 'Real estate value prediction system using the k-nearest neighbors algorithm. Training on historical data and mean squared error calculation to evaluate accuracy.')
    }
    status_map = {'En développement': 'In development'}
    for category_projects in data['projects'].values():
        for project in category_projects:
            if project['id'] in translations:
                project['title'], project['description'] = translations[project['id']]
            if 'status' in project:
                project['status'] = status_map.get(project['status'], project['status'])
    return data


def get_portfolio_data(lang='fr'):
    if lang == 'en':
        return add_ui(get_portfolio_data_en(), 'en')
    return add_ui(get_portfolio_data_fr(), 'fr')

@app.route('/')
@app.route('/<lang>')
def index(lang='fr'):
    """Page d'accueil du portfolio bilingue."""
    if lang not in ['fr', 'en']:
        lang = 'fr'
    data = get_portfolio_data(lang)
    return render_template('index.html', data=data, lang=lang)


@app.route('/api/experience')
def get_experience():
    data = get_portfolio_data()
    return jsonify(data['experience'])


@app.route('/api/projects')
def get_projects():
    data = get_portfolio_data()
    return jsonify(data['projects'])


@app.route('/api/projects/<category>')
def get_projects_by_category(category):
    data = get_portfolio_data()
    projects = data['projects'].get(category, [])
    return jsonify(projects)


@app.route('/api/project/<int:project_id>')
def get_project(project_id):
    data = get_portfolio_data()
    for category_projects in data['projects'].values():
        for p in category_projects:
            if p['id'] == project_id:
                return jsonify(p)
    return jsonify({'error': 'Project not found'}), 404


@app.route('/api/project/<int:project_id>/media')
def get_project_media(project_id):
    data = get_portfolio_data()
    for category_projects in data['projects'].values():
        for p in category_projects:
            if p['id'] == project_id:
                # Filtrer les None pour ne renvoyer que les médias existants
                media = {
                    'images': [img for img in p.get('images', []) if img],
                    'videos': [v for v in p.get('videos', []) if v],
                    'main_image': p.get('main_image')
                }
                return jsonify(media)
    return jsonify({'error': 'Project not found'}), 404


@app.route('/api/featured-projects')
def get_featured_projects():
    data = get_portfolio_data()
    featured = []
    for category_projects in data['projects'].values():
        for project in category_projects:
            if project.get('featured', False):
                featured.append(project)
    return jsonify(featured)


@app.route('/cv')
def download_cv():
    """Télécharge le CV en PDF s'il existe"""
    cv_path = 'static/cv/cv.pdf'
    if os.path.exists(cv_path):
        return send_file(cv_path, as_attachment=True,
                         download_name='Mialy_Anderson_RAKOTONDRADANO_CV.pdf')
    return jsonify({'error': 'CV non disponible'}), 404


@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    required_fields = ['name', 'email', 'message']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Champs requis manquants'}), 400

    save_contact_message(data)
    print(f"Nouveau message de {data['name']} ({data['email']}): {data['message']}")
    return jsonify({'success': True, 'message': 'Votre message a été envoyé avec succès!'})


@app.route('/upload-media', methods=['POST'])
def upload_media():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        folder = request.form.get('folder', 'projects')
        if folder not in ['projects', 'profile', 'videos']:
            folder = 'projects'

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], folder, filename)
        file.save(file_path)

        file_url = url_for('static', filename=f'media/{folder}/{filename}')
        return jsonify({
            'success': True,
            'filename': filename,
            'url': file_url,
            'type': 'video' if is_video_file(filename) else 'image'
        })

    return jsonify({'error': 'Type de fichier non autorisé'}), 400


@app.route('/media/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.context_processor
def utility_processor():
    return dict(get_media_url=get_media_url, is_video_file=is_video_file)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)