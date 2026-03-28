import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import { completeOnboarding } from '../api/client'
import { useStore } from '../store/useStore'
import type { User } from '../types'

interface OnboardingProps {
  user: User
  onComplete: (user: User) => void
}

type Step = 'language' | 'name' | 'age' | 'gender' | 'units' | 'height' | 'weight' | 'goal'
const STEPS: Step[] = ['language', 'name', 'age', 'gender', 'units', 'height', 'weight', 'goal']

const slideVariants = {
  enter: (dir: number) => ({ x: dir > 0 ? 60 : -60, opacity: 0 }),
  center: { x: 0, opacity: 1, transition: { duration: 0.28, ease: 'easeOut' } },
  exit: (dir: number) => ({ x: dir > 0 ? -60 : 60, opacity: 0, transition: { duration: 0.2 } }),
}

export function Onboarding({ user, onComplete }: OnboardingProps) {
  const { t, i18n } = useTranslation()
  const { setUser } = useStore()

  const [stepIdx, setStepIdx] = useState(0)
  const [dir, setDir] = useState(1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Form state
  const [lang, setLang] = useState(user.language || 'ru')
  const [name, setName] = useState(user.name || '')
  const [age, setAge] = useState(user.age ? String(user.age) : '')
  const [gender, setGender] = useState(user.gender || '')
  const [units, setUnits] = useState(user.units || 'metric')
  const [height, setHeight] = useState(user.height ? String(user.height) : '')
  const [weight, setWeight] = useState(user.weight ? String(user.weight) : '')
  const [goal, setGoal] = useState(user.goal || '')

  const step = STEPS[stepIdx]
  const total = STEPS.length

  const go = (delta: number) => {
    setDir(delta)
    setError(null)
    setStepIdx(i => i + delta)
  }

  const validate = (): boolean => {
    setError(null)
    if (step === 'name') {
      if (!name.trim() || name.trim().length > 64) {
        setError(t('onboarding.error_name')); return false
      }
    }
    if (step === 'age') {
      const n = parseInt(age)
      if (isNaN(n) || n < 10 || n > 100) {
        setError(t('onboarding.error_age')); return false
      }
    }
    if (step === 'height') {
      const n = parseFloat(height)
      if (units === 'metric') {
        if (isNaN(n) || n < 100 || n > 250) {
          setError(t('onboarding.error_height_metric')); return false
        }
      } else {
        if (isNaN(n) || n < 4 || n > 8) {
          setError(t('onboarding.error_height_imperial')); return false
        }
      }
    }
    if (step === 'weight') {
      const n = parseFloat(weight)
      if (units === 'metric') {
        if (isNaN(n) || n < 30 || n > 300) {
          setError(t('onboarding.error_weight_metric')); return false
        }
      } else {
        if (isNaN(n) || n < 66 || n > 660) {
          setError(t('onboarding.error_weight_imperial')); return false
        }
      }
    }
    return true
  }

  const handleNext = () => {
    if (!validate()) return
    if (step === 'language') {
      i18n.changeLanguage(lang)
      localStorage.setItem('foodai_lang', lang)
    }
    if (stepIdx < total - 1) {
      go(1)
    }
  }

  const handleFinish = async () => {
    if (!validate()) return
    setLoading(true)
    setError(null)
    try {
      // Convert height/weight if imperial
      let heightCm = parseFloat(height)
      let weightKg = parseFloat(weight)
      if (units === 'imperial') {
        const feet = Math.floor(heightCm)
        const inches = Math.round((heightCm - feet) * 10)
        heightCm = Math.round(feet * 30.48 + inches * 2.54)
        weightKg = Math.round(weightKg / 2.20462 * 10) / 10
      }

      const updated = await completeOnboarding({
        name: name.trim(),
        age: parseInt(age),
        gender,
        height: heightCm,
        weight: weightKg,
        goal,
        units,
        language: lang,
      })
      setUser(updated)
      onComplete(updated)
    } catch {
      setError('Ошибка сохранения. Попробуйте ещё раз.')
    } finally {
      setLoading(false)
    }
  }

  const renderStep = () => {
    switch (step) {
      case 'language':
        return (
          <div className="flex flex-col gap-3">
            {(['ru', 'en', 'uz'] as const).map(l => (
              <button
                key={l}
                onClick={() => setLang(l)}
                className="w-full py-4 rounded-2xl text-base font-medium transition-all"
                style={{
                  background: lang === l ? 'var(--accent)' : 'var(--bg-card)',
                  color: lang === l ? '#000' : 'var(--text-primary)',
                  border: `2px solid ${lang === l ? 'var(--accent)' : 'var(--border)'}`,
                }}
              >
                {t(`onboarding.lang_${l}`)}
              </button>
            ))}
          </div>
        )

      case 'name':
        return (
          <input
            autoFocus
            type="text"
            value={name}
            onChange={e => { setName(e.target.value); setError(null) }}
            onKeyDown={e => e.key === 'Enter' && handleNext()}
            placeholder={t('onboarding.name_placeholder')}
            className="w-full px-4 py-4 rounded-2xl text-base outline-none"
            style={{
              background: 'var(--bg-card)',
              border: `2px solid ${error ? 'var(--red)' : 'var(--border)'}`,
              color: 'var(--text-primary)',
            }}
          />
        )

      case 'age':
        return (
          <input
            autoFocus
            type="number"
            value={age}
            onChange={e => { setAge(e.target.value); setError(null) }}
            onKeyDown={e => e.key === 'Enter' && handleNext()}
            placeholder={t('onboarding.age_placeholder')}
            className="w-full px-4 py-4 rounded-2xl text-base text-center outline-none"
            style={{
              background: 'var(--bg-card)',
              border: `2px solid ${error ? 'var(--red)' : 'var(--border)'}`,
              color: 'var(--text-primary)',
            }}
          />
        )

      case 'gender':
        return (
          <div className="flex gap-3">
            {(['male', 'female'] as const).map(g => (
              <button
                key={g}
                onClick={() => setGender(g)}
                className="flex-1 py-5 rounded-2xl text-base font-medium transition-all"
                style={{
                  background: gender === g ? 'var(--accent)' : 'var(--bg-card)',
                  color: gender === g ? '#000' : 'var(--text-primary)',
                  border: `2px solid ${gender === g ? 'var(--accent)' : 'var(--border)'}`,
                }}
              >
                {g === 'male' ? '👨' : '👩'}<br />
                <span className="text-sm mt-1 block">{t(`onboarding.${g}`)}</span>
              </button>
            ))}
          </div>
        )

      case 'units':
        return (
          <div className="flex flex-col gap-3">
            {(['metric', 'imperial'] as const).map(u => (
              <button
                key={u}
                onClick={() => setUnits(u)}
                className="w-full py-4 rounded-2xl text-base font-medium transition-all"
                style={{
                  background: units === u ? 'var(--accent)' : 'var(--bg-card)',
                  color: units === u ? '#000' : 'var(--text-primary)',
                  border: `2px solid ${units === u ? 'var(--accent)' : 'var(--border)'}`,
                }}
              >
                {t(`onboarding.${u}`)}
              </button>
            ))}
          </div>
        )

      case 'height':
        return (
          <input
            autoFocus
            type="number"
            value={height}
            onChange={e => { setHeight(e.target.value); setError(null) }}
            onKeyDown={e => e.key === 'Enter' && handleNext()}
            placeholder={t(units === 'metric' ? 'onboarding.height_placeholder_metric' : 'onboarding.height_placeholder_imperial')}
            className="w-full px-4 py-4 rounded-2xl text-base text-center outline-none"
            style={{
              background: 'var(--bg-card)',
              border: `2px solid ${error ? 'var(--red)' : 'var(--border)'}`,
              color: 'var(--text-primary)',
            }}
          />
        )

      case 'weight':
        return (
          <input
            autoFocus
            type="number"
            value={weight}
            onChange={e => { setWeight(e.target.value); setError(null) }}
            onKeyDown={e => e.key === 'Enter' && (stepIdx === total - 1 ? handleFinish() : handleNext())}
            placeholder={t(units === 'metric' ? 'onboarding.weight_placeholder_metric' : 'onboarding.weight_placeholder_imperial')}
            className="w-full px-4 py-4 rounded-2xl text-base text-center outline-none"
            style={{
              background: 'var(--bg-card)',
              border: `2px solid ${error ? 'var(--red)' : 'var(--border)'}`,
              color: 'var(--text-primary)',
            }}
          />
        )

      case 'goal':
        return (
          <div className="flex flex-col gap-3">
            {(['lose', 'maintain', 'gain'] as const).map(g => (
              <button
                key={g}
                onClick={() => setGoal(g)}
                className="w-full py-4 rounded-2xl text-base font-medium transition-all"
                style={{
                  background: goal === g ? 'var(--accent)' : 'var(--bg-card)',
                  color: goal === g ? '#000' : 'var(--text-primary)',
                  border: `2px solid ${goal === g ? 'var(--accent)' : 'var(--border)'}`,
                }}
              >
                {t(`onboarding.goal_${g}`)}
              </button>
            ))}
          </div>
        )
    }
  }

  const canProceed = () => {
    switch (step) {
      case 'gender': return !!gender
      case 'goal': return !!goal
      default: return true
    }
  }

  const stepTitle: Record<Step, string> = {
    language: t('onboarding.step_language'),
    name: t('onboarding.step_name'),
    age: t('onboarding.step_age'),
    gender: t('onboarding.step_gender'),
    units: t('onboarding.step_units'),
    height: t('onboarding.step_height'),
    weight: t('onboarding.step_weight'),
    goal: t('onboarding.step_goal'),
  }

  const isLast = stepIdx === total - 1

  return (
    <div className="h-full flex flex-col" style={{ background: 'var(--bg-base)' }}>
      {/* Header */}
      <div className="px-5 pt-6 pb-4">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-xl font-bold" style={{ color: 'var(--text-primary)' }}>
            {t('onboarding.title')}
          </h1>
          <span className="text-sm" style={{ color: 'var(--text-muted)' }}>
            {stepIdx + 1} / {total}
          </span>
        </div>
        {/* Progress bar */}
        <div className="w-full h-1.5 rounded-full" style={{ background: 'var(--bg-card)' }}>
          <motion.div
            className="h-full rounded-full"
            style={{ background: 'var(--accent)' }}
            animate={{ width: `${((stepIdx + 1) / total) * 100}%` }}
            transition={{ duration: 0.3 }}
          />
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 px-5 overflow-hidden flex flex-col justify-center">
        <AnimatePresence mode="wait" custom={dir}>
          <motion.div
            key={step}
            custom={dir}
            variants={slideVariants}
            initial="enter"
            animate="center"
            exit="exit"
            className="flex flex-col gap-6"
          >
            <div>
              <h2 className="text-2xl font-bold mb-1" style={{ color: 'var(--text-primary)' }}>
                {stepTitle[step]}
              </h2>
              <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                {t('onboarding.subtitle')}
              </p>
            </div>

            {renderStep()}

            {error && (
              <p className="text-sm text-center" style={{ color: 'var(--red)' }}>
                {error}
              </p>
            )}
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Footer buttons */}
      <div className="px-5 pb-8 pt-4 flex gap-3">
        {stepIdx > 0 && (
          <button
            onClick={() => go(-1)}
            className="flex-1 py-3.5 rounded-2xl font-semibold text-base"
            style={{
              background: 'var(--bg-card)',
              color: 'var(--text-secondary)',
              border: '1.5px solid var(--border)',
            }}
          >
            {t('onboarding.btn_back')}
          </button>
        )}
        <button
          onClick={isLast ? handleFinish : handleNext}
          disabled={!canProceed() || loading}
          className="flex-1 py-3.5 rounded-2xl font-semibold text-base transition-opacity"
          style={{
            background: canProceed() && !loading ? 'var(--accent)' : 'var(--bg-card)',
            color: canProceed() && !loading ? '#000' : 'var(--text-muted)',
            opacity: loading ? 0.7 : 1,
          }}
        >
          {loading ? '...' : isLast ? t('onboarding.btn_finish') : t('onboarding.btn_next')}
        </button>
      </div>
    </div>
  )
}
