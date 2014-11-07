# -*- coding: utf-8 -*-
# Modified Hanja plugin to count statistics for Hanzi (simplified), all credits go to original authors.
# Word-list taken from previous hanzi stats plugin: Hanzi_Stats_New_HSK_20110411__show_all_hanzi__6000_chars
# Copyright: Ben Lickly <blickly@berkeley.edu>,
#            Trevor L. Davis <trevor.l.davis@gmail.com>
#            based on Japanese Stats by Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# hanzi statistics.
#

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import unicodedata
from anki.hooks import addHook
from anki.utils import ids2str
from aqt import mw
from aqt.webview import AnkiWebView
from aqt.qt import *
from aqt.utils import restoreGeom, saveGeom



freqHanzi = [
    (u'unlisted',''),
    (u'HSK Level 1',u'的出天点果什岁杯七一来北起老书友钟姐是他京星二米请八谢在家分些院师识呢菜了生高三女五火租零有们都很她见听块爸人对工去认客兴谁睡不期子商打热习吗喝国月小今做买语叫茶中多面么先医脑亮猫大能机样少爱六哪桌年本同那回太店朋狗上学车东系校午妈漂这现关想四昨写坐椅个说名西气站喜汉喂我作里水十觉读饭苹和电好影服候馆衣日前没话再飞欢雨时下明视儿钱怎九会开看你住字吃冷'),
    (u'HSK Level 2',u'以外门息诉早纸床咖公但球非介药休旁行长题足白班牛篮就员教始红绍哥圆新次路马试歌穿奶经体告考边送贵妹也等件准远黑姓羊场着运完旅左迎斤第已给共助右跑阴可间常游男千玩丈过因每望离您洗泳自比乐票找答船鸡得手身步思帮跳懂报表别备夫舞妻睛进两张快晚笑鱼蛋动意让病希错宜颜还务走号眼课忙踢司正色孩室唱慢瓜为最房真便汽雪肉晴到所问它百卖吧弟啡'),
    (u'HSK Level 3',u'市文据城单举超讲愿婚礼镜哭叔地心安调风音盘板香顾箱惯刷裤要目只几南李护突康绩草烧厨朵发力信办才清照轻择绿趣忘炼瘦者当赛把变注终史害典牙冒骑糕业通世结查越除虽乎背坏舒帽衫成位应演或居极练画刻净怪葡汁后道相感育低普春换笔句爷萄伞于如使又议包境检须束灯搬疼衬方种向选带且楼层差夏努祝聪澡用重总闻难容满健季树词迟甜饿而加物决参图干河酒邮脸熊爬矮法然己示较花半戏简附冬鸟鼻姨理情数节片根复拿遇旧蓝扫渴裙事化解空环历阳黄久鲜宾啊啤铅记特该头山响算角跟冰末梯胖筷主提界口条段双担辆怕敢腿饱蕉实平周放级必银短般借秋鞋锻定网接求易声刚街急静楚邻刮其万近直需园阿奇云脚耳糖碗'),
    (u'HSK Level 4',u'之由收首克约律效否伤油博坚础误窗奋琴寒酸幽扔谅全保格广流况林言严判食疑微讨释漫篇抱泪陪谊躺膏元性基尔改论却评态适压著毛染禁掌弃尊袋貌猪棵咸美制式消质研纪江验申减族危顿宽握诚闹耐帅厉拾笨从代社续士争优降尽播货座竟幸针赢暂骗扰猜擦骄饺内海术观户则预修破假紧弹困润尤烟饮辛傅仔饼愉咳资交达标具支警排村切括桥苦熟污醒抽聊剩丢敲肚柿民台规导亚确随料留止密吸皮输距鼓麻邀垃湿桶泼袜此管技集何功究负仍农父松恐既渐勇默忆圾孤抬吵嗽利活专指许象险访织竞免血逐乘掉挂励烦赚羽傲戚合无处济份精速底富例材沙映童森厚暗刀阅稍盐巾品费程连供即值断航绝激丽洋序遍植汗寄扮堵慕匙金计知案众仅亲景谈察细币虑怀龄戴塑译页穷歉厌价及各拉售引神彩批福互缺顺扩乱暖替贺弄盒悔乓区受任造像失划卡范养软丰秀浪墙叶址忽瓶俩乒钥入科原反光往列亿够群签码肯散键聘拒允肤凉逛怜被量际取推奖另按围停温毕惊梦齐硬巧详惜粗辣燥展至组增深职艺死省招甚永败钢脱符挺嘴呀硕猴羡将并联持整购限志命洲母悉章折概翻累撞尝汤暑恼羞部度证剧传获责积故继印味授杂扬估虎偶肥填咱窄懒'),
    (u'HSK Level 5',u'与布均益素土良贸裁射智坦迅聚凭返沟诗浓薄辩喷扶庙弯铃蜂砍晒歪脖膊阶产权类维某派冲尚涨寻守贝咨固疾豪珍郊佩妙摸涂碎糊雾纲柴逻吻睁浇蝴股团府器厂独移毒呼哈顶措献恶毫欣彻账描碍慎奈牵厘朴肌胃宴矩畏蜡娶队项卫防属铁劳编冠架野岛迹娱亏怖泛籍豆俊贡卧旬秩夕蛇摔洒梨裹髦醋建装款升石筑托征稳私享玉载骨摆灾诊摇忍唯胁疲苗倡脆陌绳叉蝶瞧逗瞎政德牌龙令执损夜幕订封盖枪倍虚凡皇腐寿链彼闪鼠锐雇狼拦炭糟撕嗓胳更形称致届登罪付倒餐胡途驶伴刺祖衡盾帝碰悄伸兄烂盼躲嫁叙踩帘鸽嚷设青施摄训临席核兵陆妇启旦残繁炒紫悲氛勤拳胶寺尺眠吓寂嫩宙甩壶丙华英率念依控似透操赶饰档册宇嘉赏卷废璃铜胆竹怒肩骂棉醉抄佣愧蹲勺投领义源古朝屋杀木频促灵沉棋乏泉横辞娘姻劣锅慰桃棒厢咬傻裔抖匀煎线营协庭武税迷略藏乡赔雄驾搞缓狂递煤慧矛辅肃憾宠闯蔬臭催捡翅恳狡立委治宣胜幅救询靠贷挑避麦劲辑捐池俗玻堆插滚呆胸匆粒慌趁晕煮橡皂强势存官占犯县宁挥震综甲贴殊阻燃闲敬践柔荐辈颗厕劝滩妨谜酱鞭椒咐企采配初状威庆纷惠秘召弱摩缩舍缘淡柜绪尘漏艳腰飘夹盆滴歇傍谦删唉版销巴承待宝退厅析荣炸痛纯拆跃迫洞灭寓披姑摘吹乙恨眉拐趟霉烫枕屉战型构落测露善汇述抢斗阵侵丁闭锁尾宿幼脏喊挣幻遵浅剪膀蜜舌绸讽猾军创曾财余革巨田拥抗遗趋伙敏佛液振敌挡壁犹炮魅姿屈悠豫浏毯耽梳馒统显置策套培融烈违伟库览谓圈丝隔恋虹吨挤欠尖谨哲丑鸭烤骤嘱乖烛桔局转击讯录轮补塔含偿延罚触逃偷恢宗秒仿拜粮戒愤磁鬼斜肺愁姥钓痒惭王未模拍充域追疗雷孙俱抓滑誉赞岸矿艰绕灰匹疯冻漠吐夸罐粘寞兔舅嚏'),
    (u'HSK Level 6',u'斯奥欧州党络监券陈央纳审额副波港媒索曲佳跌诺苏湖董探爆吉异盟攻峰晓予坛庄亡镇宅患障堂刑遭涉刊暴鲁夺盛湾伦晨债泰归杰姆端津若侧嫌栏榜赠渡晶亦驱菌叹衰怨抚舱窝逮纤巩狠忌哀冤瞩晤钉肪芒磋聋皱辙畴氢瞻腥侈惦揉杖暧馋锲川梁唐黎坡纠拼拔粉纵贩驰漆猎欺犬亭泊笼丛齿扇歹惹碳棍娇琢耍勉溶愣屁颤旷吼勿乞桨搂徙吝椭揍宫宏锦径滋廉仁墨泡蓄霸舰履窃膜舟牧仰宪绎顽罩渗贬肆脾缔兜蔓俐嵌濒韧吟缀瀑鞠秃溅嫉岔婪踌啰泽储岗仓凌胞忧侦裂艇遥庞抑稀贿浴廊刹辰辨垫挽缠溜耕谍扒熬穴焰岂掠嘲芽痪帖朽哺簸唠蔑睬讥潮辉井扣屏撑恰昆峡氏丧旺滨酬仙罢斑赤辟悟慈誓侨浑奠惕讶膝遏唇赂俭屑棕枉翘沮筐慷晾腮酗舔莫朗稿捕毁忠拓胎炎伪氧柱涵蹈御痕脂闷滞贤胀谐挨嘛溪堤凸哑蹦滤卑惫跪渣俯哇哎怯谬诧伶裳嗨隆抵杜兼捷搭腾沃霍炉涌伏翼串乳疏艘妥滥翔掏筒苍塘卸馈沧虐芦啥饥嫂泻锤捣侮拌绅眶眨痹膛熨蒙伯沿袭陷铺浮迈携愈娃阔役裕伐泄捧洽枝罕颈钦勾宰狭绣枯蚀蛮僵倦陋袍扁叨墟妒拽涮哟鄙隘斟雅偏搜署淀押猛毅诞墓臣箭杆殖帐赌啦噪皆腔哨叛巷谎碌蕴扯杠篷衍扛畔镶诫昧睦磕苟沼殃溉捎咙锋迁圣呈桑祥狱甘耗逢婆栋逊凝割舆岳砸肿墅剥骚晃钞螺崭霜丸竖隙咽馅禽挚凹憋熄嗅秤辫疙蔼暄潜恩珠欲蒂番悬拖挖惨癌扭孕缝霞拘帆纹纺袖辖喻筋株勘诵沾摧剖淹灶徊隶纬澈粥捍庇恕惋雹哆叼仪驻昌谷踪剂劫巡轰疆诱凶吁挫撒妆卓渔赋饲仇灿兽腻贼擎帜侣宵俘颂捏筛掷恍嘿廓屿拙浊嘈稠嗯塞筹拨盈颁涛疫恒魔砖惑奉悦脉赁歧弊铭睹酿淋衔荧抹幢栽喘媳魄搅斩稚隧氓袱呕怠伺掐酌诬榨呻厦焦赴跨缴颇薪泥寸鸣掘堪荒壳屡魂搏垂慨臂捉灌遣孝崩蓬钩阐磅耻奴叭趴叮蠢沐烘饪躬涕谤挎唆瓦症谋奏壮磨渠陶郎逼婴绑侠攀狮辐弥捞谱沫削吞驳昔浸弦丘搁奢剔泌烹挠咋椎缚肴敷拣唾峭茎阂援鉴盗兑揭讼畅撤酷淘尸盲郁旨祸掩茂庸爽尴坝逝绒茫稻颠捆愚酝殴萌觅啸僻抒嚼堕拧眯梢掰惰拄督奔混纽徒摊贯添肖堡械贪煌峻瓷陵垄框牺尬盯遮碧瘤膨呵蔽锈瘫悼恭柬烁汹耸猖兢渺劈淆咀迸啬郑洁乌倾拟孔岩赖旋绘覆晰昂扑诈腹粹葬塌惧凑敞旱肢叠畜溃辜攒昼坟熏沛瞪窜葫紊譬蹬啃丐惮瘸截隐伍贫诸崇虫踏抛循吊埋兆碑挪晋匪惩昏迄辱瘾殿仗壤谴澄谣讳喉拢飙橙妄陡凄哦哼搀虏嗦狈吩旗洪荡扎轨枚辽雕颖钻耀牢汰勃衷牲坑掀擅斥曝沸躁蒸彰竭铸瞒哄崖喇雌滔饶踊疤甭舶搓衅诽躇蹋'),
    (u'Frequent 500',u'的一是不了在人有我他这个们中来上大为和国地到以说时要就出会可也你对生能而子那得于着下自之年过发后作里用道行所然家种事成方多经么去法学如都同现当没动面起看定天分还进好小部其些主样理心她本前开但因只从想实日军者意无力它与长把机十民第公此已工使情明性知全三又关点正业外将两高间由问很最重并物手应战向头文体政美相见被利什二等产或新己制身果加西斯月话合回特代内信表化老给世位次度门任常先海通教儿原东声提立及比员解水名真论处走义各入几口认条平系气题活尔更别打女变四神总何电数安少报才结反受目太量再感建务做接必场件计管期市直德资命山金指克许统区保至队形社便空决治展马科司五基眼书非则听白却界达光放强即像难且权思王象完设式色路记南品住告类求据程北边死张该交规万取拉格望觉术领共确传师观清今切院让识候带导争运笑飞风步改收根干造言联持组每济车亲极林服快办议往元英士证近失转夫令准布始怎呢存未远叫台单影具罗字爱击流备兵连调深商算质团集百需价花党华城石级整府离况亚请技际约示复病息究线似官火断精满支视消越器容照须九增研写称企八功吗包片史委乎查轻易早曾除农找装广显吧阿李标谈吃图念六引历首医局突专费号尽另周较注语仅考落青随选列'),
    (u'Frequent 1000',u'武红响虽推势参希古众构房半节土投某案黑维革划敌致陈律足态护七兴派孩验责营星够章音跟志底站严巴例防族供效续施留讲型料终答紧黄绝奇察母京段依批群项故按河米围江织害斗双境客纪采举杀攻父苏密低朝友诉止细愿千值仍男钱破网热助倒育属坐帝限船脸职速刻乐否刚威毛状率甚独球般普怕弹校苦创假久错承印晚兰试股拿脑预谁益阳若哪微尼继送急血惊伤素药适波夜省初喜卫源食险待述陆习置居劳财环排福纳欢雷警获模充负云停木游龙树疑层冷洲冲射略范竟句室异激汉村哈策演简卡罪判担州静退既衣您宗积余痛检差富灵协角占配征修皮挥胜降阶审沉坚善妈刘读啊超免压银买皇养伊怀执副乱抗犯追帮宣佛岁航优怪香著田铁控税左右份穿艺背阵草脚概恶块顿敢守酒岛托央户烈洋哥索胡款靠评版宝座释景顾弟登货互付伯慢欧换闻危忙核暗姐介坏讨丽良序升监临亮露永呼味野架域沙掉括舰鱼杂误湾吉减编楚肯测败屋跑梦散温困剑渐封救贵枪缺楼县尚毫移娘朋画班智亦耳恩短掌恐遗固席松秘谢鲁遇康虑幸均销钟诗藏赶剧票损忽巨炮旧端探湖录叶春乡附吸予礼港雨呀板庭妇归睛饭额含顺输摇招婚脱补谓督毒油疗旅泽材灭逐莫笔亡鲜词圣择寻厂睡博勒烟授诺伦岸奥唐卖俄炸载洛健堂旁宫喝借君禁阴园谋宋避抓荣姑孙逃牙束跳顶'),
    (u'Frequent 1500',u'玉镇雪午练迫爷篇肉嘴馆遍凡础洞卷坦牛宁纸诸训私庄祖丝翻暴森塔默握戏隐熟骨访弱蒙歌店鬼软典欲萨伙遭盘爸扩盖弄雄稳忘亿刺拥徒姆杨齐赛趣曲刀床迎冰虚玩析窗醒妻透购替塞努休虎扬途侵刑绿兄迅套贸毕唯谷轮库迹尤竞街促延震弃甲伟麻川申缓潜闪售灯针哲络抵朱埃抱鼓植纯夏忍页杰筑折郑贝尊吴秀混臣雅振染盛怒舞圆搞狂措姓残秋培迷诚宽宇猛摆梅毁伸摩盟末乃悲拍丁赵硬麦蒋操耶阻订彩抽赞魔纷沿喊违妹浪汇币丰蓝殊献桌啦瓦莱援译夺汽烧距裁偏符勇触课敬哭懂墙袭召罚侠厅拜巧侧韩冒债曼融惯享戴童犹乘挂奖绍厚纵障讯涉彻刊丈爆乌役描洗玛患妙镜唱烦签仙彼弗症仿倾牌陷鸟轰咱菜闭奋庆撤泪茶疾缘播朗杜奶季丹狗尾仪偷奔珠虫驻孔宜艾桥淡翼恨繁寒伴叹旦愈潮粮缩罢聚径恰挑袋灰捕徐珍幕映裂泰隔启尖忠累炎暂估泛荒偿横拒瑞忆孤鼻闹羊呆厉衡胞零穷舍码赫婆魂灾洪腿胆津俗辩胸晓劲贫仁偶辑邦恢赖圈摸仰润堆碰艇稍迟辆废净凶署壁御奉旋冬矿抬蛋晨伏吹鸡倍糊秦盾杯租骑乏隆诊奴摄丧污渡旗甘耐凭扎抢绪粗肩梁幻菲皆碎宙叔岩荡综爬荷悉蒂返井壮薄悄扫敏碍殖详迪矛霍允幅撒剩凯颗骂赏液番箱贴漫酸郎腰舒眉忧浮辛恋餐吓挺励辞艘键伍峰尺昨黎辈贯侦滑券崇扰宪绕趋慈乔阅汗枝拖墨胁插箭腊粉泥氏'),
    (u'Frequent 2000',u'彭拔骗凤慧媒佩愤扑龄驱惜豪掩兼跃尸肃帕驶堡届欣惠册储飘桑闲惨洁踪勃宾频仇磨递邪撞拟滚奏巡颜剂绩贡疯坡瞧截燃焦殿伪柳锁逼颇昏劝呈搜勤戒驾漂饮曹朵仔柔俩孟腐幼践籍牧凉牲佳娜浓芳稿竹腹跌逻垂遵脉貌柏狱猜怜惑陶兽帐饰贷昌叙躺钢沟寄扶铺邓寿惧询汤盗肥尝匆辉奈扣廷澳嘛董迁凝慰厌脏腾幽怨鞋丢埋泉涌辖躲晋紫艰魏吾慌祝邮吐狠鉴曰械咬邻赤挤弯椅陪割揭韦悟聪雾锋梯猫祥阔誉筹丛牵鸣沈阁穆屈旨袖猎臂蛇贺柱抛鼠瑟戈牢逊迈欺吨琴衰瓶恼燕仲诱狼池疼卢仗冠粒遥吕玄尘冯抚浅敦纠钻晶岂峡苍喷耗凌敲菌赔涂粹扁亏寂煤熊恭湿循暖糖赋抑秩帽哀宿踏烂袁侯抖夹昆肝擦猪炼恒慎搬纽纹玻渔磁铜齿跨押怖漠疲叛遣兹祭醉拳弥斜档稀捷肤疫肿豆削岗晃吞宏癌肚隶履涨耀扭坛拨沃绘伐堪仆郭牺歼墓雇廉契拼惩捉覆刷劫嫌瓜歇雕闷乳串娃缴唤赢莲霸桃妥瘦搭赴岳嘉舱俊址庞耕锐缝悔邀玲惟斥宅添挖呵讼氧浩羽斤酷掠妖祸侍乙妨贪挣汪尿莉悬唇翰仓轨枚盐览傅帅庙芬屏寺胖璃愚滴疏萧姿颤丑劣柯寸扔盯辱匹俱辨饿蜂哦腔郁溃谨糟葛苗肠忌溜鸿爵鹏鹰笼丘桂滋聊挡纲肌茨壳痕碗穴膀卓贤卧膜毅锦欠哩函茫昂薛皱夸豫胃舌剥傲拾窝睁携陵哼棉晴铃填饲渴吻扮逆脆喘罩卜炉柴愉绳胎蓄眠竭喂傻慕浑奸扇柜悦拦诞饱乾泡'),
    (u'Frequent 2500',u'贼亭夕爹酬儒姻卵氛泄杆挨僧蜜吟猩遂狭肖甜霞驳裕顽於摘矮秒卿畜咽披辅勾盆疆赌塑畏吵囊嗯泊肺骤缠冈羞瞪吊贾漏斑涛悠鹿俘锡卑葬铭滩嫁催璇翅盒蛮矣潘歧赐鲍锅廊拆灌勉盲宰佐啥胀扯禧辽抹筒棋裤唉朴咐孕誓喉妄拘链驰栏逝窃艳臭纤玑棵趁匠盈翁愁瞬婴孝颈倘浙谅蔽畅赠妮莎尉冻跪闯葡後厨鸭颠遮谊圳吁仑辟瘤嫂陀框谭亨钦庸歉芝吼甫衫摊宴嘱衷娇陕矩浦讶耸裸碧摧薪淋耻胶屠鹅饥盼脖虹翠崩账萍逢赚撑翔倡绵猴枯巫昭怔渊凑溪蠢禅阐旺寓藤匪伞碑挪琼脂谎慨菩萄狮掘抄岭晕逮砍掏狄晰罕挽脾舟痴蔡剪脊弓懒叉拐喃僚捐姊骚拓歪粘柄坑陌窄湘兆崖骄刹鞭芒筋聘钩棍嚷腺弦焰耍俯厘愣厦恳饶钉寡憾摔叠惹喻谱愧煌徽溶坠煞巾滥洒堵瓷咒姨棒郡浴媚稣淮哎屁漆淫巢吩撰啸滞玫硕钓蝶膝姚茂躯吏猿寨恕渠戚辰舶颁惶狐讽笨袍嘲啡泼衔倦涵雀旬僵撕肢垄夷逸茅侨舆窑涅蒲谦杭噢弊勋刮郊凄捧浸砖鼎篮蒸饼亩肾陡爪兔殷贞荐哑炭坟眨搏咳拢舅昧擅爽咖搁禄雌哨巩绢螺裹昔轩谬谍龟媳姜瞎冤鸦蓬巷琳栽沾诈斋瞒彪厄咨纺罐桶壤糕颂膨谐垒咕隙辣绑宠嘿兑霉挫稽辐乞纱裙嘻哇绣杖塘衍轴攀膊譬斌祈踢肆坎轿棚泣屡躁邱凰溢椎砸趟帘帆栖窜丸斩堤塌贩厢掀喀乖谜捏阎滨虏匙芦苹卸沼钥株祷剖熙哗劈怯棠胳桩瑰娱娶沫嗓蹲焚淘嫩'),
    (u'Frequent 3000',u'韵衬匈钧竖峻豹捞菊鄙魄兜哄颖镑屑蚁壶怡渗秃迦旱哟咸焉谴宛稻铸锻伽詹毙恍贬烛骇芯汁桓坊驴朽靖佣汝碌迄冀荆崔雁绅珊榜诵傍彦醇笛禽勿娟瞄幢寇睹贿踩霆呜拱妃蔑谕缚诡篷淹腕煮倩卒勘馨逗甸贱炒灿敞蜡囚栗辜垫妒魁谣寞蜀甩涯枕丐泳奎泌逾叮黛燥掷藉枢憎鲸弘倚侮藩拂鹤蚀浆芙垃烤晒霜剿蕴圾绸屿氢驼妆捆铅逛淑榴丙痒钞蹄犬躬昼藻蛛褐颊奠募耽蹈陋侣魅岚侄虐堕陛莹荫狡阀绞膏垮茎缅喇绒搅凳梭丫姬诏钮棺耿缔懈嫉灶匀嗣鸽澡凿纬沸畴刃遏烁嗅叭熬瞥骸奢拙栋毯桐砂莽泻坪梳杉晤稚蔬蝇捣顷麽尴镖诧尬硫嚼羡沦沪旷彬芽狸冥碳咧惕暑咯萝汹腥窥俺潭崎麟捡拯厥澄萎哉涡滔暇溯鳞酿茵愕瞅暮衙诫斧兮焕棕佑嘶妓喧蓉删樱伺嗡娥梢坝蚕敷澜杏绥冶庇挠搂倏聂婉噪稼鳍菱盏匿吱寝揽髓秉哺矢啪帜邵嗽挟缸揉腻驯缆晌瘫贮觅朦僻隋蔓咋嵌虔畔琐碟涩胧嘟蹦冢浏裔襟叨诀旭虾簿啤擒枣嘎苑牟呕骆凸熄兀喔裳凹赎屯膛浇灼裘砰棘橡碱聋姥瑜毋娅沮萌俏黯撇粟粪尹苟癫蚂禹廖俭帖煎缕窦簇棱叩呐瑶墅莺烫蛙歹伶葱哮眩坤廓讳啼乍瓣矫跋枉梗厕琢讥釉窟敛轼庐胚呻绰扼懿炯竿慷虞锤栓桨蚊磅孽惭戳禀鄂馈垣溅咚钙礁彰豁眯磷雯墟迂瞻颅琉悼蝴拣渺眷悯汰慑婶斐嘘镶炕宦趴绷窘襄珀嚣拚酌浊毓撼嗜扛峭磕翘槽淌栅颓熏瑛颐忖'),
    (u'Frequent 3500',u'牡缀徊梨肪涕惫摹踱肘熔挚氯凛绎庶脯迭睦窍粥庵沧怠沁奕咙氨矗盔拇沛榻揣崭鞘鞠垦洽唾橱仕蜘痰袜峙柬蝉蟹谏鹃擎皓朕疤禺铲酶钝氓匣弧峨锥揪杠吭崛诬冉抒庚悍靡晦醋壕锯夭咦侈婢猾徘硝煽皂舵嗦狈靴捂疮郝苛秽茜搓芸酱赁檐饷蕉铀苔赦缎舷筷朔婪紊厮婿寥兢糙卦槐扒裴祀埔絮芭屉痪霄绽宵邑霖岔饵茄韧琪邹瑚憋殆噜忒忿衅淳悖髦孜粤隘濒铮畸剔坞篱淀蓦唬锣汀趾缉嫦斟鞍扳拴诅谟呃懦逞犁忏拧亥佟叱舜绊龚腮邸椒蔚湛狩眶栈薇肮瀑渣褂叽臀妞巍唔疚鲤戎肇笃辙娴阮札懊焘恤疹潇铝涤恃喽砌遁楞阱咎洼炳噬枫拷哆矶苇翩窒侬靶胰芜辫嚎妾幌踉佃葫皖拽滤睬俞匕谤嗤捍孵倪瘾敝匡磋绫淆尧蕊烘璋亢轧赂蝗榆骏诛勺梵炽笠颌闸狒樊镕垢瘟缪菇琦剃迸溺炫惚嗨陨赃羁臻嘀膳赣踌殉桔瞿闽豚掺沌惰喳椭咪霎侃猝窖戮祠瞩菁躇佬肋咄忡雍忱蕾跄硅伎炊钊蝠屎拭谛褪丞卉隧茸钳啃伢闺舔蹬挛眺袱陇殴柿梧惺弛侥琛捅酝薯曳澈锈稠眸咆簧鸥疡渎汲嬉脓骡穗槛拎巳邢廿搀曙樵隅筛谒倭痹猖佯肛奚甭抨蛾唠荧嵩漱酋攘诘篡睿噩怅盎徙鞅漓祟睫攸翎呛筐堑檀寅磊驭惘吠驮瑙炬痉曝恺胺萤敕筝幡霹竺烙毗鸠埠蒜阜嘈乒帷啄鳌毡阙褥搔笋冕狞韶骼蔼烹奄嫖沐噗岑蛟掳咏弩捻圃孚悴诣呱祁捶钠袄澎氮恪雏撮堰彷鹦晖犀腑沽橄掐亵龋嗒咀祺锚'),
    (u'Frequent 4000',u'匾乓萃贻揖觑吝憔羌诲砾蠕肴撩坍酥袅黝俾嫣穹秧妊溉鹊聿疙蘑睾楷酵茹锌滇辗纂圭幔褒揍诽倔腓颉锄嗔磺攒瘩雳吆悚墩彝囱逍辄桅俨纶悸殃帧俐绮袒籽孰愫拌橙暨敖赘抉淤剌娼顼葵哝酣麓钵琅簸禾铢璧娠彗惋腋螂阪掣劾沥粱嚓惮氖捎羔俟渲榄茧霓鹉胥琶撬橘醫拈笆痊亟渭狙珂刨蜕谚憧瞟馒拗帚钗哧喋箫刁怦缭迥湄磐渝冗闵噶黏蕃弼驿淄饺踞韬婷唆蜒偎榨漉碉皈矜笈枷鲨蹑瀚酪谑癖烬揩炙蜷侏凋漪悻蹋讪搐碘帛诠碾擂苯诃铎戊荀驹攫憬哽踵蟒漾啧吮楠氟怂叼竣偕漩蹭翌臆挝绚崽糜瘢跤阑恬豢汶跷琵憨蜗螅惴戟匮恙抿桢笺蛤瞳藥瓢衹秤跺潦芹哒饬栩曦骷嫡卤丕鬓梓嗖惦浚咔藐荃唧玺汛铐髅渤皿箍馅汾戍痔褶聆涎汞渍奂巅疣傩逵耆蟋鳄讹膺蹿筏釜沂坯峦茬摒蟀撵浒缤嵋珑苞瑾泵钾暧赓叟佚沓撂蛊甥璐晏瘪漳阉蹂鳃琏湃辘僭躏鼾懵镰寐褚攥涧蝙脐辕涣杞煜骥傣嗳祯酉秸捺瑕鑫馋窿楔胱荔蟆湍屹遐轲镯缰桦炖钡羚啬诩绯掖箓涸鸳塾呸抡擞熹坷瓮亘嗟筵跛汕欤壑颍溥姗踊枭暄稷跚涟瀛笙滕踝贰瞰恻嚏迢獗邯睑赡萦珥酮璞羹缄晾俸媲鸾恿蜿犊讷扈蜈翟藕戌蓓鋆谩谀卯谙岐蝎荼镀椰甄蟾蹊泞撸螃檬猓蔷羲瘸蘸蔗傀蚌锢遽邃恚皑锵簌焙昊鹳睽刽鳖噎呗寰唷殡淖诰恣睐婵榈氦靳蛹鸯惬蹙诙眈罡缮胤皋蛀偌疵绛葆黔喙烽儡佼斓嫔颚龈盅娓坂'),
    (u'Frequent 4500',u'町芥瘠阂挎橇荟啜垛淇瓒篓虱跻龛蹒髯瞠痫掂潼酰镁灸腆筱谆骋壬茗椋蛔潺扉耘槟雹甬谥淞燎蕙蚪蜻郸轶狰楣捋涓荪娄麝蚤薰醮搪谧湮辍瞌梆樟茉岖臼癣穑玷馍呷萼妩伫彤莓岬媛惆鳎啾囔蜓孺徇徵焊岱昵卅飙邙痞隼恫怆桀绶裆盂桧蚓抠嗷槌痘痢芮蚣闩铿飓疱蝌撅蚯斡窠荚耷砚牒赈煦嗫耙榕鞑袤谌醺秆徨橹翡缨锹嵇圪髻嗬辎痣娩谄蛐鹞翱庖籁蓿鳗疟鲇這嚅瘀颔黜黠濑馁洵忐忑砥咂罹糠匝偃淙纫喏闾祛蛰腼涝曜厩疽闰洄煊汐藓璜铬經渥靼酗苓噤咫椿鲫锭罔锺匍祗锰岌馀畹糯胫熠銮沅棣旌豌孢镭驸腌盹熵镐馐嘤癞骰韭阖瞑裨宕戾镌溟牍隽婊鹄埂拄娲虬萱啵蠡芋胭豺啻褛蛆柠掰篆倌咛蛭谡荨莞澹纭潞郅弋飕螳胄蟑猥宓昙锏蟠過柑烯匐濮蟮祐仄偈蜃箴粼嗥褴蕨蓟圩孪杳魇荤诿簪氲摞飒镂舀夙臧蒿貂蜥蹩噼钛钚獾濂铠皙霭鲈叵霾泯碴鸵峪饕瘁睢鬃迩纣夔垠饨榭隍娑篝榔洌浜鲑谔汩浣舐瞭忻咻鹑唑懋皎诒麾辏氐冽箕俚汴宸芍捱摈摺簦箔咝孀怏谝砧馕耄罂漕沣栾榘烷榷俑沱缜鹫蛳剽衢泗臊瘴酚纾晁孛炀叁憩掬椤啮畿掸镣骁椽侗滦荩泓蚱癜酯體癸蚜扪庑歆蝮蹶弈庋喟滂啕蛎獭槁翊龊邺莘燮剁觐铛谗镍臃墒晔燔嘭涿醯箩鄱睨诤坳鹭砷唏伲猬琥殁蚩泾缥殓鳅氰诋刍芷嶙逅舫呓唰茁馑妫骧苷擢峋袂懑蓑與涞祉踹掇沏诳噫饽饪绺谘飧迳铡枞熨鋈荭'),
    (u'Frequent 5000',u'赊俦戛湎幺凇芪觯龌挞嬴苻嘁鞯肽恸迨钰儆觎讫滓僮媾龇胯涮绾杈赳斛觥疸卞愠拮庠烨龢菠窈罄囤弁奘咣缫腴缈喵潢遛柚郏荻藜琨镳雉橐陽骈蛉艮搽濡寮柩佗啷诜視偻夯闱谖夥枸膑虻筠埽笞臾婀珞粑怵绻殒觊崂颧嗑榛昱蜴鳝噙淼矾硼囿泅邂钜蠹垩乩嗝淦樽诮揆啐淅榉馗辔暹骛鱿苫犷獠詈竦篙诨铰馄蜚峒滢琬靓狻璨犟鸬螨芩嘹锟蜇洹栉俪钍锨瑁壹痿竑粕犄瘙饯抟衲踮龅愎馥梏讣邝艿趺鲟剜绉罅笥衩姣斫鹗腎爻猕晗铩窕仨搡崴酢檄佞孑璀岷舛邕闿铂霁犒馏阈麋麒苁摁涔宥妍铤锷嗲恽麂赝胛哂撷呶噘懔栎桎霰飨揄噔娣薏忝咤嗵迤贲胪鍪泸蔫刈僖咿鹌嗪茏茯岫嵘轱怼铨昕郢咩馊髡澧苣濯盥囡砺佘谶弑楂翦怩蠼霏楹讴锲慵胝砭潍杵樾帼碣诌徕胴钴裟啶铣铱楫赭碛酊魑醛剐畦陂闶阄祚鹘泱趄骅陲郧倜呤燧铉粲骶峁忸渌骞髭戡钨谲苋锃蜊幄闼戕骊虢烩傥妲绌桠袈鎗薮揿杲肓厝莅氤缙衮诟旖硒唁嬗硎裱颦質靥纥煨礴鏖蝈笏羿鼐湟甑炜煲锉笕喑嶂浔弭妪锂苡孳颏醴間渚轭鹬蚝黃膘邛痨褡耦覃虛馔篾兖阋遨爰痂艄耨沤邋焓秣昶種變窣绦俎榫蟪稗謇氩類锴龉烃俣嬷肱鸢笫痤陰菏莆芨阕砣碜鼹長猷竽舸诓錾淬隗悌姘槭邈婕歙稹蹴砒痈镏羯豕鲂蓖匦笤峥徭浃烊補窸酆缢褓蚨翳趔炔誊赜仃勖葺蚴泷蛴結媸俳诖茑逡孱砦跸祜伉溴屐飚蛞鏡掮崆庾橛矸鸨'),
    (u'Frequent 5500',u'圻缂蒯诹啭饧镉鸪蛩蠖說劭哐崧杼棂螫龃饔遑颢腱襁忾濠牝蛄鲆嗄灏疥苜荞嘣夤砝颞開忤遢旎瘛魉辇見瓤荥涫娌氚臁毂碇毖壅吡缛玮羟還珈颀虼祇佝翕遴珏郛較驗玖蹇逋氅粽诂岢聒髁黍芾淝鲎鞣髋闳潆汨胍阏钤鹜鬈铵戬點崮枰樯脍畲衾蹼題劬咭囫洱刎芏琊碚鳕谪芎恂槿鲢鲧嘧绀郦噱浠潸跏鲶矍苌抻琰鹚龆臬芄呔雒觞钒饫阒槎鸩舂谠阡莒萸妗稔穰蚧餍谯芗菸葩踔厣佻嘌饩钏蠓黩倨腸缬殚钿鎏恁藿囟鄣呋婺绱瓯旃锶酩恹逶缦鸹螟菟阗濉篑醪鲛讦媪邬殇鄯芡嫠肼峤矽讧掼焖愆聩岘靛菖卟姒杷砉袢蚋笳挈關踽黾麼侩凫诔郯韪挲笪鼋莜風菅嵊裢趿箸莴莠阌旯圜涪赍柞嗍囵榧裰笾簟跎巽曷逖骓绔枋镒魃餮讵乜鄢瑭踅馓蟛鳟荛菬忪阍姹纰桉氪氘垅郃汊娉纡缟旮镢傈堋蔺庥枥腭鹕笮髂魍缁槊跞醚吒枳搿鹧蜍舻鏊禳蒺钹蜢鬻珩卮垭苄苕菀骠袷跹瘘騔論磬缶笸鸷頭芰蕲阆纨琮牦砩蠲锒锕郓妯驷鹩舢趸證養芫嗉蠊笊莸饴阃浯枇焱铆擤柢醢呲崾溆潴牖硪碓鹆鬣堀帙雱須進诎獐桁蛱鳏郴幂箝僳疝茴揶呦嗌囹螈脲镊锑胨膈痼鳊赅贽處苤峄桡雎鲋鞫鼬獯昀痍蟊鞴疖熘乇羸嵴栀槲炝炷硐锸鹂裾侪診調珐縯哔屙旆佰僦牯钪掾針仟圮芟崃廪擘笱跗鲅硷苎匏嗾圄彀粳卣勐掴涑浞玳愍畛赧貉擀湫逦椴铄箧刖鲮訇茱啖悭愀朐畈鹨蛘佶缃晟鲱凼苴颛厍匚徉洙氡胗癯鞒'),
    (u'Frequent 6000',u'锆佤錢飲細勰钺繇螭嵬轸肟肫邨瘿仞奁宄轳熳睇钼蝼跆樗鲰節诶薜铧裥榇馃術蹚怄寤缗硗碡矬鸱虺糅雠帑镧埙啁悒犍硌锩虿蛑艉钅咴筮艏糁鼍肄籴骜砻蜮龀黢劢腫耪鬯畚觳稞鹁鲲稱捌菔獬柘娆篪鲀谰孬伥谇鄄狎闫滟齑遒磔聃綦鲡蔻泠砗钕镫菹胂煅煸螯躅鲠佥罘嶝適坨菽哞徜慊洳渑灞盍钋鸫踯縻萘褫羰腦俅芤隳洮胼罴镛怛芊啉噌嫱绲膻焐裡葎亓倮莼蘅嘞缒镆網伧荏唳檩鸶蚬骱蘖澍韫颎嘏垡腚焯繻怙羧鼙倥亳艽荠昴舨魈醣枵粜甙珲杓楸楦疃蛏蠛髌茔臨诼嬖耒蜣笄跣钣戆蜉喾铍陉薹肷岵瓴荽怫钭窀缯倬摭帔楝痱蚶螬髑紅鼗狷殛裉粝萋葭衽鳢傧喁嫘罟钌裼愦蝽雖锗衿粢醵跫鐾廛墉哌輕扦堇婧暌罱镞蹰陟鳔脘臟岿侔郾唿砹疴麸薨綝滁偾拊撺呒狯猢椁榱罾铳裎鳚眦璎認崞缇蝣萑狲缱晷冼痧統蕖狍憷锛窨袼帏儋绨疠蘩嵝庀汜炅煳泶瓠窳虮蚰邰苊砀捩蹉莪螽覺蘼槔曛蛲鹾隹犸衄觀轉銎泫玢辊瞋墀酐隱堞尥嚯猗逑逯硖噻嵛畀運鲃偬鄞呖溧嬲肭鹈鹱窭黧谵沆嫒塬缣篯酃喱泔溘迕肀秫裣铋蒌曩赀箪朊鳙仫钎芑胙盱糇挹捭悱鬟緩請崤澶甾欹瞽钇鹪鞔缡铯鲚組嘬庹渖湔玎锜锊舾籼阊祕猊燹葑蓼幛岣浼甯瑷敫钔钫锼锿癔穸褊蚍篦麇樘钯禇铒續莩嵯逭遄戗睃鮈瀣皴泮轫褰炱醍锱篁葚難矇驽辚睥鸺筇戥髀驺頸哙濞逄桤攵炻磙疳醭鳇鹮迓眇楮砜謝離約菘馇'),

 ]

