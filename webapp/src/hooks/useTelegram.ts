import { useEffect } from 'react'

interface TelegramWebApp {
  ready: () => void
  expand: () => void
  close: () => void
  initDataUnsafe: {
    user?: {
      id: number
      first_name?: string
      last_name?: string
      username?: string
      language_code?: string
    }
  }
  colorScheme: 'dark' | 'light'
  themeParams: Record<string, string>
  MainButton: {
    text: string
    color: string
    textColor: string
    isVisible: boolean
    show: () => void
    hide: () => void
    onClick: (fn: () => void) => void
    offClick: (fn: () => void) => void
  }
  HapticFeedback: {
    impactOccurred: (style: 'light' | 'medium' | 'heavy') => void
    notificationOccurred: (type: 'error' | 'success' | 'warning') => void
  }
}

declare global {
  interface Window {
    Telegram?: {
      WebApp: TelegramWebApp
    }
  }
}

export function useTelegram() {
  const tg = window.Telegram?.WebApp

  useEffect(() => {
    if (tg) {
      tg.ready()
      tg.expand()
    }
  }, [tg])

  const getUserId = (): number | null => {
    // From Telegram WebApp
    if (tg?.initDataUnsafe?.user?.id) {
      return tg.initDataUnsafe.user.id
    }
    // From URL params (local dev)
    const params = new URLSearchParams(window.location.search)
    const fromUrl = params.get('user_id')
    if (fromUrl) return parseInt(fromUrl)
    // From localStorage
    const stored = localStorage.getItem('tg_user_id')
    if (stored) return parseInt(stored)
    return null
  }

  const haptic = (type: 'light' | 'medium' | 'heavy' = 'light') => {
    tg?.HapticFeedback?.impactOccurred(type)
  }

  const hapticNotification = (type: 'success' | 'error' | 'warning') => {
    tg?.HapticFeedback?.notificationOccurred(type)
  }

  return {
    tg,
    getUserId,
    haptic,
    hapticNotification,
    isInTelegram: !!tg,
  }
}
