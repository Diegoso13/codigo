from types import SimpleNamespace

from rest_framework.test import APIRequestFactory, force_authenticate

from tablaApi.models import Ciudad, Ofimatica1, Propietario, Sede, Software
from tablaApi.serializer_BusquedaEquipos.views import (
    api_buscar_equipo,
    api_exportar_todo,
    buscar_equipos,
    licencia_equipo,
)
from tablaApi.serializer_Catalogos.views import (
    lista_ciudades,
    lista_propietarios,
    lista_sedes,
    lista_software,
)
from tablaApi.serializer_EdicionEquipos.views import EquipoViewSet


class FakeQuerySet(list):
    def order_by(self, field_name):
        return FakeQuerySet(sorted(self, key=lambda item: getattr(item, field_name)))

    def filter(self, **kwargs):
        value = kwargs["nombre_equipo__icontains"]
        return FakeQuerySet([
            item for item in self
            if value.lower() in item.nombre_equipo.lower()
        ])

    def all(self):
        return self


class FakeManager:
    def __init__(self, rows):
        self.rows = FakeQuerySet(rows)

    def all(self):
        return self.rows

    def order_by(self, field_name):
        return self.rows.order_by(field_name)

    def filter(self, **kwargs):
        return self.rows.filter(**kwargs)

    def get(self, **kwargs):
        nombre_equipo = kwargs["nombre_equipo"]
        for row in self.rows:
            if row.nombre_equipo == nombre_equipo:
                return row
        raise Ofimatica1.DoesNotExist


def get_request(path="/", user_role="admin"):
    request = APIRequestFactory().get(path)
    user = SimpleNamespace(is_authenticated=True, rol=user_role)
    force_authenticate(request, user=user)
    return request


def post_view(action_name, payload, user_role="licenciamiento"):
    request = APIRequestFactory().post("/", payload, format="json")
    user = SimpleNamespace(is_authenticated=True, rol=user_role)
    force_authenticate(request, user=user)
    view = EquipoViewSet.as_view({"post": action_name})
    return view(request)


def test_buscar_equipos_returns_first_ten_matches(monkeypatch):
    rows = [
        Ofimatica1(id=i, nombre_equipo=f"PC-{i:03}")
        for i in range(12)
    ]
    monkeypatch.setattr(Ofimatica1, "objects", FakeManager(rows))

    response = buscar_equipos(get_request("/?q=PC"))

    assert response.status_code == 200
    assert len(response.data) == 10
    assert response.data[0]["nombre_equipo"] == "PC-000"


def test_licencia_equipo_returns_license_detail(monkeypatch):
    row = Ofimatica1(
        nombre_equipo="PC-001",
        software="Office",
        propietario="IT",
        sede="Bogota",
        ciudad="Bogota",
        estado="Asignada",
    )
    monkeypatch.setattr(Ofimatica1, "objects", FakeManager([row]))

    response = licencia_equipo(get_request("/?equipo=PC-001"))

    assert response.status_code == 200
    assert response.data["software"] == "Office"
    assert response.data["estado"] == "Asignada"


def test_api_buscar_equipo_blocks_consulta_download(monkeypatch):
    monkeypatch.setattr(Ofimatica1, "objects", FakeManager([]))

    response = api_buscar_equipo(get_request("/", user_role="consulta"))

    assert response.status_code == 403


def test_api_exportar_todo_requires_authorized_role(monkeypatch):
    monkeypatch.setattr(Ofimatica1, "objects", FakeManager([]))

    response = api_exportar_todo(get_request("/", user_role="mesa"))

    assert response.status_code == 403


def test_catalogo_list_views_return_ordered_data(monkeypatch):
    monkeypatch.setattr(Software, "objects", FakeManager([
        Software(id=2, nombre="Zoom"),
        Software(id=1, nombre="Office"),
    ]))
    monkeypatch.setattr(Sede, "objects", FakeManager([
        Sede(id=2, nombre="Norte"),
        Sede(id=1, nombre="Centro"),
    ]))
    monkeypatch.setattr(Ciudad, "objects", FakeManager([
        Ciudad(id=2, nombre="Medellin"),
        Ciudad(id=1, nombre="Bogota"),
    ]))
    monkeypatch.setattr(Propietario, "objects", FakeManager([
        Propietario(id=2, nombre="Mesa"),
        Propietario(id=1, nombre="IT"),
    ]))

    assert lista_software(get_request()).data[0]["nombre"] == "Office"
    assert lista_sedes(get_request()).data[0]["nombre"] == "Centro"
    assert lista_ciudades(get_request()).data[0]["nombre"] == "Bogota"
    assert lista_propietarios(get_request()).data[0]["nombre"] == "IT"


def test_edicion_create_saves_default_license_fields(monkeypatch):
    saved = {}

    class FakeSerializer:
        errors = {}

        def __init__(self, data=None, *args, **kwargs):
            self.data = data

        def is_valid(self):
            return True

        def save(self, **kwargs):
            saved.update(kwargs)

    monkeypatch.setattr(EquipoViewSet, "get_serializer", lambda self, data=None: FakeSerializer(data=data))

    response = post_view("create", {"nombre_equipo": "PC-001", "serial": "SER-001"})

    assert response.status_code == 201
    assert saved["usuario"] == ""
    assert saved["software"] == ""
    assert saved["notes"] == ""


def test_edicion_editar_nombre_returns_not_found(monkeypatch):
    monkeypatch.setattr(Ofimatica1, "objects", FakeManager([]))

    response = post_view("editar_nombre", {
        "nombre_actual": "NO-EXISTE",
        "nombre_nuevo": "PC-002",
        "serial_nuevo": "SER-002",
    })

    assert response.status_code == 404