def ishanzi(unichar):
    try:
        return unicodedata.name(unichar).find('CJK UNIFIED IDEOGRAPH') >= 0
    except ValueError:
        # a control character
        return False

class hanziStats(object):

    def __init__(self, col):
        self.col = col
        self.hanziGrades = freqHanzi
        self._gradeHash = dict()
        self.seenhanzi = set()
        for (name, chars), grade in zip(self.hanziGrades,
                                        xrange(len(self.hanziGrades))):
            for c in chars:
                c = unicodedata.normalize('NFC', c)
                h = self._gradeHash.get(c, [])
                h.append(grade)
                self._gradeHash[c] = h

    def hanziGrade(self, unichar):
        return self._gradeHash.get(unichar, [0])

    # Currently unused function for tallying a "total score" from the counts
    def totalScoreStr(self, counts):
      def score(cnts):
          MID,HIGH = 9,10
          return (16*cnts[1] + 8*cnts[2] + 4*cnts[3] + 2*cnts[4] + cnts[5]
              #+ 0.5*cnts[6] #+ 0.25*cnts[7] + 2.5
              + cnts[MID] #+ 0.5*cnts[HIGH]
              - 4
              )
      myscore = score([c[1] for c in counts])
      maxscore = score([c[2] for c in counts])
      return  _("Score: %d out of %d (%0.1f%%)") % (myscore, maxscore,
          float(myscore*100)/maxscore)


    # FIXME: as it's html, the width doesn't matter
    def hanziCountStr(self, gradename, count, total=0, width=0):
        d = {'count': self.rjustfig(count, width), 'gradename': gradename}
        if total:
            d['total'] = self.rjustfig(total, width)
            d['percent'] = float(count)/total*100
            return _("%(gradename)s: %(count)s of %(total)s (%(percent)0.1f%%).") % d
        else:
            return _("%(count)s %(gradename)s Hanzi.") % d

    def rjustfig(self, n, width):
        n = unicode(n)
        return n + "&nbsp;" * (width - len(n))


