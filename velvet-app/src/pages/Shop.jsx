import { useState, useEffect } from "react"
import { api } from "../api"
import styles from "./Shop.module.css"

export default function Shop({ lang, user, onPurchase }) {
  const [items, setItems]   = useState([])
  const [owned, setOwned]   = useState([])
  const [buying, setBuying] = useState(null)
  const [toast, setToast]   = useState(null)

  const L = (obj) => obj?.[lang] ?? obj?.en ?? ""

  useEffect(() => {
    api.getShopItems().then(setItems).catch(()=>{})
    api.getOwned().then(setOwned).catch(()=>{})
  }, [])

  const buy = async (item) => {
    if (owned.includes(item.id)) return
    if (!user || user.gems < item.price) {
      showToast(lang==="ru" ? "💎 Недостаточно кристаллов!" : lang==="uz" ? "💎 Javohirlar yetarli emas!" : "💎 Not enough gems!")
      return
    }
    setBuying(item.id)
    try {
      await api.buyItem(item.id)
      setOwned(o => [...o, item.id])
      onPurchase()
      showToast(lang==="ru" ? "✅ Куплено!" : lang==="uz" ? "✅ Sotib olindi!" : "✅ Purchased!")
    } catch {
      showToast("❌ Error")
    } finally {
      setBuying(null)
    }
  }

  const showToast = (msg) => {
    setToast(msg)
    setTimeout(() => setToast(null), 2000)
  }

  return (
    <div className={styles.wrap}>
      <div className={styles.header}>
        <span className={styles.title}>
          {lang==="ru" ? "Магазин" : lang==="uz" ? "Do'kon" : "Shop"}
        </span>
        {user && <div className={styles.gems}>💎 {user.gems}</div>}
      </div>

      <div className={styles.subtitle}>
        {lang==="ru" ? "Предметы влияют на поведение персонажа в чате"
         : lang==="uz" ? "Buyumlar chatdagi qahramonning xatti-harakatiga ta'sir qiladi"
         : "Items influence character behaviour in chat"}
      </div>

      <div className={styles.grid}>
        {items.map((item, i) => {
          const isOwned = owned.includes(item.id)
          const isBuying = buying === item.id
          return (
            <button key={item.id} className={`${styles.item} ${isOwned ? styles.owned : ""}`}
              style={{ animationDelay:`${i*40}ms` }}
              onClick={() => buy(item)}>
              <div className={styles.itemIcon}>{item.emoji}</div>
              <div className={styles.itemName}>{L(item.name)}</div>
              {isOwned
                ? <div className={styles.ownedBadge}>✓ {lang==="ru"?"Есть":lang==="uz"?"Bor":"Owned"}</div>
                : <div className={styles.price}>{isBuying ? "…" : `${item.price} 💎`}</div>
              }
            </button>
          )
        })}
      </div>

      {toast && <div className={styles.toast}>{toast}</div>}
    </div>
  )
}
