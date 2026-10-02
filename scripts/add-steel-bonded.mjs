// One-shot: insert the steel-bonded-carbide entry into every language array
// in _data/products.js so the homepage card loop (products[lang]) renders it.
import { createRequire } from "node:module";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const require = createRequire(__filename);
const SRC = path.join(__dirname, "..", "_data", "products.js");

const entry = {
  en: { name: "Steel-Bonded Cemented Carbide",
    summary: "Steel-bonded cemented carbide for tooling and demanding wear parts — machinable, forgeable and weldable in the annealed condition, hardened to HRC 60–70, pairing high-cobalt carbide wear resistance with far greater toughness; full-life cost far lower than alloy die steels." },
  zh: { name: "钢结硬质合金",
    summary: "面向刀具与苛刻耐磨件——退火态可直接车、铣、钻加工，支持锻造与焊接，无需特殊设备即可成型；淬硬后 HRC 60–70，耐磨性接近高钴硬质合金、韧性远优于普通硬质合金，全生命周期成本远低于常规合金模具钢。" },
  "zh-tw": { name: "鋼結硬質合金",
    summary: "面向刀具與苛刻耐磨件——退火態可直接車、銑、鑽加工，支持鍛造與焊接，無需特殊設備即可成型；淬硬後 HRC 60–70，耐磨性接近高鉻硬質合金、韌性遠優於普通硬質合金，全生命週期成本遠低於常規合金模具鋼。" },
  de: { name: "Stahlgebundener Hartmetall (Cemetal)",
    summary: "Stahlgebundener Hartmetall für Werkzeuge und anspruchsvolle Verschleißteile — im geglühten Zustand bearbeitbar, schmiedbar und schweißbar, nach Härtung HRC 60–70; verbindet die Verschleißbeständigkeit von Hochcobalt-Hartmetall mit deutlich höherer Zähigkeit." },
  ja: { name: "鋼結合硬質合金（Cemetal）",
    summary: "工具・高荷重耐磨部材向け。焼きなまし状態でも切削・锻造・溶接加工が可能、HRC 60–70 まで高硬度化でき、コバルト高配合硬质合金に匹敵する耐摩耗性と高い靭性を兼ね備え、合金型鋼より全ライフコストを大幅に削減します。" },
  ko: { name: "강결합 세멘테드 카바이드 (Cemetal)",
    summary: "공구와 고하중 마모 부품을 위한 강결합 세멘테드 카바이드 —annealed 상태에서 가공/단조/용접 가능, HRC 60–70까지 경화되며 고코발트 카바이드에匹敵하는 내마모성과 훨씬 높은 인성을 제공해 합금 다이 스틸 대비 총 수명 비용을 크게 낮춥니다." },
  ru: { name: "Сталевая керамика (сталь-карбид, Cemetal)",
    summary: "Сталь-карбидные твёрдосплавные материалы для инструмента и нагруженных изнашивающихся деталей: обрабатываются, ковка и сварка в отожжённом состоянии, упрочнение до HRC 60–70, износостойкость на уровне высококобальтовых сплавов при значительно большей вязкости." },
  es: { name: "Carburo Cementado Unido con Acero (Cemetal)",
    summary: "Carburo cementado unido con acero para herramientas y piezas de desgaste exigentes: mecanizable, forjable y soldable en estado recocido, endurecido a HRC 60–70; combina la resistencia al desgaste del carburo de cobalto alto con mucha mayor tenacidad y menor coste total." },
  pt: { name: "Carbeto Cimentado Unido com Aço (Cemetal)",
    summary: "Carbeto cimentado unido com aço para ferramentas e peças de desgaste severas — usinável, forjável e soldável no estado recozido, endurecido para HRC 60–70, combinando resistência ao desgaste do carbeto de cobalto alto com muito mais tenacidade e menor custo de vida útil." },
  fr: { name: "Carbure Cémentié Lié à l'Acier (Cemetal)",
    summary: "Carbure cémentié lié à l'acier pour l'outillage et les pièces de wear exigeantes — usinable, forgeable et soudable à l'état recuit, durci jusqu'à HRC 60–70 ; combine la résistance à l'usure du carbure à haut cobalt avec une ténacité nettement supérieure et un coût total réduit." },
  it: { name: "Carburo Sinterato Legato all'Acciaio (Cemetal)",
    summary: "Carburo sinterato legato all'acciaio per utensili e parti soggette a severo usura — lavorabile, forgiabile e saldabile nello stato ricotto, induribile a HRC 60–70, combina la resistenza all'usura del carburo alto-cobalto con tenacità nettamente maggiore e costo nel ciclo di vita inferiore." },
  tr: { name: "Çelik Bağlı Sementize Krom (Cemetal)",
    summary: "Kesici takım ve zor aşınma parçaları için çelik bağlı sementize krom — tavlalı durumda işlenebilir, dövülebilir ve kaynaklanabilir, HRC 60–70 sertleştirilir; yüksek kobalt karbür dayanıklılığını çok daha yüksek toklukla birleştirir ve yaşam döngüsü maliyetini düşürür." },
  ar: { name: "الكربيد المصمت بالصلب (Cemetal)",
    summary: "كربيد مثبت بالصلب للأدوات وقطع التآكل الصعبة — قابل للميكانيكا والخراطة والتهذيب واللحام في الحالة المبلورة، يَصلَّب حتى HRC 60–70، يجمع بين مقاومة التآكل للكربيد عالي الكوبالت ومتانة أعلى بكثير وتكلفة دورة حياة أقل." },
  vi: { name: "Carbide Kết Dạng Thép (Cemetal)",
    summary: "Carbide kết dạng thép (cemented carbide) cho dụng cụ và bộ phận chịu mài mòn khắc nghiệt — gia công được ở trạng thái ủ, có thể rèn và hàn mà không cần thiết bị đặc biệt, tôi cứng tới HRC 60–70, kết hợp độ chống mài mòn của carbide cao coban với độ dẻo dai vượt trội và chi phí vòng đời thấp hơn." }
};
const IMG = "/assets/img/steel-bonded-carbide.png";

const data = require(SRC);
const langs = Object.keys(data);
console.log("langs:", langs.join(", "));
let missing = [];
for (const l of langs) {
  if (!data[l]) { missing.push(l); continue; }
  const ids = data[l].map(p => p.id);
  if (ids.includes("steel-bonded-carbide")) { console.log("skip", l); continue; }
  data[l].push({ id: "steel-bonded-carbide", name: entry[l].name, summary: entry[l].summary, image: IMG });
  console.log("added", l, "->", data[l].length, "entries");
}
if (missing.length) console.warn("LANGS WITHOUT DATA:", missing.join(", "));
fs.writeFileSync(SRC, JSON.stringify(data, null, 2) + "\n", "utf8");
console.log("products.js updated with", langs.length, "language arrays; each now contains steel-bonded-carbide.");
