import { useRef, useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import { Camera, Upload, Check, X, RefreshCw, Zap } from 'lucide-react'
import { analyzeFood, saveFood } from '../api/client'
import { useStore } from '../store/useStore'
import type { FoodAnalysisResult } from '../types'

interface AnalyzeProps {
  onNavigate: (tab: string) => void
}

const pageVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.35 } },
}

const resultVariants = {
  initial: { opacity: 0, scale: 0.95, y: 10 },
  animate: { opacity: 1, scale: 1, y: 0, transition: { duration: 0.4 } },
  exit: { opacity: 0, scale: 0.95, transition: { duration: 0.2 } },
}

function MacroChip({
  label,
  value,
  color,
}: {
  label: string
  value: number
  color: string
}) {
  return (
    <div
      className="flex flex-col items-center gap-1 rounded-2xl p-3 flex-1"
      style={{ background: `${color}15`, border: `1px solid ${color}30` }}
    >
      <span className="text-xl font-bold" style={{ color }}>
        {Math.round(value)}
      </span>
      <span className="text-xs font-medium" style={{ color }}>г</span>
      <span className="text-xs" style={{ color: 'var(--text-muted)' }}>{label}</span>
    </div>
  )
}

export function Analyze({ onNavigate }: AnalyzeProps) {
  const { t } = useTranslation()
  const { user } = useStore()
  const cameraRef = useRef<HTMLInputElement>(null)
  const galleryRef = useRef<HTMLInputElement>(null)

  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<FoodAnalysisResult | null>(null)
  const [grams, setGrams] = useState<number>(100)
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showSourcePicker, setShowSourcePicker] = useState(false)

  const lang = user?.language || 'ru'

  const handleFile = useCallback(
    async (f: File) => {
      setFile(f)
      setPreviewUrl(URL.createObjectURL(f))
      setResult(null)
      setError(null)
      setSaved(false)
      setLoading(true)
      try {
        const res = await analyzeFood(f, lang)
        setResult(res)
        setGrams(res.grams)
      } catch {
        setError(t('analyze.error'))
      } finally {
        setLoading(false)
      }
    },
    [lang, t]
  )

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (f) handleFile(f)
    e.target.value = ''
  }

  const getRatio = () => {
    if (!result || result.grams === 0) return 1
    return grams / result.grams
  }

  const adjCalories = result ? Math.round(result.calories * getRatio()) : 0
  const adjProtein = result ? Math.round(result.protein * getRatio() * 10) / 10 : 0
  const adjFat = result ? Math.round(result.fat * getRatio() * 10) / 10 : 0
  const adjCarbs = result ? Math.round(result.carbs * getRatio() * 10) / 10 : 0

  const handleSave = async () => {
    if (!result) return
    setSaving(true)
    try {
      await saveFood({
        dish_name: result.dish_name,
        grams,
        calories: adjCalories,
        protein: adjProtein,
        fat: adjFat,
        carbs: adjCarbs,
        description: result.description,
      })
      setSaved(true)
      setTimeout(() => {
        onNavigate('diary')
      }, 1200)
    } catch {
      setError(t('analyze.error'))
    } finally {
      setSaving(false)
    }
  }

  const handleReset = () => {
    setPreviewUrl(null)
    setFile(null)
    setResult(null)
    setError(null)
    setSaved(false)
    setGrams(100)
  }

  return (
    <motion.div
      variants={pageVariants}
      initial="initial"
      animate="animate"
      className="flex flex-col h-full"
    >
      <div className="scroll-area flex-1 px-4 pb-6">
        {/* Header */}
        <div className="pt-4 pb-2">
          <h1 className="text-xl font-bold" style={{ color: 'var(--text-primary)' }}>
            {t('analyze.title')}
          </h1>
          <p className="text-sm mt-0.5 flex items-center gap-1.5" style={{ color: 'var(--cyan)' }}>
            <Zap size={13} />
            {t('analyze.ai_powered')}
          </p>
        </div>

        <input
          ref={cameraRef}
          type="file"
          accept="image/*"
          capture="environment"
          onChange={handleInputChange}
          className="hidden"
        />
        <input
          ref={galleryRef}
          type="file"
          accept="image/*"
          onChange={handleInputChange}
          className="hidden"
        />

        <AnimatePresence mode="wait">
          {!previewUrl ? (
            /* Upload Zone */
            <motion.div
              key="upload"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="mt-4"
            >
              <motion.button
                whileTap={{ scale: 0.97 }}
                onClick={() => setShowSourcePicker(true)}
                className="w-full rounded-3xl p-8 flex flex-col items-center gap-4"
                style={{
                  border: '2px dashed var(--border)',
                  background: 'var(--bg-card)',
                  minHeight: 260,
                }}
              >
                <motion.div
                  className="w-20 h-20 rounded-3xl flex items-center justify-center"
                  style={{
                    background: 'linear-gradient(135deg, rgba(6,182,212,0.15), rgba(245,158,11,0.15))',
                    border: '1px solid var(--border)',
                  }}
                  animate={{ scale: [1, 1.04, 1] }}
                  transition={{ duration: 2.5, repeat: Infinity, ease: 'easeInOut' }}
                >
                  <Camera size={32} style={{ color: 'var(--cyan)' }} />
                </motion.div>

                <div className="text-center">
                  <p className="font-semibold text-base" style={{ color: 'var(--text-primary)' }}>
                    {t('analyze.tap_photo')}
                  </p>
                  <p className="text-sm mt-1" style={{ color: 'var(--text-muted)' }}>
                    {t('analyze.or_gallery')}
                  </p>
                </div>

                <div
                  className="flex items-center gap-2 px-4 py-2 rounded-xl"
                  style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border)' }}
                >
                  <Upload size={14} style={{ color: 'var(--accent)' }} />
                  <span className="text-xs font-medium" style={{ color: 'var(--accent)' }}>
                    {t('analyze.upload_hint')}
                  </span>
                </div>
              </motion.button>
            </motion.div>
          ) : (
            <motion.div
              key="preview"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="mt-4 flex flex-col gap-4"
            >
              {/* Image preview */}
              <div className="relative rounded-3xl overflow-hidden" style={{ height: 220 }}>
                <img
                  src={previewUrl}
                  alt="Food"
                  className="w-full h-full object-cover"
                />
                {/* Reset button */}
                {!loading && (
                  <motion.button
                    whileTap={{ scale: 0.9 }}
                    onClick={handleReset}
                    className="absolute top-3 right-3 w-9 h-9 rounded-xl flex items-center justify-center"
                    style={{ background: 'rgba(0,0,0,0.6)' }}
                  >
                    <RefreshCw size={15} color="white" />
                  </motion.button>
                )}
                {/* Loading overlay */}
                {loading && (
                  <div
                    className="absolute inset-0 flex flex-col items-center justify-center gap-3"
                    style={{ background: 'rgba(11,20,16,0.8)' }}
                  >
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                    >
                      <svg width={40} height={40} viewBox="0 0 40 40" fill="none">
                        <circle cx="20" cy="20" r="16" stroke="var(--border)" strokeWidth={3} />
                        <path
                          d="M20 4 A16 16 0 0 1 36 20"
                          stroke="var(--cyan)"
                          strokeWidth={3}
                          strokeLinecap="round"
                        />
                      </svg>
                    </motion.div>
                    <p className="text-sm font-semibold" style={{ color: 'var(--cyan)' }}>
                      {t('analyze.analyzing_dots')}
                    </p>
                  </div>
                )}
              </div>

              {/* Error */}
              {error && (
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="rounded-2xl p-4 text-center"
                  style={{
                    background: 'rgba(248,113,113,0.1)',
                    border: '1px solid rgba(248,113,113,0.2)',
                  }}
                >
                  <p className="text-sm font-medium" style={{ color: 'var(--red)' }}>{error}</p>
                  <motion.button
                    whileTap={{ scale: 0.95 }}
                    onClick={handleReset}
                    className="mt-2 text-xs font-medium"
                    style={{ color: 'var(--text-secondary)' }}
                  >
                    {t('analyze.discard')}
                  </motion.button>
                </motion.div>
              )}

              {/* Result card */}
              <AnimatePresence>
                {result && !loading && (
                  <motion.div
                    variants={resultVariants}
                    initial="initial"
                    animate="animate"
                    exit="exit"
                    className="rounded-3xl p-4 flex flex-col gap-4"
                    style={{
                      background: 'var(--bg-card)',
                      border: '1px solid var(--border-subtle)',
                    }}
                  >
                    {!result.is_food ? (
                      <div className="text-center py-4">
                        <p className="text-2xl mb-2">🚫</p>
                        <p className="font-semibold" style={{ color: 'var(--text-primary)' }}>
                          {t('analyze.not_food')}
                        </p>
                        <p className="text-sm mt-1" style={{ color: 'var(--text-muted)' }}>
                          {t('analyze.not_food_hint')}
                        </p>
                        <motion.button
                          whileTap={{ scale: 0.95 }}
                          onClick={handleReset}
                          className="mt-4 px-6 py-2 rounded-xl text-sm font-semibold"
                          style={{
                            background: 'var(--bg-elevated)',
                            color: 'var(--text-secondary)',
                          }}
                        >
                          {t('analyze.discard')}
                        </motion.button>
                      </div>
                    ) : (
                      <>
                        {/* Dish name */}
                        <div>
                          <h2 className="text-lg font-bold" style={{ color: 'var(--text-primary)' }}>
                            {result.dish_name}
                          </h2>
                          {result.description && (
                            <p className="text-xs mt-1" style={{ color: 'var(--text-secondary)' }}>
                              {result.description}
                            </p>
                          )}
                        </div>

                        {/* Grams input */}
                        <div
                          className="flex items-center justify-between rounded-2xl p-3"
                          style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border)' }}
                        >
                          <span className="text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>
                            {t('analyze.grams_label')}
                          </span>
                          <div className="flex items-center gap-2">
                            <motion.button
                              whileTap={{ scale: 0.85 }}
                              onClick={() => setGrams((g) => Math.max(10, g - 10))}
                              className="w-7 h-7 rounded-lg flex items-center justify-center text-sm font-bold"
                              style={{ background: 'var(--bg-card)', color: 'var(--accent)' }}
                            >
                              −
                            </motion.button>
                            <input
                              type="number"
                              value={grams}
                              onChange={(e) => setGrams(Math.max(1, parseInt(e.target.value) || 1))}
                              className="w-16 text-center text-base font-bold"
                              style={{
                                background: 'transparent',
                                border: 'none',
                                color: 'var(--text-primary)',
                                padding: '0',
                              }}
                            />
                            <span className="text-sm" style={{ color: 'var(--text-muted)' }}>г</span>
                            <motion.button
                              whileTap={{ scale: 0.85 }}
                              onClick={() => setGrams((g) => g + 10)}
                              className="w-7 h-7 rounded-lg flex items-center justify-center text-sm font-bold"
                              style={{ background: 'var(--bg-card)', color: 'var(--accent)' }}
                            >
                              +
                            </motion.button>
                          </div>
                        </div>

                        <p className="text-xs text-center -mt-2" style={{ color: 'var(--text-muted)' }}>
                          {t('analyze.recalculate_hint')}
                        </p>

                        {/* Calories big display */}
                        <div className="text-center">
                          <motion.span
                            key={adjCalories}
                            initial={{ scale: 1.1 }}
                            animate={{ scale: 1 }}
                            className="text-4xl font-bold"
                            style={{ color: 'var(--accent)' }}
                          >
                            {adjCalories}
                          </motion.span>
                          <span className="text-base ml-1.5 font-medium" style={{ color: 'var(--text-muted)' }}>
                            {t('analyze.calories')}
                          </span>
                        </div>

                        {/* Macro chips */}
                        <div className="flex gap-2">
                          <MacroChip label={t('analyze.protein')} value={adjProtein} color="var(--green)" />
                          <MacroChip label={t('analyze.fat')} value={adjFat} color="var(--orange)" />
                          <MacroChip label={t('analyze.carbs')} value={adjCarbs} color="var(--blue)" />
                        </div>

                        {/* Action buttons */}
                        <AnimatePresence mode="wait">
                          {saved ? (
                            <motion.div
                              key="success"
                              initial={{ scale: 0.8, opacity: 0 }}
                              animate={{ scale: 1, opacity: 1 }}
                              className="flex items-center justify-center gap-2 py-3 rounded-2xl"
                              style={{ background: 'rgba(74,222,128,0.15)', border: '1px solid rgba(74,222,128,0.3)' }}
                            >
                              <Check size={18} style={{ color: 'var(--success)' }} />
                              <span className="font-semibold text-sm" style={{ color: 'var(--success)' }}>
                                {t('analyze.success')}
                              </span>
                            </motion.div>
                          ) : (
                            <motion.div key="actions" className="flex flex-col gap-2">
                              <motion.button
                                whileTap={{ scale: 0.97 }}
                                onClick={handleSave}
                                disabled={saving}
                                className="w-full py-3.5 rounded-2xl font-bold text-sm flex items-center justify-center gap-2"
                                style={{
                                  background: saving
                                    ? 'var(--border)'
                                    : 'linear-gradient(135deg, var(--accent), #F97316)',
                                  color: '#0B1410',
                                  opacity: saving ? 0.7 : 1,
                                }}
                              >
                                {saving ? (
                                  <motion.div
                                    animate={{ rotate: 360 }}
                                    transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                                  >
                                    <RefreshCw size={15} />
                                  </motion.div>
                                ) : (
                                  <Check size={16} />
                                )}
                                {t('analyze.save')}
                              </motion.button>
                              <motion.button
                                whileTap={{ scale: 0.97 }}
                                onClick={handleReset}
                                className="w-full py-3 rounded-2xl font-medium text-sm flex items-center justify-center gap-2"
                                style={{
                                  background: 'var(--bg-elevated)',
                                  color: 'var(--text-secondary)',
                                  border: '1px solid var(--border)',
                                }}
                              >
                                <X size={15} />
                                {t('analyze.discard')}
                              </motion.button>
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </>
                    )}
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Source picker bottom sheet */}
      <AnimatePresence>
        {showSourcePicker && (
          <>
            <motion.div
              key="backdrop"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setShowSourcePicker(false)}
              className="fixed inset-0 z-40"
              style={{ background: 'rgba(0,0,0,0.5)' }}
            />
            <motion.div
              key="sheet"
              initial={{ y: '100%' }}
              animate={{ y: 0 }}
              exit={{ y: '100%' }}
              transition={{ type: 'spring', damping: 30, stiffness: 300 }}
              className="fixed bottom-0 left-0 right-0 z-50 rounded-t-3xl p-5 flex flex-col gap-3"
              style={{ background: 'var(--bg-card)', maxWidth: 480, margin: '0 auto' }}
            >
              <div className="w-10 h-1 rounded-full mx-auto mb-1" style={{ background: 'var(--border)' }} />
              <button
                onClick={() => { setShowSourcePicker(false); setTimeout(() => cameraRef.current?.click(), 50) }}
                className="w-full py-4 rounded-2xl font-semibold text-base flex items-center justify-center gap-3"
                style={{ background: 'var(--bg-elevated)', color: 'var(--text-primary)', border: '1px solid var(--border)' }}
              >
                <Camera size={20} style={{ color: 'var(--cyan)' }} />
                {t('analyze.source_camera')}
              </button>
              <button
                onClick={() => { setShowSourcePicker(false); setTimeout(() => galleryRef.current?.click(), 50) }}
                className="w-full py-4 rounded-2xl font-semibold text-base flex items-center justify-center gap-3"
                style={{ background: 'var(--bg-elevated)', color: 'var(--text-primary)', border: '1px solid var(--border)' }}
              >
                <Upload size={20} style={{ color: 'var(--accent)' }} />
                {t('analyze.source_gallery')}
              </button>
              <button
                onClick={() => setShowSourcePicker(false)}
                className="w-full py-3 rounded-2xl text-sm font-medium"
                style={{ color: 'var(--text-muted)' }}
              >
                {t('analyze.cancel')}
              </button>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
