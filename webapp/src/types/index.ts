export interface User {
  id: number
  telegram_id: number
  username?: string
  first_name?: string
  name?: string
  age?: number
  gender?: string
  height?: number
  weight?: number
  goal?: string
  units: string
  daily_calories?: number
  language: string
  is_onboarded: boolean
  created_at: string
  updated_at: string
}

export interface FoodEntry {
  id: number
  user_id: number
  dish_name: string
  calories: number
  protein: number
  fat: number
  carbs: number
  description?: string
  photo_file_id?: string
  eaten_at: string
}

export interface MacroTotals {
  calories: number
  protein: number
  fat: number
  carbs: number
}

export interface DiaryDay {
  date: string
  entries: FoodEntry[]
  totals: MacroTotals
}

export interface DiaryToday {
  date: string
  entries: FoodEntry[]
  totals: MacroTotals
  remaining_calories: number
}

export interface DiaryWeek {
  days: DiaryDay[]
}

export interface DiaryHistory {
  entries: FoodEntry[]
  total: number
  page: number
  pages: number
}

export interface CalorieDay {
  date: string
  calories: number
}

export interface MacroAvg {
  protein: number
  fat: number
  carbs: number
}

export interface StatsOverview {
  total_entries: number
  total_calories_consumed: number
  avg_calories_per_day: number
  streak_days: number
  best_day?: string
  today_calories: number
  today_goal: number
  today_percent: number
  weekly_calories: CalorieDay[]
  monthly_calories: CalorieDay[]
  macro_totals_week: MacroAvg
  macro_avg_week: MacroAvg
}

export interface FoodAnalysisResult {
  dish_name: string
  grams: number
  calories: number
  protein: number
  fat: number
  carbs: number
  description: string
  is_food: boolean
}
