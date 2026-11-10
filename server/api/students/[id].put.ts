import { z } from 'zod'
import { studentStore } from '../../utils/store'
const schema = z.object({
  student_id: z.number().int().positive(), name: z.string().min(1),
  faculty: z.string().min(1), year: z.number().int().min(1).max(8),
  gpa: z.number().min(0).max(4), active: z.boolean(), skills: z.array(z.string())
}).strict()
export default defineEventHandler(async event => {
  const id = Number(getRouterParam(event,'id'))
  if (!studentStore.has(id)) throw createError({statusCode:404,statusMessage:'Student not found'})
  const result = schema.safeParse(await readBody(event))
  if (!result.success) throw createError({statusCode:422,statusMessage:'Invalid payload'})
  if (result.data.student_id !== id) throw createError({statusCode:400,statusMessage:'ID mismatch'})
  studentStore.set(id,result.data)
  return result.data
})
