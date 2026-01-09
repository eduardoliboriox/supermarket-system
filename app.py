from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")
IS_POSTGRES = DATABASE_URL is not None


# =========================
# CONEXÃO COM BANCO
# =========================
def get_db():
    if IS_POSTGRES:
        import psycopg
        from psycopg.rows import dict_row
        return psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row,
            autocommit=True
        )
    else:
        import sqlite3
        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        return conn


def q(sql):
    return sql if IS_POSTGRES else sql.replace("%s", "?")


# =========================
# INIT DB (LOCAL + RAILWAY)
# =========================
def init_db():
    with get_db() as db:
        if IS_POSTGRES:
            db.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id SERIAL PRIMARY KEY,
                    nome TEXT UNIQUE NOT NULL,
                    setor TEXT NOT NULL,
                    ultimo_preco NUMERIC DEFAULT 0
                )
            """)
            db.execute("""
                CREATE TABLE IF NOT EXISTS compras (
                    id SERIAL PRIMARY KEY,
                    produto_id INTEGER REFERENCES produtos(id) ON DELETE CASCADE,
                    quantidade NUMERIC DEFAULT 1,
                    preco NUMERIC DEFAULT 0,
                    comprado BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        else:
            db.executescript("""
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


# ⚠️ ISSO É O SEGREDO QUE FALTAVA
init_db()


# =========================
# ROTAS
# =========================
@app.route("/")
def home():
    with get_db() as db:
        produtos = db.execute("""
            SELECT * FROM produtos ORDER BY setor, nome
        """).fetchall()
    return render_template("home.html", produtos=produtos, page="home")


@app.route("/add", methods=["POST"])
def add_item():
    nome = request.form["produto"]
    quantidade = float(request.form["quantidade"])
    preco = float(request.form["preco"])

    with get_db() as db:
        produto = db.execute(
            q("SELECT id FROM produtos WHERE nome=%s"),
            (nome,)
        ).fetchone()

        if not produto:
            produto = db.execute(
                q("""
                    INSERT INTO produtos (nome, setor, ultimo_preco)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """),
                (nome, "Geral", preco)
            ).fetchone()
            produto_id = produto["id"]
        else:
            produto_id = produto["id"]
            db.execute(
                q("UPDATE produtos SET ultimo_preco=%s WHERE id=%s"),
                (preco, produto_id)
            )

        db.execute(
            q("""
                INSERT INTO compras (produto_id, quantidade, preco)
                VALUES (%s, %s, %s)
            """),
            (produto_id, quantidade, preco)
        )

    return redirect("/")


@app.route("/toggle/<int:id>")
def toggle_item(id):
    with get_db() as db:
        if IS_POSTGRES:
            db.execute(
                q("UPDATE compras SET comprado = NOT comprado WHERE id=%s"),
                (id,)
            )
        else:
            db.execute(
                q("""
                    UPDATE compras
                    SET comprado = CASE comprado WHEN 1 THEN 0 ELSE 1 END
                    WHERE id=%s
                """),
                (id,)
            )
    return redirect("/")


# =========================
# START
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