## Old version of hanzi-searching code, for reference.
#
#hanzi_FIELDS = ["Expression", "hanzi", u"한자", u"漢字",
#                "Kanji", "Hanzi", "Traditional Hanzi"]
#
#    def genhanziSets(self):
#        self.hanziSets = [set([]) for g in self.hanziGrades]
#        mids = self.deck.s.column0('''
#select id from models where tags like "%hanzi%"
#or tags like "%Korean%"
#or tags like "%Kanji%"
#or tags like "%Japanese%"
#or tags like "%Hanzi%"
#or tags like "%Chinese%"''')
#        fmids = []
#        for f in hanzi_FIELDS:
#            fmids2 = self.deck.s.column0(
#                "select id from fieldModels where name = :f",
#                f=f)
#            fmids.extend(fmids2)
#        all = "".join(self.deck.s.column0("""
#select value from cards, fields, facts
#where
#cards.reps > 0 and
#cards.factId = fields.factId
#and cards.factId = facts.id
#and facts.modelId in %s
#and fields.fieldModelId in %s
#""" % (ids2str(mids), ids2str(fmids))))
#        for u in all:
#            u = unicodedata.normalize('NFC', u)
#            if ishanzi(u):
#              self.seenhanzi.add(u)
#              for s in self.hanziGrade(u):
#                self.hanziSets[s].add(u)

    def genhanziSets(self):
        self.hanziSets = [set([]) for g in self.hanziGrades]
        chars = set()
        #self.mids = []
        for m in self.col.models.all():
            if True:#"japanese" in m['name'].lower():
                #self.mids.append(m['id'])
                for row in self.col.db.execute("""
select flds from notes where id in (
select n.id from cards c, notes n
where c.nid = n.id and mid = ? and c.queue > 0) """, m['id']):
                    chars.update(row[0])
        for u in chars:
            u = unicodedata.normalize('NFC', u)
            if ishanzi(u):
              self.seenhanzi.add(u)
              for s in self.hanziGrade(u):
                self.hanziSets[s].add(u)


    def report(self):
        self.genhanziSets()
        counts = [(name, len(found), len(all)) \
                  for (name, all), found in zip(self.hanziGrades, self.hanziSets)]
        out = (_("<h1>Hanzi Statistics</h1>The seen cards in this collection "
                 "contain:") +
               "<ul>" +
               # score
               #_("<li>%s</li>") % self.totalScoreStr(counts) +
               # total hanzi
               _("<li>%d total unique Hanzi.</li>") %
                 len(self.seenhanzi) +
               # hanzi not on lists
               "<li>%s</li>" % self.hanziCountStr(*counts[0])
               )

        out += "</ul><p/>" + _(u"Statistics:") + "<p/><ul>"
        L = ["<li>" + self.hanziCountStr(c[0],c[1],c[2], width=3) + "</li>"
             for c in counts[1:len(freqHanzi)]]
        out += "".join(L)
