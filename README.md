Mikrozöld-Bot 🚀

A Sentinel-Bot egy Mikrozöld Ütemező Rendszer, amely lehetővé teszi a mikrozöldek termesztési ütemezésének kezelését, rendeléseket, napi és heti feladatlistákat, valamint termékek nyilvántartását és módosítását.A projekt Flask (Python), SQLAlchemy és MySQL alapokon működik, modern webes felülettel.

📌 Funkciók és Képességek

✅ Új rendelés felvétele (automatikus termesztési ütemezéssel)

✅ Termékek kezelése (hozzáadás, módosítás)

✅ Napi és heti feladatlisták (naptár alapú kiválasztással)

✅ Feladatok nyomtatása (böngészőből történő nyomtatási lehetőség)

✅ Rendelések keresése és szűrése (partnerek, termékek, szállítási dátumok szerint)

✅ Rendelés részleteinek megtekintése (az összes kapcsolódó ütemezéssel és feladatokkal)

✅ Modern és reszponzív UI (ikonokkal és könnyen kezelhető felülettel)

🛠 Technológiák

Backend: Python (Flask, SQLAlchemy)

Adatbázis: MySQL (SQLAlchemy ORM-rel kezelve)

Frontend: HTML, CSS, Jinja2, Bootstrap, FontAwesome ikonok

Verziókövetés: Git & GitHub

📂 Projekt Struktúra

sentinel-bot/
├── app.py                # Flask backend és API kezelő
├── mikrozold.py          # Adatbázis modellek és üzleti logika
├── .env                  # Környezeti változók (adatbázis beállítások)
├── .gitignore            # Verziókövetésből kizárt fájlok listája
├── README.md             # Dokumentáció (Ez a fájl)
│
├── templates/            # HTML sablonok (Jinja2)
│   ├── base.html
│   ├── index.html
│   ├── order.html
│   ├── modify_product.html
│   ├── query_orders.html
│   ├── order_detail.html
│   ├── tasks.html
│   ├── create_product.html
│
└── static/               # Stílusfájlok és egyéb statikus elemek
    ├── styles.css

🏗 Telepítés és Futtatás

1️⃣ Git klónozása és belépés a projekt mappájába

git clone https://github.com/FELHASZNALONEV/sentinel-bot.git
cd sentinel-bot

2️⃣ Virtuális környezet létrehozása és aktiválása

python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

3️⃣ Függőségek telepítése

pip install -r requirements.txt

4️⃣ .env fájl beállítása

Hozz létre egy .env fájlt a gyökérkönyvtárban, és add hozzá az adatbázis beállításokat:

DATABASE_URL=mysql+pymysql://root:JELSZÓ@localhost/mikrozold

5️⃣ Adatbázis inicializálása

python mikrozold.py

6️⃣ Alkalmazás futtatása

python app.py

Az alkalmazás futtatása után megnyitható a böngészőben:

http://159.223.5.81:5000

🎯 Használati Útmutató

🔹 Rendelések kezelése

Új rendelés felvétele a termék kiválasztásával és szállítási dátum megadásával.

A rendszer automatikusan kiszámítja a növekedési fázisokat.

A rendeléshez kapcsolódó feladatok megjelennek a napi és heti feladatlistákban.

🔹 Feladatlisták kezelése

Napi feladatlista: Egy adott naphoz kapcsolódó összes feladat lekérdezése.

Heti feladatlista: Egy kezdő és egy záró dátum kiválasztásával több napra vonatkozó feladatok megjelenítése.

Nyomtatási lehetőség: Minden listánál van egy "Nyomtatás" gomb, amely megnyitja a böngésző nyomtatási funkcióját.

🔹 Rendelések keresése

A keresési funkcióval szűrhetünk a rendelési szám, partner neve, termék neve vagy szállítási dátum szerint.

📌 Fejlesztési Irányok

🔄 API végpontok a külső rendszerek integrációjához.

📊 Grafikonok és statisztikák a termesztési folyamatok elemzéséhez.

📦 Automatikus értesítések és e-mail küldés rendelésekről.

📜 Verziókezelés és Fejlesztési Folyamat

A projekt a Git verziókövetőt használja.A legfrissebb verzió mindig elérhető a GitHub repositoryban.

🔹 Új fejlesztések külön ágon történnek (git checkout -b uj_funkcio)

🔹 Commitolás (git commit -m "Új funkció hozzáadva")

🔹 Pusholás (git push origin uj_funkcio)

🔹 Merge a main ágba (git merge uj_funkcio)

🔹 main ágra történő fejlesztések mindig a git pull origin main paranccsal frissíthetők

🤝 Hozzájárulás

Ha fejlesztenél a projekten, forkold le, dolgozz saját ágon, majd küldj be egy Pull Requestet.

📞 Kapcsolat

Ha kérdésed van vagy segítségre van szükséged, nyugodtan írj nekem GitHub-on vagy e-mailben!

🔖 Licenc

Ez a projekt MIT licenc alatt áll, szabadon módosítható és felhasználható.
