import factory
from faker import Factory as FakerFactory
from .models import Item
from users.models import Department, User
from factory.django import DjangoModelFactory

faker = FakerFactory.create()

class ItemFactory(DjangoModelFactory):
	class Meta:
		model = Item




