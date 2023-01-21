import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from model_bakery import baker
from students.models import Course, Student
import random


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory

# проверка получения курса
@pytest.mark.django_db
def test_get_course(client, course_factory):
    course_factory(_quantity=1)
    course_instance = Course.objects.all()
    assert Course.objects.count() == 1
    course_id = course_instance[0].id
    response = client.get(f'/api/v1/courses/{course_id}/', format='json')
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == course_id


# проверка получения списка курсов
@pytest.mark.django_db
def test_get_course_list(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/', format='json')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(courses)
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name


# проверка фильтрации списка курсов по id
# + случайный выбор id из результатов фабрики
@pytest.mark.django_db
def test_course_id_filter(client, course_factory):
    course_id_list = []
    course_factory(_quantity=10)
    courses = Course.objects.values()
    # print(courses)
    for i in courses:
        course_id_list.append(i['id'])
    # print()
    # print(course_id_list)
    selected_id = random.choice(course_id_list)
    response = client.get(f'/api/v1/courses/?id={selected_id}', format='json')
    data = response.json()
    # print()
    # print(data)
    assert response.status_code == 200
    assert data[0]['id'] == selected_id


# проверка фильтрации списка курсов по названию
# + случайный выбор имени из результатов фабрики
@pytest.mark.django_db
def test_course_name_filter(client, course_factory):
    course_name_list = []
    course_factory(_quantity=10)
    courses = Course.objects.values()
    for i in courses:
        course_name_list.append(i['name'])
    # print(course_name_list)
    # print()
    selected_name = random.choice(course_name_list)
    # print(selected_name)
    response = client.get(f'/api/v1/courses/?name={selected_name}', format='json')
    data = response.json()
    # print()
    # print(data)
    assert response.status_code == 200
    assert data[0]['name'] == selected_name


# тест успешного создания курса
# + проверка заполнения модели Student и student_factory
@pytest.mark.django_db
def test_create_course(client, student_factory):

    course_students = []
    student_factory(_quantity=10)
    stud = Student.objects.values()
    for i in stud:
        course_students.append(i['id'])
    # print(course_students)
    count = Course.objects.count()
    course = {'name': 'Best Course Ever', 'students': course_students}
    response = client.post('/api/v1/courses/', data=course, format='json')
    data = response.json()
    # print(data)
    assert response.status_code == 201
    assert data['name'] == course['name']
    assert Course.objects.count() == count + 1

# тест успешного обновления курса
@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=1)
    response = client.get('/api/v1/courses/', format='json')
    data = response.json()
    assert data[0]['name'] == courses[0].name
    assert response.status_code == 200

    course_id = data[0]['id']
    course_update = {'name': 'Worst Course Ever'}
    update_response = client.patch(f'/api/v1/courses/{course_id}/', data=course_update, format='json')
    updated_data = update_response.json()
    assert update_response.status_code == 200
    assert updated_data['name'] == course_update['name']

# тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(client):
    course = {'name': 'Test Course'}
    response = client.post('/api/v1/courses/', data=course, format='json')
    data = response.json()
    assert response.status_code == 201
    assert data['name'] == course['name']
    course_id = data['id']
    delete_response = client.delete(f'/api/v1/courses/{course_id}/', format='json')
    assert delete_response.status_code == 204











# @pytest.mark.django_db
# def test_create_course(client):
#     data = dict(name='Course')
#     response = client.post('/api/v1/courses/', data, format='json')
#     assert response.status_code == 201
#
# @pytest.mark.django_db
# def test_get_course(client):
#     response = client.get('/api/v1/courses/', format='json')
#     assert response.status_code == 200


