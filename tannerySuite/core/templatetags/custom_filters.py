from django import template

register = template.Library()

@register.filter
def pad_zero(value, num_digits=2):
    """Aggiunge zeri iniziali fino a raggiungere num_digits."""
    try:
        return f"{int(value):0{num_digits}d}"
    except (ValueError, TypeError):
        return value
