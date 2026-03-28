import axios from 'axios'
import type {
  User,
  DiaryToday,
  DiaryWeek,
  DiaryHistory,
  StatsOverview,
  FoodAnalysisResult,
  FoodEntry,
} from '../types'

const BASE = '/api'

// Get user_id from URL params or localStorage for local dev
function getUserId(): string | null {
  const params = new URLSearchParams(window.location.search)
  const fromUrl = params.get('user_id')
  if (fromUrl) {
    localStorage.setItem('tg_user_id', fromUrl)
    return fromUrl
  }
  // Try Telegram WebApp
  const tg = (window as any).Telegram?.WebApp
  if (tg?.initDataUnsafe?.user?.id) {
    return String(tg.initDataUnsafe.user.id)
  }
  return localStorage.getItem('tg_user_id')
}

const api = axios.create({
  baseURL: BASE,
})

api.interceptors.request.use((config) => {
  const userId = getUserId()
  if (userId) {
    config.headers['X-Telegram-User-Id'] = userId
  }
  return config
})

// User
export const getMe = () => api.get<User>('/user/me').then(r => r.data)
export const updateMe = (data: Partial<User>) =>
  api.put<User>('/user/me', data).then(r => r.data)

// Diary
export const getDiaryToday = () => api.get<DiaryToday>('/diary/today').then(r => r.data)
export const getDiaryWeek = () => api.get<DiaryWeek>('/diary/week').then(r => r.data)
export const getDiaryHistory = (page = 1, limit = 20) =>
  api.get<DiaryHistory>('/diary/history', { params: { page, limit } }).then(r => r.data)
export const deleteEntry = (id: number) =>
  api.delete<{ ok: boolean }>(`/diary/entry/${id}`).then(r => r.data)

// Stats
export const getStatsOverview = () => api.get<StatsOverview>('/stats/overview').then(r => r.data)

// Food
export const analyzeFood = (file: File, lang: string) => {
  const form = new FormData()
  form.append('file', file)
  form.append('lang', lang)
  return api.post<FoodAnalysisResult>('/food/analyze', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }).then(r => r.data)
}

export const saveFood = (data: {
  dish_name: string
  grams?: number
  calories: number
  protein: number
  fat: number
  carbs: number
  description?: string
  photo_file_id?: string
}) => api.post<FoodEntry>('/food/save', data).then(r => r.data)

export const completeOnboarding = (data: {
  name: string
  age: number
  gender: string
  height: number
  weight: number
  goal: string
  units: string
  language?: string
}) => api.post<User>('/user/complete-onboarding', data).then(r => r.data)

export default api
