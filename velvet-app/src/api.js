const BASE = ""

function getInitData() {
  return window.Telegram?.WebApp?.initData || ""
}

async function apiFetch(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "x-init-data": getInitData(),
      ...(options.headers || {}),
    },
  })
  if (!res.ok) throw new Error(`API error ${res.status}`)
  return res.json()
}

export const api = {
  getUser:          ()         => apiFetch("/api/user"),
  getChats:         ()         => apiFetch("/api/chats"),
  getShopItems:     ()         => apiFetch("/api/shop/items"),
  getOwned:         ()         => apiFetch("/api/shop/owned"),
  buyItem:          (item_id)  => apiFetch(`/api/shop/buy/${item_id}`, { method: "POST" }),
  setLang:          (lang)     => apiFetch(`/api/user/lang/${lang}`, { method: "POST" }),
  getGemsPacks:     ()         => apiFetch("/api/gems/packs"),
  getReferralStats: ()         => apiFetch("/api/referral/stats"),
}
