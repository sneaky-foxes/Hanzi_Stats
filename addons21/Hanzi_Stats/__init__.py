# -*- coding: utf-8 -*-
# Modified Hanja plugin to count statistics for Hanzi (simplified)
# Copyright 2014, 2016-2018 Trevor L. Davis <trevor.l.davis@gmail.com>
# Copyright 2018 Kyle Waranis <infernalis@gmail.com>
# Copyright Roland Sieker <ospalh@gmail.com> and Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright Ben Lickly <blickly@berkeley.edu>
# Copyright Damien Elmes <anki@ichi2.net>
# 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
import unicodedata
from anki.hooks import addHook
from anki.utils import ids2str
from aqt import mw
from aqt.webview import AnkiWebView
from aqt.qt import *
from aqt.utils import restoreGeom, saveGeom

## Code snippet from Chinese support
def addchars(chars, txt):
    "List each chinese character, with its earliest study date"
    try:
        for c in txt:
            try:
                if re.match( "[\u3400-\u9fff]", c):
                    chars.add(c)
            except:
                chars.add(c)
    except:
        pass


freqHanziDefault = [
    ('Unlisted',''),
    ('HSK Level 1','一七三上下不东个中么九习书买了二五些京亮人什今他们会住作你候做儿先八六关兴再写冷几出分前北医十午去友叫号吃同名后吗听呢和哪商喂喜喝四回国在坐块多大天太女她好妈姐子字学客家对小少岁工师年店开影很怎想我打时明星昨是月有朋服期本机来杯果校样桌椅欢气水汉没漂点热爱爸狗猫现生电的看睡租米系老能脑苹茶菜衣西见视觉认识话语说请读谁谢起车这那都里钟钱院雨面飞饭高'),
    ('HSK Level 2','丈两为乐也事介从以件休但体便公共准别到务动助千卖可右司吧告员咖哥唱啡因场备外夫奶妹妻始姓孩它完宜室宾就左已希帮常床弟往得忙快思息您情意慢懂房所手找报教新旁旅日早晚晴最望条次歌正步每比汽泳洗游火然牛玩班球瓜男病白百真眼着睛知票离穿站笑笔第等篮累红纸绍经给羊考肉舞色药虽蛋表要让诉试课贵走足跑路跳踢身边过运近还进远送道铅错长门问间阴雪零非题颜馆鱼鸡黑'),
    ('HSK Level 3','万且世业主久乎于伞位信借假健像元其典冒冬冰决净刚刮刷刻力办加努包化半单南卡历参又双发叔变口句只史向周响哭啊啤嘴园图地坏城境声复夏头奇如姨婚季安定实害容层居山差己市带帽干平应康张当心必忘怕急怪总惯感愿戏成或才扫把护担择拿换据接提搬放故数文料斤方旧易春更末朵李束板极查树根梯检楚楼段求河法注清渴满澡灯炼烧照熊爬爷片牙物特环理瓶甜用画界留疼瘦皮盘目直相短矮碗礼秋种空突答筷简算箱糕级练终结绩绿网者而耳聊聪育胖脚脸腿自舒般船节花草蓝蕉行街衫衬被裙裤角解议记讲词该调赛超越趣跟轻较辆迎迟选遇邮邻酒重铁银锻闻阳阿附除难需静鞋音须顾风饮饱饿香马骑鲜鸟黄鼻'),
    ('HSK Level 4','与专丢严丰丽举之乒乓乘乱争云互亚交亲仅仍仔付价任份众优伙传伤估低何使例供保俩修倍倒值停偶傅傲允光克免入全具养内况凉减刀切划列则判利剧剩功励勇勺匙区博占卫印危即却厅厉压厌厕厚原厨及反取受另台叶各合否吸呀味呼命咱咳咸售嗽困围圾址坚垃基堵塑填增士处够失奋奖存孙寄密富寒察导封将尊尔尝尤尽局展巧巾帅并幸幽广序底度座建弃弄式引弹彩律微忆志怀态怜性恐恼悉悔惊惜愉慕懒戚戴户扔扬扮扰批技折抬抱抽拉拒招拜拾持挂指按挺授掉排推播擦支收改效敢散敲整断族无既普景暂暑暖术杂材松林染柿标格案桥桶梦棒森棵植概橡款歉止此死母毕毛民永汁汗江污汤沙油泉泼洋洲活流济浪海消深温演漫激烟烤烦熟父牌猜琴甚由申疑登盐盒省矿码研破础硕确示社祝禁福秀科秒积程稍究穷窗竞竟章童符笨签管篇籍粗精糖紧约纪线细绝继续缺美羞羡羽翻耐职联聘聚肚肤肥肯胳脏脱脾膊膏至航艺苦获萄落著葡虎虑袋袜观规言警计讨许论证评译诚详误谅谈谊象貌负责败货质购费贺资赚赢赶趟距躺转输辛辣连迷适通逛速遍邀郊部酸醒释量金针钢钥键镜闹阅队际降险陪随页顺预餐饺饼首骄验骗鸭麻默鼓龄'),
    ('HSK Level 5','丑丝临义乏乖乙乡亏产享亿代令仿企伟伴伸似余佛佩依促俊俗俱倡偷偿傍催傻兄充兑兔兵兼册军农冠冲冻凌凭击创初删制刺剪劝劣劲劳势勤勿匀匆匹升华卧卷厂厘厢厦县叉叙古召吐吓吨含启吵吹吻呆咨咬品哈哎哲唉唯善喊喷嗓嗯嘉器嚏团固圆圈土均坦型域培堆塘墙壁壶夕夜夸夹奈套妇妙妨姑委姥姻姿威娘娱娶婆媒嫁嫩孕孝宁守官宝宠宣宴宽宿寂寓寞寻寿射尘尚尺尾屈屉届屋属屿岛岸巨巴币布帘席幅幕幻幼庆库府废庭延弯弱强归录形彻彼征待德忍念忽怨恋恢恨恭恳恶悄悠悲惠惭愁愧慌慎慧慰憾戒战扇托执扩扶承抄抓投抖抢披押拆拍拐拥拦括拳拼挑挡挣挤挥振捐损捡掌控措描插握搜搞摄摆摇摔摘摩摸撕撞操政敌敏救敬斗斜施旦旬昆映显晒晕智暗曾替朗朝木未杀权村构析枪架某柔柜柴核桃桔档梨梳棋椒模欠欣欧歇武歪殊毒毫毯氛汇池沉沟治泛泪洒洞派浅浇测浏浓涂润涨淘淡渐湿源滑滚滩滴漏漠潮灰灵灾炒炭炮炸烂烈烫煤煮熬燃燥版状犹狂狡独狮猪献猴猾率玉王玻珍璃甩甲略疗疯疲痒痛皂盆益盖盼盾眉眠睁瞎瞧矛矩石砍硬碍碎碰神私秘秩称移税稳窄立竹筑类粘粮糊糙糟素索紫繁纯纲纳纷组织绕络统绪绳维绸综缓编缩罚置群翅耽肃肌肠股肩胁胃胆背胜胡胶胸脆脖腐腰膀臭致舅舍良艰艳苗英范荐荣营蔬薄藏虚虫虹蛇蜂蜜蝴蝶血衡补裁装裔裹览触订训讽设访诊诗询谓谦谨豆豪豫贝贡财账贴贷贸赏赔赞趁趋跃践踩蹲躲轮软载辅辈辑辞辩达迅返违迫述迹追退逃透逐递途逗造逻遗遵避配酱醉醋采钓铃链销锁锅闪闭闯闲防阵阶阻陆陌限隔雄集雷雾震霉青靠革鞭顶项顿领频颗飘食饰馒驶驾骂骤骨髦鬼魅麦鼠齐齿龙'),
    ('HSK Level 6','丁丐丘丙丛丧串丸乌乞乳予井亡亦亭仁仇仓仗仙仪仰伍伏伐伦伪伯伶伺佣佳侃侄侈侠侣侥侦侧侨侮侵俐俘俭俯倔倘倦债倾偏储僵僻儒兆党兜兢兽冤凄凑凝凡凶凸凹刊刑券刹剂削剑剔剖剥副割劈劫勃勉勘勾协卑卓卸叛叠叨叭叮叹叼吁吉吊君吝吞吟吩吼呈呕呵呻咀咋咐咙咽哀哄哆哇哑哗哦哨哺哼唆唇唐唠唤唾啃啥啦啬啰啸喇喉喘喧喻嗅嗦嗨嘈嘛嘱嘲嘿噪嚷嚼圣坑坛坝坟坠坡垂垄垫埋堂堕堡堤堪塌塔塞墅墓墟墨壤壮壳央夺奉奏奔奠奢奥奴妄妆妒妥姆娃娇婪婴媳嫂嫉嫌孔孤宅宇宏宗宙审宪宫宰宵寝寸寺尖尬尴尸屁屏屑屡履岂岔岗岩岳峡峭峰峻崇崖崩崭嵌川州巡巢巩巷帆帐帖帜帝幢庄庇庙庞庸廉廊廓异弊弥弦彰役径徊徒徘徙御循忌忠忧怒怖怠怯恍恒恕恩恰悟患悦悬悼惋惑惕惦惧惨惩惫惮惰惹愈愚愣愤慈慨慷憋截扁扎扑扒扛扣扭扯抑抒抗抚抛抵抹拄拌拓拔拖拘拙拟拢拣拧拨拽挎挖挚挠挨挪挫挽捆捉捍捎捏捕捞捣捧捷掀掏掐掘掠探掩掰掷揉揍揭援搀搁搂搅搏搓搭携摊摧撇撑撒撤撼擅擎攀攒攻敞敷斑斟斥斩斯旋旗旨旱旷旺昂昌昏昔昧昼晃晋晓晤晨晰晶晾暄暧暴曝曲朴朽杆杖杜杠杰枉枕枚枝枯柬柱栋栏株栽框桑桨梁梢械棉棍棕椎椭榜榨横橙欲欺歧歹殃残殖殴殿毁毅氏氓氧汰汹沃沐沛沧沫沮沸沼沾沿泄泊泌泡波泣泥泰泻泽洁津洪洽浊浑浮浴浸涉涌涕涛涩涮液涵淀淆淋混淹添渔渗渠渡渣港渺湖湾溃溅溉溜溪溶滋滔滞滤滥滨漆潇潜澄澈濒瀑灌灭灶灿炉炊炎炫烁烘烛烹焦焰煌煎熄熏熨爆爽牢牧牲牵牺犬犯狈狠狭狱狼猎猛珠琢瓣瓦瓷甘甭田畅畏畔畜番畴疆疏疙疤疫疾症痕痪痹瘤瘩瘫瘸瘾癌皆皇皱盈监盗盛盟盯盲眨眯眶督睦睬睹瞄瞒瞩瞪瞬瞻砖砸碌碑碳磁磅磋磕磨祖祥祸禽秃秤稀稚稠稻稼稿穴窃窍窜窝竖竭端笼筋筐筒策筛筹箭篷簸粉粒粥粹紊纠纤纬纵纹纺纽绅绎绑绒绘绣缀缉缔缘缚缝缠缴罐罕罢罩罪署翔翘翼耀耍耕耗耸耻聋肆肖肢肪肴肺肿胀胎胞脂脉腔腥腹腻腾膛膜膝膨臂臣舆舌舔舟舰舱舶艇艘芒芽苍苏苟若茂茎茫荒荡荤莫菌萌萎董葬蒂蒙蒸蓄蓬蔑蔓蔚蔼蔽蕴蕾薪藐虏虐蚀蚁蚂蛮蜡融蠢衅衍衔衰衷袍袖袭袱裂裕裳覆觅誉誓譬讥讯讳讶讼诈诞诧诫诬诱诵诸诺诽谋谍谎谐谜谣谤谬谱谴谷贤贩贪贫贬贯贼贿赁赂赋赌赖赠赤赴趴跌跨跪踊踏踪蹈蹋蹦蹬躁躬轨轰辉辐辕辖辙辜辟辨辫辰辱辽迁迄迈迸逆逊逝逢逮逼遏遣遥遭遮郁郎郑鄙酌酗酝酬酷酿野鉴钉钙钝钞钦钩钻铜铭铸铺锈锋锐锤锦锲镇镶闷阂阐阔阱陈陋陡陵陶陷隆隐隘隙障隧隶雀雅雇雌雕雹霍霜霞露霸鞠韧顽颁颂颇颈颖额颠颤饥饪饲饶馅馈馋驰驱驳驻骚魂魄魔鲁鸣鸦鸽黎'),
    ('Simplified Top 500','的一是我了不在有人个这他上大来到中们就说时你为学国要子和地也生以会着年出下那可里家后得么好过小天她看自多对没都去还能发心道用很作想然开于日而之成经面事起现行点文样方如所前当本老同法只回分情些什最公动从间但长把知意月者话高手主理己工实头女问无进新车外其种定儿业两三给又因明电与美次全教名已等打被真关第正机十力身做部见民走西几感比市门语体果重让二相场东加表此水常路位别题再口书内活信将通记觉北候气师爱应才海性声报员边安期听向特太少更入网先平化合并眼论张代每提目四使接吃由山总直放元白或物解利像系品考色世度孩处今原字住它件友怎笑校数产认政受光院金任结交风京司完区影带何乐吧制难及建英非花快该亲管马写音清告斯台万华望至城资房找科服钱便许保务男象思南五始言吗呢流立站各程王神却片妈变请叫社收跟专条计单办反费式啊干量往复传界死展喜拉格欢周强习广德图空转军留容视晚求连指早尔持商近星远满共读游深价客联红达导包李算设命术战士离队运买且基试注选观识楼节讲越义精号整林半证坐准息轻拿百级育决统改火必照调刚班形克线评步领热母失首装演酒权类夫历课阿功组需取哪布饭医研较青根父据查朋病即集江球兴脸示店则黑姐六版送究确引备阳飞未'),
    ('Simplified Top 1000','您治随谁约标切易室香终诉议参造谈规岁具际消答错八乎句念技落夜推故局似段志况支黄衣曾词史歌州爸料古尽极谢众排园希另团续午石哥米除罗馆章虽质帮底响紧足称双巴倒村千够济亚怕居案显修画府警争福苦投断般绝存突奇食份街脑简初毛助玩待票愿创久户味闻党省低剧静纪击睡穿春举景云细七害河弟责汉停列宝龙刻农哈差刘亮官钟九板背型陈丽境角营仅态令录独源项编跑委护兰印伤超环值块供采艺卡职竟器赛否雨按维皮严喝旅企戏笔速养增卖验依堂座朝某假群脚破族致惊甚菜忙土冷须围温微慢限木招呀博换律划毕优介左急唱梦察效血模右武杀层树普势掉铁获富婚痛银免革冲载派置股密属永练翻油牌短负卫拍床怪继适礼怀遇例纸乱雪充激幸藏访乡止呼牛苏港曲灵奶压赶状若款批妹担典素仍配顺贵爷顾积沙娘胡敢织余餐承药嘴屋轮兵彩预佛副草顶劳沉威松肉诗尼烟施销疑择跳肯讨构追材旁玉露靠杂忘舞杨县坚篇善奖页套邮恶索睛波欧率险洗汽鱼洲熟授防盘窗厂良湖范财异货升宁趣迷康楚呵陆退临夏休灯协概托训醒顿暗旧购健码封售贴湾秀厅庭播阅抱散登坏渐宣哭纳田检绍付鲜益软庆镇搞移默吸席妇洋叶救括舍络互啦述桌斗既抓烈策冰秋汇浪懂胜辑茶守丝莫犯阵伙译罪架婆泪聊略桥耳牙签韩补归迎恐占困摇均奥圣伯尚'),
    ('Simplified Top 1500','昨培绿伊寻姓附船册申误雅弄野判脱忆遍麻坛借监忍妻控恋秘蓝释折缺阶俄币赵姑透鸡束孙端租童忽智齐掌执帝测偷杯吉降墙谓征宿偶私狗漫晓挂握拥扬累挺探抗媒筑央宫虑烦减欲惯遗岛季吴弹丁卷淡辆含盖鲁丰唐梅挥箱狂序享冬鬼恩摆乘兄败巨镜喊刀烧伟雷鼓袋泽禁枪航宗毒审硬抽阴闹皇迫伦宜暴荣额操途巧隐咱蒙址圆贝蛋川庄祖漂努输佳骨幕亿腿盛末鞋尤绩凡纯悲厚危域塔稿净析嘛虚挑宽圈混毫晨君频伴勇寒迹诚朱峰疗零诺弃避尊逃雄税亡摩戴闲呆遭拜聚讯攻虎射刊杰珠宾摸奋库徐刺陪竞舒核偏础献闪骂摄劲敬叔弱纷唯闭隔固帖欣塞抢伸缘针甲徒触碰豆珍仿凉粉逐暖森稳萨惜映姆敌饮奔哦郑替赞览潮残赏融订饰丹琴丈启龄键鸟猫辛洞汤妙瑞俩羊寄颜孤柔恨亦坦延染悉冒麦缓返猪询距吹猜荐瓶敏娜磨朗糊宇骗岸仔贸梁爆辈搜叹洛铺抬甜魔剑津俗炼豪损怒祝灰洁迅朵胸届骑震旦泉孔幅扎勒侧刑宋悄爬予慧横档吓钢犹沿穷堆凭飘坡眉递插估曼肩泰促疼尾杜剩嘉搭燕腰滑迪炸沈疯惠灭泡荡符黎澳拒仪繁彼汗肥凤竹莱裤详诸旗瓦躺谷闷绪辉壁拖寺紫链幻患芳菲傻丢郎罢描猛忧搬违仙糖迟尖挤洪咖艾辞督壮幼拼乌锅稍涉秦缩滚冠贫郁酸腾啡仁烂番鼻润醉锁撞驾尝肚勤胖扫泥狠耐籍池彻励浓焦碎沟隆碗董擦暂薄忠倾障盟奏谋椅氏'),
    ('Simplified Top 2000','昏魂傅浮夺井奈帐柳甘瓜抵吐匆粗哲赚殊貌扩废胆怨措扣娃俺赖斤湿栏仰梯怜综曰晴慰驶姨绕召狼邻倍幽郭厉惑摘铃悠陷伍嘿脏岗玛艳夹俱填厌颗灾乔酷滴挣敲凌滋裁逼狱腐拔聘瘦跃戒兼邓踏症乃埃径愤罚圳刷恰弯潜振悔污荷乏凯祥聪植纽寂侵晶瞧躲卢尘惨娱崇厨涛墨疾锋桃扑阻荒晃柜佩玲屁拨俊昌邀邦撒衡肤盒扔诞涂锦粮泛劝吵陶堡肖涨迁钻爽悟旋璃遥驻鼠莲皆莉昆浅奉矿桑捕恢咬液邪虫塑盗帅埋毁扭牵啥允扰吻姿赢侯丧枝凶拾赫赴屏帽玻愈耀苍麽宏艰踪誉盾慕懒揭伏晕炮涌嫌氛厦颇逛辣脆饼耶扶辩摊炎卧炒纵串厕饿肃窝宅慌鸣蒋援溜袖敦拳稀裂羽桂牢赠嫁熊哎蒂扮雕添贺弗尺於辅曹哀屈拟尸践截棒冯疲袭燃柏饱寿恼捐唇渡眠凝喂偿畅爹悦欺硕莎掩篮贡跌盯秒鉴烤亏岩雾翼贾乳庙孟萧丫傲浙臣跨押臭榜矛挡廊陌缝阔丑妮轰拆棉芬怖贯赤扯抚寸诊抖吕垂堪漠捷臂赔劫欠杭棋翰贪滨渴贷浩汪牧膀茫诱慈碍夸柱蜜仇啤糟趋嗯挖喷巾苗哼愁浑琳债唤迈勃殿朴夕斜羞炉惧储灌墓薪赌抹巡胶穆尿掏舌娇裙呈芝唉悬姚挨奸乙瞬盆胎睁浴咨煤宪剪抛踢肠筹寓忌绘抄缠胞糕乖吊滩亭撑孕凑署魏杆拐删驱豫阁耗垃憾姻溪贼盈圾脉逢淋萍衫贤鸭翠舅舟痕轨潘伪砖妆祸恒弥勾蛮抑胃叙覆纠狐霞扇歉漏账兽泳遵笼辽毅堵割霍斑铜昂姜盼痴券丛箭'),
    ('Simplified Top 2500','摔旺衬柴疆浦愉澡虹绵吞撤袁腹霸盐洒巷蔡齿嘻奴帕谊笨岳颤碟逻辱瞪绑鹏晰侠携陵脖暑仓蛇腔煮桶宴厢魅捧冻谱慎披翔牲皱廉卓纹喘彭胁兔惟猴柯涯寞逝械惹哇鸿妖孝碧颠碑湘趁骚浏蝶戈徽疏岭筒歪郊兹捉砸裸泄辨趟锐匹韵愣葡吾姥驰淫猎庞瑰劣绳廷玫御剂哄恭疫循肌罩慨匙讶宠薇卜贩苹催谨坊侦誓怡翁岂晋吟婴棍踩腊颖叠嫩戚骄吁拘葬歇寝斋愧淘萄遮棵葛僧泊谅雇钥坑晒谎粒漆谜刹蓉爵衰磁闯盲枕锻框斥衷沃卑泼逆窃叉羡筋拓拦愚嗓栋娟脾庸卿峡赋裹逗玄谐涵妥塘灿崔肝役刮谦蹲枯茂肿汁瞎铭耻渠纲罐咽扁涓逸嫂辰婷熬淑勉挽舰嚷枚裕狮匪纱媳捡砍撕剥韦媚帘甩雀蓄蹈斌寨兜牺轿沾跪冤粹胳煌乾熙矮帆丘儒仗膊逊虾脂泣遂仲咪捏尬尴耍叛鹰纤侍娶伐殖祭兑喻妨鹅蒸吼酬肺咸囊颁契壳哩陕傍霜瑟屠哗旨浸碌渔垫吨藤伞哟歧遣邱馨咕哑裔莹薛宙蕾昭腻倦禅窄畏侣矩酱纺珊弦诵蜂函衔削芒瓷茅塌咳墅喇凳雁鲍驴沫锡菊鹿祈噢淀攀殷锛挪倩琪棚兆翅壶淮茨倡顽膜咋癌仆勿匠嘲呜钉喉饥烫渊搂侨溢颈躁龟凄萝鼎沪妞旬贞寡铅肆嘟竖叮趴宰缴粘霉履芙蓬禽秩钓惩嘱饶奢厘掘梳椒涩坠狭罕兮稻鹤乞侃咯膝矣恍彬崩喃樱蠢苑烛绣耸轩佐氓亩僵妓耕谭枫梨胀琼凰蟹逮坪穴昔赐蜡燥睹犬撰艇眨彦橡驳袜溃竭镑辜绒粤掀啸敞潭黛丸骤蔬姊'),
    ('Simplified Top 3000','粥蹦歹亨冈鸦叨擅哨诈喧坎芦鞭氧甸蝴夷咧坟菌婉沧靖雯揉缸潇咐弊咒昧虐陋搏祷痒钩葱宵眯搁掠瞒屡毯菩煎乒辟搅宛鄙栽嘎娅甫稚讽腕呐旭钞膏谣啪恳袍妄卦瘾浆佑耽磊魄钦屑瑶贱尹笛肢崖舱婶俯幢杉桐靓屯魁捞滥酿醋暮堤窜杏絮挫惶彪巫沸叭巩壤琢脊篷弓颂拎旷坤株邵蔽卸隶妃颊辖茵扒舆螺焰筷郝峻浜妒怯撼斩蚊楠渗躯吱陀梭澄琐仑茹芯喔豹讼惫岚嗦畜煞堕滞揣捂耿拽嚼摧秃匿朔驼憋荆萌畔焉捣芽滔淹熏朦骆贬拢瑜桩芭捆稣艘饺藉蕴曝弘揪坝咚荫爪诀焚冥俏粪烁蚁尉瞅枣浇稽橱郡钧眸擎詹乓敖拌拱倪哉溶垮剖胧姬囚悼狸茄炫屎佣僻芸翘劈槽隙俭澜彤轴怔喀铸嚣钮巢裳炭扛倚沦栗馈衍阎拂撇绸杖灶淌觅攒噪蚂嫉熄瞄勺拣颐厄璇腥砂鸽倘琦躬嘘咏勋晖禄蹭窥盏诧磕侄俘俞枉屉瀑蔚窟揽搓匀掐皓疚缕崎媛膨阐馒沛廖汝聂侮靴缀苟柄蹄巍筝斧呕翩坞惕旱窑绎拙拯芹挠汰窍卵淇瘫奕肾凸豁酥彰垒狄恤裴剔漓陡戳簿绅噜侈毙抒蔑麟莺绷讳棺沮谍茜饲诡喽楞募奎暇瞥蔓敛蝇丙渺譬嘀蒲庐蛙髦缅炳寥孜吭丐贿瘤栈吩卒惭涅洽烘叽聋皂澈寅焕吏镶朽拧薯涕奠顷渣眶瓣挚襟啼楷匈锤蒜鞠馅骏寇肇鳞檐棕逍蕉嗡嗽啃殴黯辫禾汹绽刃逾莞阮岔鞍嵌菇疤噩乍秉崭锣垄僚眷霖佬唠泻懈簸敷狡橙绰蛛灼谴哆蜀溅鑫邹萎菁橘凹聆咙浊闸炕禹铐槛杠唧'),
    ('Simplified Top 3500','猩滤瞻伺仕醇墩蚀嗅惚缚沐渝矶腺勘徊娥牡舔菱祠蹬嗨棠湛璧庚闺呻隧髓栖昼漾桔剃辐浣烹徘嘶梵迭兢唔祺砰捅嬉倔栅霓葫幺厮绞柿梧韧帜铲尧冀竿骇槐谬隋廓虞榕浠靡镖慷喳糙婿掷肪榴恕凿疮褐崛颓襄葵龚矫膛攘晤磅虔雍唾冶锈伶茎煽冉闽臀矢迄穗苔晌炖萃肴樊呗暧屿禧迦砌梢眩娴哮赎拇庵憨愕缉揍怅纬凛肘刁缆咦阜簇阀诫藩璐窦吆唬呛谛稼筐辙溥诏蝉汀埠漱邢阱溯窒蚕芜甭笋嫖窘埔溺嚎拭亢粟钝辗憧跺墟扳茉啧嗜枢眺霄榻暨曦撩锯桦赁姗钙婪淳悍缔兀隽瞿肮拷珑苇忏莽挟撮睫榄蓓杩悯沁碳痰虏鸥呃疙憬搀榆琅烙憎跋衙澶瘩孽茬畴绊洼癫涔棘卉懊腮斟炊遏癖盔槟脯椎铝秽嫣妾沥牟袱擒娄恬驹绢褪苛梗椰嗒荔蔼滇弧叁妍彷沼鸳寰伽悴筛掺峨昵绚笃泌橄霆夭怠缪臻鹃庇踱憔捍俐扼叩讥缭诬漉袅猿哧瞩蜘祀蝎涮肋惦惬狈荧袄厥炯懵棱咔磋嘈斐晦趾讪呱晾蕊蕙吝酌驿睬睿刨睦蓦馍秤煲滕鼾钗惺涡祁疹诠琉昊哽甄掰绯戎佟鸯邑柬峭犁懦戊硫蘑哒睐赃澎曙馋沽裘诲亥忿氨拴瞟膳娼赦梓莓笠靳驯箕穹丞惰褥韶酪痞瀛榨踹玮犀俨羁涟挎咀逞涤筱匣篱汕螃缎荤坷窖灏腑颅蔷缤偎痘酣叼簧诅褂酝抿樵攥熔嚓瑙崽鄂舵柠瑕栓蛤猾卤毋芊捶屹漪飙曳篡抠秧笙寐羚珀札馀昕跤琛鳄遐檀瞳渍氢恺硅盎垢喋谤茸梆鹦阪炬菠褒翟绮闵硝镐羲陛炽捎妩樟'),
    ('Simplified Top 4000','嗤摹腆嗣囔晏镞茗迢鹉蜷砚骞碱礁奄亵藻廿瓢侬辄雏惋芥檬庶辍町雌拚绥蜗惘匾矜锄钳螂舜嗔芋璋瘪伎禀羹娓鬓祟骡惮濒忡冕孰卞汩烨粱禺卯歼釜凋隘瑾匡黝恪甥桓翡酋咎畸鹊悸炙忑帷栩瑚铮萤悻剿瑛侥霎镀忐腌阑噬藕彝垦黏痪迸哺衅濂宸怦冢紊嗬蝠岑竣殉惆喵撬琶碾瀚扉噗朕殡轧铎瞌汲沌蹋赘倏瘟诽萼鲨婧婕拗韬锥巳杞弛觑徵锲渲瘸悚贮峙掂慑濡贻酵搔阙徙腼奚咄糯籽渎瀹暄毡跷擂巅俑蝙圭舶蘸逅辘炜诛沓悖淆讷噎狞涧哝堰摞邂踊汾匕蜒磷殃萦潢蚌苯籁琵潲猖茧稠萱谕帚鲤莘绛弈蕃铛漩熠唆踉嗷泸撅殆蜓羔箫钵垣邃黔浒隅镯笺飓跄猥遛呸霹麓峦豚撂驭剁蟆瞰蜿芷婊躇遁鲸骸辕粽烽缮湃岖酉踌蜻毗煜邯佼峪迂蹑脐吮雳曜靶濮邸篓咆涎荟赂匮麒冽淤纂矗睽皙驮壬抉赣嗖蹿啬诣蠕泵戛焊癸婢潺佘渥潦诃囱戌孚啄玺翌纶痊迥陇鳖谧谏崴钰仨拈圃饵毓汶熨髅蔗唏姣踵渭戮寮淼吠箍耘囡娑偌痹缁嚏蹊抡骷轶楣郸唰捺癞醺荼癣嵩祯皖谚桨苞恃榭薰伫忱箩咫撵宦搐拄帛淅蟑胯狙噼裆揖嫔苓蜕沱呦燎氯馄咣娆锺佯饨泞幌羌饪徨泾沂忖倭啜褶簌皑剌猝肛斓叱篆靛岐恁窿娩弼闾忒竺筠盹绫锵脓桢霏珂蟀磐疵坯骋摁腋镣铡憩慵纫坂璀蛾骥嬷闫姝垛谙钊抨傣臆珈烬偕喏鹭锚搪镌恣筏楮踞讹蛊冗懿袒塾镰韭荪踝泯蚤醛敝痉镓胥壕噶捻帧糜渤舀跚貂'),
    ('Simplified Top 4500','谆狰峥氲蹇咂胭晟恙缈笆咿昙篝鸠掖壑粑壹椿亟蹙覃鱿揩漳椭媲膺蹒烩瓮夥臧荀淄啷谒筵惴怂嗲芩飒臊葆咛蟋嗝泱飕狩酗胚掬蹂锷弩坍铿璞洱褚孵髻娣瞠嗑亘鳌耷榈嗳孺溉缥仄翊滢躏璨岱叟耙嫦豌擞灸胰榔甬捋枷痣皈鬟挛杈跻锹棣噔浼缨绉琥轼盅蝗恿釉缄雹窈榛舷扈纨啕涸柚鸾埚眈爻蝈疡娌皎枭牦娲蓟霾捱泓砾杳瑗霭焖锭阂稷剽龌窕闳怆攸跛糠俚佃旌歆镊祛楂粼敕沏虱埂蟒骼甯戍龊恻佚垠璁蹩酶蔫纣谩馁谑缰蛰嘭婵骅翎幡诙羯嗟皿浚煦邋鞘邝犊蚓喱砺佰罹痔搽泗跆潍舫搡ㄥ踮蚯蟠鳗掇呷掸氮蛐缇碉锌阖黠阉赡霁柑伢獗纭掳隍哐簪蛟闰潼琏裱邬颔冼掣蟾唷诩栾熹偃钾荻皋胤饽晔诋匝碴渚ㄨ遢荃槌夯懋宕烯袂闱陨锢呓湄饷摒嚅蛀堇桅螳衩荨褛坨扪绂牒犷璜栀噙诘蒿玷赈嵘饯茁铢拮秸诶蜈魇沅呲礴牍苒汴琰祚逵衮菡笈妊盂睾瘠攫翱箴恸鲫镙芮愠湮焱刽氟弋婀飚啾玟怏瘁罡铉猬偈臃嫡嘹汛鹫咻睨衲桀秆彗氩夙臾侗杵涣娠昀鲲罂颍椤萸徉嘤嗫姘桴鳝馥湍蚱愫挝镂戟贰娉钠噘炀俾骁珞龛胺藐颦赊稞晁徜啐怵绾罔苡臼噤阃榷孪傀迩荠糗焘骛佗搴蜚戾濑胄忪匍绔唁楹桧俟瞑噌俪噱盥挞睑疣瀵涝脍阆吒斡赳淞侏痤儡腓铀咩樨㈠饕镒蔻忻旮轲岌酮牯祗潞蔺豺劾孬垭丕囤漕岷镁旎枸擀幔馊郴宓挲瘴邈匐酯罄坳蠡迤迳浃嵋郅珏倌畦鬃锃淙谄衢蝌'),
    ('Simplified Top 5000','碘奂蛆洌麾ㄦ骰葭钜靥帔遽樽腩洙揿绺褴膘铧蚣傥蜃荞犟颀溟揄龇馏鸨袤趄圩浔髯滂晗潸颧鞑嘣谘玳卅恹澹氤遨谟橇趔郗胱痿堑濯崂殇栉剐楔徕麝烊瓒觊嶙仃讫銮颌妯雉睇倜旯揶柩痢蜢龈谗缑颉瘀蹉腴痫煨袈湟鳅磺奘觎蚪裟咤俸婺妤裨乜犒砣粕汞滦蹶聿洵茱咝餮韫厩㈡铨珉厝鸵箔抻诒锏ㄧ猕褰峋旖訇飨镳瓯耆绌庥庾刍滟觐唑芍碜悭骊鸪澧叵闩棂偻尕贲杲蜥懑吖灞姹缜囵岫诌砧孑喟赓轱妪墉汐囗颚胫铂觞酩畿鹑彳陂酊蓑磬啻铬铤聒赝鹂蚝嗵跎攮忾徇铹鹜佻砥杷妲谥蜴篾铠矾褓暹囫葑稔恂镭腚嘁莅啖嬴毽猷蓁缢蚩孀唢黢歙玖昱钏砝佝绻滓饬撸涿囿帼擢璺疽陲湫噫祉鹧噻畲疱斛珩誊镍燮殓泷ㄤ呤枇黜馗泠酚摈翦恫谲葳纾玑爿蛎锰诂艮獭鄱邺莆谀疟濠遑犄撷藓郦苜鸢焙膑哔琨讣弑蓿嵇铆诰嶂㈢鹄孱獒芫葩馕阒豉虬庖幄颢啮篙蹴嗄菅钿襁圜锂莠蜇幂蛹茏纰嘬烷仟嗥绶骜窠讴硌茴剜泅峒湎珲鼹淬鲑僮舐巽诿佤碣箸绗衾啵砭翳锨椋孛琬赧葺檄搠钛槁宥簋阕垅弁俎擤诟桠鹌隼汨耄肓橹骧瓤亳铄芪菏糅摺仞逡胴荚黍趸棹馔谪驸嘞屙掼佞椽夔羸伉媾柘萋囹涪屐靼膻棰阗喑虻沩粲苕豢忸桎珐舂琮勐炅缃妗侩笤荏秫狒晷逶鹞锉鹗藜莒稗牝柒怩痂镛淖蘅瑁姒楦忤鲈殒趿卟傩颏铳蕤阡赅阄鹘嚯圄呶邕梏薜孢龋镟遴揆蕨缱撺诨肽诳儆焯麋翕睢羿霰謇煸'),
    ('Simplified Top 5500','戗疸鲶竽缙猢鳕嵬驷殚髭硒矍骠裾獠啭铣伲戕毂掴鬈菸踅胛鼐谶曷瑭辇鳏怄楫笸赭钨绠傈镫淦篦倬鹳肄笳醴楝祢炷醚琚诤菖碚殁苌芡椴亻钺僭悌寤岿鳍觥暝蠹劭鏖衿蛔嵊燧腱痨肜槿斫遒粳糌绀踽舛耦讧挈哏蜍鞅桡阈舢氦唳聩畹篑埙薨韪骐昶饴乩槎鳟漯钎铰瘌酽氅耋醪洮绦弭醍欤嬗砀鄄喙蜊茯痍疥呖聃陔帏煊椹糍刎娈兖醮掮莴悱桉笏澍哞蛳茔逑谡擘笞醐骈螭稹槠镆沤涞铵ㄩ薏钤褡僳潋郜爨阌廪嘏狲埭咭郢砒氽岬纥綦泔喁痼祜狎阍爰孳痧倨荥妫鲇樾甑溧僖缛愍埸麂哂ㄚ郫薮鄢橐肱辔陉诮矽崆氵㈣菽氰螯躅蒯荦苫栎踯睥碇侉枥谌伥癜褙绱蒹跹邛邳沣痱恽殄诓酰鲟箧愆箐俳圪儋麸楸郓阚腭辎轸珥徭碛崧叻凫逦砷滁蘼鸩霈芾扦糨柞罅唛秣邰亍鞣顼荑虢绁螟椁獾轭绡踟罘侑崮犍橛堀颛抟钒讦鬻艄苋悒辊侪枞圻馐蒗芘戬庑髋貉墀谯瑷扌硼篁岘钹豕碓蓖簟崃筮俦庠缂榫阊痦怙嵯赉耒奁蹼杓沆莼泮栌鳃瓴唿邙铖洇裢渖圹獐蛭窨樯逖硷轳缗赍莜绋焐壅馑辚帙钴刈轫芨捩瘙囝绐苣驽鲠仝汊伧膈竦眦垩氐愎欹蓼趺貔逋佥鼬ㄟ黟苷忝痈蹰戢熵蜉啁锔潴砦鲔勖妣贽恚箬龃迨猱雎鹬荸燠蝼鲢陟檫煅鸷疝嫱锒俅昝龉凇矬罴呔洹塬铙傧楗臬茕蟥骟蘖猡郾枋纡骢趵蚧舸鄞捌枰峤幛栊榉鎏邗讵藿雒珙谔祆钯挹捭蒺穑溴啶猗赀垓泫皴呒镢镗蚜剡籴鲛魑貅氖茭钼胝'),
    ('Simplified Top 6000','蛏螓丶翮戆哓薅箝烃彀掾羟眇葚锟钡洄狷牖戡雠镏嘌媪莪怼瀣鬣ㄓ缫繇豇蓊濉渌芗螨璩铩訾縻檎魉桷旃瘘逄枳骝锱蘩黥炝妁鄯涠砻筲檗鼋疖疃鸹篪吡宀翥钚榘荇镬藁瓠黩盱椟侔雩腈癯糁杼狍畚筌鸬郧殳龅癔蘧荭苎粜鳜萏隗酢殍榧胪仡邾犸尻刿濞蕲箪垡酡菘魍笪埕黉凼璎笥硖矸昴溘沭耨齑ㄅ礅锑蚨笫蚶衽墒蟮溲酆螅鹩旄髌缟囟磴圮坻磔颡熘盍闼狻欷堞鲅胗鸱钣耜豸蝣溽芎鸶徼眙圉荽檩佶詈㈤沔瘢袢蚬拊嶷勰滠鹚怿呋跸耩嶝缶蔟骘艿疋岜卮彘ㄢ螫觚魈鲞郛谵秭溱孥畈滹徂玎莨氡嫫谰镉ㄣ缯穰钅镦柰谝菟磙蒌蠲淝蚵柢菰艹曩坼脔垌睚峁怛筇垆谮隹薹钌錾醅猊哌砬蛄纟鲷胼禳莳獬屣蛉嘧嫒丨痖鲮疴诔菀飧裰糸亓锴疠渑耔镡鬲餍倥棼坭膂氙隈肫溆隰鏊鲧骖睃ㄇ谂鲥躔觜蕻秕笊缦笄蕈灬萁孓瞽鞴庹铊椐嫜倮觇谠谳硪耪鬯裥哕旆锆阝偬耧炔夤跏黻眄汜彐狯锗鲱丿岙坩鹈畀郏阏鄣铱哙髫鲳逯篼鲵黧舡朐廨铗酹塍廛瘗忄赜憷镪硐礻帑嗪诜猹镔蓍郇贶裎蒡匏啉骶粢飑溏仵槭狺刂莩镝卩骓郯褊喈荜蠃鼙摭杪滗ㄆ桁豳槊墁舁蛩舨觌橼鼍鹕绲瘿阋暌麇毖帻垸跖卣籀崤鲰愀罨猓荩鲣峄蕖懔谖杌芰缣钬兕扃锶鞫篌ㄌ颟箜胨筚馓辏髑伛鳎麈浈怫埽艽嗾诹袷涑劬甙苴殛髂刖酐跬鳇辂髀煳芈皲咴垧镲燔钕鲂愦晡劢鞯蜮髟蟊ㄠ纛怍宄醯骒顸襦蚍柝颞搛拶驺锝鲡'),
    ('Traditional Top 500','的是不我一有大在人了中到資要以可這個你會好為上來學就交也用能如時文說沒他看那問生提下過請們天所多麼小之想得工出還電對都機自而子後訊家站心只去知國很台成信同何章道發地法無然但當於嗎本年現前最真新和因果意定點情其題事科方些清三樣此吧位作理行者經名什謝日正開話與實愛再華二城動比面高又或力應女種教車分像系長手次已明打太路起己相主關十間鳳外呢覺使該友才進凰她民著各全將少兩加回感式第球性老程把被公論及龍校別體重給聽水做常您見裡東風解灣月等啦部原美先音通管網區期錯否樂入找書讓四啊由選較數表內場它從快歡至立目社合望怎認告更幾考度難版頭喜許光今買算弟若統身記代號處完接計言字師並政玩張男誰山每結且星非建改連放哈活研直設陳報轉黨指五變氣西試希神取化物王任林單世受近義死便反士戰空隊跟卻北必業功寫影聲平臺員金討色則容檔片向妳市利興白強安央特議辦價總傳思花元叫保份求究呵件未決組萬竹級持笑投哪室曾走喔標流支獨貓卡需兄門共語海口阿線馬黃參般命視觀聯腦朋格兒八修料錢失吃住即另錄專象換基板拿遠速形孩備歌幫確候除界裝類講器南案畫英訴帶差乎量久掉似整引班迷圖制費賽奇識型超邊耶品舍雖始運李務權驗故六讀怪飛滿服夢收眼造念留課軍破'),
    ('Traditional Top 1000','精半約願令底答演達雄深票早院夠曲假談術棒賣黑百勝推存火準示往碟易況晚離治導七段團調證列傷永剛排哥德九甚殺照軟包怕條夜商概根供絕千客切集稱據落越竟盡待聞園忘值產消雙紅座展育跑附嘛執唱技某硬斯雲遊息助須苦介效首質例唉職復輸節規注畢查熱油館態停福救倒親害亂古步寶擊舉終嗯印限依斷輕環簡趣志響隨練續魚篇司局送極角省源陽幹習羅武免疑拉克仍樓佛足低廣煩鳥顯碼土率聖壞初具預呀眾責爭兵智誤境青順野楚貴負壓史適係測懷迎配魔慢哇懂嗚亦味評舞細醫帝屬句戀敗宜楊甲追灌春左敢靈狂際群族木騎里項戲遇狗佳博右痛營妹康善徵歷官爾按編病護補擇抓石歲隻領尋溫養止守君血田雨居謂異優跳拜爛封惡良模狀浪聊增核激維陸吳牛忙詞劇宿急啥抱靜攻亞江致陣嚴宗警壘夫密睡午店勢悲蘭幕緣週廠簽坐香爽控微登翻普蠻冷威毒俊絡輯母創堂趙套舊雜周述恐幸亮麗巴禮酒仁餐牌突腳劍招吉父仔典搞房素防授充草暴慮紹背劉委府景憶尤諸缺援漫琴罵純尚藝惜置益姐誠繼湖欲麻靠肉松刻紀退既含判釋皮波承射堆莫製鍵趕旁筆扁註奏樹律鐵榮昨毛彩歸虎罪皆葉售彈衛施銘刀塊漢欣布賞載險播升鐘寄弄付構囉磁螢偉薦洋嘿啟梅策嘻燈鬼檢宣哦媽均派豬濟架享呆訓藍劃擔努郭歉紙貼暗呼罷巧慧穿詳雷協督顧臉逢'),
    ('Traditional Top 1500','島獎游批略短幻沙散敵鄉冊輪朝窗忍河藏衝混唯乾冠熟鷹蛋尊棄敬季婚縣緊伯申衣購僅帳層秋猜偏鏡食喝偷贊犯勇顆姓束淡詩嘉曉借徒洲擁序慶績祝獅圍餘私鬥柔漂富秀範避輝譯孤笨括吸端移廳蓋末察抗揮乖積插驚蔡忠愈雪巨碩瑞凡朱籃丟盤偶港宮帥宏雅貨醒虛遺掛透爆烈滅材拍休誌圓銀互飯掌豪替挑頂熊累址健俠雞困諾輔伴玉洗敏臨街降唸憐蘇米減操瘋辛宇聚兮彼採屆尼輩藥騙綠童縮符獲默郎碰禁婆咧股抽砍恨肯刊泡漸鋼廢淚樞贏歐財訂途觸賢傑脫箱佈仙冰析蒼厭籍堅哭夏懶橋穩露詢森絲塵慣濤誼佔茶賴階豐貝暑郵危寒械隱爸汽慘旅村予振亡瓶遭哲零納珍乃席哩鄭吹骨煙胡倫洪搖娘芳索峰織惠杯浮狼隔椰租尾忽複莊款菜副企折擾揚鼠冒癡鼓刺頻喵針霸暫伊沉嘴庫悔陰寂倚探祖摩距剩遍蟲燒頁隆弱豆延蕭握寧昭盟覆憲秘耐愁丁撥沈昇髮哀龜眉固卷顏閒稍殘搭京傻耳映託恩鴻妙辯媒吵擬違憂桌拼銷藉胖屋域船勞洞寢井徐川奈戶乘額倍農擺塞橫賀皇拖怨牙齊逃障賺滾干譜烏瞭戴搬鬆瓜迫嚇奶棋鬧盛摸尺伙染佩床酷孫牠屁醉震鎖凱損潮役泰伍冬桃聰乙迴競崇撞厲淨牽羊惑溪帽眠巷溝俗宋飄淺獻麵艦滑榜圈庭縱閃蓮麥邦耀旋閱諒紫攝儀妨審描洽毀逐陪填踏跌藤慕勒闆殊姊憑寞岸芬鎮池拒葛州鋒寬拳于函驅后裁蟹阻邪革頗臥昌孟'),
    ('Traditional Top 2000','航遙翔蠍恭奧齋睛槍塔閉頓糊仰旗勵厚魂准丸宙逸裕舒訪兼薩飲赤閣庸啪搶勿砂緒丌穹儘掃慈欄嘗勸鮮奮賜菩喊闡幽擴污彰毫祥盜証罰番尖灰狐衡擎汪監籌遲誇邱稅浩拆紛吾托姑咱漏誕淑鬱砲柏牆窩傾辭秒羽渡沖廖輛齡培邀甘袋杜酸胸邏豈涼肥谷獸娃孔陷估妻徑玫潛晶胞煞脆抹猶築呂碎噴截旦婦垃荒幣圾串壯伸傲弦泥繁魯忌億叭坦恥蜜欺捨怡玲臭唐湯窮悉勁拔甜蒙逛朵摘膽糟腿喇醜躍繳泉澤碧鞋韓彥晨莉駕猛緩坡炸怒召捕幼艾恆割扯盾么吐昏辨軒巫丹鑑彎賦坪侵胎悠薪刪彬悟珠勤瑰植痴礙敝盃盼亨逝剪磨逼濃洛乏擋姆症嫌躲壁釣暖憾遜愉曰采捷嘆玄滴扣抵奔翁蹟菲爬棚夕惱戒牲泳恰滄桑蔣潔焦勉奪萊咖貪踢抄跡鍾涯箭誓穌涉稿署療礎僑涵霧粉俱徹謀屠犧唷繞壽爺騷氏翼云肚吝梁咪繪廉飽鳴貌霹炮捐啡炎嗨貢曼壢鼻奉鈴耗恢融筋撿儒飾禍侯唬挖幅瞧廷咦撐柳薄黎捲嵐吊靂擠覽迪凌茫燃瑪弘矛敦瑜錦楓賓梯琪獄側咬墨悶晴怖喬齒嶺仲韻旭綜兔蹤姿邁傢譽褲孝促駛仇粗妮牧舟糕殼蝶兇鍋懼銳吟虧枝耍闊疼拾毅刷塗夾裂陀哉鄰悅契轟爵屏駐賭蜂扇羞瓦疏欽斗坤堪洩逆抬哎餅彌貫綱惹翹墮狠頑莎擦贈凝滋靖喂允彭挺拋愚征辱朗余慰禪蛙秦災偵讚椅夥碗丙卒荷披趨劫迅笛烤肩矣遷汝鹿缸慾爐魅丈巡措秤沿痕濫漲腰賤妥液鵝軌叔陵貞'),
    ('Traditional Top 2500','扭漠祕蝦捉謠氛膠遞霖雯髒倆旺杉燕寸茂循屍鑽晃悄翅芒斜廁呦溜鶴喪盒摔愧灑津盈脈苗堡刑叉撒虫纏遵臣櫻扮渾噁趁呈牢泊欠慎琳倦腐蛇搜患伏陶柯劣疲儲桿祂塑蓉繫疾泣粒渴璃茲鄧歪棟騰玻娟叡返併弊埋晉稀鴨汗牡暢添妖劑泛柴杰攜飆壇阮匆喚昆拷儂斥垂萍勾催糖澎踩櫃蟻販抑虹潘坑曹暮腹煮襲仿臂吻浴框敲佑体彷謹岳敘賊罐寡燦侶攤芭翠羨占綿謎掩喻秩煌賠籤珊馨札脅旨拘紐喲蠢詠匙羯攔膚驟嫁廟孕俄肝罩腸叛匪倉卸祭袍謊埔几貿魏禦踴蘋卜澄麟宵陌陋屈衷崗盪曆惟舌匯誘桂娜菁睹殿傅咒謙雀粽卓鑰斌袖鈕媚叮翰堯盧捧壹憤猴粹跨螞埃枉卿撕紋瑋划囂雕乳膀仗赫筒辜桶彿衰獵譬勳衫懇瓊凍戚穎軸殖撤吋寮潭姻躺樑昂潑腔龐澳瞬寺銅閩肢糾叢卑拓宰鍊湊梭董宅刮胃芝淋斃驕奸殷墓償冥炒潤蕩妄砸餓扎佇尿眷濕盲偽踐淫鼎貧謬矩蟑駁兆淵棍馳熙扶聘斬穴槽詭昧澡螂辣匹蚊僧柱挫袁籠抖訝勃顛淘撲丘吞亭瘟癢肆漆詗尹猩帖佐昱咳祈詹毋矮苑賄緻婉斤饒闖戈歧諷熬診霜諧掙鈞覓瀟屑痞鋪黏遣蹈懸詮岡蝴汁攏帆壺瑟雁辰婷穗慨哼淒佬膜肅濾涂范恕醬纖輻懿稚郁募豫艇枯掰寵遨并漁淹岩墊鞭縫駿歹斑甄竿駝昔崎冤棵僕疊箏剎墜遮螺煎薰癮蠟瞎禱皓坎蒂焉魁唇犬弓錶籲娛甩颱屎沾撫傘嬌錫唔郝禿淪剝揭溶肇匿趟盆湧坊碳赴絃磚'),
    ('Traditional Top 3000','栗狹廿菊嘎瘦奴氧頹璋驢畏珮債摧鹽噹噓挽墾霞伐畔韋姬逍瑩脾嘟帕噪穫縛暈裙頸竊濁峽倘蘊餵囊霉薇剃衍訣廂臟枕慌豔湘熄琦蓄削鵬券渺臘伺蕾矢挨漿娶廚睜虐薛蓬垮暨鑼遂喧釘堵醇嬰耕濱葬履艱緯姦摯鴉蒸葡嚐甫璿霍尉妓棉秉爹撈綁翩嘸呻拂貳燭懲宴撇爍汰歇癌咕崩膩撰樸棺頌魄舜蕃寇萄妝遼襄薯曝諮蘿頒菌嚮氓枚酬馮嘲橘侮灘屢歎巢髓碑梨礦疋脹賈譴悸煉胏豹擅迦蠶肌攀卵闢炳嘍盞鄙浦尬弗株爪抒侍阪祇逗喉栽疫黯飼鋁鉛劈艘仕嶼郊釵鵰裸嘯璞凶頃寓狸柄挪沛鰱咚芷彙豎僚姜窄杖倩兜廊燙惶吶祺耿鏘綽迄柵夷拙煥妒鷗溯蠅沌聆潰攪吼竭磊瞄唾棲倡掏俺浸酌繭芙楣押卦苛鴿凸匠悼蛛繩掠暱瞞芋蔥墳拯啤剋逕茵佮滔崔宛贖蟬蕉貶裹燄朦芽御狄顫倪燥啞頡樺惰荳糧貸祐炫旬噢齣鱉簿喘綸腥敷悍袂僵尷締檳紮斧襟轄肖鈍腫檬蹲嗜逾瀑罕癒碌迋稻譚撼禎裏凋哨掘澀釁汙庚慚隧膨詐釀脂圭凳鑫槓綺拭捏拐瑛醋蔚筠鶯闇伶曬鬍膝亟卅曠抉惘溢剖喃琉竅蝸呃匡逮榔奕傍檸鉤襪暇扳梵泓涅刁輾蔔斐捍聳疤蜘姚忿恍黛瀚諦堤窟篠仟繡暉嗶窺晦渝禧刃沫葵匣楠隸轎嘔蔽綻丞諜襯晰膏窈嚕蘆斂皺峻孰仄瀏涕鈔沮擲窕煽袱蝕絆茹瞪丐舅詰懺鹹錐丑淳焚溉毓蒐戳雛闕佰鈺哄菱肺軀芸姨壟盯奢巾槃紗菸凹腕翟怠蟾蔭庄寰囡瑄饋阱靶腎擱搏闌穆呱'),
    ('Traditional Top 3500','犀飢蹺疵瑤樵鴛輒閥琨憧勻搗隙悵虞跪乞逞孽瀰榕徽蜀螃俏淆丰萱俯敞渣緝詛紳屐眺咫溺疆饅瓏屯沸餃鴦夭憬駱芹葦徘竄謗啼囚絮鐸乍蕙杆冗簧脊眸愿趴滯貂嘶拱掀萃彗邵徨輿朮巍徊叩妞侏苟吠嘩憊茅矯邂檯鎚禽棠崖澆啄挂銜朽嫖汐揣寥徬畜瑕氾赦筱粥稜虔湛崙瞻懦滲儡祿簾擒萎澈蓓磋膳瀉蚤椒儕塌莽琮壤矽弧茍脖憫魎鏈蕊鍛奎嚼糗楷茁偎磅笙蔓恃隅餌裘俐拚廓鄒烘汀鑄崑鑒嚷莖噸煤勘殲樽扔杏瀾廈噎穢馴峙厄躬僻酥毆郤曖繽伽閔蔑茜躁誡繕咎鏽淌曜扛頰佫麒喀蒞芥逅雇斟菇誦瞳苔樁懋曳滷閏耽駭糞卯岔琵蹋禹汲倌嗡泌捌皂晝渦岱梳莓睿鋸瞌轅惕廬旻遁贓礁毯絨淇甦莒粵焊瀨隘嫩藐垢聶譏恤怯岫巖倖訶裔蟄吭跤嘰梓鎧鱗痘朔騁驀矇椎嚎釐橄亥龔濛俞殃幟啃欖搓瓣妃噱埠硫裊閻狡橙蹄薔豚炭琶冀祟喙鷺炊糙靡塘媳筷懈嫂廝橡瓢暸兌攸唆塚溼搪茄膛祉氫炬挾瓷攬苓霆贅桐鍍狷呸嫉踹咆砌愣蜢藻瘤鞠墅瑣呎牟睏郡鉅饗遐胺霄猿蝠沐摟曦錚傀煚燼韜璇艷侃疚颺蹦恬璧霈屜篤咽荊鵑昶諱屌憎裳陡楞洶耘嚨莘淼嗤酵銓煜鷥厝轍嗓偕揍摺簫戌烹鞏盔傭骯烙蚱慷嶸徜偈焰啾誅曙藹蚵憨峨悽磯涓蒲茉揉閑璟饑畸鯉鯽銬岐雋誨稽戊臻繃扒舵巳羔睬恁癸艙紡煒韌弔娑擷冕碘豁摳肘抨曇臆熔駒壩絞疇珈肛骷朧媛嫣榨纜褪昀趾酹柚搔羹舖眨堇靨蝙'),
    ('Traditional Top 4000','鞍鏟哺惆霓癱訕蛻沼聾憋韶枷懊惚篩巒凜丫硝忱玖嵩拌絢褚汎葭鸚嶽祁矜盎噫婊筑憩鵡羈娥鏢硨蒹袒塹悴瘡俾窘亢詬扼祠厥蜴蛤痊茱儼笈榴騏蒜奄髏鬚砰迢蜥縷鯨葔糢吱眩棧戮夸樟杭笠咸棘慵籬庶荼捶漣櫥吏荐芯禾巔肋侖跆恣鳩蔬徉跎揀艸嚀蜻嬉鱷沁嗽瑾藩匕鹼酋虜噩驛奠萌嗆墉兢躇泠梢翱儉甸薑詣翡僥竇瘖撓蟀蜓躊緬憔擻梟渲耙惋塾皈訐觴眶蛀愴殭噗灸竺幌痲稟傌欒窯羲愕塢慟炯葷澱佼腺埸膺扑繆冶綴旱灼勛沱嘖嗈泄耨霎儸紊噶剔孵冉圳臼抴怔侷褒蹉粘淤雌檻彤頤俟朕綾蠣蕪霏梧妾殆狙諂甭煦眛扉揪瑚酪漓瞇諭机揖蟋匈幢瀕雍蠹琇閹惦渠愷嶄兀餒餾訢嬋炙褻迂姥鑿玟訟漪釷葳咐骰嫻踅猖訛辮汶咻儷佢囝烽晏葫僱踮桔誣癥囑罣飪癖彪俘咄渚褔庇侈詔縈箔舔擂璽迺鯊鮑疹遑藺洒桓茗辟瞋褐熹顱弋慄蓊羿噬籐窒碴跋肪睦罹臀槌瘓瀛胚揹漾卉拇釗璀娣諺鞘吩羚鉗晒竣熾翎惺丕洹跛勦蛾撩翊璁氯穀譎攘痔鈣漱噯婿瘀軾滸漩昕垣靄尸咯剿瞥骸咿貍磷繹槳霾棕燿筍吽遴鎔俑咨婪敕孺訥氮矗尪寐靴裴鵲靚仝洸磕鬢荻隕汞蚣佯珀瀝咀榷暐簇鸝隍痺鎳椏簣籽瘴胥徙痠濯朴撮搧弩寅殉竑堉麓嗔蚓睞墟疙垠蜈嬴崢夙嗅仆璜峭蜍聿蚯闋檀鈑罔摹鰻蠱葾拈媲箋湄擄鴕謾矚垚賬躪崚樊瘩蔗邃亙沂韃粱蹂旄捫諳紓叨焜螳曄劭喈漬閨瀆乩憚雱坷奚淮拗稠'),
    ('Traditional Top 4500','睽跩酗彆浙鋇琢誹饕齷隼箍吮陞掐蓁寨敖驥酉咩虱酣篷癲欸媄岑湃遏驍睭万匱濺簷戾滂鑣鬩竽芻烜銃渥燉瞑鑲衿粟笆摻錘吁蛹梖恙崛烷賏孜嶇榻綢譙遽卍爻贔葆驂娓棗餿潢庠庵剷嚥捅垛迭圃狽嗦町鯰漳澹隴齪厘杵蟆哞慫姪苯揆髦懵潞詫賂琬橢佗皎詼諄峘鏞貽壬悚摒殤邇忡逑孚劾喳糯佣濂榆緹餡馥踝鬨迥鎘叱拎猥悖膿鱈柿砥潺盥臍邰腑鎂攢隋嗣閘碇豺冇傜梗肄萼咁搥枋沽畝衙魷鑾篡璨錨泯拽鎗籟蔫戎剌貯黝徠妍沃鈦逵唄嗩馭恿灶昊胤鈿闔沬琅筐浣杞牒荃鉦艋踼驤苞痣澗洄牯啜痰莞愜嗖煇鮭倏藕芮麾雉鼐仞栩菠剽狒儺柒筏妲伎睫紜輦顰哮骼螫愫裱鐽荀晤釧雩玠吆汨糜呷毗涌弼坍垓靦乒麴黴籮噠齁悻楨鸞悱綏旳緋歛躄偌蒨謔冽蜃瞰薏腆槭宸蝗踱餞逄浬娼劊巿屹唧唏娉潦嗙蚌稔乓倔哽窠烸俸淦諫譁黌碾癟鰭檜齦毘覷帷礪魘晌缽蜿墩浯燊捆嵌釆謨徛脕茸獗鯤泱栓崧啐祀崁舫陲姍捻琛蛟磺謐咋閤瀅蝌鋤埵弛箇踞窿鼾匝荏滌踵蹶帑糰獃燁掬吒窪燻躋弭醞傯磐夯嗇酯捱蕨摃葯忝嗟絹鉀瞿鰍鄺舶晾嬤鞦繾萏軋嬸狩蚪詒爰楔擘獰縹鷸隹埤慍猾箝餚濡蹬騖鐮囈芎胱湮獺嗝恫菡琥鈾嚏啻邢偃楹閡颯蟒鼴眈謅剁宦犁翌稷閭儐忖槐箕稼箴戕喋瘍埕甯湍暝襠綣牴叟琍懾槙薈皿沅砷逖瑯嫵韆佞囤篆鯛菈梆詆軼錮饞樕猷緞頷豨迸釜蛆愎瑙諍瀧鷲阜俎褓濘玆'),
    ('Traditional Top 5000','醃攫怦昴嵋詡宥喫暄幗甡晞跚睪臧駑纓痧璉嘮儻捎惻睨衲杳姣拮槁彧栱婢簑忑腮鉻蝨躅霽忐嬿駟炘妤忪秧渙氨滕殯躑猙戟僮馱癩鰣聒嫦錡謫姒餉癈驊胭菅緲淂棣姝堐据紕捺犛椿嗷嘈醺軔涎鹵鈉鏗蜒浚婁罈嶙蝟郢拴蓀鋰邋猝倭脯滬銲甕鱸啵悌胳胯膊爿峋涘潁獠邑腋瘁坻暾鮀舴岌帘柑觔桀莠喟綵袓鈃澍耆瞠沚珣蛢褉糸痢腓蹴伝勺飴熨餛芩叼韭娩誑幡鑠膫璐鑞嫡犢挓唰蕤帛庖諉晡枰淅鋅荔紂葩緘擰躡豊烯跺甬邸氟榛璣倜焢佚疝盅噤燴窖燬珂摀櫓佶烊淙挹菀獼卞帚洱諛鵠鏤洐酮蹛炤碉蹣坵氦蓑藪矬臾舀蔻儔恚菫雎匾夤熒遢哆苳踽揩棹鳶壅謁壑鍰謳衹渤顎沝氰蛭呣胛涪畦颳繚邈幄睇臊刈肓臬蹼尻捀羡泵紲孃蠕銂轆戍刨拄渭嘹膾蹙啷蠋歿絳愍礫兀夆恪淩蝎囪嚶蠔贛忉捩掣撬黔罄芊矕孑伕陛脩鎢譟揶鄔靳陝扈痙蔘蹧氐趺甥蹊躂湠謢贀亳飩賃宕苹詘嗄粼貲榭覦纔硐圜綑嘀鮫岍坳葄熏刎潸鼬顥拺昝桎頇訖婀淬輟愔揄壼趐墬稹埂蚜靼彊沓砉罡彫諼覬褟靛鷓屄迵欉祚銼褸攙脛筌礡珪摑柜柰崽筊蓼蝣賁晟椆焙雹賑賸獷昃撂鬟炕囿軛搾簍韁婬婓瘐鴝囍玷幔筵糠玎堀胝倨棻鏖掔滮熇虌仃旌袞崴鴣翳纂畀葚鶩俚涔涸髻颼攣宓倬綩誏軂珞愾斡耦壕濠鍚嗲鰲捂腱讒忒忻萩羌寤踫錠鐺瓚凊紘洵盹暘錕鎊卬芴蕎鴞砝胼蛔嗑唅栲啖甌毐埼梏琱豋擤齰迤硯篾鐲癬驪'),
    ('Traditional Top 5500','囥玹桹詄鋃恒弁忸啣釦瘠鮪偆搵漉粿儆槤祗唳戡鉉紈皕蜉鴇芍掄滇皚褊駢臏黠囁鱔湳鍶懟閂砧痍貉慇擢璠汕听啕庾輊霑謄彝斕憭懌蕁鎯纇衊豕腴溥蜷褥瞼鬃醮鐳焗瞅熠嚓黧戇奐弒氈鮆囓惇蜇懍撻戽渟杷舢迨冢娌斛鄂裨燎臃餮讖秝蕘奲佃柢軻璩扺珗焂瑀萹踉皖鎰襤圴侄俵凈哧頎嶠顢灝孓岷柬鈷輓慼瓔种惙黽瑮闥髯橇簸咭畬綪蹓圻冑哂曷浹覃睥釉縞汔佘媞揕榚鄢翦鵒莢翕萋搆鎬蘑騫騾荇喢寑酢殞踰醛鱧倣陘幀鰓欷豝酚痾皙慳碓銖暹簌攷咈肏摽醚茨舷惴鈐綬膈豭濬旡峈洍焯殛裾撽橞嬲泗肱匍媾蓆鴆澧攆玀乜偀廌嫭坏怵晷瘉羸柪纍硃螻昉珩茪茯淖屣慬犘蹌淞硼犒颶蟠覲藷亍柎柺盻衾晢喑喏噉鋏璗鍘碁奘畚袈諶阯岬庛荎嗐瑗弈絀琿粳噥磴餽驃忤舺袪碥汾怛玥兗皋皰黍蒿賒豌檐麋砒掂跏煢艄葑壆遶錩瞴螯鯁瓃蠑苧旎孳裟錳簪霪彳扡厎柘悀砪掇嗒媺粲懨蹔蹭麤杓啁鉑頜褶醣齟鰥掤笳脢蛂戭蟘妁侑倀巽漕箸殮曩魑孥殂苠党凄剮豜憍囔艮幃煖冪簞瀲齬卌惼晹裎瑧儰撜阡姘枸栘舨瓠脣毽濮櫚櫬鼇汜岦衪郅旂茼雃犍竫摶榖儌獒闍騄糬鬘枇陂毬廄鞅輜褡怙琣腊痹樨濋苒掖釭媧愆楝萵銨鴒贗洁庳馗絣傱畹潀斲貘氖狎肴痂銑褫鍬咂坨掞摠盦鋹鴟顴叵篁嬝贍峗挴窆琚竤跫撘獪鱒伉郃涇盍鈸旖璘瞟縝饜扦哖悒揃稗触璊閰鍺瞱蹇蹩鵟饌佻泅盂浥赧萸睢稞潼'),
    ('Traditional Top 6000','螟夔怜邯苻雰祼艉餬燹櫸怏枴柞洮匐堊飭瘧燧牘霰芃妺怢怍芫苤痒螈鍇櫪蚩戢賅榫薨鍥歟魍网孢喎琡嶂噌澔諴橿襁鞥塋痱儈瘸蕈櫛璦穠鏜矓衢卲氡迣凎揠琰綃裐鉞鶻矘杠洌踟燐磬薜蠡麝粄荖埥堎蛁媜菾軫瑢踊勱謮讎轤灠褂蕞薊醴炅俛婕屙庹掅琲遄嫚摰憸擗魽圬苣酊舐綰瀋囀峓殄琁荺逋棓棱閞噘熵蓳鴗篳囫抿疥粕筧犖獐錙訄捋蛘暋駖諡薾鶚鰡俳梔涮酩縵鯧轡忮冼囹芵虯咾衁浼茬眭椄琤搐絻裞綷窳醍闃隬灕躝紉挈砟胴詁僭碣遘畿鐃芡剉嵎嫄溟鞞醯鐐攥纛斫苜桅砭訌笞鈽奭賡縊鄴壙奼柸枵洘圇祤菘嫋煲煐睒蒔嘳鄲薙鍠鶡仳牝卹氤匏堰閎煬嬈縉鷂蘸扙妗沏玓坯苺栴烔蚋凐畯詎嫈廕漼璆諅澪曛顗鶇鶖讌灩怩禺茆剜戛橈邐优冱泫呲怹苾苡砢祜茩痟痼誒諢擣闓韙蠓臠胰塽篙闈櫺蘚豸芼倢砵悾捵珽蚼傒棑硞寘楂稙暪懃謖嚙櫫蘶汛妣峒圄漯擭燮聱癘黷氶俇姽彘萁亄葥潳魠獞磲鴽鐿鶼枓琺稈櫝襖鐫孿吨柀枳秏淯狺婐掮莪堸渼楙篫諤懮艟龕尢佾傚孱隄楛痿嚅谿繒巟氘阨俓茦娸痐紺焱猢廋椳赨靸僯熞瘜蝮歕鵂嚝騅譠鷈驒鷿祆菟暍痳摭膂誥遛歙壎醱羼呅俅挎挳唪淍珺笘訧揂蛺蕓魈懰禰翾舋廾汴皴嶔撚嬪癆黜孀罌襬囗忯佸呤挀柷炷盷荂郜眥摡搕腩撗諗嬛骿旛襌齀鐙鰈鱆鷦魙圯舛柩耄莆鍔齜髖佷侗怞矸珅尃涗迾偑啍挻捰搰楜溏睕羥葀趒慓蜚嬅禛醐璫隰'),
 ]