#        out += "</ul><p/>" + _(u"HSK levels:") + "<p/><ul>"
#        L = ["<li>" + self.hanziCountStr(c[0],c[1],c[2], width=3) + "</li>"
#             for c in counts[len(HSKHanzi):]]
#        out += "".join(L)
        out += "</ul>"
        return out

    def missingReport(self, check=None):
        if not check:
            check = lambda x, y: x not in y
            out = '<a name="missing">' + _("<h1>Missing</h1>") + "</a>"
        else:
            out = '<a name="seen">' + _("<h1>Seen</h1>") + "</a>"
        for grade in range(1, len(self.hanziGrades)):
            missing = "".join(self.missingInGrade(grade, check))
            if not missing:
                continue
            out += "<h2>" + self.hanziGrades[grade][0] + "</h2>"
            out += self.mkhanziLinks(missing)
        return out + "<br/>"

    def mkhanziLinks(self, hanzi):
        out = '<font size=+2>'
        out += "".join([self.naverhanziLink(h) for h in hanzi])
        out += "</font>"
        return out

    def seenReport(self):
        return self.missingReport(lambda x, y: x in y)

    def unlistedReport(self):
        out = '<a name="unlisted">' + _("<h1>Unlisted</h1>") + "</a>"
        out += self.mkhanziLinks("".join(self.hanziSets[0]))
        return out + "<br/>"

    def naverhanziLink(self, hanzi):
        # base="http://dict.cn/"
        base="http://characterpop.com/explode/"
        url=base + hanzi
        return '<a href="%s">%s</a>' % (url, hanzi)

    def missingInGrade(self, gradeNum, check):
        existinghanzi = self.hanziSets[gradeNum]
        totalhanzi = self.hanziGrades[gradeNum][1]
        return [k for k in totalhanzi if check(k, existinghanzi)]

    def controlButtons(self):
      buttons = [
          "<a href=\"javascript:$('#missing').toggle()\">Missing</a>",
          "<a href=\"javascript:$('#seen').toggle()\">Seen</a>",
          "<a href=\"javascript:$('#unlisted').toggle()\">Unlisted</a>",
          ]
      return "<p>" + "<br/>".join(buttons) + "</p>"

