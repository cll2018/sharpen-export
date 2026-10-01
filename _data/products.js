// Product catalogue used by the homepage cards and the products page.
// Keyed by language. `image` points to a file you drop in assets/img.
// `id` is used as the in-page anchor on the products page.
module.exports = {
  en: [
    {
      id: "diamond-wheels",
      name: "Diamond Grinding Wheels",
      summary:
        "High-performance diamond wheels for hard-brittle materials — sapphire, zirconia, carbide, PCD/PCBN.",
      image: "/assets/img/diamond-wheels.jpg",
    },
    {
      id: "cbn-wheels",
      name: "CBN Grinding Wheels",
      summary:
        "Cubic boron nitride wheels with high sharpness and long life for high-speed steel and hard metals.",
      image: "/assets/img/cbn-wheels.jpg",
    },
    {
      id: "pm-high-speed-steel",
      name: "Powder Metallurgy High-Speed Steel",
      summary:
        "SAP PM high-speed steel with uniform carbides for cutting tools and precision rolls.",
      image: "/assets/img/pm-steel.jpg",
    },
    {
      id: "tinico-heat-spreader",
      name: "TiNiCo Superalloy Heat Spreader",
      summary:
        "TiNiCo superalloy heat spreader for 3D glass hot-bending and semiconductor thermal management.",
      image: "/assets/img/tinico.jpg",
    },
  ],
  zh: [
    {
      id: "diamond-wheels",
      name: "金刚石砂轮",
      summary:
        "面向硬脆材料（蓝宝石、氧化锆、硬质合金、PCD/PCBN）的高性能金刚石砂轮。",
      image: "/assets/img/diamond-wheels.jpg",
    },
    {
      id: "cbn-wheels",
      name: "立方氮化硼砂轮",
      summary:
        "高锋利度、长寿命的立方氮化硼砂轮，适用于高速钢及难加工硬金属。",
      image: "/assets/img/cbn-wheels.jpg",
    },
    {
      id: "pm-high-speed-steel",
      name: "粉末冶金高速钢",
      summary:
        "SAP 粉末冶金高速钢，碳化物分布均匀，适用于切削刀具与精密轧辊。",
      image: "/assets/img/pm-steel.jpg",
    },
    {
      id: "tinico-heat-spreader",
      name: "TiNiCo 超合金均热板",
      summary:
        "TiNiCo 超合金均热板，用于 3D 玻璃热弯与半导体热管理。",
      image: "/assets/img/tinico.jpg",
    },
  ],
};