config = mw.addonManager.getConfig(__name__)
categoriesToShow = config['categoriesToShow']
freqHanzi = []
for tt in freqHanziDefault:
    if tt[0] in categoriesToShow:
        freqHanzi.append(tt)

def ishanzi(unichar):
    try:
        return unicodedata.name(unichar).find('CJK UNIFIED IDEOGRAPH') >= 0 or unicodedata.name(unichar).find('BOPOMOFO') >= 0
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
                                        range(len(self.hanziGrades))):
            for c in chars:
                c = unicodedata.normalize('NFC', c)
                h = self._gradeHash.get(c, [])
                h.append(grade)
                self._gradeHash[c] = h

    def hanziGrade(self, unichar):
        return self._gradeHash.get(unichar, [0])

    # Currently unused function for tallying a "total score" from the counts
    # def totalScoreStr(self, counts):
    #   def score(cnts):
    #       MID,HIGH = 9,10
    #       return (16*cnts[1] + 8*cnts[2] + 4*cnts[3] + 2*cnts[4] + cnts[5]
    #           #+ 0.5*cnts[6] #+ 0.25*cnts[7] + 2.5
    #           + cnts[MID] #+ 0.5*cnts[HIGH]
    #           - 4
    #           )
    #   myscore = score([c[1] for c in counts])
    #   maxscore = score([c[2] for c in counts])
    #   return  _("Score: %d out of %d (%0.1f%%)") % (myscore, maxscore,
    #       float(myscore*100)/maxscore)

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
        n = str(n)
        return n + "&nbsp;" * (width - len(n))

    def genhanziSets(self):
        self.hanziSets = [set([]) for g in self.hanziGrades]
        # chars = set()
        # #self.mids = []
        # for m in self.col.models.all():
        #     if True:
        #     # if "chinese" in m['name'].lower():
        #         for row in self.col.db.execute("select flds from notes where id in ( select n.id from cards c, notes n where c.nid = n.id and mid = ? and c.queue > 0) ", m['id']):
        #             chars.update(row[0])

        chars = set()

        config = mw.addonManager.getConfig(__name__)
        fieldToUseForStats = config['fieldToUseForStats']

        # Code snippet from Chinese support
        # For each row, add the desired fields to the character lists.
        for fields, sortField, first_study_date in self.col.db.execute("select notes.flds, notes.sfld, min(revlog.id)/1000 as date from notes, cards, revlog where notes.id=cards.nid and cards.id=revlog.cid and cards.queue>0 group by notes.id;" ):
            if fieldToUseForStats == "all":
               fieldsAsList = fields.split('\x1F')
               for field in fieldsAsList:
                  addchars(chars, field)
            elif fieldToUseForStats == "sortField":
               addchars(chars, sortField)
            else:
               fieldsAsList = fields.split('\x1F')
               fieldIndex = int(fieldToUseForStats)
               if 0 < fieldIndex <= len(fieldsAsList):
                   addchars(chars, fieldsAsList[fieldIndex - 1]) #When using the specific column name subtract one to convert from the user displayed field numbers to the DB index.

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

        out += "</ul><p/>" + _("Statistics:") + "<p/><ul>"
        L = ["<li>" + self.hanziCountStr(c[0],c[1],c[2], width=3) + "</li>"
             for c in counts[1:len(freqHanzi)]]
        out += "".join(L)
