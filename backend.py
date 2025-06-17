from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados (ajuste conforme necessário)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost:3306/projeto_web'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_pyfile('config.py')


db = SQLAlchemy(app)

# === MODELOS ===
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date = db.Column(db.String(20))
    author = db.Column(db.String(255))  # NOVO CAMPO
    image = db.Column(db.String(500))  # Novo campo
    video = db.Column(db.String(500))  # Novo campo

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'date': self.date,
            'author': self.author,
            'image': self.image,
            'video': self.video
        }



class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'date': self.date
        }
    
class GalleryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    description = db.Column(db.Text)
    image = db.Column(db.String(500))
    video = db.Column(db.String(500))

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'description': self.description,
            'image': self.image,
            'video': self.video
        }



# === AUTENTICAÇÃO SIMPLES ===
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'
SESSIONS = set()

def require_auth(func):
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({'error': 'Unauthorized'}), 401
        token = auth.split(' ')[1]
        if token not in SESSIONS:
            return jsonify({'error': 'Unauthorized'}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == ADMIN_USERNAME and data.get('password') == ADMIN_PASSWORD:
        token = str(uuid.uuid4())
        SESSIONS.add(token)
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

# === NEWS ===
@app.route('/api/news', methods=['GET'])
def get_news():
    news = News.query.order_by(News.date.desc()).all()
    return jsonify([n.to_dict() for n in news])

@app.route('/api/news', methods=['POST'])
@require_auth
def add_news():
    data = request.json
    item = News(
    title=data['title'],
    content=data['content'],
    date=data['date'],
    author=data['author'],
    image=data.get('image'),
    video=data.get('video'))

    db.session.add(item)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/news/<int:item_id>', methods=['DELETE'])
@require_auth
def delete_news(item_id):
    item = News.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'success': True})

# === EVENTS ===
@app.route('/api/events', methods=['GET'])
def get_events():
    events = Event.query.order_by(Event.date.desc()).all()
    return jsonify([e.to_dict() for e in events])

@app.route('/api/events', methods=['POST'])
@require_auth
def add_event():
    data = request.json
    item = Event(title=data['title'], content=data['content'], date=data['date'])
    db.session.add(item)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/events/<int:item_id>', methods=['DELETE'])
@require_auth
def delete_event(item_id):
    item = Event.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    items = GalleryItem.query.order_by(GalleryItem.date.desc()).all()
    return jsonify([i.to_dict() for i in items])

@app.route('/api/gallery', methods=['POST'])
@require_auth
def add_gallery():
    data = request.json
    item = GalleryItem(
        date=data['date'],
        description=data['description'],
        image=data.get('image', ''),
        video=data.get('video', '')
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/gallery/<int:item_id>', methods=['DELETE'])
@require_auth
def delete_gallery(item_id):
    item = GalleryItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'success': True})

# === RODAR SERVIDOR ===
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # cria tabelas se não existirem
    app.run(debug=True)
