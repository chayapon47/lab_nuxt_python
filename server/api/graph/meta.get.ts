export default defineEventHandler(async event => {
  const cfg = useRuntimeConfig(event)
  if (!cfg.metaAccessToken || !cfg.metaPageId || !/^v\d+\.\d+$/.test(String(cfg.metaApiVersion)))
    throw createError({statusCode:503,statusMessage:'Meta credentials/version not configured'})
  // Fixed Meta host and fixed field list: do not forward arbitrary URLs or tokens.
  try {
    return await $fetch(`https://graph.facebook.com/${cfg.metaApiVersion}/${encodeURIComponent(String(cfg.metaPageId))}`, {
      query: {fields:'id,name',access_token:cfg.metaAccessToken},timeout:15000
    })
  } catch {
    throw createError({statusCode:502,statusMessage:'Meta API request failed; check token and permissions'})
  }
})
