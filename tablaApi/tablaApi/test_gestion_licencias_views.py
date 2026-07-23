from types import SimpleNamespace
from contextlib import nullcontext

from rest_framework.test import APIRequestFactory, force_authenticate

from tablaApi.models import Ofimatica1
import tablaApi.serializer_GestionLicencias.views as gestion_views
from tablaApi.serializer_GestionLicencias.views import LicenciaViewSet


class FakeEquipo:
    def __init__(self, nombre_equipo, **kwargs):
        self.nombre_equipo = nombre_equipo
        self.usuario = kwargs.get("usuario", "")
        self.software = kwargs.get("software", "")
        self.propietario = kwargs.get("propietario", "")
        self.sede = kwargs.get("sede", "")
        self.ciudad = kwargs.get("ciudad", "")
        self.ticket_asignacion = kwargs.get("ticket_asignacion")
        self.ticket_traslado = kwargs.get("ticket_traslado")
        self.ticket_retiro = kwargs.get("ticket_retiro")
        self.fecha = kwargs.get("fecha", "")
        self.nueva = kwargs.get("nueva", "")
        self.estado = kwargs.get("estado", "")
        self.notes = kwargs.get("notes")
        self.saved = False

    def save(self):
        self.saved = True


class FakeManager:
    def __init__(self, equipos):
        self.equipos = equipos

    def get(self, **kwargs):
        nombre_equipo = kwargs["nombre_equipo"]
        try:
            return self.equipos[nombre_equipo]
        except KeyError as exc:
            raise Ofimatica1.DoesNotExist from exc

    def select_for_update(self):
        return self


def post_view(action_name, payload, user_role="licenciamiento"):
    request = APIRequestFactory().post("/", payload, format="json")
    user = SimpleNamespace(is_authenticated=True, rol=user_role)
    force_authenticate(request, user=user)
    view = LicenciaViewSet.as_view({"post": action_name})
    return view(request)


def test_asignar_updates_equipo_and_appends_audit_note(monkeypatch):
    equipo = FakeEquipo("PC-001")
    monkeypatch.setattr(Ofimatica1, "objects", FakeManager({"PC-001": equipo}))

    response = post_view("asignar", {
        "nombre_equipo": "PC-001",
        "usuario": "usuario.final",
        "software": "Office",
        "propietario": "IT",
        "sede": "Bogota",
        "ciudad": "Bogota",
        "ticket_asignacion": "TK-100",
        "usuario_licenciamiento": "analista",
    })

    assert response.status_code == 200
    assert equipo.saved is True
    assert equipo.usuario == "usuario.final"
    assert equipo.software == "Office"
    assert equipo.ticket_asignacion == "-TK-100"
    assert equipo.estado == "Asignada"
    assert equipo.notes == "-A-Office-TKTK-100-analista"


def test_recuperar_clears_user_and_marks_license_recovered(monkeypatch):
    equipo = FakeEquipo("PC-001", usuario="usuario.final", notes="hist")
    monkeypatch.setattr(Ofimatica1, "objects", FakeManager({"PC-001": equipo}))

    response = post_view("recuperar", {
        "nombre_equipo": "PC-001",
        "software": "Office",
        "ticket_retiro": "TK-101",
        "usuario_licenciamiento": "analista",
    })

    assert response.status_code == 200
    assert equipo.saved is True
    assert equipo.usuario == ""
    assert equipo.ticket_retiro == "-TK-101"
    assert equipo.estado == "Recuperada"
    assert equipo.notes == "hist-R-Office-TKTK-101-analista"


def test_trasladar_moves_license_between_equipment(monkeypatch):
    origen = FakeEquipo(
        "PC-001",
        software="Office",
        propietario="IT",
        sede="Bogota",
        ciudad="Bogota",
        estado="Asignada",
        notes="origen",
    )
    destino = FakeEquipo("PC-002", notes="destino")
    monkeypatch.setattr(
        Ofimatica1,
        "objects",
        FakeManager({"PC-001": origen, "PC-002": destino}),
    )
    monkeypatch.setattr(gestion_views.transaction, "atomic", lambda: nullcontext())

    response = post_view("trasladar", {
        "equipo_origen": "PC-001",
        "equipo_destino": "PC-002",
        "ticket": "TK-102",
        "usuario_destino": "nuevo.usuario",
        "usuario_licenciamiento": "analista",
    })

    assert response.status_code == 200
    assert origen.saved is True
    assert destino.saved is True
    assert origen.estado == "Trasladada"
    assert origen.ticket_traslado == "-TK-102"
    assert destino.usuario == "nuevo.usuario"
    assert destino.software == "Office"
    assert destino.estado == "Asignada"
    assert destino.ticket_asignacion == "TK-102"


def test_trasladar_rejects_same_origin_and_destination():
    response = post_view("trasladar", {
        "equipo_origen": "PC-001",
        "equipo_destino": "PC-001",
        "ticket": "TK-102",
        "usuario_destino": "nuevo.usuario",
        "usuario_licenciamiento": "analista",
    })

    assert response.status_code == 400
    assert response.data["mensaje"] == "Origen y destino no pueden ser iguales"


def test_trasladar_rejects_origin_without_active_license(monkeypatch):
    origen = FakeEquipo("PC-001", software="", estado="Recuperada")
    destino = FakeEquipo("PC-002")
    monkeypatch.setattr(
        Ofimatica1,
        "objects",
        FakeManager({"PC-001": origen, "PC-002": destino}),
    )
    monkeypatch.setattr(gestion_views.transaction, "atomic", lambda: nullcontext())

    response = post_view("trasladar", {
        "equipo_origen": "PC-001",
        "equipo_destino": "PC-002",
        "ticket": "TK-102",
        "usuario_destino": "nuevo.usuario",
        "usuario_licenciamiento": "analista",
    })

    assert response.status_code == 400
    assert response.data["mensaje"] == "El origen no tiene licencia activa"


def test_licenciamiento_actions_require_allowed_role():
    response = post_view("asignar", {
        "nombre_equipo": "PC-001",
        "usuario": "usuario.final",
        "software": "Office",
        "propietario": "IT",
        "sede": "Bogota",
        "ciudad": "Bogota",
        "ticket_asignacion": "TK-100",
        "usuario_licenciamiento": "analista",
    }, user_role="consulta")

    assert response.status_code == 403
