from django import template
from django.utils.safestring import mark_safe
from ..models import SmartPhone

register = template.Library()

TABLE_HEAD = """
              <table class="table">
                <tbody>  
             """

TABLE_TAIL = """
                  </tbody>
                </table>
             """

TABLE_CONTENT = """
                <tr>
                    <td>{name}</td>
                    <td>{value}</td>
                </tr> 
                """

PRODUCT_SPEC = {
    'smartphone': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display',
        'Разрешение': 'resolution',
        'Объём батареи': 'accum_volume',
        'Оперативная память': 'ram',
        'SD': 'sd',
        'Макс. объём SD': 'sd_volume',
        'Главная камера': 'main_cam_mp',
        'Фронтальная камера': 'frontal_cam_mp',
    },
    'notebook': {
            'Диагональ': 'diagonal',
            'Тип дисплея': 'display',
            'Частота процессора': 'processor_freq',
            'Оперативная память': 'ram',
            'Видеокарта': 'videocard',
        }
}

def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, SmartPhone):
        if not product.sd:
            PRODUCT_SPEC['smartphone'].pop('Макс. объём SD', None)
        else:
            PRODUCT_SPEC['smartphone']['Макс. объём SD'] = 'sd_volume'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)
