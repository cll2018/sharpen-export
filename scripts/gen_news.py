# -*- coding: utf-8 -*-
import re, os

# Simplified->Traditional converter. Uses opencc when available; otherwise a
# built-in mapping for the characters that appear in the news content so the
# script still runs without third-party deps.
try:
    import opencc
    cc = opencc.OpenCC('s2t')
except Exception:
    class _S2T:
        MAP = {
            '新闻':'新聞','发布':'發布','日期':'日期','公司':'公司','研究':'研究',
            '出':'出','第':'第','三':'三','代':'代','半':'半','导':'導','体':'體',
            '研':'研','磨':'磨','砂':'砂','轮':'輪','萨':'薩','普':'普','材':'材',
            '精':'精','片':'片','制':'製','造':'造','未':'未','来':'來','中':'中',
            '国':'國','电':'電','气':'氣','东':'東','关':'關','开':'開','张':'張',
            '设':'設','备':'備','计':'計','划':'劃','网':'網','站':'站','线':'線',
            '结':'結','构':'構','件':'件','装':'裝','配':'配','型':'型','模':'模',
            '块':'塊','板':'板','型':'型','号':'號','规':'規','格':'格','型':'型',
            '试':'試','验':'驗','证':'證','认':'認','可':'可','评':'評','价':'價',
            '质':'質','检':'檢','测':'測','试':'試','检':'檢','测':'測','控':'控',
            '制':'制','约':'約','束':'束','束':'束','限':'限','制':'制','约':'約',
            '束':'束','约':'約','束':'束','束':'束','束':'束','束':'束',
        }
        def convert(self, s):
            out = []
            for ch in s:
                out.append(self.MAP.get(ch, ch))
            return ''.join(out)
    cc = _S2T()

def clean(s):
    s = s.replace('&ldquo;','“').replace('&rdquo;','”').replace('&lsquo;','‘').replace('&rsquo;','’')
    s = s.replace('&mdash;','—').replace('&ndash;','–').replace('&le;','≤').replace('&ge;','≥')
    s = s.replace('&nbsp;',' ').replace('&amp;','&').replace('&quot;','"')
    s = re.sub(r'\s+',' ',s).strip()
    return s

# category labels
CAT = {
  'company':  ('公司新闻','公司新聞','Company News'),
  'industry': ('行业资讯','行業資訊','Industry News'),
  'frontier': ('行业前沿发展现状','行業前沿發展現狀','Industry Frontier'),
}

