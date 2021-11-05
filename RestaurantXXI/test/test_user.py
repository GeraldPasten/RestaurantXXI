from apps.usuario.models import Usuario
import pytest


@pytest.fixture
def user_creation():
    return Usuario(
        username ='Gerald',
        email = 'Gerald.pastenn@gmail.com',
        nombres ='Mauricio gerald',
        password ='admin'
    )



#Pruebas sin fallos
@pytest.mark.django_db

def test_creacion_usuario():
    usuario = Usuario.objects.create_user(
        username = 'bobby',
        email = 'bobby@gmail.com',
        password = 'admin',
        nombres = 'bobby jackson',
        is_staff = True
    )
    assert usuario.username == 'bobby'


@pytest.mark.django_db
def test_staff_usuario():
    usuario = Usuario.objects.create_user(
        username = 'bobby',
        email = 'bobby@gmail.com',
        nombres = 'bobby jackson',
        password = 'admin',
        is_staff= True
    )
    assert usuario.is_staff


@pytest.mark.django_db
def test_creacion_susperuser():
    usuario = Usuario.objects