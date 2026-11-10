import { getDb } from '../../../utils/sqlite'
export default defineEventHandler(event => {
  const q = getQuery(event)
  const min = q.min_gpa === undefined ? 0 : Number(q.min_gpa)
  if (!Number.isFinite(min) || min < 0 || min > 4) throw createError({statusCode:400,statusMessage:'Invalid min_gpa'})
  const rows = getDb().prepare('SELECT student_id,name,faculty,year,gpa,active,skills_json FROM students WHERE gpa >= ? ORDER BY student_id').all(min) as any[]
  return {source:'sqlite',count:rows.length,data:rows.map(({skills_json,active,...s})=>({...s,active:Boolean(active),skills:JSON.parse(skills_json)}))}
})
