from types import SimpleNamespace

import pytest
from rest_framework import serializers

from tablaApi.models import Ciudad, Ofimatica1, Propietario, Sede, Software
from tablaApi.serializer_BusquedaEquipos.serializers import (
    EquipoFullSerializer,
    EquipoLicenciaSerializer,
    EquipoSimpleSerializer,
)
from tablaApi.serializer_Catalogos.serializers import (
    CiudadSerializer,
    PropietarioSerializer,
    SedeSerializer,
    SoftwareSerializer,
)
from tablaApi.serializer_EdicionEquipos.serializers import EquipoSerializer
from tablaApi.serializer_GestionLicencias.serializers import (
    AsignarLicenciaSerializer,
    RecuperarLicenciaSerializer,
    TrasladoLicenciaSerializer,
)
from tablaApi.serializer_LogIn.serializers import LoginSerializer


class ExistsResult:
    def __init__(self, value):
        self.value = value

    def exists(self):
        return self.value


class FakeRefresh:
    def __init__(self):
        self.access_token = {}

    def __str__(self):
        return "refresh-token"


def test_gestion_licencias_serializers_accept_valid_payloads():
    asignar = AsignarLicenciaSerializer(data={
        "nombre_equipo": "PC-001",
        "usuario_licenciamiento": "analista",
        "software": "Office",
        "usuario": "usuario.final",
        "propietario": "IT",
        "sede": "Bogota",
        "ciudad": "Bogota",
        "ticket_asignacion": "TK-100",
    })
    recuperar = RecuperarLicenciaSerializer(data={
        "nombre_equipo": "PC-001",
        "software": "Office",
        "ticket_retiro": "TK-101",
        "usuario_licenciamiento": "analista",
    })
    trasladar = TrasladoLicenciaSerializer(data={
        "equipo_origen": "PC-001",
        "equipo_destino": "PC-002",
        "ticket": "TK-102",
        "usuario_destino": "nuevo.usuario",
        "usuario_licenciamiento": "analista",
    })

    assert asignar.is_valid(), asignar.errors
    assert recuperar.is_valid(), recuperar.errors
    assert trasladar.is_valid(), trasladar.errors


@pytest.mark.parametrize("serializer_class, payload, missing_field", [
    (AsignarLicenciaSerializer, {
        "nombre_equipo": "PC-001",
        "usuario_licenciamiento": "analista",
        "software": "Office",
        "usuario": "usuario.final",
        "propietario": "IT",
        "sede": "Bogota",
        "ciudad": "Bogota",
    }, "ticket_asignacion"),
    (RecuperarLicenciaSerializer, {
        "nombre_equipo": "PC-001",
        "software": "Office",
        "usuario_licenciamiento": "analista",
    }, "ticket_retiro"),
    (TrasladoLicenciaSerializer, {
        "equipo_origen": "PC-001",
        "ticket": "TK-102",
        "usuario_destino": "nuevo.usuario",
        "usuario_licenciamiento": "analista",
    }, "equipo_destino"),
])
def test_gestion_licencias_serializers_require_expected_fields(
    serializer_class,
    payload,
    missing_field,
):
    serializer = serializer_class(data=payload)

    assert not serializer.is_valid()
    assert missing_field in serializer.errors


def test_busqueda_serializers_expose_expected_shapes():
    equipo = Ofimatica1(
        id=7,
        nombre_equipo="PC-007",
        software="Office",
        propietario="IT",
        sede="Bogota",
        ciudad="Bogota",
        estado="Asignada",
        serial="SER-007",
    )

    assert EquipoSimpleSerializer(equipo).data == {
        "id": 7,
        "nombre_equipo": "PC-007",
    }
    assert EquipoLicenciaSerializer(equipo).data == {
        "software": "Office",
        "propietario": "IT",
        "sede": "Bogota",
        "ciudad": "Bogota",
        "estado": "Asignada",
    }
    assert EquipoFullSerializer(equipo).data["serial"] == "SER-007"


def test_catalogo_serializers_expose_model_fields():
    assert SoftwareSerializer(Software(id=1, nombre="Office")).data == {
        "id": 1,
        "nombre": "Office",
    }
    assert SedeSerializer(Sede(id=2, nombre="Centro")).data == {
        "id": 2,
        "nombre": "Centro",
    }
    assert CiudadSerializer(Ciudad(id=3, nombre="Bogota")).data == {
        "id": 3,
        "nombre": "Bogota",
    }
    assert PropietarioSerializer(Propietario(id=4, nombre="IT")).data == {
        "id": 4,
        "nombre": "IT",
    }


def test_equipo_serializer_rejects_duplicate_name(monkeypatch):
    monkeypatch.setattr(
        Ofimatica1.objects,
        "filter",
        lambda **kwargs: ExistsResult(kwargs == {"nombre_equipo": "PC-001"}),
    )

    serializer = EquipoSerializer(data={"nombre_equipo": "PC-001", "serial": "SER-001"})

    assert not serializer.is_valid()
    assert "nombre_equipo" in serializer.errors


def test_equipo_serializer_allows_existing_instance_name(monkeypatch):
    monkeypatch.setattr(
        Ofimatica1.objects,
        "filter",
        lambda **kwargs: ExistsResult(True),
    )
    equipo = Ofimatica1(nombre_equipo="PC-001", serial="SER-001")

    serializer = EquipoSerializer(
        equipo,
        data={"nombre_equipo": "PC-001", "serial": "SER-002"},
    )

    assert serializer.is_valid(), serializer.errors


def test_login_serializer_returns_tokens_for_active_user(monkeypatch):
    user = SimpleNamespace(username="admin", rol="admin", is_active=True)
    refresh = FakeRefresh()

    monkeypatch.setattr(
        "tablaApi.serializer_LogIn.serializers.authenticate",
        lambda username, password: user,
    )
    monkeypatch.setattr(
        "tablaApi.serializer_LogIn.serializers.RefreshToken.for_user",
        lambda user: refresh,
    )

    serializer = LoginSerializer(data={"username": "admin", "password": "secret"})

    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["access"] == "{'rol': 'admin'}"
    assert serializer.validated_data["refresh"] == "refresh-token"
    assert serializer.validated_data["rol"] == "admin"


def test_login_serializer_rejects_invalid_credentials(monkeypatch):
    monkeypatch.setattr(
        "tablaApi.serializer_LogIn.serializers.authenticate",
        lambda username, password: None,
    )

    serializer = LoginSerializer(data={"username": "admin", "password": "bad"})

    assert not serializer.is_valid()
    assert isinstance(serializer.errors["non_field_errors"][0], serializers.ErrorDetail)
