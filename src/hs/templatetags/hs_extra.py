from django import template

register = template.Library()

@register.filter(name='checked')
def checked(value,arg):
    rtn = ''
    if value == arg:
        rtn = 'checked'
        return(rtn)
    else:
        return(rtn)

@register.filter(name='selected')
def checked(value,arg):
    rtn = ''
    if value == arg:
        rtn = 'selected'
        return(rtn)
    else:
        return(rtn)