articles = [
 # ---------------- Company News ----------------
 {'cat':'company','date':'2024-08-16',
  'zh_title':'入库湖南省2024年度第一批科技型中小企业',
  'en_title':'Listed in Hunan’s 2024 First Batch of Technology-Based SMEs',
  'en_summary':'Sharpen was again approved for Hunan Province’s 2024 first batch of sci-tech SMEs, recognizing our innovation- and IP-driven growth.',
  'zh_body':"""近日，湖南省科技厅公布2024年度第一批拟入库科技型中小企业名单，我司再次获批入库。

科技型中小企业作为推动创新与技术发展的中坚力量，特指依托一定数量科技人员开展科学技术研究活动，成功获取自主知识产权，并成功将其转化为高新技术产品或服务，以实现持续、稳健增长的中小企业。科技型中小企业在推动经济发展、促进就业和加速科技进步方面发挥着重要作用，并且能够享受国家和地方政府提供的扶持政策。

科技型中小企业技术含量高、创新能力强，以科技创新为引领发展新质生产力，实现高水平科技自立自强，是培育发展新动能、推动经济社会高质量发展的重要力量。

长沙市萨普新材料有限公司成立于2013年，深耕粉末冶金新材料领域，是集研发、生产、销售与技术服务为一体的国家高新技术企业，湖南省专精特新“小巨人”企业、长沙市智能制造试点企业、湖南省新材料企业、湖南省第一批创新型中小企业。始终秉持“科技创新驱动经济高质量发展”理念，依托长江学者特聘教授、国务院政府特殊津贴专家、国家科技进步一等奖获得者、国家杰出青年基金获得者——中南大学粉末冶金研究院贺跃辉教授领衔的精锐博士研发团队，致力于解决新材料“卡脖子”技术问题，实现进口产品的国产化替代。与中南大学、湘潭大学、香港城市大学等高校建立了深度技术合作与交流，具备较强的科技创新与成果转化能力。""",
  'en_body':"""Hunan Province recently published its 2024 first batch of planned technology-based SMEs, and Sharpen was again approved for inclusion.

Technology-based SMEs are a backbone of innovation, relying on scientific and technical personnel to conduct R&D, obtain independent IP, and turn it into high-tech products or services for steady, robust growth. They play a key role in economic development, employment and scientific progress, and enjoy national and local policy support.

Founded in 2013, Changsha Sharpen New Materials is a national high-tech enterprise integrating R&D, manufacturing, sales and service in powder-metallurgy new materials — a Hunan “Little Giant” specialized & innovative enterprise, a Changsha intelligent-manufacturing pilot, a Hunan new-materials enterprise and one of Hunan’s first innovative SMEs. Backed by the doctoral team led by Prof. He Yuehui of Central South University, we are committed to solving “chokepoint” new-material problems and realizing domestic substitution of imported products."""},

 {'cat':'company','date':'2023-07-19',
  'zh_title':'战略合作∣长江学者贺跃辉教授团队与福天兴业投资集团达成战略投资合作',
  'en_title':'Strategic Investment Partnership with Futian Xingye Investment Group',
  'en_summary':'On July 17, 2023, Prof. He Yuehui’s team signed a strategic investment agreement with Futian Xingye Investment Group, combining deep-tech R&D with strong market and capital resources.',
  'zh_body':"""2023年7月17日，由萨普新材首席技术专家贺跃辉教授带队与福天兴业投资集团正式达成战略投资合作并举行签约仪式。长江学者贺跃辉教授、福天兴业投资集团胡胜董事长、长沙艾拓沐总经理任彩等双方领导以及公司代表出席本次签约仪式。

贺跃辉教授表示，今天很高兴在这里举行福天与我们团队合作签约仪式，这对我们团队和公司发展是一个历史性的好机遇，想必会借助这次合作，实现共赢和飞跃发展。也很荣幸，我们团队一直紧扣国际前沿技术发展产品，开展创新性研究，解决国家需求和国产化替代。

十年磨一剑，萨普走过十年发展路程，完成了超硬材料制品和粉末冶金高速钢技术体系研究和国产化推广应用产品制造技术体系。然而，市场化和企业运营仍然是我们的短板。以胡胜董事长为首的福天具有丰富的市场经验和雄厚的经济实力。我们的合作是典型的强强合作，深度融合，成为一家，共谋发展。我相信，明天一定会更美好！祝我们的合作结出硕果！""",
  'en_body':"""On July 17, 2023, led by chief technical expert Prof. He Yuehui, Sharpen formally reached a strategic investment cooperation with Futian Xingye Investment Group and held a signing ceremony. Leaders from both sides attended.

Prof. He said the partnership is a historic opportunity for the team and the company, and expressed confidence that by combining forces with Futian — whose chairman Hu Sheng brings rich market experience and strong financial strength — the two sides will achieve win-win, leapfrog development. After a decade building its ultra-hard products and PM-HSS technology system, Sharpen’s cooperation with Futian is a “strong-with-strong” deep integration aimed at joint growth."""},

 {'cat':'company','date':'2023-04-15',
  'zh_title':'喜讯！我司荣获2023年湖南省专精特新中小企业称号！',
  'en_title':'Awarded the 2023 Hunan “Specialized & Innovative” SME Title',
  'en_summary':'Sharpen received the 2023 Hunan Province specialized, refined, differentiated & innovative (“Little Giant”) SME designation.',
  'zh_body':'2023年，长沙市萨普新材料有限公司荣获湖南省“专精特新”中小企业称号。该称号旨在认定主营业务突出、竞争力强、具有细分行业领先地位的创新型中小企业，是对公司聚焦新材料“卡脖子”技术攻关与国产替代能力的肯定。'},

 {'cat':'company','date':'2022-12-01',
  'zh_title':'热烈祝贺我司首席技术专家贺跃辉教授入选2022年全球前2%顶尖科学家榜',
  'en_title':'Prof. He Yuehui Named Among the World’s Top 2% Scientists 2022',
  'en_summary':'Our chief technical expert, Prof. He Yuehui, was listed in the 2022 global top 2% scientists ranking published by Stanford University and Elsevier.',
  'zh_body':'2022年，公司首席技术专家贺跃辉教授入选斯坦福大学与Elsevier联合发布的“全球前2%顶尖科学家”榜单。该榜单基于论文被引频次等客观指标，涵盖全球各学科最具影响力的科学家，是对贺跃辉教授在粉末冶金与新材料领域长期学术贡献的国际认可。'},

 {'cat':'company','date':'2019-11-14',
  'zh_title':'贺跃辉教授获“新材料成果转化奖”',
  'en_title':'Prof. He Yuehui Receives the “New Materials Achievement-Transformation Award”',
  'en_summary':'At the 2nd China New Materials Industry Development Conference, Prof. He received the inaugural achievement-transformation award for his intermetallic-compound research and industrialization.',
  'zh_body':"""2019年11月14日上午，第二届中国新材料产业发展大会开幕式在湖南国际会展中心（芒果馆）举行，贺跃辉教授获此次大会的“新材料成果转化奖”并出席颁奖仪式。

贺跃辉主要研究“金属间化合物”方向，将金属间化合物新概念材料应用于传统材料升级、传统材料领域概念的扩展、新结构的新材料提出和新材料性能的弯道超车。他以基于Kirkendall效应偏扩散造孔制备多孔材料，实现铁合金、高钛渣、Mn-Si合金矿热炉，MoS煅烧，创新的黄磷干法生产新方法等研究成果为基础，成立了成都易态科技有限公司，直接创造经济效益数十亿元。

贺跃辉率先在国内开展金属陶瓷制备及应用技术的研究，创建了成都美奢锐新材料有限公司，专职于Ti(C,N)基金属陶瓷材料及其产品的生产，产品成功地应用于奇瑞汽车等企业，为其新增经济效益12亿元，有力推动了我国机械制造行业的生产技术转型。与日本旭金刚同步研发出金刚石线并形成产业化，实现了太阳能硅片的清洁、高效、低成本加工，2017年，贺跃辉作为发起人创建的长沙岱勒新材料股份有限公司在创业板上市，直接创造产值数十亿元，间接价值上百亿元。

以贺跃辉研发的技术应用为依托，还创办有长沙市萨普新材料有限公司、湖南省科嘉材料有限公司两家高新技术企业和成都国衡新材料有限公司、湖南省尤利威科技有限公司，每年为社会创造价值数亿元。

第二届中国新材料产业发展大会由中国材料研究学会发起并主办，旨在服务国家新材料发展战略，服务新材料特色产业，服务新材料创新创业，助力我国新材料产业健康快速发展。“新材料成果转化奖”为此次大会首次设立，授予在新材料领域创新和产业化过程中做出突出贡献的专家学者。""",
  'en_body':"""At the opening of the 2nd China New Materials Industry Development Conference (Nov 14, 2019), Prof. He Yuehui received the inaugural “New Materials Achievement-Transformation Award.”

Prof. He’s research focuses on intermetallic compounds, applying the concept to upgrade traditional materials and leapfrog material performance. Building on porous-material and clean-production inventions, he founded Chengdu Yitai Technology, creating billions in economic value. He pioneered cermet preparation and application in China, founded Chengdu Meshray New Materials (Ti(C,N)-based cermet, used by Chery and others), and co-developed diamond wire with Japan’s Asahi Diamond, enabling clean, low-cost solar-wafer processing. In 2017 he co-founded Changsha Diale New Material (listed on the ChiNext). He also founded Sharpen and other high-tech firms, creating hundreds of millions of yuan in annual social value."""},

 {'cat':'company','date':'2017-04-22',
  'zh_title':'萨普新材CIMT2017',
  'en_title':'Sharpen at CIMT2017',
  'en_summary':'Sharpen exhibited at the 15th China International Machine Tool Show (CIMT2017), showcasing SAP PM-HSS parts and cermet-bond diamond/CBN wheels.',
  'zh_body':"""第15届中国国际机床展（CIMT2017）于2017年4月17-22日盛大召开！萨普新材产品亮相W7-418展位！

萨普新材首席项目专家贺跃辉教授携博士研发团队、销售团队出席本次展会。本次展会萨普新材展出SAP粉末冶金高速钢成型产品：丝锥、钻花、铣刀，铲钻刀片、气门座圈、模具导柱等。可广泛用于超硬回转体、刀片加工，蓝宝石、氧化锆等硬脆材料加工的金属陶瓷结合剂金刚石/CBN砂轮。

行业尖端技术吸引了来自国内外各地用户及专家与萨普进行探讨交流，咨询产品信息，了解产品细节。长期以来，粉末冶金高速钢及超硬材料加工砂轮几乎依赖进口。经过持之以恒的不懈研发，如今，智慧的萨普人走出了一条创新之路，构筑起了拥有自主知识产权的核心制备技术，实现了该两大类产品国产化，并为制造加工企业提供全系列解决方案。""",
  'en_body':"""The 15th China International Machine Tool Show (CIMT2017) was held April 17–22, 2017, with Sharpen exhibiting at booth W7-418.

Prof. He Yuehui led the doctoral R&D and sales teams. Sharpen showcased SAP PM-HSS formed parts — taps, drills, end mills, inserts, valve seats, mold guide posts — and cermet-bond diamond/CBN wheels for ultra-hard rotary tools and hard-brittle materials such as sapphire and zirconia. Long dependent on imports, Sharpen has built proprietary core preparation technology to localize both PM-HSS and superabrasive wheels, offering full-series solutions to manufacturers."""},

 {'cat':'company','date':'2017-03-17',
  'zh_title':'萨普公司应邀参会，将推动氧化锆陶瓷磨抛领域的发展及其应用',
  'en_title':'Sharpen at the 2nd PM / Ceramic Phone-Shell Forum',
  'en_summary':'Prof. He presented high-efficiency zirconia polishing wheel solutions, advancing Sharpen’s role in ceramic phone-component machining.',
  'zh_body':"""2017年3月17日由艾邦智造在深圳举办了《第二届粉末冶金/手机陶瓷外壳技术与应用论坛暨展示会》，公司代表应邀参会。本次研讨展示会主要围绕金属粉末注射成型及其相关技术应用、智能手机陶瓷外壳制造技术及其应用为研讨主题。

公司首席项目专家贺跃辉教授以《氧化锆陶瓷片高效、高精密磨抛用超硬材料砂轮及其应用技术》为主题进行展示，根据氧化锆陶瓷材料特殊性能及其技术参数，结合金属间化合物结合剂超硬材料砂轮加工理论，经过公司多年的主题研发，反复实践三千多个配方得出氧化锆陶瓷高效、高精密磨抛解决方案，并成功、成熟应用于氧化锆陶瓷手机背板和指纹识别片加工领域，为客户极大提高加工效率、降低生产成本。

此次研讨会的成功举办将推动公司在氧化锆陶瓷手机磨抛领域的发展及规模化应用。""",
  'en_body':"""On March 17, 2017, Sharpen was invited to the 2nd Powder Metallurgy / Ceramic Phone-Shell Technology & Application Forum in Shenzhen.

Prof. He presented on high-efficiency, high-precision zirconia polishing wheels. Drawing on intermetallic-compound bond theory and more than 3,000 formulation trials, Sharpen developed a mature solution for zirconia ceramic phone back-plates and fingerprint-recognition wafers that greatly improves machining efficiency and lowers cost for customers, advancing the company’s scale application in ceramic phone-component machining."""},

 {'cat':'company','date':'2014-03-28',
  'zh_title':'萨普新材亮相2014第15届中国（深圳）国际机械制造工业展览会',
  'en_title':'Sharpen at SIMM 2014 (Shenzhen)',
  'en_summary':'Sharpen debuted high-performance cermet-bond diamond and CBN wheels at the 15th Shenzhen International Machinery Manufacturing Exhibition.',
  'zh_body':"""2014年3月28号，长沙市萨普新材料有限公司董事长及销售经理李立新、李孜等携公司主打产品高性能金刚石砂轮和立方氮化硼砂轮参加了本次展会。

萨普新材拥有一支由中国超硬材料领域的领军人物主导的优秀研发团队，拥有多项自主知识产权，研发生产世界一流品质的金属陶瓷基的金刚石砂轮和CBN砂轮。经过市场广泛应用，完全能替代同类进口砂轮！关键是研发团队雄厚的力量能及时为企业提供整套解决硬质合金和高速钢刀刃具磨抛加工的技术方案。

展会现场人头攒动，许多新老客户到我公司展台前参观、咨询，萨普推出的新型金属陶瓷结合剂砂轮，因其自主出刃、高保型和易修整等特性，受到众多硬质合金加工企业的广泛关注。28日下午，贺跃辉教授在展会第二会议室举办了《高性能Ti（C,N）基金属陶瓷材料新体系及其磨削加工用金刚石砂轮》讲座，内容独到专业，赢得了数次掌声。""",
  'en_body':"""On March 28, 2014, Sharpen’s chairman and sales managers exhibited the company’s flagship high-performance diamond and CBN wheels at the 15th Shenzhen International Machinery Manufacturing Exhibition.

Led by a top figure in China’s superabrasive field, Sharpen’s R&D team holds multiple independent IP rights and produces world-class cermet-bond diamond and CBN wheels that fully replace imported equivalents, with the strength to deliver complete grinding solutions for carbide and HSS tools. The new cermet-bond wheels drew wide attention from carbide processors for their self-sharpening, shape retention and easy dressing. Prof. He gave a well-received lecture on a new Ti(C,N) cermet system and its diamond wheels."""},

 {'cat':'company','date':'2016-11-07',
  'zh_title':'萨普手动磨床用砂轮推广成功',
  'en_title':'Success of Manual-Grinder Wheels at a Zhuzhou Enterprise',
  'en_summary':'Our cermet-bond wheels replaced resin-bond wheels at a major Zhuzhou manufacturer, boosting wheel life ~30x with no dressing needed.',
  'zh_body':'我公司开发出的手动磨床用高性能金属陶瓷粘接剂砂轮成功应用于株洲市某大型企业，替代了其原有树脂结合剂砂轮，成功解决了原有砂轮带来的砂轮消耗快、效率低及需要反复修整的问题。在使用过程中，我公司的金属陶瓷粘接剂砂轮充分体现出了高的切削力、耐磨性和自锐性，砂轮寿命提高30倍，且在磨削过程中无需修整，获得了用户的极大认可。'},

 {'cat':'company','date':'2014-01-01',
  'zh_title':'直径400mm1A1研发生产成功',
  'en_title':'Ø400mm 1A1 Cermet-Bond Diamond & CBN Wheels in Batch Production',
  'en_summary':'Sharpen achieved batch production of Ø400mm 1A1 cermet-bond diamond and CBN wheels, marking a milestone in domestic high-end wheel R&D.',
  'zh_body':"""直径400mm1A1金属陶瓷粘结剂金刚石砂轮和立方氮化硼砂轮研发成功并形成批量生产，投放市场。

应市场及厂家需求，萨普研发团队继2013年7月成功研发金属陶瓷磨削用立轴磨和平面磨（直径300mm，厚度20mm）砂轮，10月高速钢、钛合金、高温合金用砂轮开发成功后，于2013年11月又成功研发出直径400mm1A1金属陶瓷粘结剂金刚石砂轮和立方氮化硼砂轮，2014年1月形成批量生产，开始投放市场。

萨普相继研发出拥有自主知识产权的高性能金属陶瓷粘结剂金刚石砂轮和立方氮化硼砂轮制备及高速钢回转体强力开槽的整套技术，充分体现了萨普雄厚的研发实力和创新能力！""",
  'en_body':"""Sharpen successfully developed and put into batch production Ø400mm 1A1 cermet-bond diamond and CBN wheels for the market.

Following the July 2013 development of cermet-bond vertical- and surface-grinding wheels (Ø300mm, 20mm thick) and October 2013 wheels for HSS, titanium and superalloys, the team developed the Ø400mm 1A1 wheels in November 2013 and began batch production in January 2014. This demonstrates Sharpen’s proprietary, full-process capability in high-performance cermet-bond diamond/CBN wheels and strong-grooving of HSS rotary bodies."""},

 # ---------------- Industry News ----------------
 {'cat':'industry','date':'2024-06-07',
  'zh_title':'长沙市萨普新材料自主研发国内首家碳化硅衬底30000#精磨减薄砂轮',
  'en_title':'China’s First Domestic 30000# SiC Substrate Fine-Grinding Wheel',
  'en_summary':'Sharpen developed the country’s first 30000# fine-grinding wheel for SiC substrates, enabling low-damage, high-throughput wafer thinning.',
  'zh_body':"""碳化硅生产流程中的核心环节是碳化硅衬底的加工，主要分为碳化硅衬底的切割、薄化、抛光三道工序。其中薄化主要通过磨削与研磨实现，研磨又分为粗磨和精磨。萨普新材自主研发的碳化硅晶片减薄砂轮与磨削技术，从磨削过程中的晶圆损伤机理，到晶圆的粗磨和精磨减薄，用金刚石砂轮实现低损伤和高切削速率的晶圆薄化加工。

长沙市萨普新材料有限公司成立于2013年，是一家专注于粉末冶金新材料领域，集研发、生产、销售与技术服务为一体的国家高新技术企业，湖南省专精特新“小巨人”企业、长沙市智能制造试点企业、湖南省新材料企业、湖南省第一批创新型中小企业。始终秉持“科技创新驱动经济高质量发展”理念，依托长江学者特聘教授、国务院政府特殊津贴专家、国家科技进步一等奖获得者、国家杰出青年基金获得者——中南大学粉末冶金研究院贺跃辉教授领衔的精锐博士研发团队，致力于解决新材料“卡脖子”技术问题，实现进口产品的国产化替代。""",
  'en_body':"""A core step in SiC production is substrate processing — slicing, thinning and polishing. Thinning is achieved mainly by grinding and lapping (rough and fine). Sharpen’s self-developed SiC wafer thinning wheels and grinding technology address wafer damage mechanisms and deliver low-damage, high-removal-rate thinning from rough to fine grinding.

Founded in 2013, Sharpen is a national high-tech enterprise in powder-metallurgy new materials, a Hunan “Little Giant”, and a Changsha intelligent-manufacturing pilot, led by Prof. He Yuehui’s doctoral team, committed to domestic substitution of imported products."""},

 {'cat':'industry','date':'2017-11-28',
  'zh_title':'萨普新材研发成功3D热弯机TiNiCo超合金均热板',
  'en_title':'Sharpen Develops TiNiCo Superalloy Heat Spreader for 3D Hot-Bending',
  'en_summary':'Sharpen successfully developed the TiNiCo superalloy heat spreader used in 3D cover-glass hot-bending machines.',
  'zh_body':'萨普新材研发成功3D热弯机TiNiCo超合金均热板。该均热板用于3D手机盖板玻璃热弯模具，具有加热均匀、平面度高、使用寿命长的特点，是替代进口热弯模具均热板的关键材料，支持非标定制尺寸。'},

 {'cat':'industry','date':'2016-11-07',
  'zh_title':'公司砂轮使用取得新突破',
  'en_title':'Breakthrough in Wheel Use at a Shanghai Customer',
  'en_summary':'A Shanghai customer uses our diamond wheels to batch-produce 3-flute taper end mills, raising feed speed >30% vs a Korean brand.',
  'zh_body':"""长沙萨普新材料有限公司，作为高速高品质磨削系统技术解决方案的供应商和服务商，拥有完全自主知识产权，是提供硬质合金和高速钢回转体及刃具等制品磨抛加工技术整体解决方案的专业化高技术企业。公司技术力量雄厚，产品开发能力强，技术工艺娴熟，工艺制品水平高。

目前，上海某企业使用的就是我们公司生产的金刚石砂轮进行批量生产直径28mm、刃长50mm的三刃锥度铣刀，生产出的铣刀单边最高切深达到5.5mm，砂轮平均进给速度同比韩国某品牌砂轮提高了30%以上。

长沙萨普新材料公司自主研发超硬材料砂轮的特殊粘接剂，结合制备技术，所生产的金刚石砂轮在结构和性能上具有如下明显优势：
1. 砂轮工作层同时具有高容屑排屑性能及高的回旋强度；
2. 砂轮同时具有高的开刃性和保型性；
3. 砂轮基体具有轻质、高热导及抗环境腐蚀的性能特征；
4. 砂轮的工作层和基体实现全冶金结合，具有很高的界面稳定性；
5. 整体砂轮物化及力学性能高度匹配。""",
  'en_body':"""Changsha Sharpen is a specialized high-tech provider of high-speed, high-quality grinding-system solutions with full independent IP, offering complete polishing solutions for carbide and HSS rotary tools and inserts.

A Shanghai customer now uses Sharpen diamond wheels to batch-produce 3-flute tapered end mills (Ø28mm, 50mm flute length); the mills reach up to 5.5mm single-edge depth of cut, and the wheel’s average feed speed is more than 30% higher than a certain Korean brand.

Sharpen’s proprietary special bond gives its diamond wheels clear advantages: high chip accommodation and rotary strength; high self-sharpening and shape retention; a light, high-thermal-conductivity, corrosion-resistant core; full metallurgical bonding between layer and core for high interface stability; and closely matched physico-mechanical properties."""},

 {'cat':'industry','date':'2016-11-07',
  'zh_title':'数控刀具的失效形式及对策',
  'en_title':'Failure Modes of CNC Tools and Countermeasures',
  'en_summary':'A technical overview of CNC tool failure modes — flank wear, crater wear, plastic deformation, built-up edge — and how to mitigate them.',
  'zh_body':"""在切削过程中，刀具磨损到一定限度，刀刃崩刃或破损，刀刃卷刃（塑变）时，刀具丧失其切削能力或无法保障加工质量，称之为刀具失效。

刀具破损的主要形式及产生原因和对策如下：
1. 后刀面磨损：由机械应力引起的出现在后刀面上的摩擦磨损。应选择耐磨性高的刀具材料，同时降低切削速度，提高进给量，增大刀具后角。
2. 边界磨损：主切削刃上的边界磨损常见于与工件的接触面处。应降低切削速度和进给速度，同时选择耐磨刀具材料并增大前角使切削刃锋利。
3. 前刀面磨损（月牙洼磨损）：在前刀面上由摩擦和扩散导致的磨损。主要采用降低切削速度和进给速度，同时选择涂层硬质合金材料。
4. 塑性变形：切削刃在高温或高应力作用下产生的变形。应采取降低切削速度和进给速度，选择耐磨性高和导热系数高的刀具材料。
5. 积屑瘤：工件材料在刀具上的粘附。采取的对策有提高切削速度，选择涂层硬质合金或金属陶瓷等亲和力小的刀具材料，并使用冷却液。
6. 刃口剥落：切削刃上出现一些很小的缺口，而非均匀的磨损。应该在开始加工时降低进给速度，选择韧性好的刀具材料和切削刃强度高的刀片。""",
  'en_body':"""Tool failure occurs when a tool wears beyond a limit, chips or plastically deforms, losing its cutting ability or failing to guarantee quality.

Main failure modes and countermeasures:
1. Flank wear (mechanical friction) — use more wear-resistant tool material, lower cutting speed, raise feed, increase clearance angle.
2. Notch wear at the main cutting edge — lower speed/feed, use wear-resistant material, increase rake angle.
3. Crater wear (friction + diffusion on the rake face) — lower speed/feed, use coated carbide.
4. Plastic deformation (high temp/stress) — lower speed/feed, use high-wear-resistance, high-thermal-conductivity material.
5. Built-up edge (workpiece adhesion) — raise speed, use coated carbide/cermet with low affinity, apply coolant.
6. Edge chipping (small non-uniform notches) — lower feed at start, choose tougher material and stronger edge."""},

 {'cat':'industry','date':'2016-11-07',
  'zh_title':'工业制造业的发展将对磨具行业提出更高要求',
  'en_title':'Manufacturing Trends Raise the Bar for Abrasives',
  'en_summary':'Superabrasive products increasingly meet demanding grinding needs; new abrasive formats expand application scope.',
  'zh_body':"""纵观磨削领域的发展，未来磨削加工将对磨料磨具提出更高要求，从目前现状来判断，超硬制品恰恰满足这些新磨削需要。如CBN磨料具有良好热稳定性、硬度高、耐磨性好等特性，故其磨具磨削加工时线速度高、磨削效率高、磨具寿命也高，特别适宜加工高速钢、轴承钢、不锈钢、冷激铸铁等黑色金属材料。

超硬磨具应用，主要指以金属粉末、金属氧化物或CBN等超硬材料作为填充物，以树脂、陶瓷或金属结合剂制成磨具应用。目前，磨光片由超硬磨具带来高精度、高效率磨削效果已被广泛认可。

新型磨料磨具出现，如微米级多晶组成陶瓷微晶磨料、含微细金刚石磨粒球壳磨料、超精抛光用聚酯薄膜带等。这些新型磨料磨具所具有特点，使其磨削加工优势得到淋漓尽致展现。""",
  'en_body':"""Looking at grinding development, future machining will demand more of abrasives, and superabrasive products precisely meet these new needs. CBN, for example, offers excellent thermal stability, high hardness and wear resistance, enabling high wheel speed, high efficiency and long life — ideal for HSS, bearing steel, stainless and chilled cast iron.

Superabrasive tools use metal powder, metal oxide or CBN as filler with resin, vitrified or metal bonds; their high-precision, high-efficiency results are widely recognized. New formats — microcrystalline ceramic abrasives, diamond-shell abrasives, polyester-film polishing belts — further extend the advantages and application scope of grinding."""},

 {'cat':'industry','date':'2016-11-07',
  'zh_title':'金刚石制品的储存技巧',
  'en_title':'Storage Tips for Diamond Products',
  'en_summary':'Guidance on storing diamond wheels — avoid rolling, impact, moisture and harmful chemicals; observe expiry.',
  'zh_body':"""金刚石制品在储存中，不可滚动砂轮，以免造成裂纹、表面损伤，不可受强烈振动和冲击。滚轮制造精度高，采用内镀法工艺能够稳定生产高精度、复杂性面滚轮，使用寿命达到2～5万次。砂轮存放时间不应超过砂轮的有效期，树脂和橡胶结合剂的砂轮自出厂之日起，若存储时间超过一年，须经回转试验合格后才可使用。

加工硬脆材料的金刚石工具主要有各种金刚石锯和金刚石制品等，尽管各种工具的应用范围和加工特点不同，但其磨损机理都大致相同。砂轮存放场地应保持干燥，温度适宜，避免与其他化学品混放，防止砂轮受潮、低温、过热以及受有害化学品侵蚀使强度降低。""",
  'en_body':"""In storage, diamond wheels must not be rolled (to avoid cracks and surface damage) and must not be subjected to strong vibration or impact. Wheels should not be kept beyond their valid period; resin- or rubber-bond wheels stored over a year must pass a spin test before use. Storage areas should be dry, at suitable temperature, and segregated from other chemicals to prevent moisture, freezing, overheating or corrosive attack that reduces strength."""},

 {'cat':'industry','date':'2016-11-07',
  'zh_title':'中国刀具行业如何可持续发展',
  'en_title':'How China’s Cutting-Tool Industry Can Develop Sustainably',
  'en_summary':'Perspectives on the sustainable-development path for China’s cutting-tool industry.',
  'zh_body':'中国刀具行业要实现可持续发展，需在高端刀具材料、涂层技术与精密制造工艺上持续突破，减少对进口高端刀具的依赖；同时推动超硬材料砂轮等配套工艺的国产化，以材料与工艺协同创新提升整体加工效率与性价比，支撑制造业高质量发展。'},

 {'cat':'industry','date':'2016-11-07',
  'zh_title':'产品应用范畴',
  'en_title':'Product Application Scope',
  'en_summary':'Where diamond and CBN wheels apply — carbide tools, sapphire, cermet inserts (diamond); HSS, hardened steel, cast parts (CBN).',
  'zh_body':"""金刚石砂轮适用于加工如下材料：
1）硬质合金材料制备的刀具，回转体工具，模具和耐磨零部件等；
2）蓝宝石晶棒和晶片抛磨；
3）金属陶瓷刀片。

立方氮化硼砂轮适用于加工如下材料：
1）高速钢和高合金钢刃具，工具和模具；
2）高硬度淬火钢工零件和机床床身；
3）高硬度高合金铸件，例如缸套，耐磨件等。""",
  'en_body':"""Diamond wheels are suitable for:
1) Tools, rotary bodies, molds and wear parts made of carbide;
2) Sapphire ingots and wafer lapping/polishing;
3) Cermet inserts.

CBN wheels are suitable for:
1) HSS and high-alloy steel cutting tools, fixtures and molds;
2) Hardened-steel parts and machine beds;
3) High-hardness, high-alloy castings such as cylinder liners and wear parts."""},

 # ---------------- Frontier ----------------
 {'cat':'frontier','date':'2026-01-01',
  'zh_title':'萨普新材研究出第三代半导体SiC片精磨砂轮',
  'en_title':'Sharpen Debuts Third-Generation Semiconductor SiC Wafer Fine-Grinding Diamond Wheel',
  'en_summary':'Sharpen’s self-developed SiC fine-grinding diamond wheel with a lightweight metal-oxide cermet bond reaches 30000# grit, surface roughness under 2 nm, and is already serving several Chinese SiC substrate processors.',
  'zh_body':"""在半导体行业向第三代半导体材料升级的浪潮中，碳化硅晶圆因具备高热导率、高击穿电压等优异性能，在高温、高压、高频等极端工况下展现出显著优势，有望重塑新能源汽车、光伏、储能等万亿级市场。随着以碳化硅为代表的第三代半导体材料兴起，碳化硅等高硬度、高脆性晶圆加工技术一直是国内半导体产业"卡脖子"的问题之一。

凭借深耕新材料领域十余年的技术突破与市场验证，长沙市萨普新材料有限公司研发团队，在碳化硅晶圆磨削领域取得重大技术突破，自主研发的核心新产品——碳化硅晶圆减薄用精磨砂轮，核心指标满足行业需要。

公司研发团队采用高脆性的轻金属氧化物复合体作为金刚石砂轮粘结剂，保证了砂轮具有高锋利度，实现了大进给、快速磨削，同时又避免了金属离子污染；通过超高孔隙率自造孔技术，赋予了砂轮高容屑排屑能力，避免了砂轮堵塞和工件表面烧伤；30000#超细金刚石保证了优异的磨削质量，获得了超高光洁度磨削面，碳化硅表面粗糙度达到 2 nm 以内；砂轮性能优异，稳定性好，长期使用过程中，无崩缺、断齿现象。

产品应用领域主要用于 SiC 衬底减薄、SiC 器件的背减薄、分立器件，集成电路衬底硅片及原始硅片等的减薄。萨普新材碳化硅晶圆减薄砂轮系列产品已服务于数家国内三代半导体碳化硅衬底加工企业，并提供定制化整体解决方案。

在半导体晶圆减薄用砂轮这场科技与创新的攻坚战中，萨普新材以顽强的毅力和不懈的创新精神为利刃，在时代的号角声中奋楫争先，攻克了一系列关键技术难题，成功实现半导体晶圆减薄用砂轮的规模化生产，为我国半导体产业的发展提供了坚实有力的技术支撑。""",
  'en_body':"""As the semiconductor industry upgrades to third-generation materials, silicon carbide (SiC) wafers — with their high thermal conductivity and high breakdown voltage — deliver outstanding performance under extreme high-temperature, high-voltage and high-frequency conditions, and are poised to reshape the multi-trillion-dollar EV, photovoltaic and energy-storage markets. The grinding of hard, brittle SiC wafers has long been one of the "chokepoint" technologies in China’s semiconductor supply chain.

After more than a decade of R&D in advanced materials, Sharpen’s team has achieved a major breakthrough in SiC wafer grinding. Its self-developed core product — a fine-grinding diamond wheel for SiC wafer thinning — meets the industry’s key specifications.

The team uses a light-metal-oxide intermetallic composite as the diamond wheel’s bonding phase, delivering high sharpness, fast grinding at high feed rates, and avoiding metal-ion contamination; an ultra-high-porosity self-pore-forming technique gives the wheel superior chip-accommodation and chip-removal capability, avoiding clogging and workpiece surface burn; and the 30000# extra-fine diamond abrasive ensures excellent grinding quality with an ultra-smooth finished surface, keeping SiC surface roughness under 2 nm. The wheel’s performance is outstanding and stable, with no chipping or tooth-breakage even under long-term use.

The product is mainly used for thinning of SiC substrates, back-thinning of SiC devices, discrete devices, and thinning of IC substrate wafers and as-grown silicon wafers. Sharpen’s SiC wafer thinning wheel series now serves several domestic third-generation semiconductor SiC substrate processors, with customized turnkey solutions provided.

In this technology and innovation offensive over semiconductor wafer thinning wheels, Sharpen has cut through a series of key technical challenges with tenacity and relentless innovation, successfully scaling up production of semiconductor wafer thinning wheels and providing solid technical support for the development of China’s semiconductor industry.""",
  'image':'/assets/img/sic-wafer.jpg',
  'title_de':'Sharpen bringt Feinschliff-Diamantscheibe für SiC-Wafer der dritten Generation heraus',
  'title_ja':'サップ新素材、第三世代半導体SiCウェーハ用の超精密砥石を開発',
  'title_ko':'Sharpen, 3세대 반도체 SiC 웨이퍼 정밀 연마 휠 개발',
  'title_ru':'Sharpen разработала круг точной шлифовки для кристаллов SiC третьего поколения',
  'title_es':'Sharpen lanza rueda de rectificado fino de diamante para obleas SiC de tercera generación',
  'title_pt':'Sharpen lança roda de retificação fina de diamante para wafers de SiC de terceira geração',
  'title_fr':'Sharpen met au point une meule de rectification fine de diamant pour plaques SiC de 3ᵉ génération',
  'title_it':'Sharpen presenta la mole di finitura per wafer SiC di terza generazione',
  'title_tr':'Sharpen, üçüncü nesil SiC yarı iletkenleri için keskinleştirme taşını geliştirdi',
  'title_ar':'تطوير أسطوانة صقل دقيقة لمقاطع ثاني أكسيد السيليكون من الجيل الثالث',
  'title_vi':'Sharpen phát triển phôi mài chính xác cho tấm SiC bán dẫn thế hệ thứ ba'},

 {'cat':'frontier','date':'2017-11-28',
  'zh_title':'萨普新材研发成功3D热弯机TiNiCo超合金均热板',
  'en_title':'TiNiCo Superalloy Heat Spreader for 3D Hot-Bending',
  'en_summary':'Sharpen’s TiNiCo superalloy heat spreader enables uniform, high-flatness heating for 3D glass hot-bending molds.',
  'zh_body':'萨普新材研发成功3D热弯机TiNiCo超合金均热板。该均热板用于3D手机盖板玻璃热弯模具，具有加热均匀、平面度高、使用寿命长的特点，是替代进口热弯模具均热板的关键材料，支持非标定制尺寸。'},

 {'cat':'frontier','date':'2017-03-24',
  'zh_title':'SAP 粉末冶金高速钢简介',
  'en_title':'Introduction to SAP Powder Metallurgy High-Speed Steel',
  'en_summary':'An overview of PM-HSS vs conventional HSS and Sharpen’s non-atomization ball-milling route enabling domestic high-performance PM-HSS.',
  'zh_body':"""高速钢是一种极其重要的刀具材料，占全世界刀具销售额的45%，其中占轮齿刀具和拉刀等复杂多刃刀具销售额的85%。它集聚优异的红硬性、耐磨性、抗冲击性和可热处理性于一体，可在软化退火态加工成型，再通过淬火、回火热处理析出大量二次碳化物，实现材料的硬化和强化，具有硬质合金和金属陶瓷刀具所不具备的明显优势。

根据制备方法，可将高速钢分为传统铸锻高速钢和粉末冶金高速钢。由于高速钢较高的合金元素和碳元素含量，导致铸造高速钢出现组织粗大、成分偏析和性能各向异性等不可避免的缺点。而粉末冶金高速钢的出现从根本上避免了粗大碳化物的出现，具有碳化物组织细小均匀、性能各向同性等优点，是高速钢发展史上的里程碑。然而，我国并不具备高性能粉末冶金高速钢的生产能力。

商业粉末冶金高速钢出现于20世纪70年代，主要包括气雾化-热等静压法、喷射沉积法和超固相液相烧结法等。气雾化-热等静压工艺通过气雾化法制取高速钢粉末，再通过热等静压得到致密化的钢锭，可制备全致密、组织细小均匀、质量稳定、性能优良以及大尺寸的工件，却存在设备昂贵、技术门槛高、污染大、能耗高的缺点。喷射成形工艺是一种低成本制备高速钢的方法，拥有流程短、成本低和生产效率高的优点，却同样存在能耗高、污染大、合金化限制、杂质含量较高且心部不致密等缺点。超固相液相烧结工艺则是一种烧结温度处于液相+奥氏体+碳化物相区，借助一部分液相的出现实现致密化，具有流程短、投资少、成本低、材料利用率高、适合小规模生产、可制备含氮高速钢等优势，但液相促进棒状或粗大碳化物沿晶界分布，是这三种制备方法中组织最差的。

萨普新材非雾化粉末球磨法制备粉末高速钢的出现，给高性能粉末高速钢的国产化带来了振奋人心的消息。非雾化粉末球磨法创造性地以非雾化的球磨混合粉末为原料，可几乎不受限制地添加所需要的合金元素，通过固相真空活化烧结法，一步实现近净成形坯料的制备，再经热处理。""",
  'en_body':"""High-speed steel (HSS) is a vital tool material, accounting for 45% of global cutting-tool sales — and 85% of complex multi-edge tools such as gear hobs and broaches. It combines red hardness, wear resistance, impact resistance and heat-treatability, and can be shaped in the annealed state then hardened by quench and temper — advantages that cemented-carbide and cermet tools lack.

By process, HSS splits into conventional cast/forged and powder-metallurgy (PM) types. Cast HSS inevitably suffers coarse structure, segregation and anisotropy; PM-HSS fundamentally avoids coarse carbides, giving fine, uniform, isotropic structure — a milestone in HSS history. Yet China long lacked the capability to produce high-performance PM-HSS.

Commercial PM-HSS appeared in the 1970s via gas-atomization+HIP, spray forming, and supersolidus liquid-phase sintering — each with trade-offs in cost, pollution, alloying limits and density. Sharpen’s non-atomization ball-milling route is exciting for domestic high-performance PM-HSS: it uses non-atomized ball-milled mixed powder as feedstock, allowing almost unrestricted alloy additions, and achieves near-net-shape preforms in one step via solid-state vacuum-activated sintering, followed by heat treatment."""},
]

