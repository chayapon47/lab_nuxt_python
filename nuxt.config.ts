export default defineNuxtConfig({
  compatibilityDate: '2026-11-01',
  devtools: { enabled: false },
  runtimeConfig: {
    openaiApiKey: process.env.OPENAI_API_KEY,
    openaiModel: process.env.OPENAI_MODEL || 'gpt-5-mini',
    metaAccessToken: process.env.META_ACCESS_TOKEN,
    metaPageId: process.env.META_PAGE_ID,
    mongoUri: process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017',
    mongoDbName: process.env.MONGODB_DB || 'nuxt_intern',
    metaApiVersion: process.env.META_API_VERSION
  }
})
