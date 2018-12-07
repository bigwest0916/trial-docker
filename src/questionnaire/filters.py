from django_filters import filters
from django_filters import FilterSet
from .models import QestionVersion, Qestion


class MyOrderingFilter(filters.OrderingFilter):
    descending_fmt = '%s （降順）'


class QuestionVersionFilter(FilterSet):

    name = filters.CharFilter(label='氏名', lookup_expr='contains')
    memo = filters.CharFilter(label='備考', lookup_expr='contains')

    order_by = MyOrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('PublishFlg', 'PublishFlg'),
            ('updated_at', 'updated_at'),
        ),
        field_labels={
            'PublishFlg': '公開可否',
            'updated_at': ' 更新日時',
        },
        label='並び順'
    )

    class Meta:

        model = QestionVersion
        fields = ('PublishFlg', 'updated_at',)