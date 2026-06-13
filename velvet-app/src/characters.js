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
    id: "mrs_grace",
    name: "Mrs. Grace",
    avatar: "👠",
    type: "realistic",
    photo_url: null,
    tagline: {
      en: "Confident, classy, in control",
      ru: "Уверенная и элегантная",
      uz: "Ishonchli va nafis",
    },
    scenarios: [
      { id: "penthouse_office", label: { en: "🏙️ Penthouse Office",     ru: "🏙️ Офис в пентхаусе",  uz: "🏙️ Penthaus ofisi"     }, gems_cost: 0  },
      { id: "grace_spa",        label: { en: "💆 Private Spa Evening", ru: "💆 Вечер в спа",        uz: "💆 Shaxsiy spa kechasi" }, gems_cost: 35 },
    ],
  },
  {
    id: "jane",
    name: "Jane",
    avatar: "📷",
    type: "realistic",
    photo_url: null,
    tagline: {
      en: "Girl-next-door with a wild side",
      ru: "Соседская девушка с дерзким характером",
      uz: "Qo'shni qiz, ammo o'zgacha",
    },
    scenarios: [
      { id: "jane_apartment", label: { en: "🏠 Cozy Apartment",  ru: "🏠 Уютная квартира", uz: "🏠 Qulay kvartira" }, gems_cost: 0  },
      { id: "jane_roadtrip",  label: { en: "🚗 Open Road Trip",  ru: "🚗 Путешествие",     uz: "🚗 Yo'l sayohati"  }, gems_cost: 25 },
    ],
  },
  {
    id: "bianca",
    name: "Bianca",
    avatar: "💋",
    type: "realistic",
    photo_url: null,
    tagline: {
      en: "Fiery Latina with big energy",
      ru: "Огненная латиноамериканка",
      uz: "Qaynoq lotin amerikalik",
    },
    scenarios: [
      { id: "bianca_kitchen", label: { en: "🍳 Sunday Kitchen",     ru: "🍳 Воскресная кухня",   uz: "🍳 Yakshanba oshxonasi" }, gems_cost: 0  },
      { id: "bianca_beach",   label: { en: "🏝️ Rio Beach Bonfire", ru: "🏝️ Костёр на пляже",    uz: "🏝️ Rio plyaji gulxani" }, gems_cost: 30 },
    ],
  },
  {
    id: "asha",
    name: "Asha",
    avatar: "🪷",
    type: "realistic",
    photo_url: null,
    tagline: {
      en: "Calm, grounding, deeply curious",
      ru: "Спокойная и любознательная",
      uz: "Tinch va qiziquvchan",
    },
    scenarios: [
      { id: "asha_garden",  label: { en: "🌿 Botanical Garden", ru: "🌿 Ботанический сад", uz: "🌿 Botanika bog'i" }, gems_cost: 0  },
      { id: "asha_retreat", label: { en: "🧘 Mountain Retreat", ru: "🧘 Горное ретрит",    uz: "🧘 Tog' retriti"   }, gems_cost: 20 },
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
  {
    id: "nika",
    name: "Nika",
    avatar: "🎮",
    type: "anime",
    photo_url: null,
    tagline: {
      en: "Playful gamer girl next door",
      ru: "Игривая соседка-геймерша",
      uz: "Qiziqchi qo'shni geymer qiz",
    },
    scenarios: [
      { id: "game_den",    label: { en: "🎮 Game Den",          ru: "🎮 Игровая комната", uz: "🎮 O'yin xonasi"      }, gems_cost: 0  },
      { id: "neon_arcade", label: { en: "🕹️ Neon Arcade Night", ru: "🕹️ Неоновая аркада", uz: "🕹️ Neon arkada tuni" }, gems_cost: 25 },
    ],
  },
  {
    id: "aurora",
    name: "Aurora",
    avatar: "🌌",
    type: "anime",
    photo_url: null,
    tagline: {
      en: "Dreamy stargazer, soft-spoken",
      ru: "Мечтательная наблюдательница звёзд",
      uz: "Xayolparast, yulduzlarni kuzatuvchi qiz",
    },
    scenarios: [
      { id: "aurora_observatory", label: { en: "🔭 Hilltop Observatory", ru: "🔭 Обсерватория на холме", uz: "🔭 Tepalik observatoriyasi" }, gems_cost: 0  },
      { id: "aurora_festival",    label: { en: "🎆 Lantern Festival",    ru: "🎆 Фестиваль фонариков",   uz: "🎆 Fonarlar festivali"      }, gems_cost: 20 },
    ],
  },
  {
    id: "coco",
    name: "Coco",
    avatar: "🍫",
    type: "anime",
    photo_url: null,
    tagline: {
      en: "Sweet tease with a sharp tongue",
      ru: "Милая, но острая на язык",
      uz: "Shirin, ammo so'zga chechan",
    },
    scenarios: [
      { id: "coco_cafe", label: { en: "🍰 Pastel Café",         ru: "🍰 Пастельное кафе",      uz: "🍰 Pastel kafesi"     }, gems_cost: 0  },
      { id: "coco_pool", label: { en: "🏊 Rooftop Pool Party",  ru: "🏊 Вечеринка у бассейна", uz: "🏊 Tom usti basseyni" }, gems_cost: 25 },
    ],
  },
  {
    id: "mistress_hellein",
    name: "Mistress Hellein",
    avatar: "🖤",
    type: "anime",
    photo_url: null,
    tagline: {
      en: "Dominant, sharp-tongued, commanding",
      ru: "Властная, острая на язык",
      uz: "Hukmron, so'zga chechan",
    },
    scenarios: [
      { id: "hellein_throne",  label: { en: "🖤 Obsidian Hall",     ru: "🖤 Обсидиановый зал", uz: "🖤 Obsidian zali"     }, gems_cost: 0  },
      { id: "hellein_dungeon", label: { en: "⛓️ Private Chambers", ru: "⛓️ Личные покои",     uz: "⛓️ Shaxsiy xonalar"   }, gems_cost: 40 },
    ],
  },
];
