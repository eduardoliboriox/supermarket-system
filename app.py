from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

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
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    );
    """)

    conn.commit()
    return conn

@app.route("/")
def home():
    db = get_db()

    produtos = db.execute("""
        SELECT *
        FROM produtos
        ORDER BY setor, nome
    """).fetchall()

    return render_template(
        "home.html",
        produtos=produtos,
        page="home"
    )


@app.route("/add", methods=["POST"])
def add_item():
    nome = request.form["produto"]
    quantidade = float(request.form["quantidade"])
    preco = float(request.form["preco"])

    db = get_db()

    produto = db.execute(
        "SELECT id FROM produtos WHERE nome=?",
        (nome,)
    ).fetchone()

    if not produto:
        db.execute(
            "INSERT INTO produtos (nome, ultimo_preco) VALUES (?, ?)",
            (nome, preco)
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

    db.execute("""
        INSERT INTO compras (produto_id, quantidade, preco)
        VALUES (?, ?, ?)
    """, (produto_id, quantidade, preco))

    db.commit()
    return redirect("/")


@app.route("/toggle/<int:id>")
def toggle_item(id):
    db = get_db()
    db.execute(
        "UPDATE compras SET comprado = CASE comprado WHEN 1 THEN 0 ELSE 1 END WHERE id=?",
        (id,)
    )
    db.commit()
    return redirect(url_for("home"))

@app.route("/carrinho")
def carrinho():
    db = get_db()
    db.row_factory = sqlite3.Row
    itens = db.execute(
        "SELECT * FROM compras WHERE comprado=1 ORDER BY created_at DESC"
    ).fetchall()
    return render_template("carrinho.html", itens=itens)

@app.route("/produto", methods=["POST"])
def salvar_produto():
    nome = request.form["nome"]
    preco = float(request.form["preco"])
    setor = request.form["setor"]

    db = get_db()

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

    db.commit()
    return redirect("/")

@app.route("/produto/excluir", methods=["POST"])
def excluir_produto():
    data = request.get_json()

    db = get_db()
    db.execute("DELETE FROM produtos WHERE id = ?", (data["id"],))
    db.commit()

    return {"status": "ok"}


@app.route("/update_preco/<int:id>", methods=["POST"])
def update_preco(id):
    novo_preco = float(request.form["preco"])
    db = get_db()

    db.execute(
        "UPDATE compras SET preco=? WHERE id=?",
        (novo_preco, id)
    )

    db.execute("""
        UPDATE produtos
        SET ultimo_preco=?
        WHERE id=(SELECT produto_id FROM compras WHERE id=?)
    """, (novo_preco, id))

    db.commit()
    return redirect("/")

@app.route("/produtos")
def produtos():
    with get_db() as conn:
        produtos = conn.execute("""
            SELECT 
                id,
                nome,
                ultimo_preco AS preco,
                setor AS categoria
            FROM produtos
            ORDER BY setor, nome
        """).fetchall()

    return render_template(
        "produtos.html",
        produtos=produtos,
        page="produtos"
    )

@app.route("/produto/atualizar", methods=["POST"])
def atualizar_produto():
    data = request.get_json()

    produto_id = data["id"]
    nome = data["nome"]
    preco = float(data["preco"])
    categoria = data["categoria"]

    db = get_db()

    db.execute("""
        UPDATE produtos
        SET nome = ?, ultimo_preco = ?, setor = ?
        WHERE id = ?
    """, (nome, preco, categoria, produto_id))

    db.commit()

    return {"status": "ok"}
   
def init_db():
    db = get_db()
    db.close()

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080, debug=True)