def genhanziStats():
    s = hanziStats(mw.col)
    rep = s.report()
    rep += s.controlButtons()
    rep += '<div id="missing">' + s.missingReport() + "</div>"
    rep += '<div id="seen">' + s.seenReport() + "</div>"
    rep += '<div id="unlisted">' + s.unlistedReport() + "</div>"
    return rep

def onhanziStats():
    mw.progress.start(immediate=True)
    rep = genhanziStats()
    d = QDialog(mw)
    l = QVBoxLayout()
    l.setMargin(0)
    w = AnkiWebView()
    l.addWidget(w)
    css = "font{word-wrap:break-word;} div{display:none;}"
    w.stdHtml(rep, css)
    bb = QDialogButtonBox(QDialogButtonBox.Close)
    l.addWidget(bb)
    bb.connect(bb, SIGNAL("rejected()"), d, SLOT("reject()"))
    d.setLayout(l)
    d.resize(500, 400)
    restoreGeom(d, "hanzistats")
    mw.progress.finish()
    d.exec_()
    saveGeom(d, "hanzistats")

def createMenu():
    a = QAction(mw)
    a.setText("Hanzi Stats")
    mw.connect(a, SIGNAL("triggered()"), onhanziStats)
    mw.form.menuTools.addAction(a)

createMenu()
