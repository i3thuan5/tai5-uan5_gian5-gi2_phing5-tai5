from behave import when, then, step
from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語平臺.辭典模型 import 華台對應表
from 臺灣言語平臺.辭典模型 import 華語表


@then('無建議的詞內底無物件')
def 無建議的詞內底無物件(context):
    無建議的詞 = context.test.client.get('/平臺項目列表/揣無建議的外語').json()['列表']
    context.test.assertEqual(len(無建議的詞), 0)


@step('有人求 {講法} 的講法')
def 有人求講法(context, 講法):
    回應 = context.test.client.post('/平臺項目/加外語', {'外語資料': 講法})
    context.test.assertEqual(回應.status_code, 200)


@then('查 豬 無任何講法')
def 講法內無揣著物件(context):
    講法 = context.test.client.get('/平臺項目列表/揣列表', {'關鍵字': '豬'}).json()['列表']
    context.test.assertEqual(len(講法), 0)


@then('無建議的詞內底有 豬')
def 無建議的詞內底有物件(context):
    無建議的詞 = context.test.client.get('/平臺項目列表/揣無建議的外語').json()['列表']
    context.test.assertEqual(無建議的詞[0]['外語資料'], '豬')


@step('有人答 {講法} 的講法')
def 有人答的講法(context, 講法):
    try:
        華語編號 = 華語表.objects.get().編號()
    except Exception:
        華語編號 = 華語表.objects.create(使用者華語=講法).編號()
    回應 = context.test.client.post(
        '/平臺項目/加新詞文本', {
            '外語項目編號': 華語編號,
            '文本資料': 講法,
            '音標資料': 講法,
        }
    )
    context.test.assertEqual(回應.status_code, 200)
    context.文本編號 = 回應.json()['平臺項目編號']


@when('有人正規化 {講法} 的講法')
def 有人校對講法(context, 講法):
    有人正規化做(context, 講法, 講法)


@when('有人共 {原本} 的講法正規化做 {正規化}')
def 有人正規化做(context, 原本, 正規化):
    華台 = 華台對應表.objects.get(使用者漢字=原本)
    _pigu = 使用者表.加使用者(
        'tsingkuihua@itaigi.tw',
        {'名': 'pigu', '出世年': '1987', '出世地': '臺灣', }
    )
    華台.提供正規化(_pigu, 華台.使用者華語, 正規化, 華台.使用者羅馬字)


@then('查 豬 會當揣著 豬仔')
def 會當揣著講法(context):
    講法 = context.test.client.get('/平臺項目列表/揣列表', {'關鍵字': '豬'}).json()['列表']
    context.test.assertEqual(講法[0]['新詞文本'][0]['文本資料'], '豬仔')


@then(u'查 {關鍵字} 會當揣著其他建議 {講法}')
def 會當揣著其他建議(context, 關鍵字, 講法):
    其他建議 = context.test.client.get('/平臺項目列表/揣列表', {'關鍵字': 關鍵字}).json()['其他建議']
    context.test.assertEqual(其他建議[0]['文本資料'], 講法)


@then(u'查 {關鍵字} 揣袂著其他建議 {講法}')
def 揣袂著其他建議(context, 關鍵字, 講法):
    其他建議 = context.test.client.get('/平臺項目列表/揣列表', {'關鍵字': 關鍵字}).json()['其他建議']

    print(華台對應表.objects.all().values())
    print(關鍵字, context.test.client.get('/平臺項目列表/揣列表', {'關鍵字': 關鍵字}).json())

    context.test.assertEqual(len(其他建議), 0)
