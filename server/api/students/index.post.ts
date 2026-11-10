import { z } from 'zod'
import { studentStore } from '../../utils/store'
const schema = z.object({
  student_id: z.number().int().positive(), name: z.string().min(1),
  faculty: z.string().min(1), year: z.number().int().min(1).max(8),
  gpa: z.number().min(0).max(4), active: z.boolean(), skills: z.array(z.string())
}).strict()
export default defineEventHandler(async event => {
  const parsed = schema.safeParse(await readBody(event))
  if (!parsed.success) throw createError({statusCode:422,statusMessage:'Invalid student payload',data:parsed.error.flatten()})
  const s = parsed.data
  if (studentStore.has(s.student_id)) throw createError({statusCode:409,statusMessage:'Duplicate student ID'})
  studentStore.set(s.student_id,s)
  setResponseStatus(event,201)
  return s
})
