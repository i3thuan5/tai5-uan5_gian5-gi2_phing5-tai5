from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.欄位資訊 import 語句

版權表.objects.get_or_create(版權='會使公開')
種類表.objects.get_or_create(種類=字詞)
種類表.objects.get_or_create(種類=語句)