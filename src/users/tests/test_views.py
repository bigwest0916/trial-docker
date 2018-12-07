import pytest
from .factories import DepartmentFactory ,UserFactory
import random
from django.urls import reverse # 鈴木さん


# export DJANGO_SETTINGS_MODULE=karl.settings.local_test; pytest -v
# -v　は詳細に出すオプション
# assert len(response.context['diagnosis']) == 2のcontextは、Viewのreturnで返すcontext

# TODO
# ログインする際のUser/Pass定義
USERNAME = "admin"
PASSWORD = "NTTCom0033"

severity = ('high', 'medium', 'low')


def ログイン(self):
	url = reverse('/')
	response=self.client



@pytest.fixture
def setup_data(db):

    vuls = []
    # vulnid = 0
    risklevel_kind = ('high', 'medium', 'low')
    reproducibility_kind = (0, 1, 10, 20)
    required_entry_kind = (0, 1, 10)
    # fix_status_kind = 10

    for i in range(1, 21):
        vuls.append(VexVulnerabilityFactory(
            vexrisklevel=random.choice(risklevel_kind),
            url = 'https://test.com/test'+str(i)+'.html',
            reproducibility=random.choice(reproducibility_kind),
            required_entry=random.choice(required_entry_kind),
            vulnerability_id=1,
            vex_result_id=1,
            plugin_id=1
        ))

    diagnosis = DiagnosisFactory() # 鈴木さん

    user = User.objects.create(username=USERNAME)
    user.set_password(PASSWORD)
    user.save()
    yield(vuls)
#    yield(diagnosis)


class TestView():

    # setup_dataは、yield(vuls)から渡されるデータ
    def test_VEX診断結果一覧が表示されるか(self, client, setup_data):

        # ログイン処理
        client.login(username=USERNAME, password=PASSWORD)
        # /operations/diagnosis/をGet
#        response = client.get('/operations/systems/1/diagnosis/001/201804/vex/')

        vuls = setup_data
        print('A')
        print(type(vuls[0]))
        print('B')
        print(vuls[0].vex_result.diagnosis)
        print('C')
        url = reverse('vex:index', args = (
            vuls.vex_result.dagnosis.system,
            vuls.vex_result.dagnosis.code,
            vuls.vex_result.dagnosis.diag_date
        ))

        # ステータスコードの確認
#        assert response.status_code == 200
        assert client.get(url).status_code == 200

        data = {'reproducibility':1,
            'reproduction_method':'再現性確認方法が更新されました。',
            'evidence':'判断根拠が更新されました。',
            'required_entry':1,
            'vulnerability':10,
            'fix_status':1,
            'skip_fix_reason':'対応不要の理由が更新されました。'
        }  # postするデータ

        response = client.post(
                    '/operations/systems/1/diagnosis/001/201804/vex/vuls/1',
                    {'reproducibility':1,
                        'reproduction_method':'再現性確認方法が更新されました。',
                        'evidence':'判断根拠が更新されました。',
                        'required_entry':1,
                        'vulnerability':10,
                        'fix_status':1,
                        'skip_fix_reason':'対応不要の理由が更新されました。'
                    }
                    )

        response = client.get('/operations/systems/1/diagnosis/001/201804/vex/')
        # ステータスコードの確認
        assert response.status_code == 200

        assert '再現性確認方法が更新されました。' in response.content.decode('utf-8')
        assert '判断根拠が更新されました。' in response.content.decode('utf-8')
        assert '対応不要の理由が更新されました。' in response.content.decode('utf-8')
