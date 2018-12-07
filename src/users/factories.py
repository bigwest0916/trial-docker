import factory
from faker import Factory as FakerFactory
from users.models import Department, User
from factory.django import DjangoModelFactory

faker = FakerFactory.create()

class DepartmentFactory(DjangoModelFactory):
	class Meta:
		model = Department
	name = factory.Faker('name')


class UserFactory(DjangoModelFactory):
	class Meta:
		model = User

	uuid = uuid_lib.uuid4
	username = 'admin'
	full_name = '大西浩'
	email = factory.Sequence(lambda n: f'person{n}@example.com')
	department = factory.SubFactory(DepartmentFactory)
	is_staff = True
	is_active = True










