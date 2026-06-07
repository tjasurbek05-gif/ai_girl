import { useState, useEffect } from "react"
import { api } from "../api"
import { CHARACTERS } from "../characters"
import styles from "./Chats.module.css"

const tg = window.Telegram?.WebApp

export default function Chats({ lang }) {
  const [chats, setChats]     = useState([])
  const [loading, setLoading] = useState(true)

  const L = (obj) => obj?.[lang] ?? obj?.en ?? ""

  useEffect(() => {
    api.getChats()
      .then(setChats)
      .catch(() => setChats([]))
      .finally(() => setLoading(false))
  }, [])

  const openChat = (chat) => {
    // Send data to bot → bot switches to that character+scenario and continues
    tg?.sendData(JSON.stringify({
      char_id:  chat.character_id,
      scene_id: chat.scenario_id,
      resume:   true,
    }))
  }

  const getChar = (id) => CHARACTERS.find(c => c.id === id)

  const getSceneLabel = (char, scene_id) => {
    if (!char) return scene_id
    const scene = char.scenarios.find(s => s.id === scene_id)
    return scene ? L(scene.label) : scene_id
  }

  const timeAgo = (dateStr) => {
    if (!dateStr) return ""
    const diff = Date.now() - new Date(dateStr).getTime()
    const mins = Math.floor(diff / 60000)
    if (mins < 1)  return lang==="ru" ? "только что" : lang==="uz" ? "hozirgina" : "just now"
    if (mins < 60) return lang==="ru" ? `${mins} мин` : `${mins}m`
    const hrs = Math.floor(mins / 60)
    if (hrs < 24)  return lang==="ru" ? `${hrs} ч` : `${hrs}h`
    return lang==="ru" ? `${Math.floor(hrs/24)} д` : `${Math.floor(hrs/24)}d`
  }

  return (
    <div className={styles.wrap}>
      <div className={styles.header}>
        <span className={styles.title}>
          {lang==="ru" ? "Чаты" : lang==="uz" ? "Suhbatlar" : "Chats"}
        </span>
      </div>

      {loading && (
        <div className={styles.center}>
          <div className={styles.spinner} />
        </div>
      )}

      {!loading && chats.length === 0 && (
        <div className={styles.empty}>
          <div className={styles.emptyIcon}>💬</div>
          <div className={styles.emptyText}>
            {lang==="ru" ? "Нет чатов. Начни разговор!" : lang==="uz" ? "Suhbatlar yo'q. Boshlang!" : "No chats yet. Start a conversation!"}
          </div>
        </div>
      )}

      <div className={styles.list}>
        {chats.map((chat, i) => {
          const char = getChar(chat.character_id)
          return (
            <button
              key={`${chat.character_id}-${chat.scenario_id}`}
              className={styles.chatRow}
              style={{ animationDelay: `${i * 50}ms` }}
              onClick={() => openChat(chat)}
            >
              {/* Avatar */}
              <div className={styles.avatar}>
                {char?.photo_url
                  ? <img src={char.photo_url} alt={char.name} />
                  : <span>{char?.avatar ?? "💬"}</span>
                }
              </div>

              {/* Info */}
              <div className={styles.info}>
                <div className={styles.chatTop}>
                  <span className={styles.charName}>{char?.name ?? chat.character_id}</span>
                  <span className={styles.time}>{timeAgo(chat.updated_at)}</span>
                </div>
                <div className={styles.sceneBadge}>
                  {getSceneLabel(char, chat.scenario_id)}
                </div>
                <div className={styles.lastMsg}>
                  {chat.last_message || "…"}
                </div>
              </div>
            </button>
          )
        })}
      </div>
    </div>
  )
}
