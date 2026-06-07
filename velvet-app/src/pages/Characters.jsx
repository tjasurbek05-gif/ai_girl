import { useState } from "react"
import { CHARACTERS } from "../characters"
import styles from "./Characters.module.css"

const tg = window.Telegram?.WebApp

export default function Characters({ lang, user }) {
  const [filter, setFilter]   = useState("anime")
  const [selected, setSelected] = useState(null)
  const [view, setView]       = useState("grid")

  const L = (obj) => obj?.[lang] ?? obj?.en ?? ""

  const filtered = filter === "custom" ? [] : CHARACTERS.filter(c => c.type === filter)

  const openChar = (char) => {
    setSelected(char)
    setView("scenarios")
    tg?.BackButton?.show()
    tg?.BackButton?.onClick(() => {
      setView("grid")
      tg?.BackButton?.hide()
    })
  }

  const chooseScenario = (char, scene) => {
    tg?.sendData(JSON.stringify({ char_id: char.id, scene_id: scene.id }))
  }

  if (view === "scenarios" && selected) return (
    <div className={styles.wrap}>
      <div className={styles.scenHeader}>
        <div className={styles.scenThumb}>
          {selected.photo_url
            ? <img src={selected.photo_url} alt={selected.name} />
            : <span>{selected.avatar}</span>}
        </div>
        <div>
          <div className={styles.scenName}>{selected.name}</div>
          <div className={styles.scenSub}>{L(selected.tagline)}</div>
        </div>
      </div>
      <div className={styles.sectionLabel}>
        {lang==="ru" ? "Выбери место встречи" : lang==="uz" ? "Joyni tanlang" : "Choose where to meet"}
      </div>
      {selected.scenarios.map((scene, i) => (
        <button key={scene.id} className={styles.sceneRow}
          style={{ animationDelay: `${i*60}ms` }}
          onClick={() => chooseScenario(selected, scene)}>
          <span className={styles.sceneTitle}>{L(scene.label)}</span>
          {scene.gems_cost > 0
            ? <span className={styles.cost}>💎 {scene.gems_cost}</span>
            : <span className={styles.free}>FREE</span>}
        </button>
      ))}
    </div>
  )

  return (
    <div className={styles.wrap}>
      <div className={styles.header}>
        <span className={styles.title}>
          {lang==="ru" ? "Персонажи" : lang==="uz" ? "Qahramonlar" : "Characters"}
        </span>
        {user && (
          <div className={styles.badge}>
            <span>⚡ {user.energy}</span>
            <span>💎 {user.gems}</span>
          </div>
        )}
      </div>

      <div className={styles.tabs}>
        {[
          {k:"anime",     l:"Anime"},
          {k:"realistic", l: lang==="ru"?"Реальные": lang==="uz"?"Real":"Realistic"},
          {k:"custom",    l: lang==="ru"?"Свой":     lang==="uz"?"O'zing":"Custom"},
        ].map(t => (
          <button key={t.k}
            className={`${styles.tab} ${filter===t.k ? styles.tabOn : ""}`}
            onClick={() => setFilter(t.k)}>{t.l}</button>
        ))}
      </div>

      <div className={styles.grid}>
        {filter === "custom" && (
          <div className={styles.customCard}>
            <div className={styles.customInner}>
              <div className={styles.gemBadge}>99 💎</div>
              {[...Array(25)].map((_,i) => (
                <div key={i} className={styles.star} style={{
                  left:`${Math.random()*100}%`, top:`${Math.random()*100}%`,
                  animationDelay:`${Math.random()*2}s`,
                  width:`${Math.random()*2+1}px`, height:`${Math.random()*2+1}px`
                }}/>
              ))}
            </div>
            <div className={styles.meta}>
              <div className={styles.name}>{lang==="ru"?"Твой персонаж": lang==="uz"?"O'z qahramoningiz":"Your character"}</div>
              <div className={styles.tagline}>{lang==="ru"?"Станет кем угодно": lang==="uz"?"Xohlagan qahramoningiz":"Will become any character you want."}</div>
            </div>
          </div>
        )}
        {filtered.map((char, i) => (
          <button key={char.id} className={styles.card}
            style={{ animationDelay:`${i*50}ms` }}
            onClick={() => openChar(char)}>
            <div className={styles.photo}>
              {char.photo_url
                ? <img src={char.photo_url} alt={char.name} draggable={false} />
                : <div className={styles.emoji}>{char.avatar}</div>}
            </div>
            <div className={styles.meta}>
              <div className={styles.name}>{char.name}</div>
              <div className={styles.tagline}>{L(char.tagline)}</div>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}
