from django.db import models
from django.utils import timezone


class QestionVersion(models.Model):

	#公開可否
	PublishFlg_Choices = (
		(0,'不可'),
		(1,'可'),
	)
	PublishFlg = models.IntegerField(
		blank = False,
		verbose_name='公開可否',
		choices=PublishFlg_Choices,
		default=0
	)

	created_at = models.DateTimeField(
		default=timezone.now,
		verbose_name = '作成日',
	)
	updated_at = models.DateTimeField(
		auto_now=True,
		verbose_name =  '更新日',

	)
	updated_by = models.TextField()


class Qestion(models.Model):

	#qestionversion
	qestionversion = models.ForeignKey(
		'QestionVersion',
		on_delete=models.CASCADE,
	)

	#質問
	question = models.TextField(
		blank = False,
		verbose_name = '質問',
	)

	#回答form形式
	FormType_Choices = (
		(1, 'text'),(2, 'checkbox'),(3, 'radio'),(4, 'file'),
		(5, 'select'),(6, 'select-multiple'),(7, 'tel'),(8, 'url'),
		(9, 'email'),(10, 'datetime'),(11, 'date'),(12, 'month'),
		(13, 'week'),(14, 'time'),(15, 'datetime-local'),(16, 'number'),
		(17, 'image'),(18, 'range'),(19, 'color'),
		(20, 'reset'),(21, 'button'),(22, 'password'),
		(23, 'search'),(24, 'hidden'),(25, 'submit'),
	)
	FormType = models.IntegerField(
		blank = False,
		verbose_name='回答追加可否フラグ',
		choices=FormType_Choices,
		default=0
	)


	#回答追加可否
	AnswerAddFlg_Choices = (
		(0,'不可'),
		(1,'可'),
	)
	AnswerAddFlg = models.IntegerField(
		blank = False,
		verbose_name='回答追加可否フラグ',
		choices=AnswerAddFlg_Choices,
		default=0
	)

	#必須フラグ
	RequiredFlg_Choices = (
		(0,'必須でない'),
		(1,'必須'),
	)

	Required = models.IntegerField(
		blank = False,
		verbose_name='必須',
		choices=RequiredFlg_Choices,
		default=0
	)

	# 回答選択肢
	AnswerValues = models.TextField(
		blank=False,
		verbose_name='回答選択肢',
	)

	#説明(吹き出し)
	Balloon = models.TextField(
		blank = False,
		verbose_name = '吹き出し',
	)

	# 回答条件選択肢
	ConditionFlg_Choices = (
		(0, '条件なし'),
		(1, '条件に合致した場合、回答必須'),
		(2, '条件に合致した場合、回答不可'),
	)

	#回答条件設定
	ConditionFlg= models.IntegerField(
		blank = False,
		verbose_name='回答条件設定',
		choices=ConditionFlg_Choices,
		default=0
	)

	#回答条件確認先質問ID
	ConfirmedId = models.IntegerField(
		verbose_name='回答条件確認先質問ID',
	)

	# 回答条件確認先 回答
	ConfirmedId = models.TextField(
		verbose_name='条件に合致する回答',
	)

	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(auto_now=True)
	updated_by = models.TextField()


class Answer(models.Model):

	#qestion
	qestion = models.ForeignKey(
		'Qestion',
		on_delete=models.CASCADE,
	)

	#回答(テキストベース)
	content = models.TextField(
		verbose_name='回答'
	)
	#回答(ファイルベース)


	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(auto_now=True)
	updated_by = models.TextField()

