from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    people_favorites_associates: Mapped[list['PeopleFavorites']] = relationship(
        back_populates='user', cascade='all, delete-orphan', lazy='joined')
    planet_favorites_associates: Mapped[list['PlanetFavorites']] = relationship(
        back_populates='user', cascade='all, delete-orphan', lazy='joined')

    def __repr__(self):
        return f'Usuario con ID {self.id} y email {self.email}'

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_active': self.is_active
        }


class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    height: Mapped[int] = mapped_column(Integer)
    user_favorite_associates: Mapped[list['PeopleFavorites']] = relationship(
        "PeopleFavorites", back_populates="character", cascade='all, delete-orphan')

    def __repr__(self):
        return f'Personaje con ID {self.id} y de nombre {self.name}'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    size: Mapped[str] = mapped_column(nullable=False)
    user_favorite_associates: Mapped[list['PlanetFavorites']] = relationship(
        "PlanetFavorites", back_populates="planet", cascade='all, delete-orphan')

    def __repr__(self):
        return f'Planeta con ID {self.id} y de nombre {self.name}'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'size': self.size
        }


class PeopleFavorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("people.id"))
    character: Mapped['People'] = relationship(
        "People", back_populates="user_favorite_associates")
    user: Mapped['User'] = relationship(
        "User", back_populates="people_favorites_associates")

    def __repr__(self):
        return f'Usuario de ID {self.user_id} le gusta personaje de ID {self.character_id}'

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'character_id': self.character_id,
        }


class PlanetFavorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped['User'] = relationship(
        "User", back_populates="planet_favorites_associates")
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped['Planet'] = relationship(
        "Planet", back_populates="user_favorite_associates")

    def __repr__(self):
        return f'Usuario de ID {self.user_id} le gusta planeta de ID {self.planet_id}'

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'planet_id': self.planet_id,
        }
