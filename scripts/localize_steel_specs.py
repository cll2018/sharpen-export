# -*- coding: utf-8 -*-
"""Localize the steel-bonded-carbide application specs in every products.md.
English stays English; each of the 13 non-EN languages gets its own localized
4-line spec list. Only the 4 <li> lines inside id="steel-bonded-carbide" change."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN = [
 "Applications: cold-extrusion, cold-heading and blanking/punching dies, firebrick shaping molds; replaces YG20-type carbide in high-load die cores.",
 "Cutting tools: carbide and high-speed-steel tooling for titanium and nickel alloys, rock-boring and geological-drilling tools.",
 "Wear parts: rollers, nozzles, bearings; high-grade grades used in aerospace and submarine-navigation components.",
 "Support for diamond/CBN grinding-wheel fixtures and CBN-mill-forming jigs; meets accuracy and wear requirements.",
]

# Localized 4-line specs per language (same order as EN).
T = {
 "zh": [
  "应用：冷挤压、冷镦及落料/冲孔模具、耐火砖成型模具；替代 YG20 型硬质合金用于高载荷模具芯。",
  "切削刀具：用于钛合金与镍合金、岩芯钻探及地质钻探的硬质合金与高速钢刀具。",
  "耐磨件：辊轮、喷嘴、轴承；高等级牌号用于航空航天及潜艇导航部件。",
  "金刚石/CBN 砂轮夹具及 CBN 铣削成型工装支撑；满足精度与耐磨要求。",
 ],
 "zh-tw": [
  "應用：冷擠壓、冷墩及落料/沖孔模具、耐火磚成型模具；替代 YG20 型硬質合金用於高負荷模具芯。",
  "切削刀具：用於鎢鋼與高速鋼刀具加工鈦合金、鎳合金，岩芯鑽探及地質鑽探。",
  "耐磨件：輥輪、噴嘴、軸承；高等級牌號用於航空航天及潛艇導航部件。",
  "金刚石/CBN 砂輪夾具及 CBN 銑削成型工装支撐；滿足精度與耐磨要求。",
 ],
 "de": [
  "Anwendungen: Kaltfließpress-, Kaltschmied- und Stanz-/Prägeleisten, Brandform-Formen für Schamott; ersetzt YG20-Hartmetall in hochbelasteten Stanzkernen.",
  "Schneidwerkzeuge: Hartmetall- und HSS-Werkzeuge für Titan- und Nickellegierungen, Tiefbohr- und geologische Bohrwerkzeuge.",
  "Verschleißteile: Rollen, Düsen, Lager; Hochwertigkeits-Güten für Luftfahrt- und U-Boot-Navigationskomponenten.",
  "Haltevorrichtungen für Diamant-/CBN-Schleifscheiben und CBN-Fräsform-Jigs; erfüllt Genauigkeits- und Verschleißanforderungen.",
 ],
 "ja": [
  "用途：冷間押出し、冷間鍛打、ブラント/パンチ金型、耐火レン形成型金型；高負荷の金型コアでYG20型超硬合金に置き換え。",
  "切削工具：チタン・ニッケル合金向けの超硬・高速度鋼工具、岩盤ボーリング・地質ドリリング工具。",
  "耐磨耗部品：ローラー、ノズル、ベアリング；高グレード品は宇宙航空・潜水艦ナビゲーション部品に使用。",
  "ダイヤモンド/CBN砥石のホルダーとCBNミルフォーミング治具のサポート；精度・耐摩耗要件を満たす。",
 ],
 "ko": [
  "용도: 콜드-외압, 콜드-두이핑, 프레스/펀칭 다이, 내화물 성형 몰드; 고하중 다이 코어에서 YG20형 세라멘트 카바이드를 대체.",
  "절삭 공구: 타이타늄·니켈 합금용 카바이드 및 HSS 공구, 암석 굴진 및 지질 시추 공구.",
  "마모 부품: 롤러, 노즐, 베어링; 고급 등급은 항공우주 및 잠수함 내비게이션 부품에 사용.",
  "다이아몬드/CBN 연마 휠 픽스처 및 CBN 밀-포밍 지그 지원; 정밀도와 내마모 요건 충족.",
 ],
 "ru": [
  "Применение: холодное выдавливание, холодная ковка, вырубные/пробойные штампы, формы для огнеупорных кирпичей; заменяет твёрдосплав YG20 в нагруженных штамп-ядрах.",
  "Режущий инструмент: твёрдосплавной и БРС-инструмент для титановых и никелевых сплавов, горно-взрывные и геологические буровые инструменты.",
  "Износостойкие детали: ролики, насадки, подшипники; высокотехнологичные марки для аэрокосмических и систем навигации подводных лодок.",
  "Поддержка станин и фиксаторов для алмазных/CBN-кругов и CBN-фрезерных-форм; соответствует требованиям к точности и износостойкости.",
 ],
 "es": [
  "Aplicaciones: extrusión en frío, encabezado en frío, diestros de troquelado/picado, moldes de refractarios; sustituye al carburo YG20 en núcleos de diestros de alta carga.",
  "Herramientas de corte: herramienta de carburo y ACP (HSS) para aleaciones de titanio y níquel, y para barrenos de roca y perforación geológica.",
  "Piezas de desgaste: rodillos, boquillas, rodamientos; las altas calidades se usan en componentes aeroespaciales y de navegación de submarinos.",
  "Soporte de fijadores de meules de diamante/CBN y de jigs de rectificado CBN; cumple requisitos de precisión y desgaste.",
 ],
 "pt": [
  "Aplicações: extrusão a frio, forjamento a frio, estampos de punção/troquel, moldes de refratário; substitui o carbureto YG20 em núcleos de estampos de alta carga.",
  "Ferramentas de corte: ferramentas de carbureto e Aço Rápido (HSS) para ligas de titânio e níquel, perfuração de rocha e perfuração geológica.",
  "Peças de desgaste: rolos, bicos, rolamentos; as grades de alta performance usadas em componentes aeroespaciais e de navegação de submarinos.",
  "Suporte para suportes de rodas de diamante/CBN e jig de usinagem CBN; atende requisitos de precisão e desgaste.",
 ],
 "fr": [
  "Applications: extrusion à froid, emboutissage froid, poinçons/trocs de frappe, moules pour briques réfractaires ; remplace le carbure YG20 dans les cœurs de matrices à forte charge.",
  "Outils de coupe : outils en carbure et ACP (HSS) pour alliages de titane et de nickel, perçage de roche et forage géologique.",
  "Pièces de wear : rouleaux, buses, roulements ; les grades haut de gamme utilisés dans les composants aérospatiaux et de navigation de sous-marins.",
  "Support de fixations de meules de diamant/CBN et de gabarits d'usinage CBN ; répond aux exigences de précision et de wear.",
 ],
 "it": [
  "Applicazioni: estrusione a freddo, stampaggio a freddo, stampi di boccettatura/punzonatura, stampi per mattoni refrattari; sostituisce il carburo YG20 nei nuclei di stampi ad alta sollecitazione.",
  "Utensili da taglio: utensili in carburo e HSS per leghe di titanio e nichel, perforazione di roccia e trivellazione geologica.",
  "Parti soggette a wear: rullini, ugelli, cuscinetti; le qualità d'alta gamma usate nei componenti aerospaziali e di navigazione di sottomarini.",
  "Supporto per supporti di mole diamantate/CBN e jig per l'usinatura CBN; soddisfa i requisiti di precisione e wear.",
 ],
 "tr": [
  "Uygulamalar: soğuk ekstrüzyon, soğuk dövme, soğuk kesme/dabba kalıpları, ateş tuğlası şekillendirme kalıpları; yüksek yük altında YG20 tipi sert metali değiştirir.",
  "Kesme takımları: titanyum ve nikel alaşımları için sert metal ve HSS takımları, kaya kazma ve jeolojik delme takımları.",
  "Aşınma parçaları: makaralar, nozullar, yataklar; yüksek dereceler havacılık-alt-uzay ve denizaltı navigasyon bileşenlerinde kullanılır.",
  "Elmas/CBN zımpara tezgâhı dübelleri ve CBN talaş şekillendirme jig'lerinin desteği; hassasiyet ve aşınma gereksinimlerini karşılar.",
 ],
 "ar": [
  "تطبيقات: البثق البارد، والعجن البارد، وقوالب القصّ/النقش، وقوالب تشكيل طوب البناء؛ تحل مكان كربيد YG20 في نوى القوالب عالية الحِمل.",
  "أدوات القطع: أدوات كربيد وفولاذ عالي السرعة للمبخرات والأدوات لحملات التنقيب الجيولوجية والتنقيب عن الخامات الصلبة.",
  "قطع التآكل: أسطوانات، فوهات، محامل؛ الدرجات العالية تُستخدم في مركبات الفضاء ومكونات توجيه الغواصات.",
  "دعامة لفكس وأسطوانه صقل الماس/CBN وفكس تشكيل CBN؛ يلبّي متطلبات الدقة والتآكل.",
 ],
 "vi": [
  "Ứng dụng: ép đùn nguội, dập nguội, khuôn đột/dập/cắt, khuôn tạo hình gạch chịu lửa; thay thế carbide YG20 ở lõi khuôn tải trọng cao.",
  "Dụng cụ cắt: dụng cụ carbide và thép tốc độ cao (HSS) cho hợp kim titan và niken, khoan đá và khoan địa chất.",
  "Chi tiết chịu mài mòn: con lăn, vòi, bạc lót; các mác cao cấp dùng trong bộ phận hàng không vũ trụ và định hướng tàu ngầm.",
  "Hỗ trợ bộ cố định phôi mài kim cương/CBN và jig CBN; đáp ứng yêu cầu độ chính xác và mài mòn.",
 ],
}

EN_BLOCK = "\n".join("      <li>" + e + "</li>" for e in EN)

def build(lang_lines):
    return "\n".join("      <li>" + l + "</li>" for l in lang_lines)

changed = 0
for lang, lines in T.items():
    path = os.path.join(ROOT, lang, "products.md")
    with open(path, encoding="utf-8") as f:
        c = f.read()
    new = build(lines)
    if EN_BLOCK in c:
        c = c.replace(EN_BLOCK, new, 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)
        changed += 1
        print("updated", lang)
    else:
        print("WARN: EN block not found in", lang)

# English stays as-is (already English).
print("Total products.md updated (non-EN):", changed)
