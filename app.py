from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")
IS_POSTGRES = bool(DATABASE_URL)

# =========================
# CONEXÃO COM BANCO
# =========================
def get_db():
    if IS_POSTGRES:
        import psycopg
        from psycopg.rows import dict_row
        conn = psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row
        )
        conn.autocommit = True
        return conn
    else:
        import sqlite3
        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        return conn


# =========================
# INIT DB (SÓ LOCAL)
# =========================
def init_db():
    with get_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            setor TEXT NOT NULL,
            ultimo_preco REAL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            quantidade REAL DEFAULT 1,
            preco REAL DEFAULT 0,
            comprado INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)

# =========================
# INIT DB SEMPRE (LOCAL E RAILWAY)
# =========================
try:
    init_db()
    print("Banco inicializado com sucesso")
except Exception as e:
    print("Erro ao inicializar banco:", e)


# =========================
# ROTAS
# =========================
@app.route("/")
def home():
    with get_db() as db:
        produtos = db.execute("""
            SELECT *
            FROM produtos
            ORDER BY setor, nome
        """).fetchall()
    return render_template("home.html", produtos=produtos, page="home")


@app.route("/add", methods=["POST"])
def add_item():
    nome = request.form["produto"]
    quantidade = float(request.form["quantidade"])
    preco = float(request.form["preco"])

    with get_db() as db:
        produto = db.execute(
            "SELECT id FROM produtos WHERE nome=?",
            (nome,)
        ).fetchone()

        if not produto:
            db.execute(
                "INSERT INTO produtos (nome, setor, ultimo_preco) VALUES (?, ?, ?)",
                (nome, "Geral", preco)
            )
            produto_id = db.execute(
                "SELECT id FROM produtos WHERE nome=?",
                (nome,)
            ).fetchone()["id"]
        else:
            produto_id = produto["id"]
            db.execute(
                "UPDATE produtos SET ultimo_preco=? WHERE id=?",
                (preco, produto_id)
            )

        db.execute(
            "INSERT INTO compras (produto_id, quantidade, preco) VALUES (?, ?, ?)",
            (produto_id, quantidade, preco)
        )

    return redirect("/")


@app.route("/toggle/<int:id>")
def toggle_item(id):
    with get_db() as db:
        db.execute(
            "UPDATE compras SET comprado = CASE comprado WHEN 1 THEN 0 ELSE 1 END WHERE id=?",
            (id,)
        )
    return redirect(url_for("home"))


@app.route("/carrinho")
def carrinho():
    with get_db() as db:
        itens = db.execute("""
            SELECT *
            FROM compras
            WHERE comprado=1
            ORDER BY created_at DESC
        """).fetchall()
    return render_template("carrinho.html", itens=itens)


@app.route("/produto", methods=["POST"])
def salvar_produto():
    nome = request.form["nome"]
    preco = float(request.form["preco"])
    setor = request.form["setor"]

    with get_db() as db:
        produto = db.execute(
            "SELECT id FROM produtos WHERE nome=?",
            (nome,)
        ).fetchone()

        if produto:
            db.execute(
                "UPDATE produtos SET ultimo_preco=?, setor=? WHERE id=?",
                (preco, setor, produto["id"])
            )
        else:
            db.execute(
                "INSERT INTO produtos (nome, setor, ultimo_preco) VALUES (?, ?, ?)",
                (nome, setor, preco)
            )

    return redirect("/")


@app.route("/produto/excluir", methods=["POST"])
def excluir_produto():
    data = request.get_json()
    with get_db() as db:
        db.execute("DELETE FROM produtos WHERE id=?", (data["id"],))
    return {"status": "ok"}


@app.route("/update_preco/<int:id>", methods=["POST"])
def update_preco(id):
    novo_preco = float(request.form["preco"])
    with get_db() as db:
        db.execute(
            "UPDATE compras SET preco=? WHERE id=?",
            (novo_preco, id)
        )
    return redirect("/")


# =========================
# START
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

