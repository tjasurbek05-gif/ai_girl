// This mirrors characters/characters.json on the bot
// photo_url: use Telegram file URLs or placeholder
// When you get file_ids from Telegram, replace photo_url with actual CDN URLs

export const CHARACTERS = [
  {
    id: "malika",
    name: "Malika",
    avatar: "🌺",
    type: "realistic",
    photo_url: null,
    tagline: {
      en: "Mysterious and elegant",
      ru: "Загадочная и элегантная",
      uz: "Sirli va nafis",
    },
    scenarios: [
      { id: "tashkent_cafe",  label: { en: "☕ Tashkent Café",  ru: "☕ Кафе в Ташкенте", uz: "☕ Toshkent Kafesi" }, gems_cost: 0 },
      { id: "dubai_yacht",    label: { en: "🛥️ Dubai Yacht",    ru: "🛥️ Яхта в Дубае",   uz: "🛥️ Dubay Yaxtasi" }, gems_cost: 0 },
    ],
  },
  {
    id: "katya",
    name: "Katya",
    avatar: "🌸",
    type: "realistic",
    photo_url: null,
    tagline: {
      en: "Sweet and genuine",
      ru: "Милая и искренняя",
      uz: "Mehribon va samimiy",
    },
    scenarios: [
      { id: "moscow_park", label: { en: "🌿 Moscow Park", ru: "🌿 Парк в Москве", uz: "🌿 Moskva Bog'i" }, gems_cost: 0 },
    ],
  },
  {
    id: "nastya",
    name: "Nastya",
    avatar: "💎",
    type: "realistic",
    photo_url: null,
    tagline: {
      en: "Bold and unapologetic",
      ru: "Дерзкая и уверенная",
      uz: "Jasur va ishonchli",
    },
    scenarios: [
      { id: "moscow_club",  label: { en: "🌃 Moscow Night Club", ru: "🌃 Ночной клуб",    uz: "🌃 Kechki klub"   }, gems_cost: 0 },
      { id: "dubai_resort", label: { en: "🏖️ Dubai Resort",      ru: "🏖️ Курорт в Дубае", uz: "🏖️ Dubay kurort"  }, gems_cost: 30 },
    ],
  },
  {
    id: "leyla",
    name: "Leyla",
    avatar: "🌙",
    type: "realistic",
    photo_url: null,
    tagline: {
      en: "Warm and poetic",
      ru: "Тёплая и поэтичная",
      uz: "Iliq va she'riy",
    },
    scenarios: [
      { id: "baku_boulevard", label: { en: "🌊 Baku Boulevard",  ru: "🌊 Бульвар в Баку", uz: "🌊 Boku bulvari"   }, gems_cost: 0  },
      { id: "samarkand",      label: { en: "🏛️ Samarkand",       ru: "🏛️ Самарканд",      uz: "🏛️ Samarqand"     }, gems_cost: 20 },
    ],
  },
  {
    id: "airi",
    name: "Airi",
    avatar: "⚡",
    type: "anime",
    photo_url: null,
    tagline: {
      en: "Loud, fun, zero filter",
      ru: "Яркая, весёлая, без фильтров",
      uz: "Yorqin, qiziqarli, befarq",
    },
    scenarios: [
      { id: "anime_arcade",   label: { en: "🕹️ Tokyo Arcade",   ru: "🕹️ Аркада в Токио",  uz: "🕹️ Tokio Arkada"  }, gems_cost: 0  },
      { id: "anime_rooftop",  label: { en: "🌆 Rooftop Sunset", ru: "🌆 Закат на крыше",   uz: "🌆 Tom usti quyosh" }, gems_cost: 20 },
    ],
  },
  {
    id: "valeria",
    name: "Valeria",
    avatar: "🖤",
    type: "anime",
    photo_url: null,
    tagline: {
      en: "Dark, sharp, magnetic",
      ru: "Тёмная, острая, притягательная",
      uz: "Qorong'u, o'tkir, jozibali",
    },
    scenarios: [
      { id: "anime_library", label: { en: "📚 Midnight Library", ru: "📚 Полночная библиотека", uz: "📚 Yarim tun kutubxona" }, gems_cost: 0  },
      { id: "anime_garden",  label: { en: "🌸 Moon Garden",      ru: "🌸 Лунный сад",          uz: "🌸 Oy bog'i"            }, gems_cost: 20 },
    ],
  },
];
