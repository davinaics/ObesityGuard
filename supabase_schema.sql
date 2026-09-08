-- ============================================================
-- Supabase SQL Schema
-- Jalankan di Supabase Dashboard → SQL Editor
-- ============================================================

-- 1. Tabel health_logs
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.health_logs (
    id                BIGSERIAL PRIMARY KEY,
    user_id           UUID        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    date              DATE        NOT NULL DEFAULT CURRENT_DATE,
    age               INTEGER     NOT NULL,
    height            FLOAT       NOT NULL,
    weight            FLOAT       NOT NULL,
    aktivitas         TEXT        NOT NULL,
    sayur             TEXT        NOT NULL,
    air               TEXT        NOT NULL,
    prediction_result TEXT        NOT NULL,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- RLS: user hanya bisa akses data milik sendiri
ALTER TABLE public.health_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own logs"
    ON public.health_logs FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own logs"
    ON public.health_logs FOR INSERT
    WITH CHECK (auth.uid() = user_id);