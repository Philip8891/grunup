import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from mikrozold import session, Product, Order, Task, compute_schedule, PHASE_ORDER

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Főoldal
@app.route("/")
def index():
    return render_template("index.html")

# Új termék hozzáadása
@app.route("/create-product", methods=["GET", "POST"])
def create_product_route():
    if request.method == "POST":
        try:
            name = request.form["name"].lower()
            csirazas_ido = int(request.form["csirazas_ido"])
            ataztasi_ido = int(request.form["ataztasi_ido"])
            sotet_fazas = int(request.form["sotet_fazas"])
            fenye_alatti_ido = int(request.form["fenye_alatti_ido"])
            mag_szukseglet = float(request.form["mag_szukseglet"])
            new_prod = Product(
                name=name,
                csirazas_ido=csirazas_ido,
                ataztasi_ido=ataztasi_ido,
                sotet_fazas=sotet_fazas,
                fenye_alatti_ido=fenye_alatti_ido,
                mag_szukseglet=mag_szukseglet
            )
            session.add(new_prod)
            session.commit()
            flash("Termék sikeresen hozzáadva!", "success")
            return redirect(url_for("order"))
        except (ValueError, SQLAlchemyError):
            session.rollback()
            flash("Hiba történt a termék hozzáadásakor!", "error")
            return redirect(url_for("create_product_route"))
    return render_template("create_product.html")

# Új rendelés felvétele
@app.route("/order", methods=["GET", "POST"])
def order():
    if request.method == "POST":
        rendeles_id = request.form["rendeles_id"]
        partner = request.form["partner"]
        partner_szam = request.form["partner_szam"]
        szallitas_str = request.form["szallitas"]
        try:
            szallitas = datetime.strptime(szallitas_str, "%Y.%m.%d. %H:%M")
        except ValueError:
            flash("Hibás dátum formátum!", "error")
            return redirect(url_for("order"))
        mennyiseg = int(request.form["mennyiseg"])
        product_id = int(request.form["product_id"])
        # Használjuk a Session.get() metódust
        prod = session.get(Product, product_id)
        if not prod:
            flash("Nem található termék!", "error")
            return redirect(url_for("order"))
        schedule = compute_schedule(prod, mennyiseg, szallitas)
        new_order = Order(
            rendeles_id=rendeles_id,
            partner=partner,
            partner_szam=partner_szam,
            product_id=prod.id,
            mennyiseg=mennyiseg,
            szallitas=szallitas
        )
        session.add(new_order)
        session.commit()
        for phase in PHASE_ORDER:
            scheduled_time = schedule.get(phase)
            if scheduled_time:
                new_task = Task(order_id=new_order.id, task_name=phase, scheduled_time=scheduled_time)
                session.add(new_task)
        session.commit()
        flash("Rendelés mentve!", "success")
        return render_template("order.html", schedule=schedule, rendeles_id=rendeles_id, partner=partner, partner_szam=partner_szam, prod=prod)
    else:
        products = session.query(Product).all()
        if not products:
            flash("Nincs termék az adatbázisban! Először add hozzá az új terméket.", "error")
            return redirect(url_for("create_product_route"))
        return render_template("order.html", products=products)

# Termék módosítása
@app.route("/modify-product", methods=["GET", "POST"])
def modify_product_route():
    if request.method == "POST":
        product_id = int(request.form["product_id"])
        prod = session.get(Product, product_id)
        if not prod:
            flash("Termék nem található!", "error")
            return redirect(url_for("modify_product_route"))
        try:
            prod.csirazas_ido = int(request.form["csirazas_ido"])
            prod.ataztasi_ido = int(request.form["ataztasi_ido"])
            prod.sotet_fazas = int(request.form["sotet_fazas"])
            prod.fenye_alatti_ido = int(request.form["fenye_alatti_ido"])
            prod.mag_szukseglet = float(request.form["mag_szukseglet"])
            session.commit()
            flash("Termékadatok frissítve.", "success")
        except (ValueError, SQLAlchemyError):
            session.rollback()
            flash("Hiba történt a módosítás során.", "error")
        return redirect(url_for("modify_product_route"))
    else:
        products = session.query(Product).all()
        return render_template("modify_product.html", products=products)

