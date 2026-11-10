import OpenAI from 'openai'
export function aiClient(event: any) {
  const config = useRuntimeConfig(event)
  if (!config.openaiApiKey) throw createError({statusCode:503,statusMessage:'OpenAI API key not configured'})
  return { client: new OpenAI({apiKey:String(config.openaiApiKey),timeout:30000,maxRetries:1}),
           model:String(config.openaiModel) }
}
export function requireTrainingAccess(event: any) {
  // These exercises must be run locally only; do not expose these endpoints publicly.
  const host = getRequestHost(event).split(':')[0]
  if (!['localhost','127.0.0.1','[::1]'].includes(host))
    throw createError({statusCode:403,statusMessage:'Local training only'})
}
