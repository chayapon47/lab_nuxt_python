import { studentStore } from '../../utils/store'
export default defineEventHandler((event) => {
  const q = getQuery(event)
  const minGpa = q.min_gpa === undefined ? 0 : Number(q.min_gpa)
  if (!Number.isFinite(minGpa) || minGpa < 0 || minGpa > 4) throw createError({statusCode:400,statusMessage:'Invalid min_gpa'})
  const faculty = typeof q.faculty === 'string' ? q.faculty.toLowerCase() : ''
  const data = [...studentStore.values()].filter(s => s.gpa >= minGpa && (!faculty || s.faculty.toLowerCase() === faculty))
  return {count:data.length, data}
})
