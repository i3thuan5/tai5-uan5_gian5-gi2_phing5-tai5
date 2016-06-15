from behave import then, step


@then('無建議的詞內底無物件')
def 無建議的詞內底無物件(context):
    無建議的詞 = context.test.client.get('/平臺項目列表/揣無建議的外語').json()['列表']
    context.test.assertEqual(len(無建議的詞), 0)


@step('有人求 豬 的講法')
def 有人求講法(context):
    回應 = context.test.client.post('/平臺項目/加外語', {'外語資料': '豬'})
    context.test.assertEqual(回應.status_code, 200)


@then('查 豬 無任何講法')
def 講法內無揣著物件(context):
    講法 = context.test.client.get('/平臺項目列表/揣列表', {'關鍵字': '豬'}).json()['列表']
    context.test.assertEqual(len(講法), 0)


@then('無建議的詞內底有 豬')
def step_impl(context):
    無建議的詞 = context.test.client.get('/平臺項目列表/揣無建議的外語').json()['列表']
    context.test.assertEqual(無建議的詞[0]['外語資料'], '豬')