# Napi feladatlista – dátumválasztás input type="date", nyomtatható változat
@app.route("/daily-tasks", methods=["GET", "POST"])
def daily_tasks():
    tasks = []
    selected_date = None
    if request.method == "POST":
        date_str = request.form["date"]
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Hibás dátum formátum!", "error")
            return redirect(url_for("daily_tasks"))
        tasks = session.query(Task).filter(
            Task.scheduled_time.between(
                datetime.combine(selected_date, datetime.min.time()),
                datetime.combine(selected_date, datetime.max.time())
            )
        ).all()
    return render_template("tasks.html", tasks=tasks, task_type="napi", selected_date=selected_date)

# Heti feladatlista – két dátumválasztó (kezdő és záró dátum), napokra csoportosítva, nyomtatható változat
@app.route("/weekly-tasks", methods=["GET", "POST"])
def weekly_tasks():
    tasks_by_day = {}
    start_date = None
    end_date = None
    if request.method == "POST":
        start_date_str = request.form["start_date"]
        end_date_str = request.form["end_date"]
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Hibás dátum formátum!", "error")
            return redirect(url_for("weekly_tasks"))
        if end_date < start_date:
            flash("A záró dátum nem lehet korábbi, mint a kezdő dátum!", "error")
            return redirect(url_for("weekly_tasks"))
        tasks = session.query(Task).filter(
            Task.scheduled_time.between(
                datetime.combine(start_date, datetime.min.time()),
                datetime.combine(end_date, datetime.max.time())
            )
        ).all()
        for task in tasks:
            task_day = task.scheduled_time.date()
            if task_day not in tasks_by_day:
                tasks_by_day[task_day] = []
            tasks_by_day[task_day].append(task)
    return render_template("tasks.html", tasks_by_day=tasks_by_day, task_type="heti", start_date=start_date, end_date=end_date)

# Rendelések lekérdezése
@app.route("/query-orders", methods=["GET", "POST"])
def query_orders():
    orders = []
    if request.method == "POST":
        rendeles_id = request.form.get("rendeles_id", "").strip()
        partner = request.form.get("partner", "").strip()
        product_name = request.form.get("product_name", "").strip()
        szallitas_date = request.form.get("szallitas_date", "").strip()
        
        query = session.query(Order)
        if rendeles_id:
            query = query.filter(Order.rendeles_id.like(f"%{rendeles_id}%"))
        if partner:
            query = query.filter(Order.partner.like(f"%{partner}%"))
        if product_name:
            query = query.join(Order.product).filter(Product.name.like(f"%{product_name}%"))
        if szallitas_date:
            try:
                date_obj = datetime.strptime(szallitas_date, "%Y-%m-%d").date()
                query = query.filter(
                    Order.szallitas.between(
                        datetime.combine(date_obj, datetime.min.time()),
                        datetime.combine(date_obj, datetime.max.time())
                    )
                )
            except ValueError:
                flash("Hibás dátum formátum a szállítás dátum szűréshez!", "error")
        orders = query.all()
    return render_template("query_orders.html", orders=orders)

# Rendelés részleteinek megtekintése – Session.get() metódus használatával
@app.route("/order-detail/<int:order_id>")
def order_detail(order_id):
    order = session.get(Order, order_id)
    if not order:
        flash("Rendelés nem található!", "error")
        return redirect(url_for("query_orders"))
    tasks = order.tasks
    return render_template("order_detail.html", order=order, tasks=tasks)

# Az alkalmazás IPv4 címen, 5000-es porton való futtatása
if __name__ == "__main__":
    app.run(host="159.223.5.81", port=5000, debug=True)