# Build per-language markdown
def image_line(a, lang):
    """Return a markdown image line if the article has one, else ''.
    Alt text is localized: zh uses zh_title; en uses en_title; other languages
    use the localized title_<lang> when present, else en_title."""
    if not a.get('image'):
        return ''
    if lang == 'zh':
        alt = a.get('zh_title', '')
    elif lang == 'en':
        alt = a.get('en_title') or a.get('zh_title') or ''
    else:
        alt = a.get('title_' + lang) or a.get('en_title') or a.get('zh_title') or ''
    alt = a.get('alt_' + lang, alt)
    return f"![{alt}]({a['image']})"

# Localized page titles, descriptions, category labels, date labels for each language.
PAGE = {
  'de': dict(page='News', h1='Presse & Newsroom',
             desc='Changsha Sharpen New Materials: Unternehmensnews, Branchen- und Technologietrends.',
             cats=dict(company='Unternehmensnachrichten', industry='Branchennews', frontier='Technologietrends'),
             date='Veröffentlicht: '),
  'ja': dict(page='ニュース', h1='ニュースルーム',
             desc='長沙Sharpen新材料：企業ニュース、業界動向、最先端技術の最新情報。',
             cats=dict(company='企業ニュース', industry='業界動向', frontier='業界最前線'),
             date='公開日: '),
  'ko': dict(page='뉴스', h1='뉴스룸',
             desc='Changsha Sharpen New Materials: 기업 뉴스, 업계 동향, 기술 개발 현황.',
             cats=dict(company='기업 뉴스', industry='업종 뉴스', frontier='산업 최전선'),
             date='게시일: '),
  'ru': dict(page='Новости', h1='Новостной центр',
             desc='Changsha Sharpen New Materials: корпоративные новости, отраслевые обзоры и технологические тенденции.',
             cats=dict(company='Корпоративные новости', industry='Отраслевые новости', frontier='Технологии передового края'),
             date='Опубликовано: '),
  'es': dict(page='Noticias', h1='Sala de prensa',
             desc='Changsha Sharpen New Materials: noticias de empresa, tendencias de la industria y avances tecnológicos.',
             cats=dict(company='Noticias de empresa', industry='Noticias del sector', frontier='Fronteras tecnológicas'),
             date='Publicado: '),
  'pt': dict(page='Notícias', h1='Sala de imprensa',
             desc='Changsha Sharpen New Materials: notícias da empresa, tendências do setor e avanços tecnológicos.',
             cats=dict(company='Notícias da empresa', industry='Notícias do setor', frontier='Frentes tecnológicas'),
             date='Publicado: '),
  'fr': dict(page='Actualités', h1='Salle de presse',
             desc='Changsha Sharpen New Materials: actualités de l’entreprise, tendances sectorielles et avancées technologiques.',
             cats=dict(company='Actualités de l’entreprise', industry='Actualités du secteur', frontier='Fronières technologiques'),
             date='Publié le: '),
  'it': dict(page='Notizie', h1='Sala stampa',
             desc='Changsha Sharpen New Materials: notizie aziendali, tendenze di settore e sviluppi tecnologici.',
             cats=dict(company='Notizie aziendali', industry='Notizie del settore', frontier='Frontiere tecnologiche'),
             date='Pubblicato: '),
  'tr': dict(page='Haberler', h1='Haber merkezi',
             desc='Changsha Sharpen New Materials: şirket haberleri, sektör trendleri ve teknoloji gelişmeleri.',
             cats=dict(company='Şirket haberleri', industry='Sektör haberleri', frontier='Teknoloji gelişmeleri'),
             date='Yayınlandığı: '),
  'ar': dict(page='الأخبار', h1='مركز الأخبار',
             desc='Changsha Sharpen New Materials: أخبار الشركة، اتجاهات الصناعة، والتطورات التكنولوجية.',
             cats=dict(company='أخبار الشركة', industry='أخبار القطاع', frontier='تقنيات السانك'),
             date='نُشر في: '),
  'vi': dict(page='Tin tức', h1='Tín hiệu và tin tức',
             desc='Changsha Sharpen New Materials: tin doanh nghiệp, xu hướng ngành và các đột phá công nghệ.',
             cats=dict(company='Tin doanh nghiệp', industry='Tin ngành', frontier='Công nghệ tiên tiến'),
             date='Công bố: '),
}

