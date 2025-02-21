# backend/app/models/association_tables.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from backend.app.db.database import Base

# Table d'association pour la relation entre cartes et boosters
booster_cards = Table(
    'booster_cards', Base.metadata,
    Column('booster_id', Integer, ForeignKey('boosters.id'), primary_key=True),
    Column('card_id', Integer, ForeignKey('cards.id'), primary_key=True)
)

# Table d'association pour la relation entre cartes et collections
collection_cards = Table(
    'collection_cards', Base.metadata,
    Column('card_id', Integer, ForeignKey('cards.id'), primary_key=True),
    Column('collection_id', Integer, ForeignKey('collections.id'), primary_key=True)
)