#        out += "</ul><p/>" + _(u"HSK levels:") + "<p/><ul>"
#        L = ["<li>" + self.hanziCountStr(c[0],c[1],c[2], width=3) + "</li>"
#             for c in counts[len(HSKHanzi):]]
#        out += "".join(L)
        out += "</ul>"
        return out

    def _ReportHelper(self, check):
        out = ''
        for grade in range(1, len(self.hanziGrades)):
            missing = "".join(self.missingInGrade(grade, check))
            if not missing:
                continue
            out += "<h2>" + self.hanziGrades[grade][0] + "</h2>"
            out += self.mkhanziLinks(missing)
        return out 

    def missingReport(self):
        check = lambda x, y: x not in y
        out = '<a name="missing">' + _("<h1>Missing</h1>") + "</a>"
        out += self._ReportHelper(check)
        return out + "<br/>"

    def mkhanziLinks(self, hanzi):
        out = '<font size=+2>'
        out += "".join([self.naverhanziLink(h) for h in hanzi])
        out += "</font>"
        return out

    def seenReport(self):
        check = lambda x, y: x in y
        out = '<a name="seen">' + _("<h1>Seen</h1>") + "</a>"
        out += self._ReportHelper(check)
        return  out + "<br/>"

    def unlistedReport(self):
        out = '<a name="unlisted">' + _("<h1>Unlisted</h1>") + "</a>"
        out += self.mkhanziLinks("".join(self.hanziSets[0]))
        return out + "<br/>"

    def naverhanziLink(self, hanzi):
        config = mw.addonManager.getConfig(__name__)
        base_url = config['hanziURL']
        url=base_url + hanzi
        return '<a href="%s">%s</a>' % (url, hanzi)

    def missingInGrade(self, gradeNum, check):
        existinghanzi = self.hanziSets[gradeNum]
        totalhanzi = self.hanziGrades[gradeNum][1]
        return [k for k in totalhanzi if check(k, existinghanzi)]

    def controlButtons(self):
      buttons = [
          "<a href='#' onclick=\"$('#missing').show(); $('#seen').hide(); $('#unlisted').hide(); return false; \"\>Missing</a>",
          "<a href='#' onclick=\"$('#missing').hide(); $('#seen').show(); $('#unlisted').hide(); return false; \"\>Seen</a>",
          "<a href='#' onclick=\"$('#missing').hide(); $('#seen').hide(); $('#unlisted').show(); return false; \"\>Unlisted</a>",
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
    w = AnkiWebView()
    l.addWidget(w)
    css = "font{word-wrap:break-word;} div{display:none;}"
    w.stdHtml(rep, css)
    d.setLayout(l)
    d.resize(500, 400)
    restoreGeom(d, "hanzistats")
    mw.progress.finish()
    d.exec_()
    saveGeom(d, "hanzistats")

def createMenu():
    a = QAction("Hanzi Stats", mw)
    a.triggered.connect(onhanziStats)
    mw.form.menuTools.addAction(a)

createMenu()
