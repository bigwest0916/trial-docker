from users.models import User
from django.db import models
from django.utils import timezone


class QuestionVersionMaster(models.Model):

	#公開可否################################
	PUBLISH_FLG_CHOICES = (
		(0,'不可'),
		(1,'可'),
	)
	#公開フラグ################################
	publish_flg = models.IntegerField(
		blank = False,
		verbose_name='公開可否',
		choices=PUBLISH_FLG_CHOICES,
		default=0
	)
	#作成日################################
	created_at = models.DateTimeField(
		default=timezone.now,
		verbose_name = '作成日',
	)
	#更新日日################################
	updated_at = models.DateTimeField(
		auto_now=True,
		verbose_name = '更新日',

	)

class CategoryMaster(models.Model):
	#questionversion################################
	questionversionmaster = models.ForeignKey(
		'QuestionVersionMaster',
		on_delete=models.CASCADE,
	)

	# カテゴリ名################################
	category_name = models.TextField(
		blank = True,
		verbose_name = 'カテゴリー名',
	)

	category_desc = models.TextField(
		blank = True,
		verbose_name = 'カテゴリー説明',
	)

	def __str__(self):
		return self.category_name

class QuestionMaster(models.Model):

	#category################################
	categorymaster = models.ForeignKey(
		'CategoryMaster',
		on_delete=models.CASCADE,
	)

	#質問################################
	question_content = models.TextField(
		blank=True,
		verbose_name = '質問',
	)

	#回答form形式################################
	FORM_TYPE_CHOICES = (
		(1, 'text'),(2, 'checkbox'),(3, 'radio'),(4, 'file'),
		(5, 'select'),(6, 'select-multiple'),(7, 'tel'),(8, 'url'),
		(9, 'email'),(10, 'datetime'),(11, 'date'),(12, 'month'),
		(13, 'week'),(14, 'time'),(15, 'datetime-local'),(16, 'number'),
		(17, 'image'),(18, 'range'),(19, 'color'),
		(20, 'reset'),(21, 'button'),(22, 'password'),
		(23, 'search'),(24, 'hidden'),(25, 'submit'),
	)
	form_type = models.IntegerField(
		blank=True,
		verbose_name='回答タイプ',
		choices=FORM_TYPE_CHOICES,
		default=0
	)


	#回答追加可否################################
	ANSWERADD_FLG_CHOICES = (
		(0,'不可'),
		(1,'可'),
	)
	answeradd_flg = models.IntegerField(
		blank=True,
		verbose_name='回答追加可否フラグ',
		choices=ANSWERADD_FLG_CHOICES,
		default=0
	)

	#必須フラグ################################
	REQUIRED_FLG_CHOICES = (
		(0,'必須でない'),
		(1,'必須'),
	)

	required_flg = models.IntegerField(
		blank=True,
		verbose_name='必須',
		choices=REQUIRED_FLG_CHOICES,
		default=0
	)

	# 回答選択肢################################
	answer_values = models.TextField(
		blank=True,
		verbose_name='回答選択肢',
	)

	#説明(吹き出し)################################
	balloon = models.TextField(
		blank = True,
		verbose_name = '吹き出し',
	)

	# 回答条件選択肢################################
	CONDITION_FLG_CHOICES = (
		(0, '条件なし'),
		(1, '条件に合致した場合、回答必須'),
		(2, '条件に合致した場合、回答不可'),
	)

	condition_flg= models.IntegerField(
		blank = True,
		verbose_name='回答条件設定',
		choices=CONDITION_FLG_CHOICES,
		default=0
	)

	#回答条件確認先質問ID################################
	confirmed_id = models.IntegerField(
		blank = True,
		verbose_name='回答条件確認先質問ID',
		default=0
	)

	# 回答条件確認先 回答################################
	confirmed_value = models.TextField(
		blank = True,
		verbose_name='条件に合致する回答',
	)

	#表示順ID################################
	disp_order = models.IntegerField(
		blank=True,
		verbose_name='表示順',
		default=0
	)

	#親の質問ID################################
	parent_id = models.IntegerField(
		blank = True,
		verbose_name='親となる質問のID',
		default=0
	)

	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(auto_now=True)

	def answer_values_as_list(self):
		return self.answer_values.split(',')


class DiagnosisMaster(models.Model):

	system_name = models.TextField(
		blank=True,
		verbose_name='システム名',
	)

	system_id = models.CharField(
		blank=True,
		verbose_name='システムID',
		max_length=100,
	)


	diag_when = models.DateField(
		blank=True,
		verbose_name='診断月',
	)

	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.system_id+" | "+self.system_name+" | "+str(self.diag_when)



class Question(models.Model):
	#question################################
	diagnosismaster = models.ForeignKey(
		'DiagnosisMaster',
		on_delete=models.CASCADE,
	)

	questionversionmaster = models.ForeignKey(
		'QuestionVersionMaster',
		on_delete=models.CASCADE,
	)

	diagnosismaster = models.ForeignKey(
		'DiagnosisMaster',
		on_delete=models.CASCADE,
	)

	categorymaster = models.ForeignKey(
		'CategoryMaster',
		on_delete=models.CASCADE,
	)

	questionmaster = models.ForeignKey(
		'QuestionMaster',
		on_delete=models.CASCADE,
	)



class Answer(models.Model):

	#question################################
	question = models.ForeignKey(
		'Question',
		on_delete=models.CASCADE,
	)


	#回答(テキストベース)################################
	answer = models.TextField(
		blank=True,
		verbose_name='回答'
	)

	#回答(ファイルベース)################################

	################################
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(auto_now=True)


