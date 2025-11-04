# api/routes.py
from flask import request
from flask_restful import Resource, abort
from marshmallow import Schema, fields, ValidationError

from . import api
import controlador_juegos
from models import Juego  # para reconocer instancias de SQLAlchemy


# ---------- Serialización ----------
def juego_to_dict(row):
    if row is None:
        return None

    # 1) Instancia SQLAlchemy
    if isinstance(row, Juego):
        return {
            "id": row.id,
            "nombre": row.nombre,
            "descripcion": row.descripcion,
            "precio": float(row.precio) if row.precio is not None else None,
        }

    # 2) Diccionario
    if isinstance(row, dict):
        return {
            "id": row.get("id"),
            "nombre": row.get("nombre"),
            "descripcion": row.get("descripcion"),
            "precio": float(row.get("precio")) if row.get("precio") is not None else None,
        }

    # 3) Tupla/lista
    if isinstance(row, (list, tuple)) and len(row) >= 4:
        return {
            "id": row[0],
            "nombre": row[1],
            "descripcion": row[2],
            "precio": float(row[3]) if row[3] is not None else None,
        }

    # 4) Fallback
    return {"id": None, "nombre": None, "descripcion": None, "precio": None}


def juegos_to_list(rows):
    return [juego_to_dict(r) for r in rows] if rows else []


# ---------- Validación entrada ----------
class JuegoInSchema(Schema):
    nombre = fields.String(required=True)
    descripcion = fields.String(required=True)
    precio = fields.Float(required=True)


in_schema = JuegoInSchema()


# ---------- Recursos ----------
class JuegoListResource(Resource):
    def get(self):
        """Lista todos los juegos
        ---
        tags:
          - Juegos
        responses:
          200:
            description: Lista de juegos en formato JSON
            schema:
              type: array
              items:
                type: object
                properties:
                  id: {type: integer}
                  nombre: {type: string}
                  descripcion: {type: string}
                  precio: {type: number}
        """
        lista = controlador_juegos.obtener_juegos()  # -> [Juego, Juego, ...]
        return juegos_to_list(lista), 200

    def post(self):
        """Crea un nuevo juego
        ---
        tags:
          - Juegos
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required: [nombre, descripcion, precio]
              properties:
                nombre: {type: string}
                descripcion: {type: string}
                precio: {type: number}
        responses:
          201:
            description: Juego creado correctamente
            schema:
              type: object
              properties:
                id: {type: integer}
                nombre: {type: string}
                descripcion: {type: string}
                precio: {type: number}
          400:
            description: Datos inválidos
        """
        try:
            data = in_schema.load(request.get_json(force=True))
        except ValidationError as err:
            abort(400, message=err.messages)

        controlador_juegos.insertar_juego(
            data["nombre"], data["descripcion"], data["precio"]
        )
        nuevo = Juego.query.order_by(Juego.id.desc()).first()
        return juego_to_dict(nuevo), 201


class JuegoResource(Resource):
    def get(self, id):
        """Obtiene un juego por ID
        ---
        tags:
          - Juegos
        parameters:
          - name: id
            in: path
            required: true
            type: integer
        responses:
          200:
            description: OK
            schema:
              type: object
              properties:
                id: {type: integer}
                nombre: {type: string}
                descripcion: {type: string}
                precio: {type: number}
          404:
            description: No encontrado
        """
        juego = controlador_juegos.obtener_juego_por_id(id)
        if not juego:
            abort(404, message="Juego no encontrado")
        return juego_to_dict(juego), 200

    def put(self, id):
        """Actualiza un juego por ID
        ---
        tags:
          - Juegos
        consumes:
          - application/json
        parameters:
          - name: id
            in: path
            required: true
            type: integer
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                nombre: {type: string}
                descripcion: {type: string}
                precio: {type: number}
        responses:
          200:
            description: Actualizado
          400:
            description: Datos inválidos
          404:
            description: No encontrado
        """
        juego = controlador_juegos.obtener_juego_por_id(id)
        if not juego:
            abort(404, message="Juego no encontrado")

        payload = request.get_json(force=True) or {}
        nombre = payload.get("nombre", juego.nombre)
        descripcion = payload.get("descripcion", juego.descripcion)
        precio = payload.get("precio", juego.precio)
        try:
            if precio is not None:
                precio = float(precio)
        except Exception:
            abort(400, message={"precio": ["Debe ser numérico"]})

        controlador_juegos.actualizar_juego(nombre, descripcion, precio, id)
        actualizado = controlador_juegos.obtener_juego_por_id(id)
        return juego_to_dict(actualizado), 200

    def delete(self, id):
        """Elimina un juego por ID
        ---
        tags:
          - Juegos
        parameters:
          - name: id
            in: path
            required: true
            type: integer
        responses:
          204:
            description: Eliminado
          404:
            description: No encontrado
        """
        juego = controlador_juegos.obtener_juego_por_id(id)
        if not juego:
            abort(404, message="Juego no encontrado")

        controlador_juegos.eliminar_juego(id)
        return "", 204


# Registro de recursos
api.add_resource(JuegoListResource, "/juegos")
api.add_resource(JuegoResource, "/juegos/<int:id>")
