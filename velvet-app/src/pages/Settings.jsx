import { useState } from "react"
import { api } from "../api"
import styles from "./Settings.module.css"

export default function Settings({ lang, user, onLangChange, onRefresh }) {
  const [saving, setSaving] = useState(false)
  const [toast, setToast]   = useState(null)

  const showToast = (msg) => {
    setToast(msg)
    setTimeout(() => setToast(null), 2000)
  }

  const setLang = async (newLang) => {
    setSaving(true)
    try {
      await api.setLang(newLang)
      onLangChange(newLang)
      onRefresh()
      showToast("✅ " + { en: "Language updated", ru: "Язык обновлён", uz: "Til yangilandi" }[newLang])
    } catch {
      showToast("❌ Error")
    } finally {
      setSaving(false)
    }
  }

  const PLANS = [
    { key: "2days",   label: { en: "2 Days",   ru: "2 Дня",    uz: "2 Kun"    }, gems: 20,  stars: 89,   days: 2   },
    { key: "1month",  label: { en: "1 Month",  ru: "1 Месяц",  uz: "1 Oy"     }, gems: 30,  stars: 199,  days: 30  },
    { key: "3months", label: { en: "3 Months", ru: "3 Месяца", uz: "3 Oy"     }, gems: 70,  stars: 449,  days: 90, popular: true },
    { key: "1year",   label: { en: "1 Year",   ru: "1 Год",    uz: "1 Yil"    }, gems: 210, stars: 1499, days: 365 },
  ]

  const LANGS = [
    { code: "en", flag: "🇬🇧", label: "English"  },
    { code: "ru", flag: "🇷🇺", label: "Русский"  },
    { code: "uz", flag: "🇺🇿", label: "O'zbek"   },
  ]

  const formatExpiry = (dateStr) => {
    if (!dateStr) return null
    try {
      return new Date(dateStr).toLocaleDateString(
        lang === "ru" ? "ru-RU" : lang === "uz" ? "uz-UZ" : "en-US",
        { day: "numeric", month: "long", year: "numeric" }
      )
    } catch { return dateStr }
  }

  return (
    <div className={styles.wrap}>
      <div className={styles.header}>
        <span className={styles.title}>
          {lang==="ru" ? "Настройки" : lang==="uz" ? "Sozlamalar" : "Settings"}
        </span>
      </div>

      {/* Plan info */}
      <div className={styles.section}>
        <div className={styles.sectionLabel}>
          {lang==="ru" ? "Ваш план" : lang==="uz" ? "Sizning rejangiz" : "Your plan"}
        </div>
        <div className={styles.planCard}>
          <div className={styles.planName}>
            {user?.premium
              ? (lang==="ru" ? "✨ Премиум" : lang==="uz" ? "✨ Premium" : "✨ Premium")
              : (lang==="ru" ? "Бесплатный" : lang==="uz" ? "Bepul" : "Free")}
          </div>
          {user?.premium && user?.sub_expires && (
            <div className={styles.planExpiry}>
              {lang==="ru" ? "До" : lang==="uz" ? "Gacha" : "Until"} {formatExpiry(user.sub_expires)}
            </div>
          )}
          {user && (
            <div className={styles.planStats}>
              <div className={styles.stat}>
                <span className={styles.statVal}>⚡ {user.energy}</span>
                <span className={styles.statLabel}>{lang==="ru"?"энергия":lang==="uz"?"energiya":"energy"}</span>
              </div>
              <div className={styles.statDivider} />
              <div className={styles.stat}>
                <span className={styles.statVal}>💎 {user.gems}</span>
                <span className={styles.statLabel}>{lang==="ru"?"кристаллы":lang==="uz"?"javohirlar":"gems"}</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Subscription plans */}
      {!user?.premium && (
        <div className={styles.section}>
          <div className={styles.sectionLabel}>
            {lang==="ru" ? "Оформить премиум" : lang==="uz" ? "Premium olish" : "Upgrade to Premium"}
          </div>
          <div className={styles.plans}>
            {PLANS.map(plan => (
              <div key={plan.key} className={`${styles.planRow} ${plan.popular ? styles.planPopular : ""}`}>
                {plan.popular && (
                  <div className={styles.popularBadge}>
                    {lang==="ru" ? "Популярно" : lang==="uz" ? "Mashhur" : "Most Popular"}
                  </div>
                )}
                <div className={styles.planLeft}>
                  <span className={styles.planRowLabel}>{plan.label[lang] || plan.label.en}</span>
                  <span className={styles.planGems}>+{plan.gems} 💎</span>
                </div>
                <div className={styles.planPrice}>⭐ {plan.stars}</div>
              </div>
            ))}
          </div>
          <div className={styles.payNote}>
            {lang==="ru" ? "Оплата через Telegram Stars" : lang==="uz" ? "Telegram Stars orqali to'lov" : "Pay with Telegram Stars"}
          </div>
        </div>
      )}

      {/* Language */}
      <div className={styles.section}>
        <div className={styles.sectionLabel}>
          {lang==="ru" ? "Язык" : lang==="uz" ? "Til" : "Language"}
        </div>
        <div className={styles.langList}>
          {LANGS.map(l => (
            <button
              key={l.code}
              className={`${styles.langRow} ${lang === l.code ? styles.langActive : ""}`}
              onClick={() => setLang(l.code)}
              disabled={saving}
            >
              <span className={styles.langFlag}>{l.flag}</span>
              <span className={styles.langLabel}>{l.label}</span>
              {lang === l.code && <span className={styles.langCheck}>✓</span>}
            </button>
          ))}
        </div>
      </div>

      {toast && <div className={styles.toast}>{toast}</div>}
    </div>
  )
}
