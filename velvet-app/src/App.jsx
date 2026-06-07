import { useState, useEffect } from "react"
import { api } from "./api"
import Characters from "./pages/Characters"
import Shop from "./pages/Shop"
import Chats from "./pages/Chats"
import Settings from "./pages/Settings"
import styles from "./App.module.css"

const tg = window.Telegram?.WebApp

export default function App() {
  const [tab, setTab]       = useState("characters")
  const [lang, setLang]     = useState("en")
  const [user, setUser]     = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!tg) return
    tg.ready()
    tg.expand()
    tg.setHeaderColor("#0a0a0f")
    tg.setBackgroundColor("#0a0a0f")
    const tlang = tg.initDataUnsafe?.user?.language_code?.slice(0,2)
    if (["en","ru","uz"].includes(tlang)) setLang(tlang)
  }, [])

  useEffect(() => {
    api.getUser()
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false))
  }, [])

  const refreshUser = () => api.getUser().then(setUser).catch(() => {})

  if (loading) return (
    <div className={styles.loading}>
      <div className={styles.loadingDot} />
    </div>
  )

  const TABS = [
    { id: "characters", icon: "♥", label: { en: "Characters", ru: "Персонажи", uz: "Qahramonlar" } },
    { id: "shop",       icon: "🍸", label: { en: "Shop",       ru: "Магазин",   uz: "Do'kon"      } },
    { id: "chats",      icon: "💬", label: { en: "Chats",      ru: "Чаты",      uz: "Suhbatlar"   } },
    { id: "settings",   icon: "⚙️", label: { en: "Settings",   ru: "Настройки", uz: "Sozlamalar"  } },
  ]

  return (
    <div className={styles.root}>
      <div className={styles.page}>
        {tab === "characters" && <Characters lang={lang} user={user} />}
        {tab === "shop"       && <Shop       lang={lang} user={user} onPurchase={refreshUser} />}
        {tab === "chats"      && <Chats      lang={lang} />}
        {tab === "settings"   && <Settings   lang={lang} user={user} onLangChange={setLang} onRefresh={refreshUser} />}
      </div>

      {/* Bottom nav — exactly like Lucid Dreams */}
      <nav className={styles.bottomNav}>
        {TABS.map(t => (
          <button
            key={t.id}
            className={`${styles.navBtn} ${tab === t.id ? styles.navActive : ""}`}
            onClick={() => setTab(t.id)}
          >
            <span className={styles.navIcon}>{t.icon}</span>
            <span className={styles.navLabel}>{t.label[lang] || t.label.en}</span>
          </button>
        ))}
      </nav>
    </div>
  )
}
