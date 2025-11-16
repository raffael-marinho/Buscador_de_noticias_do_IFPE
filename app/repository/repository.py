from app.database.database import get_connection

def salvar_noticia(noticia):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO noticias (titulo, html_puro, conteudo, campus, url, coletado_em)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (noticia.titulo, noticia.html_puro, noticia.conteudo, noticia.campus, noticia.url, noticia.coletado_em))

    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id


def buscar_todas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, conteudo, campus, url FROM noticias")
    data = cursor.fetchall()
    conn.close()

    return [
        {"id": row[0], "titulo": row[1], "conteudo": row[2], "campus": row[3], "url": row[4]}
        for row in data
    ]


def buscar_por_id(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, titulo, conteudo, campus, url FROM noticias WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"id": row[0], "titulo": row[1], "conteudo": row[2], "campus": row[3], "url": row[4]}
    return None


def atualizar_noticia(id, campos):
    conn = get_connection()
    cursor = conn.cursor()

    sets = []
    valores = []

    for campo, valor in campos.items():
        if valor is not None:
            sets.append(f"{campo} = ?")
            valores.append(valor)

    if not sets:
        return False

    valores.append(id)
    sql = f"UPDATE noticias SET {', '.join(sets)} WHERE id = ?"

    cursor.execute(sql, valores)

    conn.commit()
    sucesso = cursor.rowcount > 0
    conn.close()

    return sucesso


def deletar_noticia(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM noticias WHERE id = ?", (id,))
    conn.commit()
    sucesso = cursor.rowcount > 0
    conn.close()

    return sucesso
