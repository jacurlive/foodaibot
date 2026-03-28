import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User, DiaryToday } from '../types'

interface AppState {
  user: User | null
  theme: 'dark' | 'light'
  diaryToday: DiaryToday | null

  setUser: (user: User | null) => void
  setTheme: (theme: 'dark' | 'light') => void
  toggleTheme: () => void
  setDiaryToday: (diary: DiaryToday | null) => void
}

export const useStore = create<AppState>()(
  persist(
    (set, get) => ({
      user: null,
      theme: 'dark',
      diaryToday: null,

      setUser: (user) => set({ user }),
      setTheme: (theme) => {
        set({ theme })
        if (theme === 'light') {
          document.documentElement.classList.add('light')
          document.documentElement.classList.remove('dark')
        } else {
          document.documentElement.classList.remove('light')
          document.documentElement.classList.add('dark')
        }
      },
      toggleTheme: () => {
        const current = get().theme
        get().setTheme(current === 'dark' ? 'light' : 'dark')
      },
      setDiaryToday: (diary) => set({ diaryToday: diary }),
    }),
    {
      name: 'foodai-store',
      partialize: (state) => ({ theme: state.theme }),
    }
  )
)
