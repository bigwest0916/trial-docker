from django import template

register = template.Library()

@register.filter(name='splitanswer')
def splitanswer(value,arg):
	context = value.split(arg)
	return context

@register.filter(name='checkboxanswer')
def checkboxanswer(q):
	answers = q.answer_values.split(",")
	checkbox={}
	i=0
	for a in answers:
		checkbox[i] = a
		i += 1
	return checkbox


@register.filter(name='radioanswer')
def radioanswer(q):
	answers = q.answer_values.split(",")
	radio={}
	i=0
	for a in answers:
		radio[i] = a
		i += 1
	return radio

@register.filter(name='selectanswer')
def selectanswer(q):
	answers = q.answer_values.split(",")
	select={}
	i=0
	for a in answers:
		select[i] = a
		i += 1
	return select
