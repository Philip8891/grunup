import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Dict
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

# .env betöltése és DATABASE_URL beolvasása
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise Exception("Nincs beállítva a DATABASE_URL a .env fájlban!")

# SQLAlchemy beállítása
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Állandók
KARTON_KAPACITAS = 6   # Egy karton kapacitása
TALCA_KAPACITAS = 8    # Egy tálca kapacitása
PHASE_ORDER = [
    "Áztatás kezdete",
    "Csírázás kezdete",
    "Sötét fázis kezdete",
    "Fény alatti növekedés kezdete",
    "Betakarítás (Szállítás)"
]

# Adatbázis modellek
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    csirazas_ido = Column(Integer, nullable=False)       # nap
    ataztasi_ido = Column(Integer, nullable=False)       # óra
    sotet_fazas = Column(Integer, nullable=False)        # nap
    fenye_alatti_ido = Column(Integer, nullable=False)   # nap
    mag_szukseglet = Column(Float, nullable=False)       # g/darab

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    rendeles_id = Column(String, nullable=False)
    partner = Column(String, nullable=False)
    partner_szam = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'))
    mennyiseg = Column(Integer, nullable=False)
    szallitas = Column(DateTime, nullable=False)
    product = relationship("Product")
    tasks = relationship("Task", back_populates="order")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    task_name = Column(String, nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    order = relationship("Order", back_populates="tasks")

# Táblák létrehozása, ha még nem léteznek
Base.metadata.create_all(engine)

def format_timedelta(td: timedelta) -> str:
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes = remainder // 60
    parts = []
    if days > 0:
        parts.append(f"{days} nap")
    if hours > 0:
        parts.append(f"{hours} óra")
    if minutes > 0 and days == 0:
        parts.append(f"{minutes} perc")
    return " ".join(parts) if parts else "0 óra"

def compute_schedule(prod: Product, mennyiseg: int, szallitas: datetime) -> Dict:
    # Fázisok visszaszámolása a szállítási dátumtól
    fenyes = szallitas - timedelta(days=prod.fenye_alatti_ido)
    sotet = fenyes - timedelta(days=prod.sotet_fazas)
    csirazas = sotet - timedelta(days=prod.csirazas_ido)
    atazt = csirazas - timedelta(hours=prod.ataztasi_ido)
    teljes = szallitas - atazt
    durations = {
        "Áztatás": csirazas - atazt,
        "Csírázás": sotet - csirazas,
        "Sötét fázis": fenyes - sotet,
        "Fény alatti növekedés": szallitas - fenyes,
    }
    kartonok = (mennyiseg + KARTON_KAPACITAS - 1) // KARTON_KAPACITAS
    talcak = (mennyiseg + TALCA_KAPACITAS - 1) // TALCA_KAPACITAS
    return {
        "Áztatás kezdete": atazt,
        "Csírázás kezdete": csirazas,
        "Sötét fázis kezdete": sotet,
        "Fény alatti növekedés kezdete": fenyes,
        "Betakarítás (Szállítás)": szallitas,
        "Mennyiség": mennyiseg,
        "Kartonok száma": kartonok,
        "Tálcák száma": talcak,
        "Mag szükséglet (g/darab)": prod.mag_szukseglet,
        "Mag szükséglet (g/tálca)": prod.mag_szukseglet * TALCA_KAPACITAS,
        "Mag összesen (g)": mennyiseg * prod.mag_szukseglet,
        "Teljes termesztési idő": teljes,
        "Fázisok időtartama": durations
    }
