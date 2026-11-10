import courses from '../../../../public/data/courses.json'
import { aiClient, requireTrainingAccess } from '../../../utils/ai'
export default defineEventHandler(async event => {
  requireTrainingAccess(event)
  const id = getRouterParam(event,'id')
  const course = courses.find(c => String(c.course_id) === id)
  if (!course) throw createError({statusCode:404,statusMessage:'Course not found'})
  const {client,model} = aiClient(event)
  try {
    const response = await client.responses.create({
      model, instructions:'Explain this course in Thai using only supplied data; no invented details.',
      input:JSON.stringify(course), max_output_tokens:250
    })
    return {course_id:id,course_name:course.course_name,summary:response.output_text,usage:response.usage}
  } catch { throw createError({statusCode:502,statusMessage:'OpenAI request failed'}) }
})
