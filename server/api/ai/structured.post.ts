import { z } from 'zod'
import { zodTextFormat } from 'openai/helpers/zod'
import { aiClient, requireTrainingAccess } from '../../utils/ai'
const CourseSummary = z.object({course_name:z.string(),summary:z.string(),keywords:z.array(z.string())})
export default defineEventHandler(async event => {
  requireTrainingAccess(event)
  const body = await readBody(event)
  if (typeof body?.description !== 'string' || body.description.length < 1 || body.description.length > 2000)
    throw createError({statusCode:422,statusMessage:'description must be 1–2000 characters'})
  const {client,model} = aiClient(event)
  try {
    const response = await client.responses.parse({
      model, input:`Summarize this course in Thai based only on the text: ${body.description}`,
      text:{format:zodTextFormat(CourseSummary,'course_summary')},
      max_output_tokens:350
    })
    if (!response.output_parsed) throw Error('No structured output')
    return {data:response.output_parsed,usage:response.usage}
  } catch { throw createError({statusCode:502,statusMessage:'Structured AI request failed'}) }
})
