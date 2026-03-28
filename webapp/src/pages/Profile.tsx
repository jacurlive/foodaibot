import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import { Edit2, Save, X, Sun, Moon } from 'lucide-react'
import { updateMe } from '../api/client'
import { useStore } from '../store/useStore'
import i18n from '../i18n'
import type { User } from '../types'

const pageVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.35 } },
}

interface FieldProps {
  label: string
  value: string
  editing: boolean
  onEdit: () => void
}

function ProfileField({
  label,
  value,
  children,
  editing,
  onEdit,
}: {
  label: string
  value: string
  children?: React.ReactNode
  editing: boolean
  onEdit: () => void
}) {
  return (
    <div
      className="flex items-center justify-between py-3 px-4 rounded-2xl"
      style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border-subtle)',
      }}
    >
      <div className="flex-1">
        <p className="text-xs mb-1" style={{ color: 'var(--text-muted)' }}>{label}</p>
        {editing && children ? (
          children
        ) : (
          <p className="font-semibold text-sm" style={{ color: 'var(--text-primary)' }}>
            {value}
          </p>
        )}
      </div>
      {!editing && (
        <motion.button
          whileTap={{ scale: 0.85 }}
          onClick={onEdit}
          className="w-7 h-7 rounded-lg flex items-center justify-center ml-2"
          style={{ background: 'var(--bg-elevated)', color: 'var(--text-muted)' }}
        >
          <Edit2 size={13} />
        </motion.button>
      )}
    </div>
  )
}

