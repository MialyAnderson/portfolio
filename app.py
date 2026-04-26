from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
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

# Créer les dossiers nécessaires
def create_directories():
    directories = [
        'static/media',
        'static/media/projects',
        'static/media/profile',
        'static/media/videos',
        'static/media/thumbnails',
        'templates'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

create_directories()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def get_media_url(filename, folder='projects'):
    """Génère l'URL pour un fichier média"""
    if filename and os.path.exists(f'static/media/{folder}/{filename}'):
        return url_for('static', filename=f'media/{folder}/{filename}')
    return url_for('static', filename='media/placeholder.jpg')

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

# Données du portfolio avec catégories de projets
def get_portfolio_data():
    return {
        'about': {
            'name': 'Mialy Anderson RAKOTONDRADANO',
            'title': 'Développeur Full Stack',
            'description': 'Passionné par le développement web, les jeux vidéo et les nouvelles technologies. Je me spécialise en programmation avec Python, C++, Java ainsi qu\'en conception de jeux avec Unreal Engine.',
            'email': 'andyrakotondradano@gmail.com',
            'phone': '+1 579 372 6108',
            'location': 'Montréal, QC',
            'profile_image': get_media_url('profile.png', 'profile')
        },
        'skills': [
            {'name': 'Python', 'level': 90, 'category': 'Backend'},
            {'name': 'JavaScript', 'level': 85, 'category': 'Frontend'},
            {'name': 'Java', 'level': 90, 'category': 'Backend'},
            {'name': 'C', 'level': 75, 'category': 'Système'},
            {'name': 'C++', 'level': 90, 'category': 'Jeux'},
            {'name': 'Unreal Engine', 'level': 85, 'category': 'Jeux'},
            {'name': 'Unity Engine', 'level': 90, 'category': 'Jeux'},
            {'name': 'SQL', 'level': 70, 'category': 'Base de données'},
            {'name': 'Git', 'level': 90, 'category': 'Outils'},
            {'name': 'Flask/Django', 'level': 80, 'category': 'Backend'},
            {'name': 'HTML/CSS', 'level': 85, 'category': 'Frontend'},
            {'name': 'React', 'level': 75, 'category': 'Frontend'},
            {'name': 'Spring Boot', 'level': 85, 'category': 'Backend'},
            {'name': 'Angular', 'level': 80, 'category': 'Frontend'}
        ],
        'experience': [
             {
                'id': 1,
                'title': 'Programmeur Gameplay - Concours Ubisoft Game Lab 2026 (UQAM)',
                'company': 'Ubisoft Montréal',
                'location': 'Montréal, QC',
                'type': 'Compétition étudiante',
                'period': 'Janvier 2026 - Avril 2026',
                'duration': '4 mois',
                'description': 'Participation au prestigieux concours Ubisoft Game Lab 2026 avec développement d\'un beat-em-up nommé A GLITCH IN TIME en intégrant le thème "année 80-90". Prototype présenté chez Ubisoft Montréal devant un jury de professionnels de l\'industrie du jeu vidéo.',
                'responsibilities': [
                    'Développement gameplay : système de combat avec combos, dash avec effets visuels, mécaniques de plateforme',
                    'Programmation d\'IA : ennemis avec NavMesh AI et système d\'object pooling pour optimiser les performances',
                    'Implémentation de l\'accessibilité : remapping des touches via ApplyBindingOverride, vibrations haptiques pour manettes',
                    'Création d\'un système d\'animation hybride : frame-swap mesh animation custom pour le personnage 80s et Mixamo/Humanoid pour le 90s',
                    'Développement d\'effets visuels : trails de dash, slash effects, particules pour les attaques',
                    'Gestion d\'interface : menu pause avec navigation D-pad, système de UI accessible'
                ],
                'activities': [
                    'Collaboration en équipe de 8',
                    'Résolution de conflits Git (git checkout --ours) lors des merges complexes',
                    'Debugging de problèmes techniques (offset Y-axis Mixamo, timing des animations)',
                    'Présentation du prototype chez Ubisoft Montréal',
                    'Itérations rapides basées sur les feedbacks de l\'équipe',
                    'Architecture orientée objet avec hiérarchies de classes abstraites (PlayerBase, MovementBase)'
                ],
                'technologies': ['Unity 6.1', 'C#', 'Input System', 'NavMesh AI', 'Animation Events', 'Mixamo', 'VFX Graph', 'Cinemachine', 'Object Pooling', 'Git'],
                'achievements': [
                    'Prototype finalisé et présenté chez Ubisoft Montréal',
                    'Implémentation de deux systèmes d\'animation distincts dans un même jeu',
                    'Système d\'accessibilité complet (remapping + haptics)',
                    'Architecture modulaire avec classes abstraites réutilisables',
                    'Collaboration efficace en équipe de 4 personnes sur 4 mois'
                ]
            },

            {
                'id': 2,
                'title': 'Développeur Full Stack Java Spring/Angular',
                'company': 'Shop Imerina',
                'location': 'Antananarivo, Madagascar',
                'type': 'Télétravail',
                'period': 'Septembre 2023 - Présent',
                'duration': 'En cours',
                'description': 'Développement d\'applications de gestion pour le commerce en ligne spécialisé dans les produits malgaches.',
                'responsibilities': [
                    'Gestion d\'approvisionnement : entrée et sortie de stocks, bon de commande, facturation, bon de livraison, facturation, tableau de bord',
                    'Gestion de stock : développement d\'un système de suivi des entrées et sorties de produits avec gestion des mouvements selon les méthodes FIFO, inventaire en temps réel, tableaux de bord dynamiques',
                    'Facturation : génération automatique des bons de commande, bons de livraison'
                ],
                'activities': [
                    'Développement des applications, suivis des tests d\'intégration et de performances',
                    'Implémentation des bonnes pratiques en matière de sécurité des données et protection des informations sensibles',
                    'Déploiement et mise en production des applications',
                    'Rédaction des manuels d\'utilisation et maintenances des applications',
                    'Débogage et résolution de bugs complexes : Analyse des erreurs et dysfonctionnements dans le code source',
                    'Participation à l\'analyse des besoins des utilisateurs et à la définition des spécifications techniques',
                    'Conception, développement, test et déploiement des applications Java',
                    'Maintenance évolutive et corrective des applications existantes',
                    'Revue de code et transmission de feedbacks constructifs',
                    'Codage'
                ],
                'technologies': ['Java', 'Spring Boot', 'Angular', 'TypeScript', 'MySQL', 'Git', 'REST API', 'Maven', 'IntelliJ IDEA'],
                'achievements': [
                    'Développement complet d\'un système de gestion des stocks avec méthode FIFO',
                    'Mise en place d\'un système de facturation automatisé',
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
                'color': '#e74c3c',
                'gradient': 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)'
            },
            {
                'id': 'software',
                'name': 'Logiciels',
                'description': 'Applications desktop et outils spécialisés',
                'icon': 'fas fa-desktop',
                'color': '#3498db',
                'gradient': 'linear-gradient(135deg, #3498db 0%, #2980b9 100%)'
            },
            {
                'id': 'web',
                'name': 'Sites Web',
                'description': 'Applications web modernes et responsives',
                'icon': 'fas fa-globe',
                'color': '#2ecc71',
                'gradient': 'linear-gradient(135deg, #2ecc71 0%, #27ae60 100%)'
            },
            {
                'id': 'ai',
                'name': 'Intelligence Artificielle',
                'description': 'Projets IA, Machine Learning et Deep Learning',
                'icon': 'fas fa-brain',
                'color': '#9b59b6',
                'gradient': 'linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%)'
            }
        ],
        'projects': {
            'games': [
                {
                    'id': 1,
                    'title': 'CUBI 2026 - Beat-em-up Ubisoft Game Lab',
                    'description': 'Beat-em-up développé pour le concours Ubisoft Game Lab 2026. Jeu avec deux personnages distincts (style 80s et 90s), système de combat avancé avec combos, dash avec effets visuels, ennemis IA NavMesh, et accessibilité complète. Utilise des systèmes hybrides : animation custom frame-swap pour le personnage 80s et Mixamo/Humanoid pour le 90s.',
                    'technologies': ['Unity 6.1', 'C#', 'Input System', 'NavMesh AI', 'Animation Events', 'Object Pooling', 'VFX Graph', 'Cinemachine', 'Mixamo'],
                    'images': [
                        get_media_url('cubi_1.jpg', 'projects'),
                    ],
                    'videos': [
                        get_media_url('cubi_demo.mp4', 'videos')
                    ],
                    'main_image': get_media_url('cubi_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/CUBI-GameLab2026.git',
                    'demo': None,
                    'category': 'games',
                },
                {
                    'id': 2,
                    'title': 'Simulateur de conduite en 3D avec Unreal Engine et Chaos Vehicle',
                    'description': 'Simulateur de conduite développé sous Unreal Engine 5.5 avec physique réaliste basée sur ChaosVehicle. Contrôle complet du véhicule (freinage, marche arrière, caméra dynamique), matériaux personnalisés et système d\'entrée en C++ sans Blueprint parent.',
                    'technologies': ['Unreal Engine 5.5', 'C++', 'Chaos Vehicle', 'Niagara', 'Blueprint', 'Skeletal Mesh', 'Enhanced Input System'],
                    'images': [
                        get_media_url('simulateur_1.jpg', 'projects'),
                        get_media_url('simulateur_2.jpg', 'projects'),
                    ],
                    'videos': [
                        get_media_url('simulateur_demo.mp4', 'videos')
                    ],
                    'main_image': get_media_url('simulateur_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/SimulateurVoiture.git',
                    'demo': None,
                    'category': 'games',
                },
                {
                    'id': 3,
                    'title': 'JeuAventure - Jeu d\'aventure 3D avec IA Unity',
                    'description': 'Jeu d\'aventure/plateforme 3D avec système de collection, sauvetage d\'amis et combat contre des ennemis intelligents. Mécaniques physiques réalistes, effets visuels avancés et IA basée sur NavMesh pour les comportements ennemis.',
                    'technologies': ['Unity 6.1', 'C#', 'Universal Render Pipeline', 'NavMesh AI', 'iTween', 'Post-Processing', 'Terrain Tools', 'Particle Systems'],
                    'images': [
                        get_media_url('jeuaventure_1.jpg', 'projects'),
                        get_media_url('jeuaventure_2.jpg', 'projects'),
                    ],
                    'videos': [
                        get_media_url('jeuaventure_demo.mp4', 'videos')
                    ],
                    'main_image': get_media_url('jeuaventure_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/JeuAventure.git',
                    'demo': None,
                    'category': 'games',
                },
                {
                    'id': 4,
                    'title': 'Aventure 3D - Jeu d\'exploration et collecte avec Unreal Engine',
                    'description': 'Jeu d\'aventure 3D développé entièrement avec le système Blueprint d\'Unreal Engine 5.5. Le joueur explore un monde ouvert en collectant des pièces, utilise un système de vol pour atteindre des zones élevées, et résout des énigmes avec un mécanisme clé-porte pour débloquer de nouvelles zones d\'exploration.',
                    'technologies': ['Unreal Engine 5.5', 'Blueprint Visual Scripting', 'Third Person Character', 'Enhanced Input System', 'Collision Detection', 'Level Design', 'Animation Blueprint', 'Particle Systems'],
                    'images': [
                        get_media_url('aventure3d_1.jpg', 'projects'),
                        get_media_url('aventure3d_2.jpg', 'projects'),
                        get_media_url('aventure3d_3.jpg', 'projects'),
                    ],
                    'videos': [
                        get_media_url('aventure3d_demo.mp4', 'videos')
                    ],
                    'main_image': get_media_url('aventure3d_1.jpg', 'projects'),
                    'demo': None,
                    'category': 'games'
                },
                {
                    'id': 5,
                    'title': 'Aventure Open World - Jeu de quêtes 3D Unity (En développement)',
                    'description': 'Jeu d\'aventure open world en développement sous Unity avec système de quêtes immersif. Actuellement implémenté : map complète et système de mouvement avancé du personnage avec physiques réalistes (marche, course, saut), animations fluides et effets visuels. Projet en cours de développement avec mécaniques de quêtes et interactions à venir.',
                    'technologies': ['Unity 6.1', 'C#', 'Rigidbody Physics', 'Animator Controller', 'Particle Systems', 'Audio System', 'Input System', 'LayerMask', 'Raycast Detection'],
                    'images': [
                        get_media_url('openworld_1.jpg', 'projects'),
                        get_media_url('openworld_2.jpg', 'projects'),
                    ],
                    'videos': [
                        get_media_url('openworld_demo.mp4', 'videos')
                    ],
                    'main_image': get_media_url('openworld_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/OpenWorld.git',
                    'demo': None,
                    'status': 'En développement',
                    'category': 'games'
                },
                {
                    'id': 6,
                    'title': 'Jeu de tir à la 3e personne / FPS – Unreal Engine (En développement)',
                    'description': 'Projet de jeu de tir hybride avec vue à la 3e personne, basculant en vue FPS lors du tir. Implémenté actuellement : animations complètes du personnage, gestion de la caméra dynamique, impact des tirs sur objets/personnages, modes de tir (unique et rafale). IA ennemie en cours de développement.',
                    'technologies': ['Unreal Engine 5.5', 'C++', 'Blueprints', 'Animation Blueprint', 'State Machines', 'Line Trace', 'Niagara FX'],
                    'images': [
                        get_media_url('fps_tps_1.jpg', 'projects'),
                        get_media_url('fps_tps_2.jpg', 'projects'),
                    ],
                    'videos': [
                        get_media_url('fps_tps_demo.mp4', 'videos')
                    ],
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
                    'title': 'Bataille Navale - Jeu en Console C',
                    'description': 'Implémentation complète du jeu de bataille navale en langage C avec interface console interactive. Gestion du plateau de jeu 6x6, placement des navires, système de tir, détection des coulés et statistiques de jeu. Code structuré avec makefile pour compilation.',
                    'technologies': ['C', 'Console Interface', 'Data Structures', 'Game Logic', 'File I/O', 'Makefile', 'Memory Management'],
                    'images': [
                        get_media_url('bataille_navale_1.jpg', 'projects'),
                        get_media_url('bataille_navale_2.jpg', 'projects'),
                        get_media_url('bataille_navale_3.jpg', 'projects'),
                    ],
                    'main_image': get_media_url('bataille_navale_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/BatailleNavale.git',
                    'category': 'software'
                },
                {
                    'id': 8,
                    'title': 'SpaceTaxi Tower Defense - Jeu Java avec Interface Graphique',
                    'description': 'Jeu de tower defense développé en Java avec interface graphique complète. Le joueur défend son château contre des vagues d\'ennemis en plaçant stratégiquement des tours. Système de génération d\'ennemis, gestion des projectiles, interface utilisateur interactive avec boutons d\'amélioration et économie de jeu intégrée.',
                    'technologies': ['Java', 'Swing', 'AWT', 'Graphics2D', 'Game Development', 'Object-Oriented Design', 'Event Handling', 'GUI Design'],
                    'images': [
                        get_media_url('spacetaxi_tower_defense_1.jpg', 'projects'),
                        get_media_url('spacetaxi_tower_defense_2.jpg', 'projects'),
                        get_media_url('spacetaxi_tower_defense_3.jpg', 'projects'),
                        get_media_url('spacetaxi_tower_defense_4.jpg', 'projects'),
                    ],
                    'main_image': get_media_url('spacetaxi_tower_defense_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/SpaceTaxiTowerDefense.git',
                    'category': 'software'
                },
                {
                    'id': 9,
                    'title': 'Automates Cellulaires Unidimensionnels - OCaml',
                    'description': 'Implémentation complète d\'automates cellulaires unidimensionnels en programmation fonctionnelle avec OCaml. Le projet inclut la simulation d\'automates comme Sierpinski et chaos, avec fonctions d\'évolution, mémoïsation pour l\'optimisation, et interface en ligne de commande pour la visualisation des motifs générés.',
                    'technologies': ['OCaml', 'Functional Programming', 'Cellular Automata', 'Dune Build System', 'Pattern Matching', 'Memoization', 'Mathematical Modeling'],
                    'images': [
                        get_media_url('cellular_automata_1.jpg', 'projects'),
                        get_media_url('cellular_automata_2.jpg', 'projects'),
                        get_media_url('cellular_automata_3.jpg', 'projects'),
                        get_media_url('cellular_automata_4.jpg', 'projects'),
                    ],
                    'main_image': get_media_url('cellular_automata_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/CellularAutomata.git',
                    'category': 'software'
                }
            ],
            'web': [
                {
                    'id': 10,
                    'title': 'Jeux by Anderson - Plateforme de Jeux en Ligne',
                    'description': 'Plateforme de jeux de société en ligne permettant de jouer avec des amis ou d\'autres joueurs. Propose une collection de jeux classiques incluant Tic-Tac-Toe, Échecs et Shogi (échecs japonais) avec interface interactive et gameplay multijoueur.',
                    'technologies': ['HTML', 'CSS', 'JavaScript', 'Node.js', 'Socket.io', 'Express.js', 'Game Logic'],
                    'images': [
                        get_media_url('jeux_anderson_1.jpg', 'projects'),
                        get_media_url('jeux_anderson_2.jpg', 'projects'),
                        get_media_url('jeux_anderson_3.jpg', 'projects'),
                    ],
                    'main_image': get_media_url('jeux_anderson_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/JeuxByAnderson.git',
                    'demo': 'https://jeuxbyanderson-5yke.onrender.com/',
                    'category': 'web',
                },
                {
                    'id': 11,
                    'title': 'Contraventions Montréal - Recherche d\'Infractions Alimentaires',
                    'description': 'Application web permettant de rechercher et consulter les contraventions alimentaires des restaurants de Montréal. Interface de recherche rapide avec affichage détaillé des infractions incluant l\'établissement, le nombre de contraventions, les dates, descriptions et montants des amendes.',
                    'technologies': ['HTML', 'CSS', 'JavaScript', 'Node.js', 'Express.js', 'API Integration', 'Data Processing', 'Bootstrap'],
                    'images': [
                        get_media_url('contraventions_mtl_1.jpg', 'projects'),
                        get_media_url('contraventions_mtl_2.jpg', 'projects'),
                        get_media_url('contraventions_mtl_3.jpg', 'projects'),
                    ],
                    'main_image': get_media_url('contraventions_mtl_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/ContraventionsMontreal.git',
                    'demo': 'https://contravention-montreal-wlpz.onrender.com/',
                    'category': 'web',
                },
                {
                    'id': 12,
                    'title': 'FillGood - Boutique de Créations au Crochet',
                    'description': 'Site e-commerce spécialisé dans la vente de créations artisanales au crochet et macramé. Catalogue diversifié incluant vêtements pour bébé (brassières, bonnets), accessoires décoratifs, jouets (amigurumi, jeux éducatifs), et articles de mode fait main. Chaque pièce est unique et confectionnée avec soin.',
                    'technologies': ['HTML', 'CSS', 'JavaScript', 'Python', 'Flask', 'SQLite', 'Bootstrap', 'E-commerce', 'Image Gallery'],
                    'images': [
                        get_media_url('fillgood_1.jpg', 'projects'),
                        get_media_url('fillgood_2.jpg', 'projects'),
                        get_media_url('fillgood_3.jpg', 'projects'),
                    ],
                    'main_image': get_media_url('fillgood_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/FillGood-Crochet.git',
                    'demo': 'http://fillgood-decobyat-4n9e.onrender.com/',
                    'category': 'web'
                }
            ],
            'ai': [
                {
                    'id': 13,
                    'title': 'Jeu ±123D - Bot IA avec Algorithme Minimax',
                    'description': 'Implémentation d\'un bot intelligent pour le jeu ±123D utilisant l\'algorithme Minimax avec élagage alpha-beta. Jeu de stratégie à deux joueurs sur plateau 1D avec drapeau, développé en Python avec interface graphique et mode console.',
                    'technologies': ['Java', 'Minimax Algorithm', 'Alpha-Beta Pruning', 'Game AI', 'Strategy Game', 'GUI', 'Object-oriented Programming'],
                    'main_image': get_media_url('plus_minus_123d_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/PlusMinus123D.git',
                    'category': 'ai',
                },
                {
                    'id': 14,
                    'title': 'Monde des Wumpus - Résolution par MDP et Itération par Valeurs',
                    'description': 'Implémentation d\'un agent intelligent pour naviguer dans le monde des Wumpus en utilisant un Processus de Décision Markovien (MDP). L\'agent utilise l\'algorithme d\'itération par valeurs pour optimiser sa stratégie de collecte d\'or tout en évitant les monstres et obstacles dans un environnement stochastique.',
                    'technologies': ['Python', 'Markov Decision Process', 'Value Iteration', 'Reinforcement Learning', 'AI Planning', 'Stochastic Environment', 'Game Theory'],
                    'images': [
                        get_media_url('wumpus_world_1.jpg', 'projects'),
                        get_media_url('wumpus_world_2.jpg', 'projects'),
                        get_media_url('wumpus_world_3.jpg', 'projects'),
                    ],
                    'main_image': get_media_url('wumpus_world_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/WumpusWorldMDP.git',
                    'category': 'ai',
                },
                {
                    'id': 15,
                    'title': 'Prédiction Immobilière - Algorithme KNN (k-nearest neighbors)',
                    'description': 'Système de prédiction des valeurs de propriétés immobilières utilisant l\'algorithme des k plus proches voisins (KNN). Le programme entraîne un modèle sur des données historiques et prédit les prix de nouvelles propriétés avec calcul d\'erreur quadratique moyenne pour évaluer la précision.',
                    'technologies': ['Python', 'Java', 'C++', 'K-Nearest Neighbors', 'Machine Learning', 'Data Analysis', 'CSV Processing', 'Real Estate Prediction'],
                    'images': [
                        get_media_url('knn_real_estate_1.jpg', 'projects'),
                        get_media_url('knn_real_estate_2.jpg', 'projects'),
                        get_media_url('knn_real_estate_3.jpg', 'projects'),
                    ],
                    'main_image': get_media_url('knn_real_estate_1.jpg', 'projects'),
                    'github': 'https://github.com/MialyAnderson/RealEstatePredictionKNN.git',
                    'category': 'ai',
                }
            ]
        }
    }

@app.route('/')
def index():
    """Page d'accueil du portfolio"""
    data = get_portfolio_data()
    return render_template('index.html', data=data)

@app.route('/api/experience')
def get_experience():
    """API pour récupérer l'expérience professionnelle"""
    data = get_portfolio_data()
    return jsonify(data['experience'])

@app.route('/api/projects')
def get_projects():
    """API pour récupérer tous les projets"""
    data = get_portfolio_data()
    return jsonify(data['projects'])

@app.route('/api/projects/<category>')
def get_projects_by_category(category):
    """API pour récupérer les projets d'une catégorie"""
    data = get_portfolio_data()
    projects = data['projects'].get(category, [])
    return jsonify(projects)

@app.route('/api/project/<int:project_id>')
def get_project(project_id):
    """API pour récupérer un projet spécifique"""
    data = get_portfolio_data()
    project = None
    
    # Chercher dans toutes les catégories
    for category_projects in data['projects'].values():
        for p in category_projects:
            if p['id'] == project_id:
                project = p
                break
        if project:
            break
    
    if project:
        return jsonify(project)
    return jsonify({'error': 'Project not found'}), 404

@app.route('/api/project/<int:project_id>/media')
def get_project_media(project_id):
    """API pour récupérer tous les médias d'un projet"""
    data = get_portfolio_data()
    project = None
    
    # Chercher dans toutes les catégories
    for category_projects in data['projects'].values():
        for p in category_projects:
            if p['id'] == project_id:
                project = p
                break
        if project:
            break
    
    if project:
        media = {
            'images': project.get('images', []),
            'videos': project.get('videos', []),
            'main_image': project.get('main_image')
        }
        return jsonify(media)
    return jsonify({'error': 'Project not found'}), 404

@app.route('/api/featured-projects')
def get_featured_projects():
    """API pour récupérer les projets mis en avant"""
    data = get_portfolio_data()
    featured = []
    
    for category_projects in data['projects'].values():
        for project in category_projects:
            if project.get('featured', False):
                featured.append(project)
    
    return jsonify(featured)

@app.route('/api/contact', methods=['POST'])
def contact():
    """API pour traiter les messages de contact"""
    data = request.json
    
    required_fields = ['name', 'email', 'message']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Champs requis manquants'}), 400
    
    # Sauvegarder le message
    save_contact_message(data)
    
    # Log pour le développement
    print(f"Nouveau message de {data['name']} ({data['email']}): {data['message']}")
    
    return jsonify({
        'success': True,
        'message': 'Votre message a été envoyé avec succès!'
    })

@app.route('/upload-media', methods=['POST'])
def upload_media():
    """Route pour uploader des fichiers média"""
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Déterminer le dossier de destination
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
    """Route pour servir les fichiers média"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/admin')
def admin():
    """Interface d'administration simple pour gérer les médias"""
    # Lister tous les fichiers média
    media_files = {
        'projects': [],
        'profile': [],
        'videos': []
    }
    
    for folder in media_files.keys():
        folder_path = f'static/media/{folder}'
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                if allowed_file(filename):
                    media_files[folder].append({
                        'filename': filename,
                        'url': url_for('static', filename=f'media/{folder}/{filename}'),
                        'type': 'video' if is_video_file(filename) else 'image'
                    })
    
    return render_template('admin.html', media_files=media_files)

# Context processor pour les templates
@app.context_processor
def utility_processor():
    """Injecte des fonctions utiles dans tous les templates"""
    return dict(
        get_media_url=get_media_url,
        is_video_file=is_video_file
    )

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)