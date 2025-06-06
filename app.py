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

# Données du portfolio avec vos informations
def get_portfolio_data():
    return {
        'about': {
            'name': 'Rakotondradano Mialy Anderson',
            'title': 'Développeur Full Stack',
            'description': 'Passionné par le développement web, les jeux vidéo et les nouvelles technologies. Spécialisé en Python, C++, Java et le développement avec Unreal Engine.',
            'email': 'andyrakotondradano@gmail.com',
            'phone': '+1 579 372 6108',
            'location': 'Montréal, QC',
            'profile_image': get_media_url('profile.jpg', 'profile')
        },
        'skills': [
            {'name': 'Python', 'level': 90},
            {'name': 'JavaScript', 'level': 85},
            {'name': 'Java', 'level': 90},
            {'name': 'C', 'level': 75},
            {'name': 'C++', 'level': 90},
            {'name': 'Unreal Engine', 'level': 85},
            {'name': 'Unity Engine', 'level': 90},
            {'name': 'SQL', 'level': 70},
            {'name': 'Git', 'level': 90},
            {'name': 'Flask/Django', 'level': 80},
            {'name': 'HTML/CSS', 'level': 85}
        ],
        'projects': [
            {
                'id': 1,
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
                'github': 'https://github.com/andyrakoto/simulateur-conduite',
                'demo': None
            },
            {
                'id': 2,
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
                'github': 'https://github.com/andyrakoto/jeu-aventure',
                'demo': None
            },
            {
                'id': 3,
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
                'github': 'https://github.com/andyrakoto/aventure3d-unreal',
                'demo': None
            },
            {
                'id': 4,
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
                'github': 'https://github.com/andyrakoto/aventure-openworld',
                'demo': None,
                'status': 'En développement'
            }
        ],
    }

@app.route('/')
def index():
    """Page d'accueil du portfolio"""
    data = get_portfolio_data()
    return render_template('index.html', data=data)

@app.route('/api/projects')
def get_projects():
    """API pour récupérer tous les projets"""
    data = get_portfolio_data()
    return jsonify(data['projects'])

@app.route('/api/projects/<int:project_id>')
def get_project(project_id):
    """API pour récupérer un projet spécifique"""
    data = get_portfolio_data()
    project = next((p for p in data['projects'] if p['id'] == project_id), None)
    if project:
        return jsonify(project)
    return jsonify({'error': 'Project not found'}), 404

@app.route('/api/project/<int:project_id>/media')
def get_project_media(project_id):
    """API pour récupérer tous les médias d'un projet"""
    data = get_portfolio_data()
    project = next((p for p in data['projects'] if p['id'] == project_id), None)
    if project:
        media = {
            'images': project.get('images', []),
            'videos': project.get('videos', []),
            'main_image': project.get('main_image')
        }
        return jsonify(media)
    return jsonify({'error': 'Project not found'}), 404

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

@app.route('/create-placeholders')
def create_placeholders():
    """Crée des images et vidéos de placeholder pour tester"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        placeholders = [
            # Images de projets
            ('projects/simulateur_main.jpg', 'Simulateur\nUnreal Engine', (70, 130, 180)),
            ('projects/simulateur_1.jpg', 'Vue Conduite\nSimulateur', (85, 145, 195)),
            ('projects/simulateur_2.jpg', 'Physique\nChaos Vehicle', (100, 160, 210)),
            ('projects/simulateur_3.jpg', 'Interface\nUtilisateur', (115, 175, 225)),
            
            ('projects/portfolio_main.jpg', 'Portfolio\nFlask', (34, 139, 34)),
            ('projects/portfolio_1.jpg', 'Interface\nResponsive', (49, 154, 49)),
            ('projects/portfolio_2.jpg', 'Animations\nModernes', (64, 169, 64)),
            
            ('projects/farmshop_main.jpg', 'Farmshop\nMadagascar', (220, 20, 60)),
            ('projects/farmshop_1.jpg', 'Gestion\nStocks', (235, 35, 75)),
            ('projects/farmshop_2.jpg', 'Interface\nAdmin', (250, 50, 90)),
            
            # Image de profil
            ('profile/profile.jpg', 'Rakotondradano\nMialy Anderson', (128, 128, 128)),
            
            # Placeholder général
            ('placeholder.jpg', 'Image\nPlaceholder', (169, 169, 169))
        ]
        
        created_files = []
        
        for filename, text, color in placeholders:
            file_path = f'static/media/{filename}'
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Créer une image 400x250 (ou 400x400 pour le profil)
            if 'profile' in filename:
                img = Image.new('RGB', (400, 400), color=color)
            else:
                img = Image.new('RGB', (400, 250), color=color)
            
            draw = ImageDraw.Draw(img)
            
            # Ajouter le texte
            lines = text.split('\n')
            line_height = 30
            total_height = len(lines) * line_height
            start_y = (img.height - total_height) // 2
            
            for i, line in enumerate(lines):
                # Calculer la position pour centrer le texte
                bbox = draw.textbbox((0, 0), line)
                text_width = bbox[2] - bbox[0]
                x = (img.width - text_width) // 2
                y = start_y + i * line_height
                
                draw.text((x, y), line, fill='white')
            
            img.save(file_path)
            created_files.append(filename)
        
        # Créer une vidéo placeholder simple (fichier texte qui simule une vidéo)
        video_placeholder_path = 'static/media/videos/simulateur_demo.mp4'
        os.makedirs(os.path.dirname(video_placeholder_path), exist_ok=True)
        
        # Créer un fichier texte comme placeholder de vidéo
        with open(video_placeholder_path.replace('.mp4', '_placeholder.txt'), 'w') as f:
            f.write("Placeholder pour la vidéo de démonstration du simulateur.\n")
            f.write("Remplacez ce fichier par votre vraie vidéo MP4.\n")
        
        return jsonify({
            'success': True, 
            'message': f'{len(created_files)} fichiers de placeholder créés',
            'files': created_files
        })
        
    except ImportError:
        return jsonify({
            'error': 'PIL/Pillow non installé. Installez avec: pip install Pillow',
            'needed_files': [
                'static/media/projects/simulateur_main.jpg',
                'static/media/projects/portfolio_main.jpg',
                'static/media/projects/farmshop_main.jpg',
                'static/media/profile/profile.jpg',
                'static/media/videos/simulateur_demo.mp4'
            ]
        })

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