export function Profile() {
  const { t } = useTranslation()
  const { user, setUser, theme, toggleTheme } = useStore()
  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)

  const [form, setForm] = useState({
    name: user?.name || '',
    age: user?.age?.toString() || '',
    gender: user?.gender || '',
    height: user?.height?.toString() || '',
    weight: user?.weight?.toString() || '',
    goal: user?.goal || '',
    units: user?.units || 'metric',
    language: user?.language || 'ru',
  })

  const [changed, setChanged] = useState(false)

  useEffect(() => {
    if (user) {
      setForm({
        name: user.name || '',
        age: user.age?.toString() || '',
        gender: user.gender || '',
        height: user.height?.toString() || '',
        weight: user.weight?.toString() || '',
        goal: user.goal || '',
        units: user.units || 'metric',
        language: user.language || 'ru',
      })
    }
  }, [user])

  const handleChange = (field: string, value: string) => {
    setForm((f) => ({ ...f, [field]: value }))
    setChanged(true)
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      const updated = await updateMe({
        name: form.name || undefined,
        age: form.age ? parseInt(form.age) : undefined,
        gender: form.gender || undefined,
        height: form.height ? parseFloat(form.height) : undefined,
        weight: form.weight ? parseFloat(form.weight) : undefined,
        goal: form.goal || undefined,
        units: form.units,
        language: form.language,
      } as Partial<User>)
      setUser(updated)
      setChanged(false)
      setEditing(false)
      // Update language
      i18n.changeLanguage(form.language)
      localStorage.setItem('foodai_lang', form.language)
    } finally {
      setSaving(false)
    }
  }

  const handleCancel = () => {
    if (user) {
      setForm({
        name: user.name || '',
        age: user.age?.toString() || '',
        gender: user.gender || '',
        height: user.height?.toString() || '',
        weight: user.weight?.toString() || '',
        goal: user.goal || '',
        units: user.units || 'metric',
        language: user.language || 'ru',
      })
    }
    setChanged(false)
    setEditing(false)
  }

  const displayName = user?.name || user?.first_name || user?.username || '—'
  const initials = (displayName || 'U')
    .split(' ')
    .map((w: string) => w[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)

  const goalLabel = form.goal
    ? t(`profile.goal_${form.goal}`)
    : t('profile.not_set')

  const memberSince = user?.created_at
    ? new Date(user.created_at).toLocaleDateString('ru', { month: 'long', year: 'numeric' })
    : '—'

  return (
    <motion.div
      variants={pageVariants}
      initial="initial"
      animate="animate"
      className="flex flex-col h-full"
    >
      <div className="scroll-area flex-1 px-4 pb-8">
        {/* Header */}
        <div className="flex items-center justify-between pt-4 pb-2">
          <h1 className="text-xl font-bold" style={{ color: 'var(--text-primary)' }}>
            {t('profile.title')}
          </h1>
          <motion.button
            whileTap={{ scale: 0.9 }}
            onClick={() => setEditing(!editing)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-sm font-medium"
            style={{
              background: editing ? 'rgba(248,113,113,0.12)' : 'var(--bg-card)',
              border: `1px solid ${editing ? 'rgba(248,113,113,0.3)' : 'var(--border)'}`,
              color: editing ? 'var(--red)' : 'var(--text-secondary)',
            }}
          >
            {editing ? <X size={14} /> : <Edit2 size={14} />}
            {editing ? t('profile.cancel') : t('profile.edit')}
          </motion.button>
        </div>

        {/* Avatar */}
        <div className="flex flex-col items-center py-5 gap-3">
          <motion.div
            className="w-20 h-20 rounded-3xl flex items-center justify-center text-2xl font-bold"
            style={{
              background: 'linear-gradient(135deg, var(--accent), #F97316)',
              color: '#0B1410',
              boxShadow: '0 8px 24px rgba(245,158,11,0.3)',
            }}
            whileTap={{ scale: 0.95 }}
          >
            {initials}
          </motion.div>
          <div className="text-center">
            <p className="font-bold text-lg" style={{ color: 'var(--text-primary)' }}>
              {displayName}
            </p>
            {user?.goal && (
              <span
                className="text-xs px-2.5 py-1 rounded-full font-medium mt-1 inline-block"
                style={{
                  background: 'rgba(245,158,11,0.15)',
                  color: 'var(--accent)',
                }}
              >
                {t(`profile.goal_${user.goal}`)}
              </span>
            )}
          </div>

          {/* Meta stats */}
          <div className="flex gap-4 mt-1">
            <div className="text-center">
              <p className="font-bold text-base" style={{ color: 'var(--text-primary)' }}>
                {user?.daily_calories ? Math.round(user.daily_calories) : '—'}
              </p>
              <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
                {t('profile.kcal')}
              </p>
            </div>
            <div className="w-px" style={{ background: 'var(--border)' }} />
            <div className="text-center">
              <p className="font-bold text-base" style={{ color: 'var(--text-primary)' }}>
                {memberSince}
              </p>
              <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
                {t('profile.member_since')}
              </p>
            </div>
          </div>
        </div>

        {/* Fields */}
        <div className="flex flex-col gap-2">
          {/* Name */}
          <ProfileField
            label={t('profile.name')}
            value={form.name || t('profile.not_set')}
            editing={editing}
            onEdit={() => setEditing(true)}
          >
            <input
              value={form.name}
              onChange={(e) => handleChange('name', e.target.value)}
              className="text-sm font-semibold bg-transparent border-none outline-none p-0 w-full"
              style={{ color: 'var(--text-primary)' }}
              placeholder={t('profile.not_set')}
            />
          </ProfileField>

          {/* Age */}
          <ProfileField
            label={t('profile.age')}
            value={form.age ? `${form.age} ${t('profile.years')}` : t('profile.not_set')}
            editing={editing}
            onEdit={() => setEditing(true)}
          >
            <input
              type="number"
              value={form.age}
              onChange={(e) => handleChange('age', e.target.value)}
              className="text-sm font-semibold bg-transparent border-none outline-none p-0 w-full"
              style={{ color: 'var(--text-primary)' }}
              placeholder="—"
            />
          </ProfileField>

          {/* Gender */}
          <div
            className="flex items-center justify-between py-3 px-4 rounded-2xl"
            style={{
              background: 'var(--bg-card)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <div className="flex-1">
              <p className="text-xs mb-1.5" style={{ color: 'var(--text-muted)' }}>{t('profile.gender')}</p>
              {editing ? (
                <div className="flex gap-2">
                  {[
                    { value: 'male', label: t('profile.gender_male') },
                    { value: 'female', label: t('profile.gender_female') },
                  ].map((g) => (
                    <motion.button
                      key={g.value}
                      whileTap={{ scale: 0.93 }}
                      onClick={() => handleChange('gender', g.value)}
                      className="px-3 py-1 rounded-lg text-xs font-semibold"
                      style={{
                        background: form.gender === g.value ? 'var(--accent)' : 'var(--bg-elevated)',
                        color: form.gender === g.value ? '#0B1410' : 'var(--text-secondary)',
                        border: `1px solid ${form.gender === g.value ? 'var(--accent)' : 'var(--border)'}`,
                      }}
                    >
                      {g.label}
                    </motion.button>
                  ))}
                </div>
              ) : (
                <p className="font-semibold text-sm" style={{ color: 'var(--text-primary)' }}>
                  {form.gender ? t(`profile.gender_${form.gender}`) : t('profile.not_set')}
                </p>
              )}
            </div>
          </div>

          {/* Height */}
          <ProfileField
            label={t('profile.height')}
            value={form.height ? `${form.height} ${t('profile.cm')}` : t('profile.not_set')}
            editing={editing}
            onEdit={() => setEditing(true)}
          >
            <div className="flex items-center gap-1">
              <input
                type="number"
                value={form.height}
                onChange={(e) => handleChange('height', e.target.value)}
                className="text-sm font-semibold bg-transparent border-none outline-none p-0 w-20"
                style={{ color: 'var(--text-primary)' }}
                placeholder="—"
              />
              <span className="text-xs" style={{ color: 'var(--text-muted)' }}>{t('profile.cm')}</span>
            </div>
          </ProfileField>

          {/* Weight */}
          <ProfileField
            label={t('profile.weight')}
            value={form.weight ? `${form.weight} ${t('profile.kg')}` : t('profile.not_set')}
            editing={editing}
            onEdit={() => setEditing(true)}
          >
            <div className="flex items-center gap-1">
              <input
                type="number"
                value={form.weight}
                onChange={(e) => handleChange('weight', e.target.value)}
                className="text-sm font-semibold bg-transparent border-none outline-none p-0 w-20"
                style={{ color: 'var(--text-primary)' }}
                placeholder="—"
              />
              <span className="text-xs" style={{ color: 'var(--text-muted)' }}>{t('profile.kg')}</span>
            </div>
          </ProfileField>

          {/* Goal */}
          <div
            className="flex items-center justify-between py-3 px-4 rounded-2xl"
            style={{
              background: 'var(--bg-card)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <div className="flex-1">
              <p className="text-xs mb-1.5" style={{ color: 'var(--text-muted)' }}>
                {t('profile.goal_label')}
              </p>
              {editing ? (
                <div className="flex gap-2 flex-wrap">
                  {['lose', 'maintain', 'gain'].map((g) => (
                    <motion.button
                      key={g}
                      whileTap={{ scale: 0.93 }}
                      onClick={() => handleChange('goal', g)}
                      className="px-3 py-1 rounded-lg text-xs font-semibold"
                      style={{
                        background: form.goal === g ? 'var(--accent)' : 'var(--bg-elevated)',
                        color: form.goal === g ? '#0B1410' : 'var(--text-secondary)',
                        border: `1px solid ${form.goal === g ? 'var(--accent)' : 'var(--border)'}`,
                      }}
                    >
                      {t(`profile.goal_${g}`)}
                    </motion.button>
                  ))}
                </div>
              ) : (
                <p className="font-semibold text-sm" style={{ color: 'var(--text-primary)' }}>
                  {goalLabel}
                </p>
              )}
            </div>
          </div>

          {/* Units */}
          <div
            className="flex items-center justify-between py-3 px-4 rounded-2xl"
            style={{
              background: 'var(--bg-card)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <div className="flex-1">
              <p className="text-xs mb-1.5" style={{ color: 'var(--text-muted)' }}>
                {t('profile.units_label')}
              </p>
              <div className="flex gap-2">
                {[
                  { value: 'metric', label: t('profile.units_metric') },
                  { value: 'imperial', label: t('profile.units_imperial') },
                ].map((u) => (
                  <motion.button
                    key={u.value}
                    whileTap={{ scale: 0.93 }}
                    onClick={() => editing && handleChange('units', u.value)}
                    className="px-3 py-1 rounded-lg text-xs font-semibold"
                    style={{
                      background: form.units === u.value ? 'var(--accent)' : 'var(--bg-elevated)',
                      color: form.units === u.value ? '#0B1410' : 'var(--text-secondary)',
                      border: `1px solid ${form.units === u.value ? 'var(--accent)' : 'var(--border)'}`,
                      opacity: editing ? 1 : 0.7,
                    }}
                  >
                    {u.label}
                  </motion.button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Divider */}
        <div className="my-4" style={{ height: 1, background: 'var(--border-subtle)' }} />

        {/* Language */}
        <div
          className="rounded-2xl p-4"
          style={{
            background: 'var(--bg-card)',
            border: '1px solid var(--border-subtle)',
          }}
        >
          <p className="text-xs mb-3" style={{ color: 'var(--text-muted)' }}>
            {t('profile.language')}
          </p>
          <div className="flex gap-3">
            {[
              { code: 'ru', flag: '🇷🇺', label: 'RU' },
              { code: 'en', flag: '🇬🇧', label: 'EN' },
              { code: 'uz', flag: '🇺🇿', label: 'UZ' },
            ].map((lang) => (
              <motion.button
                key={lang.code}
                whileTap={{ scale: 0.9 }}
                onClick={() => {
                  handleChange('language', lang.code)
                  i18n.changeLanguage(lang.code)
                  localStorage.setItem('foodai_lang', lang.code)
                }}
                className="flex-1 flex flex-col items-center gap-1 py-2.5 rounded-xl"
                style={{
                  background:
                    form.language === lang.code ? 'rgba(245,158,11,0.15)' : 'var(--bg-elevated)',
                  border: `1px solid ${
                    form.language === lang.code ? 'rgba(245,158,11,0.4)' : 'var(--border)'
                  }`,
                }}
              >
                <span className="text-xl">{lang.flag}</span>
                <span
                  className="text-xs font-bold"
                  style={{
                    color:
                      form.language === lang.code ? 'var(--accent)' : 'var(--text-muted)',
                  }}
                >
                  {lang.label}
                </span>
              </motion.button>
            ))}
          </div>
        </div>

        {/* Theme toggle */}
        <div
          className="rounded-2xl p-4 mt-2 flex items-center justify-between"
          style={{
            background: 'var(--bg-card)',
            border: '1px solid var(--border-subtle)',
          }}
        >
          <div>
            <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
              {t('profile.theme')}
            </p>
            <p className="font-semibold text-sm mt-0.5" style={{ color: 'var(--text-primary)' }}>
              {theme === 'dark' ? t('profile.dark') : t('profile.light')}
            </p>
          </div>
          <motion.button
            whileTap={{ scale: 0.88 }}
            onClick={toggleTheme}
            className="w-12 h-6 rounded-full relative flex items-center"
            style={{
              background:
                theme === 'light' ? 'var(--accent)' : 'var(--bg-elevated)',
              border: '1px solid var(--border)',
            }}
          >
            <motion.div
              className="w-5 h-5 rounded-full flex items-center justify-center absolute"
              animate={{ left: theme === 'light' ? '2px' : 'calc(100% - 22px)' }}
              transition={{ type: 'spring', stiffness: 400, damping: 25 }}
              style={{ background: 'var(--bg-base)' }}
            >
              {theme === 'dark' ? (
                <Moon size={10} style={{ color: 'var(--text-secondary)' }} />
              ) : (
                <Sun size={10} style={{ color: 'var(--accent)' }} />
              )}
            </motion.div>
          </motion.button>
        </div>

        {/* Save button */}
        <AnimatePresence>
          {(editing || changed) && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
              className="mt-4 flex gap-2"
            >
              <motion.button
                whileTap={{ scale: 0.97 }}
                onClick={handleCancel}
                className="flex-1 py-3.5 rounded-2xl font-semibold text-sm"
                style={{
                  background: 'var(--bg-elevated)',
                  color: 'var(--text-secondary)',
                  border: '1px solid var(--border)',
                }}
              >
                {t('profile.cancel')}
              </motion.button>
              <motion.button
                whileTap={{ scale: 0.97 }}
                onClick={handleSave}
                disabled={saving}
                className="flex-1 py-3.5 rounded-2xl font-bold text-sm flex items-center justify-center gap-2"
                style={{
                  background: 'linear-gradient(135deg, var(--accent), #F97316)',
                  color: '#0B1410',
                  opacity: saving ? 0.7 : 1,
                }}
              >
                <Save size={16} />
                {t('profile.save')}
              </motion.button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  )
}
