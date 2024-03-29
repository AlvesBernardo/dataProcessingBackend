from app.extensions import db
from sqlalchemy.orm import relationship


class Subtitle(db.Model):
    __tablename__ = 'tblSubtitle'
    idSubtitle = db.Column(db.Integer, primary_key=True)
    fiMovie = db.Column(db.Integer, db.ForeignKey("tblMovie.idMovie"))
    movie = relationship("Movie")
    fiLanguage = db.Column(db.Integer, db.ForeignKey("tblLanguage.idLanguage"))
    language = relationship("Language")

    def __repr__(self):
        return '<Subtitle %r>' % self.idSubtitle
