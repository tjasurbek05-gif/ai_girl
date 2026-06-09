import { useState, useEffect } from "react"
import { CHARACTERS } from "./characters"
import styles from "./App.module.css"

const tg = window.Telegram?.WebApp

export default function App() {
  const [lang, setLang]         = useState("en")
  const [filter, setFilter]     = useState("anime")
  const [selected, setSelected] = useState(null)
  const [view, setView]         = useState("grid")
  const [sending, setSending]   = useState(false)

  useEffect(() => {
    if (!tg) return
    tg.ready()
    tg.expand()
    tg.setHeaderColor("#0a0a0f")
    tg.setBackgroundColor("#0a0a0f")
    const tlang = tg.initDataUnsafe?.user?.language_code?.slice(0, 2)
    if (["en", "ru", "uz"].includes(tlang)) setLang(tlang)
  }, [])

  useEffect(() => {
    if (!tg) return
    if (view === "scenarios") {
      tg.BackButton.show()
      tg.BackButton.onClick(() => {
        setView("grid")
        tg.BackButton.hide()
      })
    } else {
      tg.BackButton.hide()
    }
  }, [view])

  const filtered = CHARACTERS.filter(c =>
    filter === "custom" ? false : c.type === filter
  )

  const L = (obj) => obj?.[lang] ?? obj?.en ?? ""

  const chooseScenario = async (char, scene) => {
    if (sending) return
    setSending(true)

    try {
      // sendData works when opened via KeyboardButton WebApp
      // initData is present when opened properly via Telegram
      if (tg?.initData) {
        tg.sendData(JSON.stringify({
          char_id: char.id,
          scene_id: scene.id,
        }))
        // sendData closes the app automatically
      } else {
        // Fallback for testing in browser
        alert(`Selected: ${char.id} / ${scene.id}`)
        setSending(false)
      }
    } catch (e) {
      console.error(e)
      setSending(false)
    }
  }

  const openChar = (char) => {
    setSelected(char)
    setView("scenarios")
  }

  // ── Scenarios view ───────────────────────────────────────────────────────
  if (view === "scenarios" && selected) {
    return (
      <div className={styles.root}>
        <div className={styles.topBar}>
          <span className={styles.logo}>velvet</span>
        </div>
        <div className={styles.scenariosView}>
          <div className={styles.scenHeader}>
            <div className={styles.scenPhotoWrap}>
              {selected.photo_url
                ? <img src={selected.photo_url} alt={selected.name} className={styles.scenPhoto} />
                : <div className={styles.scenEmojiPlaceholder}>{selected.avatar}</div>
              }
            </div>
            <div className={styles.scenInfo}>
              <div className={styles.scenName}>{selected.name}</div>
              <div className={styles.scenTagline}>{L(selected.tagline)}</div>
            </div>
          </div>

          <div className={styles.scenSectionLabel}>
            {lang === "ru" ? "Выбери место встречи"
             : lang === "uz" ? "Uchrashuv joyini tanlang"
             : "Choose where to meet"}
          </div>

          <div className={styles.scenList}>
            {selected.scenarios.map((scene, i) => (
              <button
                key={scene.id}
                className={`${styles.sceneCard} ${sending ? styles.disabled : ""}`}
                style={{ animationDelay: `${i * 60}ms` }}
                onClick={() => chooseScenario(selected, scene)}
                disabled={sending}
              >
                <span className={styles.sceneLabel}>{L(scene.label)}</span>
                {scene.gems_cost > 0
                  ? <span className={styles.sceneCost}>💎 {scene.gems_cost}</span>
                  : <span className={styles.sceneFree}>FREE</span>
                }
              </button>
            ))}
          </div>
        </div>
      </div>
    )
  }

  // ── Grid view ────────────────────────────────────────────────────────────
  return (
    <div className={styles.root}>
      <div className={styles.topBar}>
        <span className={styles.logo}>velvet</span>
        <span className={styles.sectionTitle}>
          {lang === "ru" ? "Персонажи" : lang === "uz" ? "Qahramonlar" : "Characters"}
        </span>
      </div>

      <div className={styles.tabRow}>
        {[
          { key: "anime",     label: "Anime" },
          { key: "realistic", label: lang === "ru" ? "Реальные" : lang === "uz" ? "Real" : "Realistic" },
          { key: "custom",    label: lang === "ru" ? "Свой" : lang === "uz" ? "O'z" : "Custom" },
        ].map(tab => (
          <button
            key={tab.key}
            className={`${styles.tab} ${filter === tab.key ? styles.tabActive : ""}`}
            onClick={() => setFilter(tab.key)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className={styles.grid}>
        {filter === "custom" && (
          <div className={styles.customCard}>
            <div className={styles.customInner}>
              <div className={styles.customGems}>99 💎</div>
              {[...Array(30)].map((_, i) => (
                <div key={i} className={styles.star} style={{
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 100}%`,
                  animationDelay: `${Math.random() * 2}s`,
                  width: `${Math.random() * 2 + 1}px`,
                  height: `${Math.random() * 2 + 1}px`,
                }} />
              ))}
            </div>
            <div className={styles.cardMeta}>
              <div className={styles.charName}>
                {lang === "ru" ? "Твой персонаж" : lang === "uz" ? "O'z qahramoningiz" : "Your character"}
              </div>
              <div className={styles.charTagline}>
                {lang === "ru" ? "Станет кем угодно" : lang === "uz" ? "Xohlagan qahramoningiz" : "Will become anyone you want"}
              </div>
            </div>
          </div>
        )}

        {filter !== "custom" && filtered.map((char, i) => (
          <button
            key={char.id}
            className={styles.charCard}
            style={{ animationDelay: `${i * 50}ms` }}
            onClick={() => openChar(char)}
          >
            <div className={styles.cardPhoto}>
              {char.photo_url
                ? <img src={char.photo_url} alt={char.name} draggable={false} />
                : <div className={styles.emojiPlaceholder}>{char.avatar}</div>
              }
            </div>
            <div className={styles.cardMeta}>
              <div className={styles.charName}>{char.name}</div>
              <div className={styles.charTagline}>{L(char.tagline)}</div>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}
