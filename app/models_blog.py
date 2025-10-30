from .extensions import db
from .models_blog import BaseModel

class Blog(BaseModel):
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    comment = db.Column(db.Text(), nullable=True)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Blog {self.title} for {self.author.username}>'