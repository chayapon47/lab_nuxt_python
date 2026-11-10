import { aiClient, requireTrainingAccess } from '../../utils/ai'
export default defineEventHandler(async event => {
  requireTrainingAccess(event)
  const body = await readBody(event)
  if (typeof body?.text !== 'string' || body.text.length < 1 || body.text.length > 2000)
    throw createError({statusCode:422,statusMessage:'text must be 1–2000 characters'})
  const {client,model} = aiClient(event)
  try {
    const result = await client.responses.create({
      model, instructions:'Summarize the provided content in Thai. Do not invent facts.',
      input:body.text, max_output_tokens:250
    })
    return {summary:result.output_text, usage:result.usage}
  } catch { throw createError({statusCode:502,statusMessage:'OpenAI request failed'}) }
})