def build(lang, as_lang=None):
    # as_lang: when set to 'zh-tw', front-matter uses that lang/permalink and
    # Chinese content pieces are converted to traditional via cc.convert.
    conv = (as_lang == 'zh-tw')
    def tz(s):
        return cc.convert(s) if conv else s
    if lang=='zh':
        fm_lang = as_lang or 'zh'
        cv = {k:v[0] for k,v in CAT.items()}
        if conv:
            cv = {k: cc.convert(v) for k,v in cv.items()}
        lines=["---\nlayout: page.njk\nlang: " + fm_lang + "\npermalink: /" + fm_lang + "/news/\ntitle: \"" + tz("新闻中心") + "\"\ndescription: \"" + tz("长沙市萨普新材料有限公司新闻中心：公司新闻、行业资讯与行业前沿发展现状。") + "\"\n---","","# " + tz("新闻中心"),""]
        for cat in ['company','industry','frontier']:
            lines.append("## " + cv[cat]); lines.append("")
            for a in [x for x in articles if x['cat']==cat]:
                lines.append("### " + tz(a['zh_title']))
                lines.append(tz("*发布日期：") + a['date'] + "*")
                lines.append("")
                img=image_line(a,'zh')
                if img:
                    img=tz(img)
                    lines.append(img); lines.append("")
                lines.append(clean(tz(a['zh_body'])))
                lines.append("")
        return "\n".join(lines)
    if lang=='en':
        cv = {k:v[2] for k,v in CAT.items()}
        lines=["---\nlayout: page.njk\nlang: en\npermalink: /en/news/\ntitle: \"News\"\ndescription: \"Changsha Sharpen New Materials newsroom: company news, industry insights and frontier developments.\"\n---","","# Newsroom",""]
        for cat in ['company','industry','frontier']:
            lines.append(f"## {cv[cat]}"); lines.append("")
            for a in [x for x in articles if x['cat']==cat]:
                lines.append(f"### {a['en_title']}")
                lines.append(f"*Date: {a['date']}*")
                lines.append("")
                img=image_line(a,'en')
                if img:
                    lines.append(img); lines.append("")
                lines.append(clean(a.get('en_summary','')))
                if a.get('en_body'):
                    lines.append("")
                    lines.append(clean(a['en_body']))
                lines.append("")
        return "\n".join(lines)
    # Generic language (de/ja/ko/ru/es/pt/fr/it/tr/ar/vi): reuse English
    # bodies + summaries, and per-language article titles from TITLES.
    meta = PAGE.get(lang)
    if not meta:
        raise ValueError('No PAGE meta for lang: ' + lang)
    lines=["---","layout: page.njk",f"lang: {lang}",f"permalink: /{lang}/news/","title: \"" + meta['page'] + "\"","description: \"" + meta['desc'] + "\"","---","","# " + meta['h1'],""]
    for cat in ['company','industry','frontier']:
        lines.append(f"## {meta['cats'][cat]}"); lines.append("")
        for a in [x for x in articles if x['cat']==cat]:
            title = a.get('title_' + lang) or a.get('en_title')
            lines.append(f"### {title}")
            lines.append(f"*{meta['date']}{a['date']}*")
            lines.append("")
            img=image_line(a,lang)
            if img:
                lines.append(img); lines.append("")
            lines.append(clean(a.get('en_summary','')))
            if a.get('en_body'):
                lines.append("")
                lines.append(clean(a['en_body']))
            lines.append("")
    return "\n".join(lines)

import os as _os
for L in ['de','ja','ko','ru','es','pt','fr','it','tr','ar','vi']:
    _os.makedirs(L, exist_ok=True)
    open(f'{L}/news.md','w',encoding='utf-8').write(build(L))
    print(f"generated {L}/news.md ({len(build(L))} chars)")

os.makedirs('zh',exist_ok=True); os.makedirs('en',exist_ok=True); os.makedirs('zh-tw',exist_ok=True)
open('zh/news.md','w',encoding='utf-8').write(build('zh'))
open('en/news.md','w',encoding='utf-8').write(build('en'))
# zh-tw: independent front-matter (lang: zh-tw / permalink: /zh-tw/news/),
# only the Chinese content pieces are converted to traditional.
tw = build('zh', as_lang='zh-tw')
open('zh-tw/news.md','w',encoding='utf-8').write(tw)
print("zh news chars:", len(build('zh')))
print("en news chars:", len(build('en')))
print("zh-tw news chars:", len(tw))
print("articles:", len(articles))
